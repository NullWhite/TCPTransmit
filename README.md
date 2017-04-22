# TCPTransmit
转发TCP网络端口数据至另一个IP端口
#使用要求
要求电脑安装Python3.5或以上版本，我使用的是Python3.5.2，其他低版本的Python3没试过，Python2无法使用<br>
支持MacOS,Windows,Ubuntu其它Linux发行版未测试，理论上只要能安装Python3.5就可以使用。
#文件概述
run.py是GUI界面
transmiter.py是主转发程序
testclient.py是用于测试的客户端程序
testserver.py是用于测试的服务端程序
#使用方法
#Ubuntu(Linux),MaxOS
从命令行启动GUI<br>
python run.py<br>
从命令行启动非GUI<br>
python transminter.py arg1 arg2 arg3 arg4<br>
其中arg1,arg2,arg3,arg4分别是监测的端口号,检测的IP地址,转发目标端口号,转发目标的IP地址<br>
从命令行启动测试客户端<br>
python testclient.py arg1 arg2
arg1是监测端口,arg2是“run.py”运行的IP地址
从命令行启动测试服务端<br>
python testserver.py arg1<br>
arg1是转发端口<br>
#联系方式
hust_wfr@163.com

