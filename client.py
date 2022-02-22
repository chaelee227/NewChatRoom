import socket
import threading
import sys
import argparse

EXIT = ":Exit"
HAPPY = ":)"
SAD = ":("
TIME = ":mytime"
PLUS_HOUR = ":+1hr"

def display(name) :
    you=name +" : "
    sys.stdout.write(you)
    sys.stdout.flush()

parser = argparse.ArgumentParser()
parser.add_argument('-join', action="store_true")
parser.add_argument('-host')
parser.add_argument('-port')
parser.add_argument('-username')
parser.add_argument('-passcode')
args = parser.parse_args()

localhost = args.host
port = args.port
username = args.username
userPwd = args.passcode

if len(username)>8:
    username = username[0:8]
    print(username)
    
if len(userPwd)>5:
    print("invalid passcode - the passcod has to be up to 5 length")
    sys.exit()
elif userPwd.isalnum() == False:
    print("invalid passcode - only alpha numberic character is allowed")
    sys.exit()

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
            elif message == 'PASS':
                client.send(userPwd.encode('ascii'))
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
 
def Main():       
    receive_thread = threading.Thread(target= receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

if __name__ == '__main__':
    Main()