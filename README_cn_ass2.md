# COL672: Assignment2
#Author:Kashish jain


### __How to run :__

 1.First run server.py program to run the server application on command terminal using command- python server.py or any IDE.
   You can input server port address as command line argumennt also by using command-python server.py serverPort ,
   but I have hard coded it also in program.
 2.While the server program is running it will wait for the clients to join.
 3.Then run client.py program to run the client application on any different command terminal using command- python client.py 
   or any IDE.
   Also you can give the username(eg:localhost), serverIP, serverPort as command line arguments using command-python client.py
   username serverIP serverPort,but I have hard coded these system arguments to localhost,127.0.0.1,8004 as well in the program.
 4.You can run multiple client programs on different terminals.
 5.While client program is running,user have to give message in format @username message,where username is username of the client
   to whom he wants to communicate and message is plain text message.
 6.If INVALID username is given then it will show "No such user is registered".
 7.While sending messages to other users, client will simultaneously receive messages also from other clients.

    