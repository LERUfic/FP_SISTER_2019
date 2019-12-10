import Pyro4
import sys

namainstance = "rm"
serverlist=[]

class FileServer(object):
    def __init__(self):
        pass

    def add_server(self, server_name):
        if server_name not in serverlist:
            serverlist.append(server_name)

    def get_serverlist(self):
        return serverlist

    def another_server(self, servername):
        uri = "PYRONAME:{}@localhost:7777".format(servername)
        replserver = Pyro4.Proxy(uri)
        return replserver

    def consistency(self, from_server, board, boardplayer):
        for server in serverlist:
            # print(str(server))
            if str(server) != str(from_server):
                # print(str(server))
                try:
                    fserver = self.another_server(server)
                    fserver.inputboard(board,boardplayer,0)
                except Exception as e:
                    pass
        return "ok"



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



if __name__ == '__main__':
    start_with_ns()
