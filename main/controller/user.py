import csv
import json
import sqlite3
import jwt
import flask
from flask import request, jsonify, make_response
import pandas as pd
from flask_cors import CORS, cross_origin
from flask_swagger import swagger
import  test as t

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/users', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@cross_origin()
def users(arr=None):
    if request.method == 'POST':
        userName = request.json['userName']
        email = request.json['email']
        password = request.json['password']
        available=''
        # Create connection Object
        conn = sqlite3.connect('pmtdb.db')
        print("Opened database successfully")
        parameterized_query = conn.execute("SELECT * FROM users WHERE EMAIL = ? AND PASSWORD = ?", (email, password))
        for row in parameterized_query:
            available = json.dumps({"ID": row[0], "NAME ": row[1], "EMAIL ": row[2], "PASSWORD ": row[3]})

        if available != '':
            response = app.response_class(
                response="Already Exist",
                status=200,
                mimetype='application/json'
            )
        else:
            conn.execute("INSERT INTO users (USERNAME,EMAIL,PASSWORD) VALUES  (?, ?, ?)", (userName, email, password))
            conn.commit()
            print("Records created successfully")
            cursor = conn.execute("SELECT * from users")
            for row in cursor:
                print(row[0])
                res = json.dumps({"ID": row[0], "NAME ": row[1], "EMAIL ": row[2]})
            response = app.response_class(
                response=res,
                status=200,
                mimetype='application/json'
            )
            print("Operation done successfully")
            conn.close()



        return response

    if request.method == 'GET':
        print("Im in userGEt")
        # Create connection Object
        conn = sqlite3.connect('pmtdb.db')
        cursor = conn.execute("SELECT * from users")

        print("Opened database successfully")
        cursor = conn.execute("SELECT * from users")
        conn.commit()

        rows = cursor.fetchall()
        arr = []
        for row in rows:
            y = {"ID": row[0], "userName": row[1], "email": row[2], "password": row[3]}
            arr.append(y)
            print(y)
        print("Array :", arr)
        return jsonify(arr)


@app.route('/api/authenticate', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@cross_origin()
def authenticate(arr=None, encoded=None):
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        res = ''
        token = ''
        response=''
        conn = sqlite3.connect('pmtdb.db')
        parameterized_query = conn.execute("SELECT * FROM users WHERE EMAIL = ? AND PASSWORD = ?", (email, password))
        for row in parameterized_query:
            res = json.dumps({"ID": row[0], "NAME": row[1], "EMAIL": row[2], "PASSWORD": row[3]})

        conn.close()
        if res != '':
            encoded = jwt.encode({'email': email}, 'pmtdb', algorithm='HS256')
            print("Payload :", jwt.decode(encoded, 'pmtdb', algorithms=['HS256']))
            response = app.response_class(
                response=res,
                status=200,
                mimetype='application/json'
            )
        else:
            response = app.response_class(
                response="UNAUTHORISED",
                status=200,
                mimetype='application/json'
            )

        print("RESPONSE:", response)
        return response

    if request.method == 'GET':
        conn = sqlite3.connect('pmtdb.db')
        sql = '''CREATE TABLE users(
           ID INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL,
           USERNAME CHAR(30) NOT NULL,
           EMAIL CHAR(30) NOT NULL,
           PASSWORD CHAR(30)  NOT NULL

        )'''
        conn.execute(sql)
        print("Table created successfully........")
        return "Success"


def  sample(request):
    userName = request.json['uname']
    password = request.json['pwd']

    res = json.dumps({"Username": userName, "Password": password})
    response = app.response_class(
        response=res,
        status=200,
        mimetype='application/json'
    )
    if userName != "":
        res = json.dumps({"Authentication": "Success", "Message": "You are Successfully authenticated"})
        return res
    res = json.dumps({"Authentication": "Failure", "Message": "Auth Failed"})
    return res









@app.route('/api/auth', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@cross_origin()
def test(arr=None, encoded=None):

    if request.method == 'GET':
        return "GET API response Success"

    if request.method == 'POST':
        print(request)
        #res= t.sample(request)
        response1 = sample(request)

        response = app.response_class(
            response=response1,
            status=200,
            mimetype='application/json'
        )
        return response






if __name__ == '__main__':
    app.run(debug=True, port=5000)
