import random 
from Deck import * 
import numpy 

###Random AI

class EasyAI(Player):
    pActions = ["Income", "Foreign Aid", "Steal", "Exchange", "Tax", "Assasinate", "Coup"]
    def __init__(self, gData):
        super().__init__(gData)
        self.playedMoves = []
        self.decisionTime = gData.challengeCountMax / (2 * 4)
        self.decisionCount = 0
    
    
    def stats(self, gData):
        super().stats(gData)
    
    def pickAction(self, gData):
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0
        if self.coins >= 3 and self.coins <=6:
            return self.pActions[random.randint(0,5)]
        elif self.coins >=7:
            return self.pActions[6]
        else:
            return self.pActions[random.randint(0,4)]
            
        pass
    
    
            
    def run(self, gData, data):
        data.canMove = False
        target = None
        if not self.targetting:
            move = self.pickAction(gData)
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
            # Carries out Foreign Aid 
            if move == "Foreign Aid":
                canMove, executeFn = primaryActions.foreignAid(gData, self, data)
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
            # Carries out the Exchange Method 
            if move == "Exchange":
                canMove, executeFn = self.exchange(gData, self, data)
                self.playedMoves.append("Ambassadoer")
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
                
            # Carries out the Tax Method
            if move == "Tax":
                canMove, executeFn = primaryActions.tax(gData, self, data)
                self.playedMoves.append("Duke")
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
            # Carries out the Assasinate Method 
            if move == "Assasinate":
                # Check for target within the player list 
                self.targetting = True
                if self.targetting:
                    player = random.randint(0,3)
                    if str(player) in ["0", "1", "2", "3"]:
                        opposingPlayer = gData.players[player]
                        self.assignInput(data, "")
                    else:
                        self.move = move
                        return None
                self.targetting = False
                target = opposingPlayer
                self.target = target
                # Does the assasination part 
                canMove, executeFn = primaryActions.assasinate(gData, self, data, target)
                data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                self.playedMoves.append("Assasin")
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
            # Carries out the steal move 
            if move == "Steal":
                self.targetting = True
                if self.targetting:
                    player = random.randint(0,3)
                    if str(player) in ["0", "1", "2", "3"]:
                        opposingPlayer = gData.players[player]
                        self.assignInput(data, "")
                    else:
                        self.move = move
                        return None
                self.targetting = False
                target = opposingPlayer
                self.target = target
                # Runs the steal method 
                canMove, executeFn = primaryActions.steal(gData, self, data, target)
                data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                self.playedMoves.append("Captain")
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
            # Carries out the coup action 
            if move == "Coup":
                # Gets the target 
                self.targetting = True
                if self.targetting:
                    player = random.randint(0,3)
                    if str(player) in ["0", "1", "2", "3"]:
                        opposingPlayer = gData.players[player]
                        self.assignInput(data, "")
                    else:
                        self.move = move
                        return None
                self.targetting = False
                target = opposingPlayer
                self.target = target
                # Carries out the coup 
                canMove, executeFn = primaryActions.coup(gData, self, data, target)
                data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
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
        # Checks for any Challengers for the allowed Moves 
        self.targetting = False
        self.execute = True
        move = self.move
        target = self.target
        self.text = ""
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
                    self.execute = not self.execute and not result
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
        gData.turnCount += 1 
                
        
    def willBlock(self, data, player, move, gData):
        # Checks if a player wants to block
        # Asks for the decision of the Player
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0 
        decision = random.randint(0,1)
        # if yes 
        if decision == 0:
            return True 
        # if no 
        elif decision == 1:
            return None 
            
    def willChallenge(self, data, gData, player, move):
        # Checks for challengers 
            # Asks for the decision of the player
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0
        decision = random.randint(0,1)
            # Yes 
        if decision == 0:
            return True 
            # No
        elif decision == 1:
            return False 
    
    
    def isDead(self):
        # Checks if the player is dead 
        if self.lives == 0:
            return True 
        return False 
        
    def printLostCard(f):
        def g(*args):
            result = f(*args)
            if result == None:
                return None
            data = args[1]
            self = args[0]
            data.server.send(("Lost " + result + " " + str(self) + "\n").encode())
            data.moveList.insert(0,["Player%s showed a %s" % (str(self), result), 950, 750])
            data.textFlag = True
            return result
        return g
    
    @printLostCard
    def loseACard(self, data, move = None):
        # Player loses a card 
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0
        lostCard = None 
        if len(self.hand) == 1:
            lostCard = self.hand.pop()
            return lostCard
        elif len(self.hand) == 2:
            lostCard = self.hand[random.randint(0,1)]
            self.hand.remove(lostCard)
        return lostCard
    pass
    
    def exchange(self, gData, player, opposingPlayer = None):
        # User input asking which two cards they would like to keep
        if player.coins >= 10:
            return False, None
        if len(player.hand) == 1:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Exchange \n"
                card1 = gData.deck.pop(0)
                card2 = gData.deck.pop(0)
                possibleCards = [player.hand.pop(), card1, card2]
                choice = possibleCards[random.randint(0,2)]
                possibleCards.remove(choice)
                gData.deck.append(possibleCards.pop(0))
                gData.deck.append(possibleCards.pop(0))
                player.hand = [choice]
                return True 
            return True, execute 
            #choice = input("Pick a card: ")
        elif len(player.hand) == 2:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Exchange \n"
                card1 = gData.deck.pop(0)
                card2 = gData.deck.pop(0)
                possibleCards = [player.hand.pop(), player.hand.pop(), card1, card2]
                choice = possibleCards[random.randint(0,3)]
                possibleCards.remove(choice)
                player.hand.append(choice)
                choice = possibleCards[random.randint(0,2)]
                possibleCards.remove(choice)
                player.hand.append(choice)
                gData.deck.append(possibleCards.pop(0))
                gData.deck.append(possibleCards.pop(0))
                return True 
            return True, execute
        

    





from DeckOperations import *