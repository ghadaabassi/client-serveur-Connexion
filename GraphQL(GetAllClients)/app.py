from flask import Flask, render_template
from flask_cors import CORS
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema, List, Field, Int
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)

CORS(app, resources={r"/graphql": {"origins": "*"}})


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/rest_table'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(20))

class ClientType(ObjectType):
    
    id = Int()
    name = String()
    email = String()
    phone = String()

class Query(ObjectType):
    clients = List(ClientType, description="Get the list of clients")

    def resolve_clients(self, info):
        clients = Client.query.all()
        print("Clients from server:", clients)
        return clients


schema = Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.route('/')
def index():
    return render_template('client.html')

if __name__ == '__main__':

    app.run(debug=True)
