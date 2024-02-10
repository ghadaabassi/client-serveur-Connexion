from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
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

class ClientService(ServiceBase):
    @rpc(Unicode, Unicode, Unicode, _returns=Unicode)
    def add_client(ctx, name, email, phone):
        try:
            with connection.cursor() as cursor:
                
                sql = "INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)"
                cursor.execute(sql, (name, email, phone))
                connection.commit()
           
            soap_response = f"""
                <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:web="urn:client_service">
                    <soapenv:Header/>
                    <soapenv:Body>
                        <web:add_clientResponse>
                        <result>Client added successfully to the database.</result>
                        </web:add_clientResponse>
                    </soapenv:Body>
                </soapenv:Envelope>
            """
            
            return soap_response
        except Exception as e:
           
           soap_error_response = f"""
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
        xmlns:web="urn:client_service">
        <soapenv:Header/>
        <soapenv:Body>
            <soapenv:Fault>
                <faultcode>soapenv:Client</faultcode>
                <faultstring>Error adding client: {str(e)}</faultstring>
            </soapenv:Fault>
        </soapenv:Body>
    </soapenv:Envelope>
"""
        return soap_error_response

application = Application([ClientService], 'urn:client_service', in_protocol=Soap11(validator='lxml'), out_protocol=Soap11())
wsgi_application = WsgiApplication(application)


@app.route('/', methods=['POST'])
def soap_endpoint():
   
    def start_response(status, headers, exc_info=None):
        return

    try:
        response = wsgi_application(request.environ, start_response)
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return render_template('soap_index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8095, debug=True)
