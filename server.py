import Pyro4
import sys
import random

namainstance = sys.argv[1] or "fileserver"

board = [[None for j in range(9)] for i in range(9)]

class FileServer(object):
    def __init__(self):
        pass

    def get_greet(self, name='NoName'):
        lucky_number = random.randint(1, 100000)
        return "Hello {}, this is your lucky number {}".format(name, lucky_number)

    def updateserver(self):
        return board

    def inputserver(self, posisi=None):
        board = posisi
        return "tunggu pemain lawan"

def start_with_ns():
    #name server harus di start dulu dengan  pyro4-ns -n localhost -p 7777
    #gunakan URI untuk referensi name server yang akan digunakan
    #untuk mengetahui instance apa saja yang aktif gunakan pyro4-nsc -n localhost -p 7777 list

    daemon = Pyro4.Daemon(host="localhost")
    ns = Pyro4.locateNS("localhost",7777)
    x_FileServer = Pyro4.expose(FileServer)
    uri_fileserver = daemon.register(x_FileServer)
    ns.register("{}" . format(namainstance), uri_fileserver)
    #untuk instance yang berbeda, namailah fileserver dengan angka
    #ns.register("fileserver2", uri_fileserver)
    #ns.register("fileserver3", uri_fileserver)
    daemon.requestLoop()


def replica():
    uri = "PYRONAME:rm@localhost:7777"
    fserver = Pyro4.Proxy(uri)
    return fserver

if __name__ == '__main__':
    rm = replica()
    rm.add_server(sys.argv[1])
    print(rm.get_serverlist())
    start_with_ns()
