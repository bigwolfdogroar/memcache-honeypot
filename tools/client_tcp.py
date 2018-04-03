from socket import *

ip_port = ('127.0.0.1',11211)
sk = socket()
sk.connect(ip_port)

while True:
#    data = data = "set a 0 0 1" + "\r\na" + "\r\n"
#    data = 'get a\r\n'
#    data = "set y 0 0 1006" + "\r\n" + 'y' * 1006 + "\r\n"
    data = "stats\r\n"
    sk.send(bytes(data,'utf8'))
    msg = sk.recv(1024)
    print(str(msg,'utf8'))
    input()
sk.close()
