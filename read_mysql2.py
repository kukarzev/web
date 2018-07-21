import MySQLdb
import ftfy
import pandas as pd
from bs4 import BeautifulSoup

def fix_photo_url(url):
    if 'photoalbum' in url:
        #print(url)
        l_path = url.split('%2F')[1:]
        #print(l_path)
        l_path[-1] = l_path[-1].split('&')[0]
        _res = 'http://kukartsev.com/photos/{}'.format('/'.join(l_path))
    else:
        _res = url
    return(_res)

def fix_images(text):
    _res = ''
    for l in text.splitlines():
        _start = l.find('%image(')
        _end = l.find(')',_start)
        _line = l
        if _start>0 and _end>0 and _end>_start:
            _img_pars = tuple(l[_start+7:_end].split('|'))
            _inline = "[WPIMPINLINE:{}|width='{}'|height='{}'|alt='{}']".format(*_img_pars)
            _line = _inline
        _res += '{}\n'.format(_line)

    soup = BeautifulSoup(_res, 'html.parser')
    for link in soup.find_all('a'):
        _href = link.get('href')
        _filename = link.get('href').split('image=')[-1].split('&')[0]
        print(fix_photo_url(_href))
        #print(link.contents)
    #print(soup)
        
    return(_res)



if __name__=='__main__':
    MySQLdb.connect('localhost','root','narube09','nucleus')
    con = MySQLdb.connect('localhost','root','narube09','nucleus')
    cur = con.cursor()
    cur.execute('''
SELECT 
    i.itime
    ,i.ititle 
    ,i.ibody
    ,i.imore
    ,m.mname
FROM nucleus_item i
inner join nucleus_member m
    on m.mnumber=i.iauthor
where 
    iblog=7
''')

    _dt = []
    _title = []
    _text = []
    _author = []

    # pictures
    _media = '/home/www-data/blog/media/'

    res = cur.fetchall()
    for r in res:

        # find local images
        # assume one per line - replace the whole line
        _current_text = '{}\n{}'.format(ftfy.fix_text(r[2]),ftfy.fix_text(r[3]))
        _fixed_text = fix_images(_current_text)
        #print(_fixed_text)
        _dt.append(r[0])
        _title.append(ftfy.fix_text(r[1]))
        _text.append('{}\n{}'.format(ftfy.fix_text(r[2]),ftfy.fix_text(r[3])))
        _author.append(ftfy.fix_text(r[4]))
    
    df = pd.DataFrame({'datetime':_dt,
                       'title':_title,
                       'text':_text,
                       'fixed_text':_fixed_text,
                       'author':_author})

    df.iloc[11:17,:].to_csv('test3.csv',index=False)
    print(df.iloc[11:17,:].head(10))
