# !/usr/bin/env python
# _*_coding:utf-8_*_

import socketserver
from time import ctime

stats_response = '\x00\x00\x00\x00\x00\x01\x00\x00STAT pid 4140\r\nSTAT uptime 1338\r\nSTAT time 1522495130\r\nSTAT version 1.2.2\r\nSTAT pointer_size 64\r\nSTAT rusage_user 0.031995\r\nSTAT rusage_system 0.014997\r\nSTAT curr_items 0\r\nSTAT total_items 0\r\nSTAT bytes 0\r\nSTAT curr_connections 1\r\nSTAT total_connections 2\r\nSTAT connection_structures 2\r\nSTAT cmd_get 0\r\nSTAT cmd_set 0\r\nSTAT get_hits 0\r\nSTAT get_misses 0\r\nSTAT evictions 0\r\nSTAT bytes_read 30\r\nSTAT bytes_written 474\r\nSTAT limit_maxbytes 104857600\r\nSTAT threads 1\r\nEND\r\n'

class TCP_Handler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            addr = self.client_address
            receive = self.request.recv(1024).decode()
            log = "\033[1;32m[TCP]\033[0m" + " %s \033[1;34m%s\033[0m {%s}"%(ctime(),addr,receive.strip())
            if receive :
                with open('log','a') as logs:
                    logs.write(log+'\n')
            if receive[:5] == 'stats':
                data = stats_response

            elif receive[:3] == "set":
                flag = receive.split('\r\n')[0].split()
                name = flag[1]
                size = flag[4]
                content = receive.split('\r\n')[1]
                while len(content) < int(size):
                    next = self.request.recv(1024).decode()
                    content += next
                    if next[-2:] == '\r\n':
                        content = content.strip()
                        break
                if len(content) == int(size):
                    with open('./data/'+name,'w') as file:
                        file.write(content)
                    data = 'STORED\r\n'
                else:
                    data = 'ERROR\r\n' 

            elif receive[:3] == "get":
                flag = receive.split('\r\n')[0].split()
                name = flag[1]
                with open('/data/'+name) as file:
                    data = file.read().strip() 
                if data:
                    data = 'VALUE '+name+' 0 '+str(len(data))+'\r\n'+data+'\r\nEND\r\n'
                else:
                    data = "ERROR\r\n"
            self.request.send(data.encode())

if __name__ == '__main__':
    host,port = '0.0.0.0',11211
    tcpserver = socketserver.ThreadingTCPServer((host,port), TCP_Handler)
    tcpserver.serve_forever()
