import os,sys
path=os.path.dirname(__file__)
sys.path.append(path)
from TcpServer import tcpserver

if __name__ == '__main__':
    tcpserver.server_run()