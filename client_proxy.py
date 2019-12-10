import Pyro4
import Pyro4.errors
import Pyro4.naming
import sys
import random
import time
import threading

namainstance = "clientproxy"
list_fserver = ['fileserver1','fileserver2','fileserver3']
uri_now = "PYRONAME:@"
server = ''
konek = 0

class proxy(object):
    # def __init__(self):
    #     self.f=fileserver()
    #     server=self.f.connect()

    def getboard(self):
        while True:
            try:
                kungking = server.getserver_board()
                return kungking
            except (Pyro4.errors.ConnectionClosedError,Pyro4.naming.NamingError,Pyro4.errors.CommunicationError,Pyro4.errors.PyroError) as e:
                pass

    def getboardplayer(self):
        while True:
            try:
                kungking = server.getserver_boardplayer()
                return kungking
            except (Pyro4.errors.ConnectionClosedError,Pyro4.naming.NamingError,Pyro4.errors.CommunicationError,Pyro4.errors.PyroError) as e:
                pass

    def update(self):
        p = Pyro()
        return p.updateserver()

    def getStatus(self):
        return konek

    def input(self, board,boardplayer):
        while True:
            try:
                kungking = server.inputboard(board,boardplayer)
                return kungking
            except (Pyro4.errors.ConnectionClosedError,Pyro4.naming.NamingError,Pyro4.errors.CommunicationError,Pyro4.errors.PyroError) as e:
                pass

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

def connect():
    global uri_now
    global konek
    while True:
        print("trying to connect server...")
        uri = fserver_availibility()
        if uri != 0:
            gserver = Pyro4.Proxy(uri)
            uri_now = uri
            print(uri_now)
            print("connected!")
            konek = 1
            print("konek="+str(konek))
            return gserver
        # time.sleep(1)

def ping_ack(a):
    global uri_now
    global server
    global konek
    while True:
        with Pyro4.Proxy(uri_now) as p:
            try:
                p._pyroBind()
            except (Pyro4.naming.NamingError,Pyro4.errors.CommunicationError,Pyro4.errors.PyroError) as e:
                print("server disconected!")
                konek = 0
                print("konek="+str(konek))
                server=connect()
                konek = 1
                print("konek="+str(konek))

def fserver_availibility():
    for x in list_fserver:
        oke=0
        uri = "PYRONAME:"+str(x)+"@localhost:7777"
        # print(uri)
        with Pyro4.Proxy(uri) as p:
            try:
                p._pyroBind()
                # print("ada")
                oke = 1
            except (Pyro4.naming.NamingError,Pyro4.errors.CommunicationError,Pyro4.errors.PyroError) as e:
                pass
        if oke == 1:
            return uri
    return 0


if __name__ == '__main__':
    ack = threading.Thread(target=ping_ack, args=(1,))
    ack.start()

    start_with_ns()