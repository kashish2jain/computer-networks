from socket import *
import threading
import sys
import sys

sys.argv = [
    __file__,
    'localhost',
    '127.0.0.1',
    8009
]
serverPort = sys.argv[3]
username = sys.argv[1]
serverIP = sys.argv[2]


clientSocket1 = socket(AF_INET, SOCK_STREAM)
clientSocket1.connect((serverIP,serverPort))

clientSocket2 = socket(AF_INET, SOCK_STREAM)
clientSocket2.connect((serverIP,serverPort))
register='REGISTER TOSEND '+ username +' \n \n'
clientSocket1.send(register.encode())
message = clientSocket1.recv(1024)
message = message.decode("ascii")
temp = message.split()
if  temp[2]!='Malformed':
    register2='REGISTER TORECV ' + username + '\n \n'
    clientSocket2.send(register2.encode())
    message=clientSocket2.recv(1024)
    message = message.decode("ascii")
elif temp[2]=='Malformed':
    print('Malformed Username !!')
    clientSocket1.close()
    clientSocket2.close()
    sys.exit()

def infinity():
    while True:
        yield
def read_input():
    
    for _ in infinity():
        input_msg = input()
        temp = input_msg.split()
        if len(temp)==0:
            clientSocket1.close()
            sys.exit()
            return
        inp=input_msg[1:]
        data=inp.split()
        if len(data) < 2:
            print("Incorrect message sending format. Please try again", flush=True)
            continue
        else:
            dest=data[0]
            message=inp[len(data[0]) + 1:]
        if input_msg[0]!='@':
            print('Invalid Format! Please type again.')
            continue

        temp1=temp
        
        msg = ' '.join(temp[1:])
        rec='SEND ' + temp[0][1:] + '\n Content-length: ' + str(len(msg) )+ '\n\n ' + msg
        clientSocket1.send(rec.encode())
        msg1=clientSocket1.recv(1024)
        message = msg1.decode("ascii")
        temp = message.split()
        if temp[0]!='Send' and temp[1]=='103':
            print('Header incomplete or wrong Content length !!!')
            clientSocket1.close()
            sys.exit('Header Incomplete')
        elif temp[0]!='Send' and  temp[1]=='101':
            print('No such user registered!')
        elif temp[0]=='SEND':
            print('Message delivered to  '+temp1[0][1:])

        else:
            print('Unable to send') 
            

def read_forward():
    # print('Thread to read incoming msgs on !!')
    for _ in infinity():
        try:
            message=clientSocket2.recv(1024)
        except:
            print('Socket closed. Closing the thread')
            return
        message =message.decode("ascii")
        temp = message.split()
        if len(temp)==0:
            clientSocket2.close()
            return
        if temp[0]=='FORWARD' and ((len(temp)>2) and temp[2]=='Content-length:' and temp[3].isdigit()):
            sender_username = temp[1]
            clientSocket2.send(bytes('RECEIVED '+sender_username+'\n \n',encoding='ascii'))
            print(sender_username+': ' + ' '.join(temp[4:]))
        elif temp[0]=='FORWARD' and ((len(temp)<=2) or temp[2]!='Content-length:' or temp[3].isdigit()==False):
            clientSocket2.send(bytes('ERROR 103 Header Incomplete\n \n',encoding='ascii'))
        else:
            continue
data=message.split()
if data[0] == "REGISTERED":
        print("Registration Completed",flush=True)
        print("My username is " + sys.argv[1])
        print('Thread to take input is running !! Enter your message ')
        x = threading.Thread(target=read_input, args=())
        print('Thread to read incoming messages is running !!')
        y = threading.Thread(target=read_forward, args=())

####################
        x.start()
        y.start()
else:
        print("Some error, Try changing username and reapply",flush=True)


