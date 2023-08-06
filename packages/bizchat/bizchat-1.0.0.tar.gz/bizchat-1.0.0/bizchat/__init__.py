from socket import*


def server():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen()
    print("server listening...")
    connection, adress = server.accept()
    print("connected to client")

    while True:
        data = input("server : ")
        connection.send(bytes(data, 'utf-8'))
        recdata = connection.recv(1024).decode()
        print('client : ', recdata)
    server.close()


def client():
    client = socket()
    client.connect(('localhost', 9999))
    print("connected to server")

    while True:
        recdata = client.recv(1024).decode()
        print('server: ', recdata)
        data = input("client: ")
        client.send(bytes(data, 'utf-8'))
    client.close()
