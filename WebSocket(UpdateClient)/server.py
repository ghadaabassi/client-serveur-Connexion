from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import mysql.connector


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*") 
CORS(app, resources={r"/*": {"origins": "*"}}) 

@app.route('/')
def index():
    return render_template('client.html')

@socketio.on('get_data')
def handle_get_data(email):
    db = mysql.connector.connect(
       host="localhost",
        user="root",
        password="1234",
        database="rest_table"
    )
    cursor = db.cursor()
    query = f"SELECT * FROM clients WHERE email = '{email}';"
    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        socketio.emit('display_data', {'name': result[1], 'email': result[2] , 'phone': result[3]})
    else:
        socketio.emit('display_data', {'error': 'Client not found'})
    cursor.close()
    db.close()

@socketio.on('update_data')
def handle_update_data(data):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="rest_table"
    )
    cursor = db.cursor()

    query = f"UPDATE clients SET name = '{data['name']}', email = '{data['email']}' , phone='{data['phone']}' WHERE email = '{data['email']}';"
    cursor.execute(query)
    db.commit()

    cursor.close()
    db.close()

if __name__ == '__main__':
    socketio.run(app, port=9090, debug=True)
