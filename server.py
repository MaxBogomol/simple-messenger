import socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#server = input("Сервер --> ")
#port = input("Порт --> ")
#if server=="":
server="0.0.0.0"
#if port=="":
port=1883
port=int(port)
sock.bind ((server,port))
print(socket.gethostbyname(socket.gethostname()))
client = []
print ('Start Server')
while 1 :
         data , addres = sock.recvfrom(1024)
         print (addres[0], addres[1])
         print(client)
         if  addres not in client : 
                 client.append(addres)
         for clients in client :
                 if clients == addres : 
                     continue 
                 sock.sendto(data,clients)
