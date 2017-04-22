from tkinter import *
from controlpanel import ControlPanel
if __name__=='__main__':
    root=Tk()
    panel=ControlPanel(root)
    panel.pack(expand=YES,fill=BOTH)
    root.mainloop()