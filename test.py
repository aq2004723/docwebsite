from pymongo import Connection
import time

con = Connection("localhost", 27017)
db = con.test

users = db.users.find(limit=20)

doc ={
    'title':"hellowword",
    'description':"it's my first book",
    'classname':"seu ",
    'pdflocation':"static/JN.pdf",
    'sourcelocation':"/src",
    'uploadtime':time.strftime('%F %X',time.localtime(time.time())),
    'downloadcount':0,
    'username':"coco",
    'cover':"/src",
}

db.docs.insert(doc)

docs = list(db.users.find())

for i in docs:
	print i

print ""
print ""

for j in docs:
	print i


for i in docs:
	print i

