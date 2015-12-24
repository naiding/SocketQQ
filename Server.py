#!/usr/bin/env python
#*-* coding:utf-8 *-*

import socket
import select
from PyQt4 import QtCore, QtGui, uic

class ChatServer():
  def __init__(self, host = '', port = 8888, timeout = 10, backlog = 5, textBrower = None):
    
    self.textBrower = textBrower
    #记录连接的客户端数量
    self.clients =0
    #存储连接的客户端socket和地址对应的字典
    self.clientmap={}
    #存储连接的客户端socket
    self.outputs = []
    #建立socket
    self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    self.server.bind((host,port))
    self.server.listen(backlog)

  def print_to_textBrower(self, content):
    self.textBrower.append(content)

  def close():
    self.server.close()


  #主函数，用来启动服务器
  def run(self):
    #需要监听的可读对象
    inputs = [self.server]
    
    self.print_to_textBrower( 'Waiting for connection...' )
    #添加监听主循环
    while True:
      try:
        readable,writeable,exceptional = select.select(inputs,self.outputs,[])
        #此处会被select模块阻塞，只有当监听的三个参数发生变化时，select才会返回
      except select.error,e:
        break
      #当返回的readable中含有本地socket的信息时，表示有客户端正在请求连接
      if self.server in readable:
        #接受客户端连接请求
        client,addr=self.server.accept()
        
        self.print_to_textBrower("New Connection from %s\n"%str(addr))

        #客户数量加1
        self.clients += 1

        #2，self.outputs增加一列
        self.outputs.append(client)

        #3，self.clientmap增加一对
        self.clientmap[client]=addr

        #4, 给input添加可读监控
        inputs.append(client)
      
      #readable中含有已经添加的客户端socket，并且可读
      elif len(readable) != 0:
        #1, 取出这个列表中的socket
        csock = readable[0]
        #2, 根据这个socket，在事先存放的clientmap中，去除客户端的地址，端口的详细信息
        host,port = self.clientmap[csock]
        #3,取数据, 或接受关闭请求，并处理
        try:
          # 接受数据
          data = csock.recv(1024)
          # 打印数据
          self.print_to_textBrower( host + ' ' + str(port) + ' > ' + data)
          # 循环查找目的主机
          for cs in self.outputs:
            # 如果不是发送主机，则向其发送该主机发送的内容
            if cs != csock:
                clientText =  host + ' ' + str(port) + ' : ' + data
                cs.send(clientText)

        except socket.error,e:
          self.clients -= 1
          inputs.remove(csock)
          self.outputs.remove(csock)
          del self.clientmap[csock]
        
# if __name__ == "__main__":
  # chat = ChatServer("",11222)
  # chat.run()
