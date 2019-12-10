import configparser
import uuid

class Player:
    def __init__(self):
        self.configs = configparser.ConfigParser()
        try:
            with open('config.ini', 'r') as fh:
                self.configs.read('config.ini')        
        except FileNotFoundError:
            self.configs['DEFAULT']['PLAYERID'] = str(uuid.uuid1())
            self.configs['DEFAULT']['GAME_STATUS'] = '0'
            self.configs['DEFAULT']['BOARD_ID'] = '-1'
            self.configs['DEFAULT']['PAWN'] = '0'
            with open('config.ini', 'w+') as configfile:
                self.configs.write(configfile)


    def saveData(self):
        with open('config.ini', 'w') as configfile:
            self.configs.write(configfile)

    def resetData(self):
        self.configs['DEFAULT']['PLAYERID'] = str(uuid.uuid1())
        self.configs['DEFAULT']['GAME_STATUS'] = '0'
        self.configs['DEFAULT']['BOARD_ID'] = '-1'
        self.configs['DEFAULT']['PAWN'] = '0'

        self.saveData()

    def loadData(self):
        self.configs.read('config.ini')

    def getGameStatus(self):
        return self.configs['DEFAULT']['GAME_STATUS']

    def getBoardID(self):
        return self.configs['DEFAULT']['BOARD_ID']

    def getPawn(self):
        return self.configs['DEFAULT']['PAWN']

    def getPlayerID(self):
        return self.configs['DEFAULT']['PLAYERID']

    def setGameStatus(self,game_status):
        self.configs['DEFAULT']['GAME_STATUS'] = game_status

    def setBoardID(self, board_id):
        self.configs['DEFAULT']['BOARD_ID'] = board_id

    def setPawn(self, pawn):
        self.configs['DEFAULT']['PAWN'] = pawn