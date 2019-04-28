from random import shuffle
from tkinter import * 
# from Coup_Client import *

### Game Setup and Player Setup
    
class GameData(object):
    
    def __init__(self):
        self.data()
    
    def data(self):
        # Initializes the list of players 
        self.players = []
        # The of the revealed cards 
        self.shownCards = []
        # Initializes the deck
        self.deck = ["Captain", "Ambassador", "Assasin", "Contessa", "Duke"] * 3 
        # Shuffles the deck 
        self.shuffle()
        self.turnCount = 0 
        self.challengeFlag = False
        self.challengeFlag2 = False
        self.challengeCount = 0
        self.blockCount = 0
        self.challengeCountMax = 150
    
    def shuffle(self):
        # Method that shuffles the deck 
        shuffle(self.deck)
    
    def blocks(self, p, move, data, target, gData):
        # Return the players that want to block 
        if move == "Steal":
            bMove = "Block Stealing"
        if move == "Assasinate":
            bMove = "Block Assasination"
        if move == "Foreign Aid":
            bMove = "Block Foreign Aid"
        for player in self.players:
            self.blockCount += 1
            if self.blockCount == self.challengeCountMax:
                for pl in self.players:
                    pl.text = ""
                    pl.assignInput(data, "")
                    pl.updateAIData()
                self.blockCount = 0
                data.server.send(("Block " + "-1" + "\n").encode())
                data.moveList.insert(0,["No one blocks", 950, 750])
                data.textFlag = True
                return True, None, ""
            if player == p or not player.isAlive:
                continue
            if move != "Foreign Aid" and player != target:
                continue
            result = player.willBlock(data, player, move, gData)
            if result == True:
                data.server.send(("Block " + str(player) + "\n").encode())
                data.moveList.insert(0,["Player%s blocks" % (str(player)), 950, 750])
                data.textFlag = True
                #data.moveList.insert(0, ["Player " + str(self.players.index(player)) + " blocks", 950, 750])
                data.shiftUp = True
                # for move in data.moveList:
                #     move[2] -= 20
                #     if move[2] < 200:
                #         data.moveList.remove(move)
                self.blockCount = 0
                # The Issue: You cant return None here because it kicks back out to result which ask if you want to challenge again 
                for pl in self.players:
                    pl.text = ""
                    pl.assignInput(data, "")
                    pl.updateAIData()
                return False, player, bMove
            else:
                continue
        return None, None, None
    
    
    def challenges(self, p, move, data, primaryAction = True):
        # This function was written this way in order to deal with the run function
        
        # These act as flags which let the user know when something was challenged 
        if self.challengeFlag2:
            p = self.playerWhoMoved
            player = self.playerWhoChallenged
            cards = self.cards
            card2 = player.loseACard(data, move)
            if card2 == None:
                return None, ""
            player.assignInput(data, "")
            player.text = ""
            self.shownCards.append(card2)
            self.killPlayers()
            self.challengeFlag = False
            self.challengeFlag2 = False
            return True, player
        if self.challengeFlag:
            p = self.playerWhoMoved
            player = self.playerWhoChallenged
            cards = self.cards
            card = p.loseACard(data,move)
            if card == None:
                return None, ""
            p.assignInput(data, "")
            p.text = ""
            if card in cards:
                self.deck.append(card)
                p.hand.append(self.getCard())
                self.challengeFlag2 = True
                return None, ""
            else:
                self.shownCards.append(card)
                self.killPlayers()
                self.challengeFlag = False
                self.challengeFlag2 = False
                return False, player
        for player in self.players:
            self.challengeCount += 1
            if self.challengeCount == self.challengeCountMax:
                for pl in self.players:
                    pl.text = ""
                    pl.assignInput(data, "")
                    pl.updateAIData()
                self.challengeCount = 0
                data.server.send(("Challenge " + "-1" + "\n").encode())
                data.moveList.insert(0,["No one challenges" , 950, 750])
                data.textFlag = True
                return True, "No one"
            if player.isAlive:
                if player == p:
                    continue
                result = player.willChallenge(data, self, player, move)
                if result == True:
                    data.server.send(("Challenge " + str(player) + "\n").encode())
                    data.moveList.insert(0,["Player%s challenges" % (str(player)), 950, 750])
                    data.textFlag = True
                    #data.moveList.insert(0, ["Player " + str(self.players.index(player)) + " challenges", 950, 750])
                    data.shiftUp = True
                    # for move in data.moveList:
                    #     move[2] -= 20
                    #     if move[2] < 200:
                    #         data.moveList.remove(move)
                    self.challengeCount = 0
                    # The Issue: You cant return None here because it kicks back out to result which ask if you want to challenge again 
                    for pl in self.players:
                        pl.text = ""
                        pl.assignInput(data, "")
                        pl.updateAIData()
                    if primaryAction:
                        cards = primaryActions.actions[move]
                    else:
                        cards = secondaryActions.actions[move]
                    self.cards = cards
                    self.playerWhoMoved = p
                    self.playerWhoChallenged = player
                    self.challengeFlag = True
                    return None, ""
                else:
                    continue
            else:
                continue
        return None, ""
                
    def getBlockers(self):
        pass
        
    def getCard(self):
        # Gets a card from the deck 
        card = self.deck[0]
        self.deck.pop(0)
        return card
    
    def checkBlocker(player):
        pass
    
    def killPlayers(self):
        for player in self.players:
            if len(player.hand) == 0:
                player.isAlive = False
                # self.players.remove(player)

class Player():
    def __init__(self, gData):
        self.stats(gData)
        self.targetting = False
        self.runFlag1 = False
        self.runFlag2 = False
        self.runFlag3 = False
        self.runFlag4 = False
        self.firstPassExchange = True
        self.input = ""
        self.text = ""
        self.name = gData.players.index(self)
        self.playedMoves = [] 
    
    def updateAIData(self):
        self.decisionCount = 0
    
    def updateData(self, data):
        if data.mode == "LocalMultiplayer":
            index = data.newGame.players.index(self)
            if index == 0:
                data.text = self.text
                self.input = data.input
            if index == 1:
                data.text2 = self.text
                self.input = data.input2
            if index == 2:
                data.text3 = self.text
                self.input = data.input3
            if index == 3:
                data.text4 = self.text
                self.input = data.input4
        elif data.mode == "OnlineMultiplayer":
            index = data.newGame.players.index(self)
            if type(self) == Player:
                if index == 0:
                    data.text = self.text
                    self.input = data.input
                if index == 1:
                    data.server.send(("Text1 "+ "Text:" + self.text + "\n").encode())
                    self.input = data.others["Player1"]
                if index == 2:
                    data.server.send(("Text2 "+ "Text:" + self.text + "\n").encode())
                    self.input = data.others["Player2"]
                if index == 3:
                    data.server.send(("Text3 "+ "Text:" + self.text + "\n").encode())
                    self.input = data.others["Player3"]
            else:
                self.input = ""
    
    def assignInput(self, data, input):
        if data.mode == "LocalMultiplayer":
            self.input = input
            index = data.newGame.players.index(self)
            if index == 0:
                data.input = self.input
            if index == 1:
                data.input2 = self.input
            if index == 2:
                data.input3 = self.input
            if index == 3:
                data.input4 = self.input
        elif data.mode == "OnlineMultiplayer":
            self.input = input
            index = data.newGame.players.index(self)
            if index == 0:
                data.input = self.input
            if index == 1:
                data.others["Player1"] = self.input
            if index == 2:
                data.others["Player2"] = self.input
            if index == 3:
                data.others["Player3"] = self.input
    
    def __repr__(self):
        return "%d" % self.name
        
    def stats(self, gData):
        # Initializes each individual players hand 
        self.hand = [gData.getCard(), gData.getCard()]
        # Initilizes the coins 
        self.coins = 2
        # Adds the player to the list of players 
        gData.players.append(self)
        gData.currPlayer = gData.players[0]
        self.isAlive = True
        
    def run(self, gData, data):
        data.canMove = False
        target = None
        if not self.targetting:
            move = self.input
        else:
            move = self.move
        if not self.runFlag1:
            self.target = "Abhi"
            if move == "":
                return None
            if move not in primaryActions.actions:
                self.text = "Illegal move- Choose a Move"
                return None
            # Carries out Income Action
            if move == "Income":
                canMove, executeFn = primaryActions.income(gData, self, data)
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + "\n").encode())
                    data.moveList.insert(0,["Player%s played %s" % (str(self), self.move), 950, 750])
                    data.textFlag = True
                message = "Played Income \n"
            # Carries out Foreign Aid 
            if move == "Foreign Aid":
                canMove, executeFn = primaryActions.foreignAid(gData, self, data)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + "ForeignAid" + " " + str(self) + "\n").encode())
                    data.moveList.insert(0,["Player%s played %s" % (str(self), self.move), 950, 750])
                    data.textFlag = True
                message = "Played Foreign Aid \n" 
                #data.server.send(message.encode())
            # Carries out the Exchange Method 
            if move == "Exchange":
                canMove, executeFn = primaryActions.exchange(gData, self, data)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                self.playedMoves.append("Ambassador")
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + "\n").encode())
                    data.moveList.insert(0,["Player%s played %s" % (str(self), self.move), 950, 750])
                    data.textFlag = True
                message = "Played Exchange \n"
                #data.server.send(message.encode())
            # Carries out the Tax Method 
            if move == "Tax":
                canMove, executeFn = primaryActions.tax(gData, self, data)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                self.playedMoves.append("Duke")
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + "\n").encode())
                    data.moveList.insert(0,["Player%s played %s" % (str(self), self.move), 950, 750])
                    data.textFlag = True
                message = "Played Tax \n"
                #data.server.send(message.encode())
            # Carries out the Assasinate Method 
            if move == "Assasinate":
                # Check for target within the player list 
                self.targetting = True
                if self.targetting:
                    self.text = "Pick a player to assasinate"
                    if  self.input in ["0", "1", "2", "3"]:
                        opposingPlayer = gData.players[int( self.input)]
                        self.assignInput(data, "")
                    else:
                        self.move = move
                        return None
                self.targetting = False
                target = opposingPlayer
                self.target = target
                # Does the assasination part 
                canMove, executeFn = primaryActions.assasinate(gData, self, data, target)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                self.playedMoves.append("Assasin")
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + " " + str(self.target) + "\n").encode())
                    data.moveList.insert(0, ["Player%s played %s, target %s" % (str(self), self.move, str(self.target)), 950, 750])
                    data.textFlag = True
                message = "Played Assasinate \n" 
                #data.server.send(message.encode())
            # Carries out the steal move 
            if move == "Steal":
                self.targetting = True
                if self.targetting:
                    self.text = "Pick a player to steal from"
                    if  self.input in ["0", "1", "2", "3"]:
                        opposingPlayer = gData.players[int( self.input)]
                        self.assignInput(data, "")
                    else:
                        self.move = move
                        return None
                self.targetting = False
                target = opposingPlayer
                self.target = target
                # Runs the steal method 
                canMove, executeFn = primaryActions.steal(gData, self, data, target)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                self.playedMoves.append("Captain")
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + " " + str(self.target) + "\n").encode())
                    data.moveList.insert(0,["Player%s played %s, target %s" % (str(self), self.move, str(self.target)), 950, 750])
                    data.textFlag = True
                message = "Played Steal \n"
                #data.server.send(message.encode())
            # Carries out the coup action 
            if move == "Coup":
                # Gets the target 
                self.targetting = True
                if self.targetting:
                    self.text = "Pick a player to coup"
                    if  self.input in ["0", "1", "2", "3"]:
                        opposingPlayer = gData.players[int( self.input)]
                        self.assignInput(data, "")
                    else:
                        self.move = move
                        return None
                self.targetting = False
                target = opposingPlayer
                self.target = target
                # Carries out the coup 
                canMove, executeFn = primaryActions.coup(gData, self, data, target)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + " " + str(self.target) + "\n").encode())
                    data.moveList.insert(0,["Player%s played %s, target %s" % (str(self), self.move, str(self.target)), 950, 750])
                    data.textFlag = True
                message = "Played Coup \n"
                #data.server.send(message.encode())
        # Checks for any Challengers for the allowed Moves 
        self.targetting = False
        self.execute = True
        move = self.move
        target = self.target
        self.text = ""
        self.updateAIData()
        if not self.runFlag2:
            self.challenger = "No one"
            if move in primaryActions.actions and (move != "Income" and move != "Coup" and move != "Foreign Aid"):
                execute, challenger = gData.challenges(self, move, data, True)
                if execute == None:
                    return None
                else:
                    self.runFlag2 = True
                    self.execute = execute
                    self.challenger = challenger
            else:
                self.runFlag2 = True

        execute = self.execute
        challenger = self.challenger
        # Checks for any Blockers in the allowed move 
        if not self.runFlag3:
            self.blocker = None
            self.blockingMove = None
            if move in primaryActions.actions and (move != "Income" and move != "Coup" and move != "Tax" and move != "Exchange") and execute:
                if target != challenger:
                    execute, blocker, blockingMove = gData.blocks(self, move, data, target, gData)
                    if execute == None:
                        return None
                    else:
                        self.runFlag3 = True
                        self.blocker = blocker
                        self.blockingMove = blockingMove
                        self.execute = execute
        blocker = self.blocker
        blockingMove = self.blockingMove
        # Write the case where someone challenges the block 
        if not self.runFlag4:
            if blocker != None and blocker != "Noone":
                result = gData.challenges(blocker, blockingMove, data, False)[0]
                if result == None:
                    return None
                else:
                    self.execute = not result
                    self.runFlag4 = True
        execute = self.execute
        if execute:
            result = self.executeFn()
            if result == None:
                return None
            else:
                gData.killPlayers()
        if not execute and blocker != None and move == "Assasinate":
            self.coins -= 3
        gData.turnCount += 1 
        data.newTurn = True
        self.runFlag1 = False
        self.runFlag2 = False
        self.runFlag3 = False
        self.runFlag4 = False
        self.blocker = None
        self.challenger = "No one"
        self.target = "Abhi"
        self.blockingMove = None
        self.assignInput(data, "")
        return True
        
    def willBlock(self, data, player = None, move = None, gData = None):
        # Checks if a player wants to block 
        self.text = "Will you block?"
        if self.input == "Yes":
            return True 
        # if no 
        elif self.input == "No":
            return False  
        else:
            return None 
                
    def willChallenge(self, data, gData, player = None, move = None):
        # Checks for challengers 
        # decision = input("Do you want to challenge?. Reply Yes or No")
        # Yes 
        self.text = "Will you challenge?"
        if self.input == "Yes":
            return True 
        # No
        elif self.input == "No":
            return False 
        else:
            return None
    
    def isDead(self):
        # Checks if the player is dead 
        if self.lives == 0:
            return True 
        return False 
        
    def loseACard(self, data, move = None):
        # Player loses a card 
        #lostCard = input("Which card do you show?")
        lostCard =  self.input
        self.text = "Which card do you show"
        if lostCard == "":
            return None 
        if lostCard in self.hand:
            #lostCard = input("Illegal Card: Which card do you show?")
            lostCard =  self.input
            self.hand.remove(lostCard)
            data.server.send(("Lost " + lostCard + " " + str(self) + "\n").encode())
            data.moveList.insert(0,["Player%s showed a %s" % (str(self), lostCard), 950, 750])
            data.textFlag = True
            return lostCard
        else:
            self.text = "Illegal Card"
            return None

from Deck_Run import *

 