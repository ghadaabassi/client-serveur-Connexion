import grpc
import clients_pb2
import clients_pb2_grpc

def delete_client(email):
    channel = grpc.insecure_channel('localhost:50051')
    stub = clients_pb2_grpc.ClientServiceStub(channel)

    request = clients_pb2.ClientRequest(email=email)
    response = stub.DeleteClient(request)

    return response.success, response.message

if __name__ == '__main__':
    email_to_delete="mame@gmail.com"
    success, message = delete_client(email_to_delete)

    if success:
        print(f"Client with email '{email_to_delete}' deleted successfully")
    else:
        print(f"Error deleting client: {message}")
