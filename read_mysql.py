import os
import MySQLdb
import ftfy
import pandas as pd
from bs4 import BeautifulSoup
from shutil import copyfile


def fix_photo_url(url):
    '''
    Replace old photoalbum links with current ones
    '''
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
    '''
    Migrate images from Nucleus posts to Wordpress...
    '''

    _res = ''

    # embedded images
    for l in text.splitlines():
        _start = l.find('%image(')
        _end = l.find(')',_start)
        _line = l
        if _start>0 and _end>0 and _end>_start:
            _pars = [wp_content]
            _pars.extend(l[_start+7:_end].split('|'))
            _img_pars = tuple(_pars)
            #_inline = "[WPIMPINLINE:{}|width='{}'|height='{}'|alt='{}']".format(*_img_pars)
            _inline = '<img class="size-medium wp-image-7 alignright" style="font-size: 1rem;" src="{}/{}" width="{}" height="{}" alt="{}"/>'
            _inline = _inline.format(*_img_pars)
            _line = _inline
        _res += '{}'.format(_line)

    # linked images from old photoalbum and just links
    soup = BeautifulSoup(_res, 'html.parser')
    for link in soup.find_all('a'):
        _href = link.get('href')
        _filename = None
        if 'image=' in _href:
            process_inline_image(soup,link,_href,image_marker='image')
        else:
            link['href'] = fix_photo_url(_href)

    for link in soup.find_all('img'):
        _src = link['src']
        process_inline_image(soup, link, href=_src,image_marker='obj_name')
            
    _res = soup
    #print(_res)
    return(_res)

def process_inline_image(soup, link, href,
                         image_marker='image'):
    _debug = False
    if image_marker in href:
        # extract image file name
        _filename = href.split('{}='.format(image_marker))[-1].split('&')[0]
    else:
        _filename = href.split('/')[-1]
        #print(_filename)
        _debug=True
        
    # replace link to an embedding directive
    #sup = soup.new_tag('sup')
    #sup.string = "\n[WPIMPINLINE:{}]\n".format(_filename)
    #link.insert_after(sup)
    #link.unwrap()
    #sup.unwrap()

    # replace link to an embedding directive
    sup = soup.new_tag('img')
    #sup.string = '\n<img class="size-medium wp-image-7 aligncenter" style="font-size: 1rem;" src="{}/{}" width="" height="" alt=""/>\n'.format(wp_content,_filename)
    sup['class'] = "size-medium wp-image-7 aligncenter"
    sup['style'] = "font-size: 1rem;"
    sup['src'] = "{}/{}".format(wp_content,_filename)
    sup['width'] = ""
    sup['height'] = ""
    sup['alt'] = ""
    link.insert_after(sup)
    link.unwrap()
    #sup.unwrap()

    if _debug:
        print(soup)
    
    # extract path to file from root of the photoalbum
    # (we will copy the file for embedding into wordpress
    if 'blog/media' in href:
        _ipath = '/'.join(href.split('blog/media')[1].split('/')[:-1])
        old_path = old_media
    else:
        l_path = href.split('%2F')[1:]
        _ipath = '/'.join(l_path).split('&')[0]
        old_path = old_photos

    # normalize slashes
    _ipath = _ipath.strip('/')+'/'
        
    # try to copy image to a directory to be uploaded and embedded
    # save path and name to file if fails
    try:
        _src = old_path+_ipath+_filename
        if os.path.exists(_src)==False:
            # replace %28, %29 ()
            _src = _src.replace('%28','(')
            _src = _src.replace('%29',')')
        _dest = img_dir+'/'+_filename
        if os.path.exists(_dest)==False:
            copyfile(_src,_dest)
    except:
        append_to_file(_ipath+_filename,img_dir+'/missing_images.txt')


def create_dir(dir_name):
    try:
        _abs_path = os.path.abspath(dir_name)
        if not os.path.exists(_abs_path):
            os.makedirs(_abs_path)
    except OSError:
        print('Error: cannot create directory {}'.format(dir_name))

def append_to_file(text, filename):
    '''
    Append text to file separated with newlines
    Create file if it does not exist
    '''
    if os.path.exists(filename):
            append_write = 'a' # append if already exists
    else:
            append_write = 'w' # make a new file if not

    _file = open(filename,append_write)
    _file.write('\n{}\n'.format(text))
    _file.close()
    
        
if __name__=='__main__':

    # create image dir if not present
    # we will copy embedded img files there

    # location of old photoalbum files
    global old_photos
    global old_media
    old_photos = '/home/www-data/old_root/photos/'
    old_media = '/home/www-data/blog/media/'

    # where to upload images manually
    global wp_content
    wp_content = 'http://kukartsev.com/vika/wp-content/img'

    # where to copy files to be embedded
    global img_dir
    img_dir = os.path.abspath('./img')
    create_dir(img_dir)
    
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

    #i = 0
    res = cur.fetchall()
    for r in res:
        #i += 1

        # find local images
        # assume one per line - replace the whole line
        _current_text = '{}\n{}'.format(ftfy.fix_text(r[2]),ftfy.fix_text(r[3]))
        _fixed_text = fix_images(_current_text)
        #print(_fixed_text)
        _dt.append(r[0])
        _title.append(ftfy.fix_text(r[1]))
        #_text.append(_current_text)
        _text.append(_fixed_text)
        _author.append(ftfy.fix_text(r[4]))

        # debug
        print(_fixed_text)
        print('--------------------------')
        #if i==100:
        #    raise(Exception)

        
    df = pd.DataFrame({'post_date_time':_dt,
                       'title':_title,
                       'text':_text,
                       'author':_author
    })

    # remove stupid datetime - duplicates
    df.loc[df.post_date_time>'1970-01-01',['author','post_date_time','title','text']].to_csv('vika6.csv',index=False)
    print(df.iloc[11:17,:].head(10))
