import Pyro4
import sys
import random
import pickle
from pathlib import Path

namainstance = sys.argv[1] or "fileserver"


class FileServer(object):
    def __init__(self):
        self.board = [[None for j in range(9)] for i in range(9)]
        self.f=replication()
        self.replica=self.f.connect()
        self.boardplayer = [[None,None,None],[None,None,None],[None,None,None],
                            [None,None,None],[None,None,None],[None,None,None],
                            [None,None,None],[None,None,None],[None,None,None]]

    def coba2(self):
        return "bisa fileserver"

    def getserver_board(self):
        # self.board[8][5] = 2
        # self.board[7][6] = 2
        # self.board[1][7] = 2
        # 
        my_file = Path("board_data.db")
        if my_file.is_file():
            with open('board_data.db','rb') as f:
                self.board = pickle.load(f)
        else:
            self.board = [[None for j in range(9)] for i in range(9)]
            with open('board_data.db','wb') as f:
                pickle.dump(self.board,f, pickle.HIGHEST_PROTOCOL)

        return self.board

    def getserver_boardplayer(self):
        my_file = Path("board_playerdata.db")
        if my_file.is_file():
            with open('board_playerdata.db','rb') as f:
                self.boardplayer = pickle.load(f)
        else:
            self.boardplayer = [[None,None,None],[None,None,None],[None,None,None],
                                [None,None,None],[None,None,None],[None,None,None],
                                [None,None,None],[None,None,None],[None,None,None]]
            with open('board_playerdata.db','wb') as f:
                pickle.dump(self.boardplayer,f, pickle.HIGHEST_PROTOCOL)

        return self.boardplayer

    def inputboard(self, newboard,boardplayer):
        self.board = newboard
        with open('board_data.db','wb') as f:
            pickle.dump(self.board,f, pickle.HIGHEST_PROTOCOL)
        print(namainstance)
        self.replica.consistency(namainstance,self.board)

        self.boardplayer = boardplayer
        with open('board_playerdata.db','wb') as f:
            pickle.dump(self.boardplayer,f, pickle.HIGHEST_PROTOCOL)


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

class replication:
    def connect(self):
        uri = "PYRONAME:rm@localhost:7777"
        fserver = Pyro4.Proxy(uri)
        return fserver


if __name__ == '__main__':
    rm = replication()
    replica = rm.connect()
    replica.add_server(namainstance)
    print(replica.get_serverlist())
    start_with_ns()