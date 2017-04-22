from socket import *



if __name__=='__main__':
    import sys
    port=6062
    if len(sys.argv)==2:
        port=int(sys.argv[1])
    print('listen %s' %port)
    mysockobj=socket(AF_INET,SOCK_STREAM)
    mysockobj.bind(("",port))
    mysockobj.listen(5)
    while True:
        conn,add=mysockobj.accept()
        data=conn.recv(1024)
        print('connect to->',add)
        print("recvData->",end='')
        print(data)
        conn.send(b"this is test from server")
        conn.close()