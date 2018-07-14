import MySQLdb
MySQLdb.connect('localhost','root','narube09','nucleus')
con = MySQLdb.connect('localhost','root','narube09','nucleus')
cur = con.cursor()
cur.execute('SELECT ibody,imore FROM nucleus_item where iblog=9')
res = cur.fetchall()
for r in res:
    print(r[0])
    print(r[1])

