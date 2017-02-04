# ccSystem.py
# http://localhost:8000/

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape
import sqlite3
import json

def application(environ, start_response):
        status = '200 OK'
        response_headers = [('Content-Type', 'text/html'),
                            ('Access-Control-Allow-Origin', '*'),
                            ('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept')]
        start_response(status, response_headers)
        response_body = '<h1>Hello, %s!</h1>' % (environ['PATH_INFO'][1:] or 'web')
        
        loginPage='''<form action="/login" method="post">
                              <p>username: <input name="username"></p>
                              <p>password: <input name="password" type="password"></p>
                              <p><button type="submit">Sign In</button></p>
                              </form>'''
        
        #query_string=parse_qs(environ['QUERY_STRING'])
        #print 'QUERY_STRING: %s' % query_string
        method = environ['REQUEST_METHOD']
        path = environ['PATH_INFO']

        if method=='GET' and path=='/login':
                response_body= loginPage
        
        if method=='POST' and path=='/login':
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
                request_body = environ['wsgi.input'].read(request_body_size)
                par = parse_qs(request_body)
                print 'par:%s' % par
                username = escape(par.get('username',[''])[0]) # [''] is default values,if not exists 'username' then return default value
                password = escape(par.get('password',[''])[0])
                if username=='' or password=='':
                        return loginPage+'''<p><font color="red">Please enter your username and password.</font></p>'''

                conn=sqlite3.connect('ccSystem.db')
                cursor = conn.cursor()
                cursor.execute('select id,name,password from user where id=?', (username,))
                sqlValues = cursor.fetchone()
                cursor.close()
                conn.close()
                
                if sqlValues!= None:
                        #colname = {'id','name','password'}
                        #userinfo = dict(zip(colname,list(sqlValues)))
                        #print 'userinfo:%s' % userinfo
                        #correctPassword = userinfo['password']
                        #showName = str(userinfo['name'])

                        correctPassword = sqlValues[2]
                        showName = str(sqlValues[1])

                        if password==correctPassword:
                                response_body = '<h3>welcome, %s!</h3>' % showName
                        else :
                                response_body = loginPage+'''<p><font color="red">Wrong password.</font></p>'''
                else:
                        response_body = loginPage+'''<p><font color="red">Wrong username.</font></p>'''
                       
        if method=='GET' and path=='/users':
                #response_body='[{"id":"admin","name":"Admin"},{"id":"test","name":"Test"}]'
                conn=sqlite3.connect('ccSystem.db')
                cursor = conn.cursor()
                cursor.execute('select id,name from user')
                sqlValues = cursor.fetchall()
                cursor.close()
                conn.close()

                jsonData = []
                for row in sqlValues:
                        result = {}
                        result['id'] = str(row[0])
                        result['name'] = str(row[1])
                        jsonData.append(result)

                print str(jsonData).replace("'", "\"")
                response_body=str(jsonData).replace("'", "\"")
            
        return [response_body]
        
httpd = make_server('', 8000, application)
print "Serving HTTP on port 8000..."
httpd.serve_forever()


