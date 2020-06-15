from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
from datetime import datetime
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
user_session_key='user'

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

##INDEX.HTML
@app.route('/', methods=['GET'])
def get_index():
    return render_template('index.html')

##AUTHENTICATE
@app.route("/authenticate",methods=['POST'])
def authenticate():
    b = json.loads(request.data)
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User).filter(entities.User.username==b['username']).filter(entities.User.password==b['password'])
    db_session.close()
    user = respuesta[:]
#   if b['username']==b['password']:
    if user:
        session[user_session_key] = json.dumps(user[0], cls= connector.AlchemyEncoder)
        msg = {'message':'ok'}
        json_message = json.dumps(msg, cls=connector.AlchemyEncoder)
        rpta = Response(json_message, status = 200, mimetype = 'application/json')
    else:
        msg = {'message':'F'}
        json_message = json.dumps(msg, cls=connector.AlchemyEncoder)
        rpta = Response(json_message, status = 202, mimetype = 'application/json')
    return rpta

##CRUD users
@app.route('/users', methods = ['POST'])
def create_user():
    #c = json.loads(request.data)
    c = json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    session.close()
    r_msg = {'msg':'UserCreated'}
    json_msg = json.dumps(r_msg)
    return Response(json_msg, status=201)

@app.route('/current', methods = ['GET'])
def current():
    user_json = session['user']
    return Response(user_json, status=200, mimetype='application/json')

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    db_session.close()
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')
    message = { 'status': 404, 'message': 'Not Found'}
    return Response(json.dumps(message), status=404, mimetype='application/json')

#------------cache
cache = {}
key_users ='users'

@app.route('/users', methods = ['GET'])
def get_users():
    data = []
    update_cache: bool = False
    max_time = 20

    if key_users in cache:
        update_cache = (datetime.now() - cache[key_users]['time']).total_seconds() < max_time
        #Get cache
        data = cache[key_users]['data']
    else:
        update_cache = True

    if update_cache:
        session = db.getSession(engine)
        dbResponse = session.query(entities.User).order_by(entities.User.username)
        session.close()
        data = dbResponse[:]
        #Set cache
        cache[key_users] = {'data':data, 'time':datetime.now()}
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    session.close()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])

    session.add(user)
    session.commit()
    session.close()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    user = session.query(entities.User).filter(entities.User.id == id).one()
    session.delete(user)
    session.commit()
    session.close()
    return "Deleted User"

## Tarea
#CRUD messages--------------------------------------------
@app.route('/messages', methods = ['POST'])
def createMessage():
    new = json.loads(request.form['values'])
    new_message = entities.Message(
        content=new['content'],
        user_from_id=new['user_from_id'],
        user_to_id=new['user_to_id']
    )
    session = db.getSession(engine)
    session.add(new_message)
    session.commit()
    session.close()
    rpt = {'message':'Mensaje creado'}
    json_msg = json.dumps(rpt)
    return Response(json_msg, status=201)

@app.route('/messages/<id>', methods = ['GET'])
def getMessage(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    db_session.close()
    for message in messages:
        js = json.dumps(message, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')
    msg = { 'status': 404, 'message': 'No existe'}
    return Response(json.dumps(msg), status=404, mimetype='application/json')

@app.route('/messages', methods = ['GET'])
def getMessages():
    session = db.getSession(engine)
    rdmsg = session.query(entities.Message)
    session.close()
    contenido = rdmsg[:]
    return Response(json.dumps(contenido, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/messages', methods = ['PUT'])
def updateMessage():
    session = db.getSession(engine)
    id = request.form['key']
    msg = session.query(entities.Message).filter(entities.Message.id == id).first()
    now = json.loads(request.form['values'])
    for key in now.keys():
        setattr(msg, key, now[key])
    session.add(msg)
    session.commit()
    session.close()
    return 'Mensaje actualizado'

@app.route('/messages', methods = ['DELETE'])
def deleteMessage():
    id = request.form['key']
    session = db.getSession(engine)
    msg= session.query(entities.Message).filter(entities.Message.id == id).one()
    session.delete(msg)
    session.commit()
    session.close()
    return "Mensaje borrado"
#--------------------------Chat
@app.route('/sendMessages', methods = ['POST'])
def createMessageChat():
    new = json.loads(request.data)
    new_message = entities.Message(
        content=new['content'],
        user_from_id=new['user_from_id'],
        user_to_id=new['user_to_id']
    )
    session = db.getSession(engine)
    session.add(new_message)
    session.commit()
    session.close()
    rpt = {'message':'Mensaje creado'}
    json_msg = json.dumps(rpt)
    return Response(json_msg, status=201)


@app.route('/messages/<user_from>/<user_to>', methods = ['GET'])
def get_message_chat(user_from, user_to):
    db_session = db.getSession(engine)
    #messages = db_session.query(entities.Message).filter(entities.Message.user_from_id == user_from).filter(entities.Message.user_to_id == user_to)
    messages = db_session.query(entities.Message).filter((entities.Message.user_from_id == user_from) | ( entities.Message.user_from_id == user_to), (entities.Message.user_to_id == user_from) | (entities.Message.user_to_id == user_to))
    db_session.close()
    data=messages[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/logout', methods=['GET'])
def logout():
    if user_session_key in session:
        session.pop(user_session_key)
    response = {'message':'Cerrar sesión'}
    json_response = json.dumps(response)
    return Response(json_response, mimetype='application/json')

#main
if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
