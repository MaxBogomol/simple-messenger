import socket
import select
import random
import os
import json
import time

HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 25565

print(socket.gethostbyname(socket.gethostname()))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()
sockets_list = [server_socket]
server_socket.setblocking(0)
clients = {}

MESSAGES_PER_LOAD = 50

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
            self.userid = ID

            self.username_header = f"{len(self.username.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')
            self.usertag_header = f"{len(self.usertag.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')
            self.password_header = f"{len(self.password.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')
            self.userid_header = f"{len(self.userid.encode('utf-8')):<{HEADER_LENGTH}}".encode('utf-8')

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
        if header == 4:
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            
            return {'message_header': message_header, 'message': client_socket.recv(message_length),
                    'type': 4}
        if header == 100:
            return {'type': 100}
        else:
            return False
    except:
        return False

def send_users_data(client_socket):
    with open('users.json','r', encoding="utf-8") as f:
        users = json.load(f)
        for ID in users.keys():
            if not ID == "total":
                userid = ID.encode('utf-8')
                username = users[ID]["username"].encode('utf-8')
                usertag = users[ID]["usertag"].encode('utf-8')

                socket_header = f"{3:<{HEADER_LENGTH}}".encode('utf-8')
                userid_header = f"{len(userid):<{HEADER_LENGTH}}".encode('utf-8')
                username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
                usertag_header = f"{len(usertag):<{HEADER_LENGTH}}".encode('utf-8')
                    
                client_socket.send(socket_header + userid_header + username_header + usertag_header + userid + username + usertag)

def send_messages_data(client_socket):
    with open('messages.json','r', encoding="utf-8") as f:
        users = json.load(f)
        for ID in users.keys():
            if not ID == "total":
                userid = users[ID]["userid"].encode('utf-8')
                messageid = ID.encode('utf-8')
                data = users[ID]["data"].encode('utf-8')

                socket_header = f"{0:<{HEADER_LENGTH}}".encode('utf-8')
                userid_header = f"{len(userid):<{HEADER_LENGTH}}".encode('utf-8')
                messageid_header = f"{len(messageid):<{HEADER_LENGTH}}".encode('utf-8')
                data_header = f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')
                    
                client_socket.send(socket_header + userid_header + userid + messageid_header + messageid + data_header + data)

def send_messages_data_end(client_socket, count):
    with open('messages.json','r', encoding="utf-8") as f:
        users = json.load(f)
        total = users["total"] - count
        for ID in users.keys():
            if not ID == "total":
                if int(ID) >= total - 1:
                    userid = users[ID]["userid"].encode('utf-8')
                    messageid = ID.encode('utf-8')
                    data = users[ID]["data"].encode('utf-8')

                    socket_header = f"{0:<{HEADER_LENGTH}}".encode('utf-8')
                    userid_header = f"{len(userid):<{HEADER_LENGTH}}".encode('utf-8')
                    messageid_header = f"{len(messageid):<{HEADER_LENGTH}}".encode('utf-8')
                    data_header = f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')
                        
                    client_socket.send(socket_header + userid_header + userid + messageid_header + messageid + data_header + data)

def send_messages_data_count_up(client_socket, message_id, count):
    with open('messages.json','r', encoding="utf-8") as f:
        users = json.load(f)
        if message_id - count < 0:
            count = count + (message_id - count)
        if message_id > 1:
            for i in range(0, count):
                ID = str(message_id - i)
                
                userid = users[ID]["userid"].encode('utf-8')
                messageid = ID.encode('utf-8')
                data = users[ID]["data"].encode('utf-8')

                socket_header = f"{5:<{HEADER_LENGTH}}".encode('utf-8')
                userid_header = f"{len(userid):<{HEADER_LENGTH}}".encode('utf-8')
                messageid_header = f"{len(messageid):<{HEADER_LENGTH}}".encode('utf-8')
                data_header = f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')

                client_socket.send(socket_header + userid_header + userid + messageid_header + messageid + data_header + data)
            
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

            if user['type'] == 101:
                client_socket.send(f"{101:<{HEADER_LENGTH}}".encode('utf-8'))
            
            print('Accepted new connection from {}'.format(client_address))
        else:
            message = receive_message(notified_socket)

            if message is False:
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

                        send_users_data(client_socket)
                        send_messages_data_end(client_socket, MESSAGES_PER_LOAD)

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

                        send_users_data(client_socket)
                        send_messages_data_end(client_socket, MESSAGES_PER_LOAD)
                        
                        print('New login from {}:{}, username: {}#{}'.format(*client_address, username, usertag))
                    else:
                        connect = "0".encode('utf-8')
                        socket_header = f"{2:<{HEADER_LENGTH}}".encode('utf-8')
                        connect_header = f"{len(connect):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(socket_header + connect_header + connect)
                    
            else:
                if message['type'] == 0:
                    print(f'Received message from {user.username}#{user.usertag}: {message["data"].decode("utf-8")}')

                    if not os.path.isfile('./messages.json'):
                        my_file = open('./messages.json', 'w')
                        my_file.write('{}')
                        my_file.close()
                    with open('messages.json','r', encoding="utf-8") as f:
                        messages = json.load(f)
                        if not "total" in messages:
                            messages["total"] = 0
                        messages[str(messages["total"])] = {}
                        messages[str(messages["total"])]["userid"] = user.userid
                        messages[str(messages["total"])]["data"] =  message['data'].decode('utf-8')
                        total = messages["total"]
                        messages["total"] = messages["total"] + 1
                    with open('messages.json','w', encoding="utf-8") as f:
                        json.dump(messages,f)

                    for client_socket in clients:
                        #if client_socket != notified_socket:
                        socket_header = f"{0:<{HEADER_LENGTH}}".encode('utf-8')
                        total = str(total).encode('utf-8')
                        total_header = f"{len(total):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(socket_header + user.userid_header + user.userid.encode('utf-8') + total_header + total + message['header'] + message['data'])

                if message['type'] == 4:
                    for client_socket in clients:
                        if client_socket == notified_socket:
                            send_messages_data_count_up(client_socket, int(message['message'].decode('utf-8')), MESSAGES_PER_LOAD)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
