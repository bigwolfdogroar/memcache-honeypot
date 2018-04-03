#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from socket import *

HOST ='127.0.0.1'
PORT = 11111
BUFFSIZE=2048
ADDR = (HOST,PORT)

memcachedClient = socket(AF_INET,SOCK_STREAM)
memcachedClient.connect(ADDR)

data = "get i"  + "\r\n"
memcachedClient.sendall(data.encode())
data = memcachedClient.recv(BUFFSIZE)
print(data.decode())
memcachedClient.close()
