from socket import *

if __name__=='__main__':
    import sys
    port=6060
    ip='127.0.0.1'
    if len(sys.argv)==3:
        port=int(sys.argv[1])
        ip=sys.argv[2]
    mysock=socket(AF_INET,SOCK_STREAM)
    print('connect %s:%s'%(ip,port))
    mysock.connect((ip,port))
    mysock.send(b'this is test from client')
    data=mysock.recv(2048)
    print("recvData->",end='')
    print(data)