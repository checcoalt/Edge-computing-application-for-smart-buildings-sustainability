import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8000))
s.send("3C3D3E06451B20B4BD3C195E206E6F64655F3031231434641500000000006185EB3F0100000000046179913E4A7B14C4414C005462424DBFD0C647460000000047000000004800000000".encode("utf-8"))