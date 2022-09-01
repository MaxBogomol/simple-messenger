import socket
import select
import random
import os
import json

HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 25565

print(socket.gethostbyname(socket.gethostname()))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}

print(f'Listening for connections on {IP}:{PORT}...')

class User():
    def __init__(self, ID):
        if not os.path.isfile('./users.json'):
            my_file = open('./users.json', 'w')
            my_file.write('{}')
            my_file.close()
        with open('users.json','r', encoding="utf-8") as f:
            users = json.load(f)
            self.username = users[ID]["username"]
            self.usertag = users[ID]["usertag"]
            self.password = users[ID]["password"]

            self.username_header = f"{len(self.username.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')
            self.usertag_header = f"{len(self.usertag.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')
            self.password_header = f"{len(self.password.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')

    def can_connect(username, usertag, password):
        connect = None
        if not os.path.isfile('./users.json'):
            my_file = open('./users.json', 'w')
            my_file.write('{}')
            my_file.close()
        with open('users.json','r', encoding="utf-8") as f:
            users = json.load(f)
            for ID in users.keys():
                if not ID == "total":
                    if users[ID]["username"] == username and users[ID]["usertag"] == usertag and users[ID]["password"] == password:
                        connect = ID
        return connect

    def can_registration(username):
        reg = None
        tags = []
        for i in range(0, 9999):
            tags.append(i)
        if not os.path.isfile('./users.json'):
            my_file = open('./users.json', 'w')
            my_file.write('{}')
            my_file.close()
        with open('users.json','r', encoding="utf-8") as f:
            users = json.load(f)
            for ID in users.keys():
                if not ID == "total":
                    if users[ID]["username"] == username:
                        tags.remove(int(users[ID]["usertag"]))
                        
        if len(tags):
            reg = tags[random.randint(0,len(tags))]
            usertag_len = 4 - len(str(reg))
            usertag = "0" * usertag_len
            usertag = usertag + str(reg)
            reg = usertag

        return reg

    def registration(username, usertag, password):
        if not os.path.isfile('./users.json'):
            my_file = open('./users.json', 'w')
            my_file.write('{}')
            my_file.close()
        with open('users.json','r', encoding="utf-8") as f:
            users = json.load(f)
            if not "total" in users:
                users["total"] = 0
            ID = users["total"]
            users["total"] = users["total"] + 1
            users[ID] = {}
            users[ID]["username"] = username
            users[ID]["usertag"] = usertag
            users[ID]["password"] = password
        with open('users.json','w', encoding="utf-8") as f:
            json.dump(users,f)
        

def receive_message(client_socket):
    try:
        socket_header = client_socket.recv(HEADER_LENGTH)

        if not len(socket_header):
            return False

        header = int(socket_header.decode('utf-8').strip())
        if header == 1:
            username_header = client_socket.recv(HEADER_LENGTH)
            username_length = int(username_header.decode('utf-8').strip())
            password_header = client_socket.recv(HEADER_LENGTH)
            password_length = int(password_header.decode('utf-8').strip())
            
            return {'username_header': username_header, 'password_header': password_header,
                    'username': client_socket.recv(username_length), 'password': client_socket.recv(password_length),
                    'type': 1}
        if header == 2:
            username_header = client_socket.recv(HEADER_LENGTH)
            username_length = int(username_header.decode('utf-8').strip())
            usertag_header = client_socket.recv(HEADER_LENGTH)
            usertag_length = int(usertag_header.decode('utf-8').strip())
            password_header = client_socket.recv(HEADER_LENGTH)
            password_length = int(password_header.decode('utf-8').strip())

            return {'username_header': username_header, 'usertag_header': usertag_header, 'password_header': password_header,
                    'username': client_socket.recv(username_length), 'usertag': client_socket.recv(usertag_length), 'password': client_socket.recv(password_length),
                    'type': 2}
        if header == 0:
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
                
            return {'header': message_header, 'data': client_socket.recv(message_length),
                    'type': 0}
        if header == 100:
            return {'type': 100}
        else:
            return False
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            clients[client_socket] = None

            print('Accepted new connection from {}'.format(client_address))
        else:
            message = receive_message(notified_socket)

            if message is False:
                #print('Closed connection from: {}#{}'.format(clients[notified_socket]['username'].decode('utf-8'), clients[notified_socket]['usertag'].decode('utf-8')))
                print('Closed connection from: {}'.format(client_address))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            if user == None:
                if message['type'] == 1:
                    username = message['username'].decode('utf-8')
                    password = message['password'].decode('utf-8')
                
                    usertag = User.can_registration(username)
                    if not usertag == None:
                        User.registration(username, usertag, password)
                        ID = User.can_connect(username, usertag, password)
                        clients[notified_socket] = User(ID)

                        usertag = usertag.encode('utf-8')
                        connect = "1".encode('utf-8')
                        socket_header = f"{1:<{HEADER_LENGTH}}".encode('utf-8')
                        connect_header = f"{len(connect):<{HEADER_LENGTH}}".encode('utf-8')
                        usertag_header = f"{len(usertag):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(socket_header + connect_header + usertag_header + connect + usertag)

                        print('New registration from {}:{}, username: {}#{}'.format(*client_address, username, usertag.decode('utf-8')))
                    else:
                        usertag = usertag.encode('utf-8')
                        connect = "0".encode('utf-8')
                        socket_header = f"{1:<{HEADER_LENGTH}}".encode('utf-8')
                        connect_header = f"{len(connect):<{HEADER_LENGTH}}".encode('utf-8')
                        usertag_header = f"{len(usertag):<{HEADER_LENGTH}}".encode('utf-8')
                        
                        client_socket.send(socket_header + connect_header + usertag_header + connect + usertag)
                        
                if message['type'] == 2:
                    username = message['username'].decode('utf-8')
                    usertag = message['usertag'].decode('utf-8')
                    password = message['password'].decode('utf-8')
                    
                    ID = User.can_connect(username, usertag, password)
                    if not ID == None:

                        clients[notified_socket] = User(ID)

                        connect = "1".encode('utf-8')
                        socket_header = f"{2:<{HEADER_LENGTH}}".encode('utf-8')
                        connect_header = f"{len(connect):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(socket_header + connect_header + connect)
                        
                        print('New login from {}:{}, username: {}#{}'.format(*client_address, username, usertag))
                    else:
                        connect = "0".encode('utf-8')
                        socket_header = f"{2:<{HEADER_LENGTH}}".encode('utf-8')
                        connect_header = f"{len(connect):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(socket_header + connect_header + connect)
                    
            else:
                print(f'Received message from {user.username}#{user.usertag}: {message["data"].decode("utf-8")}')

                for client_socket in clients:
                    if client_socket != notified_socket:
                        socket_header = f"{0:<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(socket_header + user.username_header + user.usertag_header + user.username.encode('utf-8') + user.usertag.encode('utf-8') + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
