#db service layer
import sqlite3

def getUserInfo(**kw):
        conn=sqlite3.connect('ccSystem.db')
        cursor = conn.cursor()
        
        sql='select id,name,password from user where 1=1'
        param=[]
        for k, v in kw.iteritems():
                sql+=' and %s=?' % k
                param.append(v)

        cursor.execute(sql,tuple(param))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

def getUserInfoById(userid=None):
        conn=sqlite3.connect('ccSystem.db')
        cursor = conn.cursor()
        
        sql='select id,name,password from user'
        param=()
        
        if(userid!=None):
                sql+=' where id=?'
                param=(userid,)
        
        cursor.execute(sql,param)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
