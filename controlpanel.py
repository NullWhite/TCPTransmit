from tkinter import *
from tkinter.messagebox import *
from transmiter import Transmiter
class ControlPanel(Frame):
    def __init__(self,parent=None,**kwargs):
        Frame.__init__(self,parent,**kwargs)

        self.transmitlist=[]#item->((5430,127.0.0.1,5423,127.0.0.1),Transmiter)

        self.createWindow()
        self.updatelistbox()

    def __del__(self):
        self.clearTransmitList()

    def createWindow(self):
        self.configrow = Frame(self)
        self.configrow.pack(side=TOP, fill=X)

        self.monitorportlabel = Label(self.configrow, text="监视端口:")
        self.monitorportlabel.pack(side=LEFT)
        self.monitorportentry = Entry(self.configrow, width=6)
        self.monitorportentry.pack(side=LEFT)
        self.monitorportentry.insert(0, '6060')

        self.monitoriplabel = Label(self.configrow, text='监视IP:', anchor=E, )
        self.monitoriplabel.pack(side=LEFT)
        self.monitoripentry = Entry(self.configrow, width=20)
        self.monitoripentry.pack(side=LEFT)
        self.monitoripentry.insert(0, '127.0.0.1')

        self.transmitportlabel = Label(self.configrow, text="转发端口:", width=15, anchor=E)
        self.transmitportlabel.pack(side=LEFT)
        self.transmitportentry = Entry(self.configrow, width=6)
        self.transmitportentry.pack(side=LEFT)
        self.transmitportentry.insert(0, '6062')

        self.transmitiplabel = Label(self.configrow, text='转发IP:', anchor=E)
        self.transmitiplabel.pack(side=LEFT)
        self.transmitipentry = Entry(self.configrow, width=20)
        self.transmitipentry.pack(side=LEFT)
        self.transmitipentry.insert(0, '127.0.0.1')

        self.controlrow=Frame(self)
        self.controlrow.pack(side=TOP,fill=X)

        self.addbutton = Button(self.controlrow, text="添加")
        self.addbutton.config(command=self.addTransmitItem)
        self.addbutton.pack(side=LEFT)

        self.removebutton=Button(self.controlrow,text='移除')
        self.removebutton.config(command=self.removeTransmitItem)
        self.removebutton.pack(side=LEFT)

        self.clearbutton=Button(self.controlrow,text="清除")
        self.clearbutton.config(command=self.clearTransmitItem)
        self.clearbutton.pack(side=LEFT)

        self.listrow = Frame(self)
        self.listrow.pack(side=TOP, expand=YES, fill=BOTH)
        self.transmitlistbox = Listbox(self.listrow, heigh=30)
        self.transmitlistbox.pack(expand=YES, fill=BOTH)

        self.transmitlistbox.insert(0,'rest')
        self.transmitlistbox.insert(1,'rest1')
        self.pack(expand=YES, fill=BOTH)

    def addTransmitItem(self):
        try:
            monitport=int(self.monitorportentry.get())
        except ValueError:
            showerror("错误！","端口号应该为整数")
            return
        try:
            transmitport=int(self.transmitportentry.get())
        except ValueError:
            showerror("错误！","端口号应该为整数")
            return
        monitip=self.monitoripentry.get()
        transmitip=self.transmitipentry.get()
        transmititem=(monitport,monitip,transmitport,transmitip)
        exit,i=self.isPortUsed(transmititem)
        if exit:
            if i<0:
                showerror("错误","监视端口,IP与转发端口,IP不应相同")
                return
            showerror("错误!","端口:%s,IP:%s已占用"%(transmititem[2*i],transmititem[2*i+1]))
            return
        tran=Transmiter(transmititem[0],transmititem[2],transmititem[1],transmititem[3])
        self.transmitlist.append((transmititem,tran))
        self.updatelistbox()
        tran.registerExceptFunc(lambda e:self.dealTransmitException(transmititem,e))
        tran.start()

    def dealTransmitException(self,transmititem,e):
        showerror("错误！",'端口:%s,IP:%s->端口:%s,IP:%s;转发失败\n%s'%(transmititem[0],transmititem[1],transmititem[2],transmititem[3],str(e)))
        for i,item in enumerate(self.transmitlist):
            if item[0]==transmititem:
                self.transmitlist.pop(i)
                self.updatelistbox()
                item[1].exit()

    def removeTransmitItem(self):
        indextuple=self.transmitlistbox.curselection()
        if not indextuple:
            return
        item=self.transmitlist.pop(indextuple[0])
        item[1].exit()
        self.updatelistbox()

    def clearTransmitItem(self):
        self.clearTransmitList()
        self.updatelistbox()

    def clearTransmitList(self):
        for item in self.transmitlist:
            item[1].exit()
        self.transmitlist.clear()

    def isPortUsed(self,transmititem):
        if transmititem[0]==transmititem[2] and transmititem[1]==transmititem[3]:
            return TRUE,-1
        for item in self.transmitlist:
            for i in range(0,2):
                for j in range(0,2):
                    if transmititem[2*i]==item[0][2*j] and transmititem[2*i+1]==item[0][2*j+1]:
                        return TRUE,i
        return FALSE,None

    def updatelistbox(self):
        self.transmitlistbox.delete(0,END)
        for i,item in enumerate(self.transmitlist):
            self.transmitlistbox.insert(i,'监视端口:%s,监视IP:%s->转发端口:%s,转发IP:%s。'%(item[0][0],item[0][1],item[0][2],item[0][3]))