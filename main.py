import json
import time

from flask import Flask,request

app=Flask(__name__)
import queue,datetime

# import pymysql
import random
from pathlib import Path
import os,sys
import sqlite3
mysqlhost='localhost'
mysql_user='root'
password='123456'
root_path=Path(os.path.abspath(__file__)).parent
project=str(Path(root_path).parent)
sys.path.append(project)
sys.path.append(root_path)
source="sqlite3"
# source="mysql"
def db_source():
    global sql_str
    if source=='sqlite3' :
        import sqlite3
        sql_str='?'
        con = sqlite3.connect("db.sqlite3")
        return con
    if source=='mysql' :
        import pymysql
        con = pymysql.connect(host=mysqlhost, user=mysql_user, password=password, db='test', charset='utf8')
        sql_str = '%s'
        return con
def add_space_mysql(data):
    #
    # con=sqlite3.connect(Path(os.path.abspath(__file__)).parent.parent/Path("db.sqlite3"))
    con=db_source()
    cur=con.cursor()
    sql=f"insert into space(spaceid,level,spacename,parentid,code)values({sql_str},{sql_str},{sql_str},{sql_str},{sql_str})"
    # sql=f"insert into defspace(spaceid,level,spacename,parentid)value({spaceid},{level},{spacename},{parentid})"
    cur.execute(sql,data)
    con.commit()
    cur.close()
    con.close()
def add_organization_mysql(data):
    #
    # con=sqlite3.connect(Path(os.path.abspath(__file__)).parent.parent/Path("db.sqlite3"))
    con=db_source()
    cur=con.cursor()
    sql=f"insert into organization(spaceid,organizationid)values({sql_str},{sql_str})"
    # sql=f"insert into defspace(spaceid,level,spacename,parentid)value({spaceid},{level},{spacename},{parentid})"
    cur.execute(sql,data)
    con.commit()
    cur.close()
    con.close()
def add_operator_mysql(data):

    # con=sqlite3.connect(Path(os.path.abspath(__file__)).parent.parent/Path("db.sqlite3"))
    con=db_source()
    cur=con.cursor()
    sql=f"insert into operator(operatorid,organizationid)values({sql_str},{sql_str})"
    # sql=f"insert into defspace(spaceid,level,spacename,parentid)value({spaceid},{level},{spacename},{parentid})"
    cur.execute(sql,data)
    con.commit()
    cur.close()
    con.close()
a=queue.Queue()

def datatime_num():
    if a.qsize()<5:
        for i in range(11,99):
            a.put_nowait(i)
    b=datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    return b+str(a.get())
def num_to_list(num,num_list):
    return num_list if num//13<1 else num_to_list(num//13,num_list+[num%13])
def get_zimu():
    a=num_to_list(int(datatime_num()),[])
    c=[chr(int(i)+random.choice([97,110,65,78])) for i in a]
    return ''.join(c)

@app.route('/service/space/0.1.0/add',methods=['POST'])
def addspace():
    body=json.loads(request.get_data())
    code=body['code']
    level=body['level']
    spacename=body['spacename']
    parentid=body["spacename"]
    spaceid=get_zimu()
    time.sleep(0.3)
    add_space_mysql((spaceid,level,spacename,parentid,code))
    time.sleep(0.1)
    return json.dumps({"recode":0,"result":[{"spaceid":spaceid}]})
@app.route('/service/organization/0.1.0/add',methods=['POST'])
def addorganization():
    body=json.loads(request.get_data())
    spaceid=body['spaceid']

    organizationid=get_zimu()
    time.sleep(0.3)
    add_organization_mysql((spaceid,organizationid))
    time.sleep(0.1)
    return json.dumps({"recode":0,"result":[{"organizationid":organizationid}]})
@app.route('/service/operator/0.1.0/add',methods=['POST'])
def addoperator():
    body=json.loads(request.get_data())
    organizationid=body['organizationid']

    operatorid=get_zimu()
    time.sleep(0.3)
    add_operator_mysql((operatorid,organizationid))
    time.sleep(0.1)
    return json.dumps({"recode":0,"result":[{"operatorid":operatorid}]})

if __name__=='__main__':
    app.run()