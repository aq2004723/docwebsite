#coding = uft-8

from pymongo import Connection
import datetime
import uuid

class Worker:
    def __init__(self):
        self.con = Connection("localhost", 27017)
        self.db = self.con.test

    def register(self,username,password):
        if self.db.users.find_one({'username':username}) is None:
       	    return None
        newuser = {'username': username,'password':password}
        return self.db.users.insert(newuser)

    def signin(self,username,password):
        user = self.db.users.find_one({'username':username,'password':password})
        if user is not None:
            return str(user.get('_id'))
        else:
            return None

    def getuserinfo(self,username):
    	return self.db.users.find_one({'username':username})

    def getonedoc(self,docid):
        doc = self.db.docs.find_one({'_id':doc})
        return doc

    def userupload(self,myfile,userid,classname,title):
        day = time.strftime('%Y/%m/%d',time.localtime(time.time()))
        source_path = os.path.join('static/file/source', day)
        if not os.path.isdir(source_path):
            os.makedirs(source_path)

        #make the pdf dict
        pdf_path = os.path.join('static/file/pdf', day)
        if not os.path.isdir(pdf_path):
            os.makedirs(pdf_path)

        #generate the only filename
        onlyname = uuid.uuid4().hex
        typename = myfile['filename'][myfile['filename'].find('.'):]
        source_path = os.path.join(source_path,onlyname + typename)
        pdf_path = os.path.join(pdf_path,onlyname + ".pdf")

        #save the file into source_patf
        with open(source_path,'wb') as up:
            up.write(myfile['body'])

        if not typename == '.pdf':
            pass
        else:
            with open(pdf_path,'wb') as f:
                f.write(myfile['body'])

        doc ={
            'title':title,
            'classname':classname,
            'pdflocation':pdf_path,
            'sourcelocation':source_path,
            'uploadtime':time.strftime('%F %X',time.localtime(time.time())),
            'downloadcount':0,
            'userid':userid,
            'cover':"",
        }

        return self.db.docs.insert(doc)
    def getIndexDoc(self):
        post = self.db.doc


if __name__ == '__main__':
    t = Worker()
    print t.register('','541788')
