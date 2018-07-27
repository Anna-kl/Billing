"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import Flask, jsonify,request
from Billing import app
import psycopg2
import requests
import json

@app.route('/')
@app.route('/bill',methods=['POST'])
def home():
    if not request.json:
        abort(400)
    conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
    try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
    except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
    answer=request.json
    answer=json.loads(answer)
    if answer['resource']=='Selectel':
        if answer['task']=='bill':
           
                
                url='https://mandarin-solutions.bitrix24.ru/rest/43/0qznu04iuae09fvm/crm.company.get?ID=test'
    
                data=requests.get(url)
                bill=0
               
                id=str(answer['id'])
                url=url.replace('test',id)
                data=requests.get(url)
                data=data.content.decode('utf8','replace')
                data=json.loads(data)
                data=data['result']
                money=float(data['UF_CRM_1507212611'])
                quotas=answer['quotas']
                sql='''SELECT base_disk, fast_disk, universal_disk, ram, vcpu, public_network_253, public_network_125, public_network_61, public_network_29, public_network_13, public_network_5, floating_api, licence_windows, over_limit
FROM billing.price;'''
                try:
                    cur = conn.cursor()

                    cur.execute(sql)
                    data = cur.fetchall()

                except psycopg2.Error as err:
                    print("Query error: {}".format(err))
                cores=quotas['compute_cores']
                if cores is not None:
                    bill+=(float)(data[0][4])*(float)(cores[0]['value'])
                RAM=quotas['compute_ram']
                if RAM is not None:
                     bill+=(float)(data[0][3])*(float)(RAM[0]['value'])
                try:
                    Basic=quotas['volume_gigabytes_basic']
             
                    bill+=(float)(data[0][3])*(float)(Basic[0]['value'])
                except:
                    bill+=0
                try:
                    Fast=quotas['volume_gigabytes_fast']
                    bill+=(float)(data[0][3])*(float)(Fast[0]['value'])
                except:
                    bill+=0
                try:
                    Universal=quotas['volume_gigabytes_universal']
                
                    bill+=(float)(data[0][3])*(float)(Universal[0]['value'])
                except:
                    bill+=0
                responce={}
                responce['bill']=bill
                responce['status']='Ok'
                if money>bill:
                  return jsonify(responce)
                else:
                    return jsonify({'bill': bill, 'status':'Ok'})
        
        elif answer['task']=='subnet':
            sql='''SELECT public_network_253 FROM billing.price;'''
            prefix=str(answer['prefix'])
            sql=sql.replace('_253', '_'+prefix)
            try:
                    cur = conn.cursor()

                    cur.execute(sql)
                    prefix = cur.fetchall()

            except psycopg2.Error as err:
                    print("Query error: {}".format(err))
            url='https://mandarin-solutions.bitrix24.ru/rest/43/0qznu04iuae09fvm/crm.company.get?ID=test'
            id=str(answer['id'])
            url=url.replace('test',id)
            data=requests.get(url)
            data=data.content.decode('utf8','replace')
            data=json.loads(data)
            data=data['result']
            money=prefix[0][0]
            money=float(data['UF_CRM_1507212611'])
            if float(prefix[0][0])<money:
                responce={}
                responce['bill']=money
                responce['report']='Ok'
                return jsonify(responce)
            else:
                    return jsonify({'report': 'enough'})
        elif answer['task']=='floating_ip':
            sql='''SELECT floating_api FROM billing.price;'''
            
            try:
                    cur = conn.cursor()

                    cur.execute(sql)
                    prefix = cur.fetchall()

            except psycopg2.Error as err:
                    print("Query error: {}".format(err))
            wasting=prefix[0][0]*float(answer['count_ip'])
            url='https://mandarin-solutions.bitrix24.ru/rest/43/0qznu04iuae09fvm/crm.company.get?ID=test'
            id=str(answer['id'])
            url=url.replace('test',id)
            data=requests.get(url)
            data=data.content.decode('utf8','replace')
            data=json.loads(data)
            data=data['result']
           
            money=float(data['UF_CRM_1507212611'])
            if float(wasting)<money:
                responce={}
                responce['bill']=wasting
                responce['report']='Ok'
                return jsonify(responce)
            else:
                    return jsonify({'report': 'enough'})






@app.route('/information',methods=['POST'])
def contact():
    if not request.json:
        abort(400)
    conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
    try:
        conn = psycopg2.connect(database="postgres", user="postgres", password="2537300", port=5433)
    except psycopg2.Error as err:
        print("Connection error: {}".format(err))
    answer = request.json
    answer = json.loads(answer)
    if answer['task'] == 'create_project':
        sql = '''INSERT INTO billing.information (id_company, date_start, id_project, bill, "Full", description,id_services) VALUES('''
        sql += str(answer['id_company']) + ',\'' + str(datetime.now()) + '\',\'' + answer['id_project'] + '\',' + str(
            answer['bill']) + '\',' + 'project' + '\''+',\''+answer['id_project']+'\');'
        try:
            cur = conn.cursor()

            cur.execute(sql)
            conn.commit()
        except psycopg2.Error as err:
            jsonify({'report': err})
        return jsonify({'report': 'Ok'})

    elif answer['task'] == 'subnet':
        if answer['status'] == 'buy':
            sql = '''INSERT INTO billing.information (id_company, date_start, id_project, bill, "Full", description,id_services) VALUES('''
            sql += str(answer['id_company']) + ',\'' + str(datetime.now()) + '\',\'' + answer[
                'id_project'] + '\',' + str(answer['bill']) + ',\'' + answer['full'] + '\',\'buy subnet\',\''+str(answer['id_services'])+'\');'
            try:
                cur = conn.cursor()

                cur.execute(sql)
                conn.commit()
            except psycopg2.Error as err:
                jsonify({'report': err})
            return jsonify({'report': 'Ok'})
        elif answer['status'] == 'delete':
            sql='''UPDATE billing.information
SET date_end='test1' where id_project='test2' and id_services='test3';'''
            sql=sql.replace('test1',str(datetime.now())).replace('test2',answer['id_project']).replace('test3',answer['id_project'])
            try:
                cur = conn.cursor()

                cur.execute(sql)
                conn.commit()
            except psycopg2.Error as err:
                jsonify({'report': err})
            return jsonify({'report': 'Ok'})
    elif answer['task'] == 'floating_ip':
        if answer['status'] == 'buy':
            sql = '''INSERT INTO billing.information (id_company, date_start, id_project, bill, "Full", description,id_services ) VALUES('''
            sql += str(answer['id_company']) + ',\'' + str(datetime.now()) + '\',\'' + answer['id_project'] + '\',' + str(answer['bill']) + ',\'' + answer['full'] + '\',\'buy ip\',\''+answer['id_services']+'\');'
            try:
                cur = conn.cursor()

                cur.execute(sql)
                conn.commit()
            except psycopg2.Error as err:
                jsonify({'report': err})
            return jsonify({'report': 'Ok'})
    elif answer['task'] == 'delete_project':
        
            sql = '''UPDATE billing.information SET date_end='test1' where id_project='test2' and id_services='test3';'''
            sql=sql.replace('test1',str(datetime.now())).replace('test2',answer['id_project']).replace('test3',answer['id_services'])
            try:
                cur = conn.cursor()

                cur.execute(sql)
                conn.commit()
            except psycopg2.Error as err:
                jsonify({'report': err})
            return jsonify({'report': 'Ok'})
 





@app.route('/region',methods=['POST'])
def about():
    if not request.json:
        abort(400)
    conn_string = "dbname='PostgreSQL 9.5' user='postgres' host='localhost' password='2537300' port='5433'"
    try:
                    conn = psycopg2.connect(database="postgres", user="postgres", password="2537300",port=5433)
    except psycopg2.Error as err:
                    print("Connection error: {}".format(err))
    answer=request.json
    ##answer=json.loads(answer)
    if answer['resource']=='Selectel':
        if answer['task']=='get_zone':
            sql='''SELECT id, "name" FROM resources.region;'''
            try:
                cur = conn.cursor()
     
                cur.execute(sql)
                data=cur.fetchall()
            except psycopg2.Error as err:
                    jsonify({'report': err})
            return jsonify(data)

