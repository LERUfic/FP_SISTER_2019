import Pyro4
import sys
import random

namainstance = sys.argv[1] or "clientproxy"

class proxy(object):
    def __init__(self):
        self.f=fileserver()
        self.server=self.f.connect()

    def coba(self):
        fileserver = Pyro()
        server = fileserver.fileserver()
        return server.coba2()

    def getboard(self):
        return self.server.getserver_board()

    def getboardplayer(self):
        return self.server.getserver_boardplayer()

    def update(self):
        p = Pyro()
        return p.updateserver()

    def input(self, board,boardplayer):
        return self.server.inputboard(board,boardplayer)

class fileserver:
    def connect(self):
        uri = "PYRONAME:fileserver@localhost:7777"
        gserver = Pyro4.Proxy(uri)
        return gserver

def start_with_ns():
    #name server harus di start dulu dengan  pyro4-ns -n localhost -p 7777
    #gunakan URI untuk referensi name server yang akan digunakan
    #untuk mengetahui instance apa saja yang aktif gunakan pyro4-nsc -n localhost -p 7777 list

    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS("localhost",7777)
    x_FileServer = Pyro4.expose(proxy)
    uri_fileserver = daemon.register(x_FileServer)
    ns.register("{}" . format(namainstance), uri_fileserver)
    #untuk instance yang berbeda, namailah fileserver dengan angka
    #ns.register("fileserver2", uri_fileserver)
    #ns.register("fileserver3", uri_fileserver)
    daemon.requestLoop()

if __name__ == '__main__':
    start_with_ns()
