#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 9090))
c_list = []
while True:
    adr, data  = sock.recvfrom(1024)

    if adr not in c_list:
        c_list.append(adr)
    for client in c_list:
        if client != adr:
            sock.sendto(data, client)