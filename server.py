import socket, time, threading, sys, argparse
from datetime import datetime
from datetime import timedelta

parser = argparse.ArgumentParser()
parser.add_argument('-start', action="store_true")
parser.add_argument('-port')
parser.add_argument('-passcode')
args = parser.parse_args()

#print(args.port)
#print(args.passcode)

port = args.port
clients = []
usernames = []
userPwd = args.passcode
chatroom_pwd = args.passcode
host = "127.0.0.1"

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
            msgList = message.split()
            name = msgList[0].decode("utf-8")
            msg = msgList[1].decode("utf-8")
            exitlist = name.split(":")
            exitname = exitlist[0]
            #print(type(msg))
            #print("this is name " + name)
            #print("this is msg " + msg)
            if(msg == ":)"):
                print(name+ " [feeling happy]")
                sys.stdout.flush()
                broadcast((name+" [feeling happy]").encode())
                continue
            
            elif(msg == ":("):
                print(name+ " [feeling sad]")
                sys.stdout.flush()
                broadcast((name+" [feeling sad]").encode())
                continue
            
            elif(msg == ":mytime"):
                #client.send(time.ctime(time.time()).encode()) #현재시간을 전송
                print(name+ datetime.today().strftime("%a %b %-d %H:%M:%S %Y"))
                sys.stdout.flush()
                broadcast(datetime.now().strftime("%a %b %-d %H:%M:%S %Y").encode())
                continue
            
            elif(msg == ":+1hr"):
                now = datetime.now()+timedelta(hours=1)
                current_time = now.strftime("%a %b %-d %H:%M:%S %Y")
                print(name+ current_time)
                sys.stdout.flush()
                broadcast(current_time.encode())
                continue
            elif(msg == ":Exit"):
                print(exitname + " left the chatroom")
                sys.stdout.flush()
                #broadcast(name+ "left the chatroom".encode('ascii'))
                broadcast((exitname+ " left the chatroom").encode('ascii'))
                clients.remove(client)
                time.sleep(0.1)
                parse = name.split(":")
                name = parse[0]
                usernames.remove(name)
                client.send('QUIT'.encode('ascii'))
                break    
                
            else:
                broadcast(message)
                print(message.decode("utf-8"))
                sys.stdout.flush()
                continue
            
        except: #cut the connection to this particular client and remove it from the list and terminate the function
           
            index = clients.index(client)
            username = usernames[index]
            print(f'{username} left the chatroom')
            sys.stdout.flush()
            broadcast(f'{username} left the chatroom'.encode('ascii'))
            clients.remove(client)
            client.close()
            usernames.remove(username) 
            break          

def receive():
    #클라이언트가 커넥트를 통해 연결요청을 받게되면
    while True:
    #client -> 소켓 통신용
    #s -> 서버소켓 연결용
    #연결허용 (client socket, rem_addr)반환  rem_Addr =ip +port
        client, addr = server.accept()
        client.send('NICK'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        client.send('PASS'.encode('ascii'))
        userPwd = client.recv(1024).decode('ascii')
        #usernames.append(username)
        #clients.append(client)
        if userPwd == chatroom_pwd:
            if username in usernames:
                print("Username already exist")
                sys.stdout.flush()
                client.send('DUPL'.encode('ascii'))
            else:
                
                #print(f"Connected with {str(addr)}")
                #print(usernames)
                #client.send(time.ctime(time.time()).encode()) #현재시간을 전송
                print(f'{username} joined the chatroom')
                sys.stdout.flush()
                broadcast(f'{username} joined the chatroom\n'.encode('ascii'))
                usernames.append(username)
                clients.append(client)
                client.send(("Connected to "+host+" on port " + port).encode('ascii'))
            
                thread = threading.Thread(target = handle, args=(client,))
                thread.start()
        else:
            print ("password incorrect!! Closing the chatroom")
            sys.stdout.flush()
            #client.send("INCORRECT PASSCODE".encode())
            client.send('QUIT'.encode('ascii'))
            print("sent quit")
            sys.stdout.flush()
			
        #client.close() #소켓 종료


def Main():
    print ("Server started on port "+port+". Accepting connections")
    sys.stdout.flush()
    receive()
    
if __name__ == '__main__':
    Main()