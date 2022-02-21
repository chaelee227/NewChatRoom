import socket 
import time
import threading
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-start', action="store_true")
parser.add_argument('-port')
#parser.add_argument('-passcode')
args = parser.parse_args()

#print(args.port)
#print(args.passcode)

port = args.port
clients = []
usernames = []
#userPwd = args.passcode
chatroom_pwd = "1234"


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
address = ('127.0.0.1', int(port))  
server.bind(address) 
server.listen(10)  

def broadcast(message): #sending a message from a server to all the clients
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try: #when we receive a message from the client, bradcast it to all other clients
            message = client.recv(1024)
            broadcast(message)
            print(message.decode("utf-8") )
        except: #cut the connection to this particular client and remove it from the list and terminate the function
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index] 
            broadcast(f'{username} left the chatroom'.encode('ascii'))
            usernames.remove(username) 
            break          

def receive():
    #클라이언트가 커넥트를 통해 연결요청을 받게되면
    while True:
    #client -> 소켓 통신용
    #s -> 서버소켓 연결용
        client, addr = server.accept() #연결허용 (client socket, rem_addr)반환  rem_Addr =ip +port
        
        print(f"Connected with {str(addr)}")
        #client.send(time.ctime(time.time()).encode()) #현재시간을 전송
        
        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        #userPwd = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)
        
        print(f'{username} joined the chatroom\n')
        broadcast(f'{username} joined the chatroom\n'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))
        
        thread = threading.Thread(target = handle, args=(client,))
        thread.start()
        
        #client.close() #소켓 종료



print ("*************************Listening for the clients*************************")
receive()

