import socket
s = socket.socket()
s.settimeout(3)
r = s.connect_ex(('127.0.0.1', 3306))
if r == 0:
    print('OPEN')
else:
    print('CLOSE')