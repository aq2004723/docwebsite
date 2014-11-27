#coding=utf-8
from pymongo import Connection
import time
from tornado.httpclient import AsyncHTTPClient,HTTPRequest
import tornado.ioloop
import json
import os

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

#db.docs.insert(doc)
"""
def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body

appid = "5281805fd692ca46f4ef8a40ffa780bd"

url = "http://herald.seu.edu.cn/uc/auth"
body = "user:213120657,password:woshiyou88,'appid':%s"%appid

request = HTTPRequest(url = url ,method ='POST',body=str(body))
http_client = AsyncHTTPClient()
http_client.fetch(request, handle_request)
tornado.ioloop.IOLoop.instance().start()

"""
#users = db.users.find()

#user = {'username':'coco','password':'541788','upload':[]}

#db.users.insert(user)
#for i in users:
    #print i

#s=db.users.find_one(asnkjs='asdawasd')
#s['upload'].append('asdasd')
#db.users.save(s)

#db.users.drop()

#print s

#db.docs.drop()

#for i in db.docs.find():
    #print i

#key_words="haha hehe ~~ and haha"
#key_word = []
#for i in key_words.split(' '):
#    if i not in key_word:
#        key_word.append(i)


#for j in key_word:
#    print j

docs = db.docs.find()
for i in docs:
    print i