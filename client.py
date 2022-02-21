import socket
import threading
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-join', action="store_true")
parser.add_argument('-host')
parser.add_argument('-port')
parser.add_argument('-username')
#parser.add_argument('-passcode')
args = parser.parse_args()

localhost = args.host
port = args.port
username = args.username
#userPwd = args.passcode

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = (localhost, int(port))
client.connect((address))
#print("current time:", sock.recv(1024).decode())

def receive():
    while True:
        try: 
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(username.encode('ascii'))
                #client.send(userPwd.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break
        
def write():
    while True:
        message = f'{username}: {input("")}'
        client.send(message.encode('ascii'))
        
receive_thread = threading.Thread(target= receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()