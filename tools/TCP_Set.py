#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from socket import *

HOST ='127.0.0.1'
PORT = 11111
BUFFSIZE=2048
ADDR = (HOST,PORT)
memcachedClient = socket(AF_INET,SOCK_STREAM)

memcachedClient.connect(ADDR)
for i in "ab":
    print("set "+i)
    data = "set " + i + " 0 0 1048501" + "\r\n" + i * 1048501 + "\r\n"
    memcachedClient.sendall(data.encode())
    print(memcachedClient.recv(BUFFSIZE).decode())
memcachedClient.close()
