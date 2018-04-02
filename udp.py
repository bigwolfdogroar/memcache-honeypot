# !/usr/bin/env python
# _*_coding:utf-8_*_

import socketserver
from time import ctime
import math

stats_response = '\x00\x00\x00\x00\x00\x01\x00\x00STAT pid 4140\r\nSTAT uptime 1338\r\nSTAT time 1522495130\r\nSTAT version 1.2.2\r\nSTAT pointer_size 64\r\nSTAT rusage_user 0.031995\r\nSTAT rusage_system 0.014997\r\nSTAT curr_items 0\r\nSTAT total_items 0\r\nSTAT bytes 0\r\nSTAT curr_connections 1\r\nSTAT total_connections 2\r\nSTAT connection_structures 2\r\nSTAT cmd_get 0\r\nSTAT cmd_set 0\r\nSTAT get_hits 0\r\nSTAT get_misses 0\r\nSTAT evictions 0\r\nSTAT bytes_read 30\r\nSTAT bytes_written 474\r\nSTAT limit_maxbytes 104857600\r\nSTAT threads 1\r\nEND\r\n'

class UDP_Handler(socketserver.BaseRequestHandler):
    def handle(self):
        addr = self.client_address
        receive = self.request[0].decode()[8:]
        socket = self.request[1]
        log = "\033[1;31m[UDP]\033[0m" + " %s \033[1;34m%s\033[0m {%s}"%(ctime(),addr,receive.strip())
        with open('log','a') as logs:
            logs.write(log+'\n')
        if receive[:5] == 'stats':
            data = stats_response
        elif receive[:3] == "set":
            data = "\x00\x00\x00\x00\x00\x01\x00\x00STORED\r\n"

        elif receive[:3] == "get":
            flag = receive.split('\r\n')[0].split()
            name = flag[1]
            with open('./data/'+name) as file:
                data = file.read().strip() 
            clothes = len(name)+len(str(len(data)))+26
            if len(data) < 1400 - clothes:
                data = '\x00\x00\x00\x00\x00\x01\x00\x00VALUE '+name+' 0 '+str(len(data))+'\r\n'+data+'\r\nEND\r\n'
            elif len(data) > 1400-clothes and len(data) < 2800-clothes-8:
                data = '\x00\x00\x00\x00\x02\x2f\x00\x00VALUE '+name+' 0 '+str(len(data))+'\r\n'+data[:1407-clothes] 
                socket.sendto(data.encode(),addr)
                data = '\x00\x00\x00\x01\x02\x2f\x00\x00'+data[1407-clothes:]+'\r\nEND\r\n'
            elif len(data) > 2800-clothes-8:
                content = data
                data = '\x00\x00\x00\x00\x02\x2f\x00\x00VALUE '+name+' 0 '+str(len(content))+'\r\n'+data[:1407-clothes] 
                socket.sendto(data.encode(),addr)
                count = math.ceil((len(content)-2800+clothes+8)/1392)
                for i in range(count):
                    data = '\x00\x00\x00\x00\x02\x2f\x00\x00'+content[1392*i+1407-clothes:1392*i+2799-clothes]
                    socket.sendto(data.encode(),addr)
                data = '\x00\x00\x00\x00\x02\x2f\x00\x00'+content[1392*count+1407-clothes:]+'\r\nEND\r\n'
            else:
                data = "\x00\x00\x00\x00\x00\x01\x00\x00ERROR\r\n"
        socket.sendto(data.encode(),addr)

if __name__ == '__main__':
    host,port = '0.0.0.0',11211
    udp_server = socketserver.ThreadingUDPServer((host,port),UDP_Handler)
    udp_server.serve_forever()

