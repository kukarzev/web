import MySQLdb
import ftfy
MySQLdb.connect('localhost','root','narube09','nucleus')
con = MySQLdb.connect('localhost','root','narube09','nucleus')
cur = con.cursor()
cur.execute('SELECT itime, ititle, ibody, imore FROM nucleus_item where iblog=7')
#cur.execute('SELECT distinct iblog FROM nucleus_item')
res = cur.fetchall()
for r in res:
    print('Date and time: {}'.format(r[0]))
    print('TITLE: {}'.format(ftfy.fix_text(r[1])))
    print()
    print(ftfy.fix_text(r[2]))
    print('---')
    print(ftfy.fix_text(r[3]))
    print()
    print('=======================================================')
    print()

