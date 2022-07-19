from socket import *
import threading
import sys
sys.argv = [
    __file__,

    8009
]
serverPort = sys.argv[1]
clients_send = {}  #dictionary for mapping username with corresponding sending socket
clients_recv = {}  #dictionary for mapping username with corresponding receiving socket
#function for creating server socket
def ss(serverPort):

    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    return serverSocket



def infinity():
    while True:
        yield
#function for checking whether username is in correct format
def check(username):
    i=0
    while i<len(username):

        if not username[i].isdigit():
            if not username[i].isalpha():
                return False
        if username[i].isdigit() or username[i].isalpha():
            i=i+1
    return True
#function for sending response messages to client
def send1(msgg,connectionSocket):
    msgg=msgg.encode()
    connectionSocket.send(msgg)
    return connectionSocket
#function for deleting entry of client
def dlt(username,clt,clt1):
    del clt[username]
    del clt1[username]
#function for sending error msg and closing socket
def s_sd_cl(msg4,connectionSocket):
    connectionSocket=send1(msg4, connectionSocket)

    connectionSocket.shutdown(SHUT_RDWR)
    connectionSocket.close()
    return connectionSocket
#function for sending response message
def t1(clients_send,temp_,username):
    mes1='SEND ' + username + '\n \n'
    mes1=mes1.encode()
    clients_send[temp_[1]].send(mes1)
#function for sending error 103 message
def error_103(connectionSocket):
    msg4='ERROR 103 Header incomplete\n \n'
    connectionSocket=s_sd_cl(msg4, connectionSocket)

    # sys.exit()
#functioon for sending error 102 message
def error_102(temp_,clients_send):
    sender=temp_[1]
    mes2='ERROR 102 Unable to send\n \n'
    mes2=mes2.encode()
    clients_send[sender].send(mes2)
#function for broadcasting message
def all_recipients(clients_recv,username,temp,i,msg,clients_send):
    cnt=0
    for i in clients_recv:
        if i == username:
            continue
        clients_recv[i].send(
            bytes('FORWARD ' + username + '\n Content-length: ' + temp[3] + ' \n\n' + msg, encoding='ascii'))
        message=clients_recv[i].recv(1024).decode("ascii")
        temp_=message.split()
        if temp_[0] == 'RECEIVED':
            cnt+=1
            sender=temp_[1]
            clients_send[sender].send(bytes('SEND ' + username + '\n \n', encoding='ascii'))
        elif temp_[1] == '103':
            # print('ERROR 103 Header Incomplete')
            connectionSocket.send(bytes('ERROR 103 Header incomplete\n \n', encoding='ascii'))
            connectionSocket.shutdown(SHUT_RDWR)
            connectionSocket.close()
            sys.exit()
        else:
            sender=temp_[1]
            clients_send[sender].send(bytes('ERROR 102 Unable to send\n \n', encoding='ascii'))
#function for unicasting message
def not_all_recipients(message,clients_send,connectionSocket,username):
    temp=message.split()
    if temp[0] == 'RECEIVED':

        t1(clients_send, temp, username)

    elif temp[1] == '103':

        error_103(connectionSocket)
        dlt(username,clients_send,clients_recv)

    else:
        error_102(temp_, clients_send)
#function for communicating with clients
def communicate(connectionSocket, addr,temp):

    username=temp[2]
    if len(temp)<1:
        connectionSocket.close()
        sys.exit()
        return

    if not check(username):
        msgg='ERROR 100 Malformed username\n \n'
        connectionSocket=s_sd_cl(msgg,connectionSocket)

        sys.exit()
    elif check(username):
        if temp[1]!='TOSEND':
            msgg='REGISTERED TORECV ' + username + '\n \n'
            connectionSocket=send1(msgg, connectionSocket)

            clients_recv[username]=connectionSocket
            sys.exit()

        elif temp[1]=='TOSEND':
            t='REGISTERED TOSEND ' + username + '\n \n'
            t=t.encode()
            connectionSocket.send(t)
            clients_send[username] = connectionSocket
            for _ in infinity():
                temp = connectionSocket.recv(1024).decode("ascii").split()

                
                if temp[0]=='SEND':

                    if temp[1] !='ALL':
                        if (temp[1] not in clients_recv):
                            msggg='ERROR 101 No user registered \n \n'
                            connectionSocket=send1(msggg,connectionSocket)

                            continue
                        elif (temp[1] not in clients_send):
                            msggg='ERROR 101 No user registered \n \n'
                            connectionSocket=send1(msggg, connectionSocket)

                            continue

                    str=''
                    for i in temp[4:]:
                        str=str+i
                    msg=str

                    if (len(msg)+1)!=int(temp[3]):
                        msg2='ERROR 103 Header incomplete\n \n'
                        connectionSocket=send1(msg2, connectionSocket)

                        connectionSocket.close()
                        clients_recv[username].close()
                        dlt(username,clients_send,clients_recv)

                        sys.exit()
                    recipient=temp[1]

                    if temp[1]!='ALL':
                        mg1='FORWARD ' + username + '\n Content-length: ' + temp[3] + ' \n\n' + msg
                        mg1=mg1.encode()

                        clients_recv[recipient].send(mg1)
                        message=clients_recv[recipient].recv(1024).decode("ascii")
                        not_all_recipients(message,clients_send, connectionSocket,username)

                    elif recipient == 'ALL':

                        i=0
                        all_recipients(clients_recv,username,temp,i,msg,clients_send)

print('The server is running !')
serverSocket=ss(serverPort)
#creating thread
for _ in infinity():
    connectionSocket, addr = serverSocket.accept()
    temp=connectionSocket.recv(1024).decode("ascii").split()
    x = threading.Thread(target=communicate, args=(connectionSocket, addr,temp))
    x.start()




