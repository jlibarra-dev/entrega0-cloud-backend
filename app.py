from flask import Flask
import psycopg2
from flask_cors import CORS

# Server constants
SERVER_DIR = "54.165.45.105"
SERVER_DB = "eventmanagerdb"

app = Flask(__name__)
CORS(app)

# Login request


@app.route('/login/<email>/<password>')
def login(email, password):
    engine = psycopg2.connect(database=SERVER_DB, user="postgres",
                              password="postgres", host=SERVER_DIR, port='5432')
    cur = engine.cursor()
    cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
    rows = cur.fetchall()
    cur.close()
    engine.close()
    if not rows:
        return {'message': 'Incorrect email', }
    elif rows[0][2] != password:
        return {'message': 'Incorrect password'}
    else:
        return {'message': 'Correct auth', 'id': rows[0][0]}

# Register request


@app.route('/register/<email>/<password>/<username>')
def register(email, password, username):
    engine = psycopg2.connect(database=SERVER_DB, user="postgres",
                              password="postgres", host=SERVER_DIR, port='5432')
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
        return {'message': 'User registered'}
    else:
        engine.close()
        return {'message': 'Email in use'}

# Delete event request


@app.route('/deleteEvent/<id>')
def deleteEvent(id):
    engine = psycopg2.connect(database=SERVER_DB, user="postgres",
                              password="postgres", host=SERVER_DIR, port='5432')
    cur = engine.cursor()
    cur.execute(f"""DELETE FROM events WHERE eventid = {id};""")
    engine.commit()
    cur.close()
    engine.close()
    return {'message': 'Event deleted'}

# Get events request


@app.route('/getEvents/<id>')
def getEvents(id):
    print('Entro aca')
    engine = psycopg2.connect(database=SERVER_DB, user="postgres",
                              password="postgres", host=SERVER_DIR, port='5432')
    cur = engine.cursor()
    cur.execute(
        f"select * from events where userid = {id} order by fechacreacion desc")
    rows = cur.fetchall()
    cur.close()
    engine.close()
    if not rows:
        return {'message': 'Incorrect id', }
    else:
        return {'message': 'Correct query', 'events': rows}


# Create event request
@app.route('/createEvent/<name>/<category>/<place>/<startdate>/<finishdate>/<address>/<type>/<userid>')
def createEvent(name,category,place,startdate,finishdate,address,type,userid):
    engine = psycopg2.connect(database=SERVER_DB, user="postgres",
                              password="postgres", host=SERVER_DIR, port='5432')
    cur = engine.cursor()
    cur.execute(f"""INSERT INTO events
VALUES (DEFAULT, '{name}', '{category}', '{place}', '{startdate}', '{finishdate}', NOW(), '{address}', '{type}', {userid});""")
    engine.commit()
    cur.close()
    engine.close()
    return {'message': 'Event created'}
