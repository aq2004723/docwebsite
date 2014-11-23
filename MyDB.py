#coding=utf-8

import MySQLdb
import sys
import time
from unotest import DocumentConverter,DocumentConversionException
import uuid
import os
from com.sun.star.task import ErrorCodeIOException
import base64

class MyDB(object):
    def __init__(self):
        self.conn=MySQLdb.connect(host='localhost',user='root',passwd='541788',db='heralddoc',port=3306)
        self.cursor=self.conn.cursor()
    def __delete__(self):
        self.conn.close()

    def getRandomCookieSecret(self):
        return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
   
    def getDoc(self,docID):
        sql=r"SELECT docID,docname,cover,pdflocation,docdescribe,downloadcount FROM document WHERE docID = "+ str(docID)
        rs = {}
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                rs['docID'] = row[0]
                rs['docname'] = row[1]
                rs['cover'] = row[2]
                rs['pdflocation'] = row[3]
                rs['docdescribe'] = row[4]
                rs['downloadcount'] = row[5]
        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
        """
        for i in rs:
            print "rs[%s]=" % i,rs[i] 
        """
        return rs

    def news20doc(self):
        sql= "SELECT document.docid, document.docname, document.cover, \
        userupload.uploaddate,document.docdescribe FROM document \
        LEFT JOIN userupload ON document.docID=userupload.docID \
        ORDER BY userupload.uploaddate LIMIT 0,20;"
        rs = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                pdf_temp = {}
                pdf_temp['id'] = row[0]
                pdf_temp['name']= row[1]
                pdf_temp['cover'] = row[2]
                pdf_temp['time']= row[3]
                pdf_temp['desc']= row[4]
                rs.append(pdf_temp)
        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)

        return rs

    def upload(self,userID,filename,description,myfile):
        #check the file is right 
        
        #make a dict for the file
        day = time.strftime('%Y/%m/%d',time.localtime(time.time()))
        source_path = os.path.join(os.getcwd()+ '/static/file/source', day)
        if not os.path.isdir(source_path):
            os.makedirs(source_path)

        #make the pdf dict
        pdf_path = os.path.join(os.getcwd()+ '/static/file/pdf', day)
        if not os.path.isdir(pdf_path):
            os.makedirs(pdf_path)

        #generate the only filename
        onlyname = uuid.uuid4().hex
        typename = myfile['filename']
        typename = typename[typename.find('.'):]
        source_path = os.path.join(source_path,onlyname + typename)
        pdf_path = os.path.join(pdf_path,onlyname + ".pdf")

        #save the file into source_patf
        with open(source_path,'wb') as up:
            up.write(myfile['body'])

        #if not pdf ,call DocumentConverter to translate the doc to pdf
        if not typename ==".pdf":
            try:
                converter = DocumentConverter()    
                converter.convert(source_path, pdf_path)
            except DocumentConversionException, exception:
                print "ERROR! " + str(exception)
                return False
            except ErrorCodeIOException, exception:
                print "ERROR! ErrorCodeIOException %d" % exception.ErrCode 


        try:
            source_path = source_path[source_path.find('file/'):]
            if typename ==".pdf":
                pdf_path= source_path
            else:
                pdf_path[pdf_path.find('file/'):]

            sql = "insert into document(docname,cover,sourcelocation,pdflocation,docdescribe,downloadcount)\
            value('%s','%s','%s','%s','%s','%d')"%(filename,"",source_path,pdf_path,description,0)
            self.cursor.execute(sql)
            self.conn.commit()

            sql ="select max(docID) from document"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            docID = 0
            for row in results:
                docID = row[0]

            sql = "insert into userupload(docID,uploaddate,userID) \
            value(%d,'%s',%d)"%(docID,time.strftime('%Y-%m-%d %H:%M:%S'),long(userID))

            self.cursor.execute(sql)
            self.conn.commit()
        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
        
    def checkuser(self,username,password):
        sql = "select userID from user where username = '%s' and password = '%s'"%(username,password)
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                if not row:
                    return 0
                else:
                    return row[0]
        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)

    def get_doc_cover(self,docID):
        sql = "select docuname,cover,uploaddate,pdflocation from document left join userupload \
            on userupload.docID = document.docID where document.docID = '%d'"%(docID)
        rs = {}
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                rs['docuname'] = row[0]
                rs['cover'] = row[1]
                rs['time'] = row[2]
                rs['pdflocation'] = row[3]

        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)

        return rs

    def getdoc(self,docID):
        sql = "select docuname,sourcelocation,pdflocation, \
        docdescribe,downloadcount from document where docID = '%d'"%(docID)
        rs = {}
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for row in results:
                rs['docuname'] = row[0]
                rs['sourcelocation'] = row[1]
                rs['pdflocation'] = row[2]
                rs['docdescribe'] = row[3]
                rs['downloadcount'] = row[4]

        except:
            s=sys.exc_info()
            print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)

        return rs



if __name__ == "__main__":
    t = MyDB()
    s= t.checkuser('coco','541788')
    print s