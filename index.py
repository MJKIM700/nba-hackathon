import csv
class Player:
    gameID = ""
    personID = ""
    teamID = ""
    period = 0
    plusminus = 0
    inGame = True


    def __init__(self, gameid, person, team, period):
        self.gameID = gameid
        self.period = period
        self.personID = person
        self.teamID = team

    def setPeriod(self, period):
        self.period = period

    def setGameID(self, gameID):
        self.gameID = gameID

    def setInGame(self, toggle):
        self.inGame = toggle

    def add(self, num):
        self.plusminus = self.plusminus + num

    def subtract(self, num):
        self.plusminus = self.plusminus - num



notFirst = False
lineupGameID = []
lineupPeriod = []
lineupPersonID = []
lineupTeamID = []
with open('Basketball Analytics - Lineup 7%2F12.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if notFirst:
            lineupGameID.append(row[0])
            lineupPeriod.append(int(row[1]))
            lineupPersonID.append(row[2])
            lineupTeamID.append(row[3])
        else:
            notFirst = True


pbpGameID = []
pbpEventMSG = []
pbpPeriod = []
pbpWCTime = []
pbpPCTime = []
pbpActionType = []
pbpOption1 = []
pbpTeamID = []
pbpPerson1 = []
pbpPerson2 = []
pbpEventNum = []
notFirst2 = False
with open('Basketball Analytics - Play by Play 7-10.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if notFirst2:
            pbpGameID.append(row[0])
            pbpEventNum.append(row[1])
            pbpEventMSG.append(row[2])
            pbpPeriod.append(int(row[3]))
            pbpWCTime.append(row[4])
            pbpPCTime.append(row[5])
            pbpActionType.append(row[6])
            pbpOption1.append(int(row[7]))
            pbpTeamID.append(row[10])
            pbpPerson1.append(row[11])
            pbpPerson2.append(row[12])
        else:
            notFirst2 = True
currentGameID = ""
currentPeriod = 0
game = []
i = 0

def compareTwoArrays(array1, array2):
    s = set(array2)
    temp = [x for x in array1 if x not in s]
    return temp

def checkTotalPlayers(gameID):
    playersInGame = []
    for indx, gameIden in enumerate(pbpGameID):
        if gameIden == gameID and pbpPerson1[indx] != '6bcf6c1f8c373d25fca1579bc4464a91':
            if pbpPerson1[indx] not in playersInGame:
                playersInGame.append(pbpPerson1[indx])
    return playersInGame



def getCurrentGamePersonIDArray():
    currentGamePersonID = []
    for players in game:
        currentGamePersonID.append(str(players.personID))
    return currentGamePersonID

def getCurrentTeamIDsArray():
    currentGameTeamID = []
    for players in game:
        currentGameTeamID.append(str(players.teamID))
    return currentGameTeamID

def getCurrentGamePlusMinusArray():
    currentGamePlusMinus = []
    for players in game:
        currentGamePlusMinus.append(players.plusminus)
    return currentGamePlusMinus

def getCurrentGameInGame():
    currentGameInGame = []
    for players in game:
        currentGameInGame.append(players.inGame)
    return currentGameInGame

def returnAmountinGame():
    count = 0
    for players in game:
        if players.inGame:
            count += 1
    return count


def fixFreeThrow(player1, player2):  # subtract a free throw from the first player, add to the first player
    for idx, playerInGame in enumerate(getCurrentGamePersonIDArray()):
        if playerInGame == player1:
            game[idx].plusminus -= 1
        if playerInGame == player2:
            game[idx].plusminus += 1


def totalPlusMinusSum():
    sum = 0
    for sums in getCurrentGamePlusMinusArray():
        sum += sums
    return sum


def newGame():
    if game:
        print getCurrentGamePersonIDArray()
        print getCurrentGamePlusMinusArray()
        print totalPlusMinusSum()
        print getCurrentGameInGame()
        print len(game)
        k = 0
        while k < len(game):
            f = open('Voluminous Lumberjacks_Q1_BBALL.csv', 'a')
            f.write(currentGameID + "," + getCurrentGamePersonIDArray()[k] + ',' + str(getCurrentGamePlusMinusArray()[k]) + '\n')
            f.close()
            k += 1
        #print compareTwoArrays(getCurrentGamePersonIDArray(), checkTotalPlayers(str(currentGameID)))


def scoreAction():
    scoringTeamID = ''
    for idx, playerInGame in enumerate(getCurrentGamePersonIDArray()):
        if playerInGame == pbpPerson1[i]:
            scoringTeamID = game[idx].teamID
            break
    if scoringTeamID == '':
        for idx, playerInGame in enumerate(lineupPersonID):
            if playerInGame == pbpPerson1[i]:
                scoringTeamID = lineupTeamID[idx]
                break
    for player in game:
        if player.teamID == scoringTeamID and player.inGame:
            player.add(int(pbpOption1[i]))
        if player.teamID != scoringTeamID and player.inGame:
            player.subtract(int(pbpOption1[i]))
    # print getCurrentTeamIDsArray()
    # print scoringTeamID
    # print getCurrentGamePlusMinusArray()
    # print totalPlusMinusSum()
    # print getCurrentGamePersonIDArray()
    # print getCurrentGameInGame()
    # print returnAmountinGame()
    # print 'players: ' + str(len(game))
    # print 'event id: ' + pbpEventNum[i]


def checkFreeThrow():
    previousEvts = pbpEventMSG[:i + 1]
    for index, event in enumerate(previousEvts):
        if event == '8' and pbpPCTime[index] == pbpPCTime[i] and pbpGameID[index] == pbpGameID[i]:
            fixFreeThrow(pbpPerson2[index], pbpPerson1[index])



while i < len(pbpGameID):
    if currentGameID == pbpGameID[i]:
        if currentPeriod == pbpPeriod[i]:
            if pbpOption1[i] > 0:
                if pbpEventMSG[i] == '1':
                    scoreAction()
                if pbpEventMSG[i] == '3' and pbpOption1[i] == 1:
                    scoreAction()
                    checkFreeThrow()
            if pbpEventMSG[i] == '8':
                for index, players in enumerate(getCurrentGamePersonIDArray()):
                    if players == str(pbpPerson1[i]):
                        game[index].setInGame(False)
                        leavingPlayerTeamID = game[index].teamID
                if pbpPerson2[i] not in getCurrentGamePersonIDArray():
                    y = Player(currentGameID, pbpPerson2[i], leavingPlayerTeamID, currentPeriod)
                    game.append(y)
                else:
                    for index, players in enumerate(getCurrentGamePersonIDArray()):
                        if players == pbpPerson2[i]:
                            game[index].setInGame(True)

                #print returnAmountinGame()
        else:
            currentPeriod = pbpPeriod[i]
            for players in game:
                players.setInGame(False)
            for index, players in enumerate(lineupGameID):
                if players == currentGameID and lineupPeriod[index] == currentPeriod:
                    if str(lineupPersonID[index]) not in getCurrentGamePersonIDArray():
                        y = Player(currentGameID, lineupPersonID[index], lineupTeamID[index], lineupPeriod[index])
                        game.append(y)
                    else:
                        for idx, playerInGame in enumerate(getCurrentGamePersonIDArray()):
                            if playerInGame == lineupPersonID[index]:
                                game[idx].setInGame(True)
            #print str(returnAmountinGame()) + ' break in period'
            i -= 1
    else:
        currentGameID = pbpGameID[i]
        currentPeriod = 1
        i -= 1
        newGame()
        game = []
        for index, players in enumerate(lineupGameID):
            if players == currentGameID and lineupPeriod[index] == 1:
                y = Player(currentGameID, lineupPersonID[index], lineupTeamID[index], lineupPeriod[index])
                game.append(y)
    i += 1

#[18, -12, -26, 14, -17, 23, -10, 13, 7, -10, -1, -9, -4, 15, 9, -6, -12, 6, 10]