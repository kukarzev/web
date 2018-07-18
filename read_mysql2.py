import MySQLdb
import ftfy
import pandas as pd

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
_text1 = []
_text2 = []
_text = []
_author = []

# pictures
_media = '/home/www-data/blog/media/'

res = cur.fetchall()
for r in res:
    _dt.append(r[0])
    _title.append(ftfy.fix_text(r[1]))
    _text1.append(ftfy.fix_text(r[2]))
    _text2.append(ftfy.fix_text(r[3]))
    _text.append('{}\n{}'.format(ftfy.fix_text(r[2]),ftfy.fix_text(r[3])))
    _author.append(ftfy.fix_text(r[4]))

    # find local images
    _start = _text[-1].find('%image(')
    _end = _text[-1].find(')',_start)
    if _end>_start:
        print(_text[-1][_start:_end])
    
df = pd.DataFrame({'datetime':_dt,
                   'title':_title,
                   'text1':_text1,
                   'text2':_text2,
                   'text':_text,
                   'author':_author})

df.iloc[11:17,:].to_csv('test3.csv',index=False)
print(df.iloc[11:17,:].head(10))
