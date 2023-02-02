from flask import Flask
import psycopg2
from flask_cors import CORS

# Server constants
SERVER_DIR = "54.160.96.31"
SERVER_DB = "eventmanagerdb"

app = Flask(__name__)
CORS(app)

# Login request
@app.route('/login/<email>/<password>')
def login(email, password):
    engine = psycopg2.connect(database=SERVER_DB,user="postgres",password="postgres",host=SERVER_DIR,port='5432')
    cur = engine.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
    rows = cur.fetchall()
    cur.close() 
    engine.close()
    if not rows:
        return {'message':'Incorrect email'}
    elif rows[0][2] != password:
        return {'message':'Incorrect password'}
    else:
        return f"<p>Hello, {rows[0][3]}, id: {rows[0][0]}!</p>"

# Register request
@app.route('/register/<email>/<password>/<username>')
def register(email, password, username):
    engine = psycopg2.connect(database=SERVER_DB,user="postgres",password="postgres",host=SERVER_DIR,port='5432')
    cur = engine.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
    rows = cur.fetchall()
    cur.close() 
    if not rows:
        cur = engine.cursor()
        cur.execute(f"""INSERT INTO users (email, password, username)
            VALUES ('{email}', '{password}', '{username}');""")
        engine.commit()
        cur.close()
        engine.close()
        return {'message':'User registered'}
    else:
        engine.close()
        return {'message':'Email in use'}
        
    
