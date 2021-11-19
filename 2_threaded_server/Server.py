#!/usr/bin/bash/env python
# -*- coding: utf-8 -*-

import socket
import sys
import threading
import os

def run(port=9090):
    sock = create_sock(port)
    cid = 0
    while True:
        client_sock = accept(sock, cid)
        threading.Thread(target=client,args=(sock, client_sock, cid)).start()
        cid += 1

def client(sock, client_sock, cid):
    while True:
        request = read(client_sock)
        if request is None:
            print(f'Client #{cid} unexpectedly disconnected')
            break
        else:
            if 'exit' in request.decode('utf-8'):
                write_response_close(client_sock, cid)
                break
            if 'sstop' in request.decode('utf-8'):
                write_response(sock, client_sock, cid)
                break
            response = request(request)
            write_response(client_sock, response)

def create_sock(serv_port):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,proto=0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', serv_port))
    sock.listen()
    return sock

def accept(sock, cid):
    c_sock, c_addr = sock.accept()
    print(f'Client #{cid} connected '
        f'{c_addr[0]}:{c_addr[1]}')
    return c_sock

def read(client_sock):
    request = bytearray()
    try:
        request = client_sock.recv(1024)
        if not request:
            # Клиент преждевременно отключился.
            return None
        return request

  except ConnectionResetError:
    # Соединение было неожиданно разорвано.
    return None
  except:
    raise

def request(request):
    return request[::-1]

def write(client_sock, response):
    client_sock.sendall(response)

def write_response_close(client_sock, cid):
    client_sock.close()
    print(f'Client #{cid} ')

def write_response(serv_sock, client_sock, cid):
    client_sock.close()
    serv_sock.close()
    print(f'Client #{cid} has been stoped server')
    os._exit(0)


run(port=int(sys.argv[1]))