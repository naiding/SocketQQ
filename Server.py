#!/usr/bin/env python
#*-* coding:utf-8 *-*

import socket
import select
import time
from PyQt4 import QtCore, QtGui, uic

class ChatServer():

    def __init__(self, host = '', port = 8888, timeout = 10, backlog = 5, logBrowser = None, onlineBrowser = None):
    
        # 获得GUI的logBrowser，以便输出日志
        self.logBrowser = logBrowser
        # 获得GUI的onlineBrowser，以便在线情况
        self.onlineBrowser = onlineBrowser
        # 记录连接的客户端数量
        self.clients = 0
        # 存储连接的客户端socket和地址对应的字典
        self.clientmap = {}
        # 存储连接的客户端socket
        self.outputs = []
        # 建立socket
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind((host,port))
        self.server.listen(backlog)

    # 打印日志函数
    def print_to_logBrowser(self, content):
        self.logBrowser.append(content)

    # 打印在线情况函数
    def print_to_onlineBrowser(self):
        self.onlineBrowser.append('\n%s:'%time.ctime())
        for key in self.clientmap.keys():
            self.onlineBrowser.append("%s"%str(self.clientmap[key]))

    # 关闭
    def close():
        self.server.close()

    #主函数，用来启动服务器
    def run(self):
        #需要监听的可读对象
        inputs = [self.server]
        # 输出日志
        self.print_to_logBrowser( 'Waiting for connection...' )
        #添加监听主循环
        while True:
            try:
                readable, writeable, exceptional = select.select(inputs, self.outputs, [])
                #此处会被select模块阻塞，只有当监听的三个参数发生变化时，select才会返回
            except select.error, e:
                break

            #当返回的readable中含有本地socket的信息时，表示有客户端正在请求连接
            if self.server in readable:
                #接受客户端连接请求
                client,addr = self.server.accept()
                # 打印连接日志
                self.print_to_logBrowser("New Connection from %s"%str(addr))
                #客户数量加1
                self.clients += 1
                #self.outputs增加一列
                self.outputs.append(client)
                #self.clientmap增加一对
                self.clientmap[client]=addr
                #4给input添加可读监控
                inputs.append(client)
                self.print_to_onlineBrowser()
            #readable中含有已经添加的客户端socket，并且可读
            elif len(readable) != 0:
                #取出这个列表中的socket
                csock = readable[0]
                #根据这个socket，在事先存放的clientmap中，去除客户端的地址，端口的详细信息
                host,port = self.clientmap[csock]
                #取数据, 或接受关闭请求，并处理
                try:
                    # 接受数据
                    data = csock.recv(1024)
                    # 打印数据
                    self.print_to_logBrowser( time.ctime() + '\n' + host + ' ' + str(port) + ' > ' + data + '\n')
                    # 循环查找目的主机
                    for cs in self.outputs:
                        # 如果不是发送主机，则向其发送该主机发送的内容
                        if cs != csock:
                            clientText =  time.ctime() + '\n' + host + ' ' + str(port) + ' : ' + data + '\n'
                            cs.send(clientText)

                except socket.error, e:
                    #客户端数量减一
                    self.clients -= 1
                    #移除客户端监控
                    inputs.remove(csock)
                    #移除客户端接收监控
                    self.outputs.remove(csock)
                    #打印日志
                    self.print_to_logBrowser("Lose Connection %s"%str(self.clientmap[csock]))
                    del self.clientmap[csock]
                    self.print_to_onlineBrowser()