from socket import *

host  = '192.168.1.101'
port = 11111
bufsize = 1024

addr = (host,port)
udpClient = socket(AF_INET,SOCK_DGRAM)

while True:
    data="\x00\x00\x00\x00\x00\x01\x00\x00get a\r\n"
#   data=input()+'\r\n'
    if not data:
        break
    data = data.encode()
    udpClient.sendto(data,addr)
    print("send success")
    data,addr = udpClient.recvfrom(bufsize)
    print(data.decode())
    input()

udpClient.close()
