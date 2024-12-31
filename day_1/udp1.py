import socket

# 创建一个UDP套接字
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# IP:port
udp.bind(('127.0.0.1', 9999))
# 发送数据
udp.sendto('hello'.encode(), ('127.0.0.1', 8888))
# 接收数据
data = udp.recvfrom(1024)
print(data)
