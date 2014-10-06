import socket               
import subprocess
import sys
import signal

s = socket.socket()         
IP = '10.10.220.108'
port = 10000
s.bind((IP, port))       
#interrupt handler to clean up when quitting
def signal_handler_listening(signal, frame):
    s.close()
    sys.exit(0)

def signal_handler_receiving(signal, frame):
    c.close()
    s.close()
    sys.exit(0)


#Waits for a connection and then accepts it
while True:
    signal.signal(signal.SIGINT, signal_handler_listening)
    s.listen(5)
    c, addr = s.accept()
    while True:
        signal.signal(signal.SIGINT, signal_handler_receiving)
        #Waits for command from the client
        communication = c.recv(200)
        #Removes the \n 
        communication = communication[:-1]
        #Parses the string into a list, separated by ' '
        com_list = communication.split(' ')
        com = com_list[0];

        if com == 'ls': #LS command
            #Pipes the contents of the ls into a variable
            contents = subprocess.Popen(["ls", "-l"], stdout=subprocess.PIPE)
            out, err = contents.communicate()
            c.send(out)
        elif com == 'get': #Getting files from the server
            fileName = com_list[1]
            print fileName
            sendFile = open(fileName)
            chunk = sendFile.read(65536)
            c.sendall(chunk)
        elif com == 'exit':
            c.close()
            break
