import socket
import threading
def read_sok():
     while 1 :
         data = sor.recv(1024)
         print(data.decode('utf-8'))
#server = input("Сервер --> ")
#port = input("Порт --> ")
#if server=="":
server="10.0.0.179"
#if port=="":
port=1883
port=int(port)
server = server,port
alias = input("Имя --> ") 
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sor.bind(('', 0)) 
sor.sendto((alias+' Connect to server').encode('utf-8'), server)
potok = threading.Thread(target= read_sok)
potok.start()
while 1 :
     mensahe = input()
     sor.sendto(('['+alias+'] '+mensahe).encode('utf-8'), server)
