from socket import *
import _thread as thread

class Transmiter:
    def __init__(self,clientPort,serverPort,clientIp,serverIp):
        self.clientport=clientPort
        self.serverport=serverPort
        self.clientIp=clientIp
        self.serverIp=serverIp
        self.curServerNum=0
        self.curClientNum=0
        self.serverSocketNum=0
        self.registerFunc=None

    def start(self):
        self.closeConnectSock()
        self.serverSocketNum+=1
        try:
            self.serverSocket.close()
        except AttributeError:
            pass
        self.serverSocket=socket(AF_INET,SOCK_STREAM)
        self.serverSocket.bind(("",self.clientport))
        self.serverSocket.listen(5)
        thread.start_new_thread(self.serverListen,(self.serverSocket,self.serverSocketNum))

    def exit(self):
        try:
            self.serverSocket.close()
        except AttributeError:
            pass
        self.closeConnectSock()

    def serverListen(self,serverSocket,threadNum):
        try:
            while threadNum==self.serverSocketNum:
                self.connection,self.address=serverSocket.accept()
                print(self.address)
                self.connection.settimeout(1)
                if self.address[0]==self.clientIp:
                    self.curServerNum+=1
                    self.curClientNum+=1
                    self.closeConnectSock()
                    self.serverConnect=self.connection
                    self.clientSock=self.clientLink()
                    thread.start_new_thread(self.clientRecv,(self.clientSock,self.serverConnect,self.curClientNum))
                    thread.start_new_thread(self.serverRecv,(self.clientSock,self.serverConnect,self.curServerNum))
                    continue
                self.connection.close()
        except OSError:
            pass

    def clientLink(self):
        try:
            clientSocket=socket(AF_INET,SOCK_STREAM)
            clientSocket.connect((self.serverIp, self.serverport))
            return clientSocket
        except Exception as e:
            if self.registerFunc:
                self.registerFunc(e)
            else:
                print(e)

    def registerExceptFunc(self,fun):
        self.registerFunc=fun

    def clientRecv(self,clientSock,serverSock,threadNum):
        try:
            while threadNum==self.curClientNum:
                curData=clientSock.recv(1024)
                if curData:
                    self.serverSendDataPraser(curData)
                    serverSock.send(curData)
        except (OSError,AttributeError):
            return

    def serverRecv(self,clientSock,serverSock,threadNum):
        try:
            while threadNum==self.curServerNum:
                curData=serverSock.recv(1024)
                if curData:
                    self.clientSendDataPraser(curData)
                    clientSock.send(curData)
        except OSError:
            return

    def closeConnectSock(self):
        try:
            self.clientSocket.close()
        except AttributeError:
            pass
        try:
            self.serverConnect.close()
        except AttributeError:
            pass

    def clientSendDataPraser(self, data):
        print('clientSend->',data)

    def serverSendDataPraser(self, data):
        print('serverSend->',data)

if __name__=='__main__':
    import sys
    monitport=6060
    monitip="127.0.0.1"
    transmitport=6062
    transmitip="127.0.0.1"
    print(sys.argv)
    if len(sys.argv)==5:
        monitport=int(sys.argv[1])
        monitip=sys.argv[2]
        transmitport=int(sys.argv[3])
        transmitip=sys.argv[4]
    myTransmit=Transmiter(monitport,transmitport,monitip,transmitip)
    print('端口:%s,IP:%s->端口:%s,IP:%s'%(monitport,monitip,transmitport,transmitip))
    myTransmit.start()
    while True:
        a=input('退出(Q/q)：')
        if a=='Q' or a=='q':
            break