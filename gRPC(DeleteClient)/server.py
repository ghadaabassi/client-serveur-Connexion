import grpc
import concurrent.futures
import clients_pb2
import clients_pb2_grpc
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(20))


engine = create_engine('mysql+pymysql://root:1234@localhost/rest_table', echo=True)
Base.metadata.create_all(bind=engine)

class ClientService(clients_pb2_grpc.ClientServiceServicer):
    def DeleteClient(self, request, context):
        email_to_delete = request.email

        try:

            Session = sessionmaker(bind=engine)
            session = Session()


            client_to_delete = session.query(Client).filter_by(email=email_to_delete).first()

            if client_to_delete:
                session.delete(client_to_delete)
                session.commit()

                return clients_pb2.ClientResponse(success=True, message=f"Client with email '{email_to_delete}' deleted successfully")
            else:
                return clients_pb2.ClientResponse(success=False, message=f"Client with email '{email_to_delete}' not found")

        except Exception as e:
            return clients_pb2.ClientResponse(success=False, message=f"Error deleting client: {str(e)}")

def serve():
    server = grpc.server(concurrent.futures.ThreadPoolExecutor())
    clients_pb2_grpc.add_ClientServiceServicer_to_server(ClientService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
