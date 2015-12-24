#!/usr/bin/env python
#*-* coding:utf-8 *-*

from socket import *
from time import ctime
import select
import sys

BUFSIZ = 1024

class ChatClient():

    def __init__(self, host = 'localhost', port = 8888, textBrower = None):
        
        self.textBrower = textBrower
        self.host = host
        self.port = port

    def pring_to_brower(self, text):      
        self.textBrower.append(text)

    def run(self):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def close(self):
        self.client.close()

    def send_message(self, text):
        if text:
            self.client.send(text)

    def receive_message(self):
        while True:
            data = self.client.recv(BUFSIZ)
            if data:
                self.pring_to_brower(data)
                print data


    

