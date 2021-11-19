#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading

#слушаем сервер
def listen(sock):
     while True:
         data, server = sock.recvfrom(1024)
         print(data.decode())


user_name = input("Введите Ваше имя: ")
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #создаем UDP сокет

sock.sendto((f"Пользователь {user_name} подключился к чату").encode(), ('localhost', 9090))
threading.Thread(target = listening, args = (sock, )).start() # создаем поток прослушивания сообщений от сервера

#получаем и отправляем сообщения
while True:
    message = input('Вы: ')
    sock.sendto((user_name + ": " + message).encode(), ('localhost', 9090))

