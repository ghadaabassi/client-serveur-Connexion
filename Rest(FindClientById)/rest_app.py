from flask import Flask, render_template, jsonify
from flask_cors import CORS
import pymysql.cursors

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}) 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'rest_table'

connection = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB'],
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/client/<int:client_id>', methods=['GET'])
def get_client(client_id):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM clients WHERE id = {client_id}")
        client_data = cursor.fetchone()

    if client_data:
        client = {
            'id': client_data['id'],
            'name': client_data['name'],
            'email': client_data['email'],
            'phone': client_data['phone']
        }
        return jsonify(client)
    else:
        return jsonify({'error': 'Client not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090, debug=True)
    app.run(debug=True)

