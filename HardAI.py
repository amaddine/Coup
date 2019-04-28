import random as rnd
from random import random 
from Deck import *
import numpy 

##### This is the Hard AI 
##### Uses Probabilty to calculate moves


class HardAI(Player):
    
    # Taken from https://github.com/hexparrot/the-resistance-coup-ai/blob/master/heuristics.py
    
    IMPLIED_INFORMATION = {
        'perform': {
            'Steal': ['Captain'],
            'Tax': ['Duke'],
            'Assasinate': ['Assassin'],
            },
        'block': {
            'Foreign Aid': ['Duke'],
            'Steal': ['Ambassador', 'Captain'],
            'Assasinate': ['Contessa']
            },
        'suboptimal_move': {
            'Foreign Aid': ['Duke'],
            'Income': ['Duke'],
            'Coup': ['Assassin']
            }
        }
        
    WEIGHTS = {
        'performed_action': 1,
        'blocked_selfishly': 1,
        'blocked_selflessly': 6,
        'suboptimal_move': -3, #income when could have taxed, -x to likelihood of duke
        'didnt_block_selfishly': -10, #eg allowed somebody to steal from him, but was captain/ambass
        'didnt_block_selflessly': -1 #didnt block a foreign aid, for example
        }
    
    PROBABILITIES = {
        "Two of Same Card": 1/35, 
        "One Card given One of the type is in Deck": 24/91, 
        "Atleast One Card Given Other in Deck" : 25/91,
        "Both Cards Given Other in Deck" : 1/91 
        }
        
    PAYOFFS = {
        "Success": 1, 
        "Fail": -1
        }
    
    # Probability that a player is dealt to two dukes
        
    def __init__(self, gData):
        self.stats(gData)
        self.otherPlayersAction = dict()
        self.PotentialDeck = []
        self.playedMoves = [] 
        self.challengedMoves = []
        self.targetting = False
        self.runFlag1 = False
        self.runFlag2 = False
        self.runFlag3 = False
        self.runFlag4 = False
        self.firstPassExchange = True
        self.input = ""
        self.text = ""
        self.cards = ["Duke", "Captain", "Ambassador", "Assasin", "Contessa"]
        #self.otherPlayersActionDictIntialization(gData)
        self.name = gData.players.index(self)
        self.decisionTime = gData.challengeCountMax / (2 * 4)
        self.decisionCount = 0
    
    def stats(self, gData):
        super().stats(gData)
        pass
        
    def otherPlayersActionDictIntialization(self, gData):
        for player in gData.players:
            if player != self:
                self.otherPlayersAction[player] = {}
        for player in self.otherPlayersAction:
            for count in range(5):
                self.otherPlayersAction[player][self.cards[count]]  = 0 
                
    
    def willBlock(self, data, player = None, move = None, gData = None):
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0
        AlivePlayers = [] 
        # Gets all of the players who are alive 
        for player in gData.players:
            if player.isAlive:
                AlivePlayers.append(player)
            
        
        
        if move == "Assasinate":
            # Edge Case for if all cards have been shown 
            if gData.shownCards.count("Assasin") == 3 or self.hand.count("Assasin") + gData.shownCards.count("Assasin") == 3:
                return True
            # You should always block if Contessa in hand 
            elif "Contessa" in self.hand:
                return True 
            else:
                # All three assasins are on the table so you should block 
                if "Assasin" in self.hand:
                    if "Assasin" in gData.shownCards:
                        if "Assasin" in self.PotentialDeck:
                            return True 
                        # This finds the probability that the other person has an assasin 
                        elif ( 2 * len(gData.players) - len(gData.shownCards))/(14 - len(gData.shownCards)) < .4:
                            return True
                        # If the other person has claimed Assasin multiple times you don't want to bluff and block     
                        elif player.playedMoves.count("Assasin") >= 3:
                            if gData.turnCount < 3:
                                return False
                            return True 
                        else:
                            return False 
                    else:
                        return False 
                else:
                    # Calculates the probability 
                    if "Assasin" in gData.shownCards:
                        if gData.shownCards.count("Assasin") == 1:
                            if "Assasin" in self.PotentialDeck:
                                x = len(gData.players) 
                                y = len(gData.shownCards)
                                if 24/91 - (2 * x - y/(14 - y)) < .1:
                                    return True 
                                return False 
                            else:
                                # Bluffs a contessa if there is only one contessa showns 
                                if gData.shownCards.count("Contessa") < 2:
                                    return True 
                                return False 
                        else:
                            # If the placement of one Assasin is known it blocks 
                            if "Assasin" in self.PotentialDeck:
                                return True 
                            else:
                                return False
                    else:
                        # If two contessa's are on the board it is too dangerous to bluff 
                        if "Contessa" in gData.shownCards:
                            if gData.shownCards.count("Contessa") == 2:
                                return False
                            else:
                                # Just for random purposes 
                                if random() < .1:
                                    return True 
                                return False 
                        else:
                            return False

            
        elif move == "Foreign Aid":
            if gData.shownCards.count("Duke") == 3:
                return False 
            # Should block only half the time in order to not give cards away
            elif "Duke" in self.hand:
                # If there are only two players you always want to block 
                if len(AlivePlayers) == 2:
                    return True 
                # Otherwise you only want to block half the time     
                elif random() < .5:
                    return True 
                else:
                    return False 
            else:
                # Checks if it is worth bluffing a Duke 
                if "Duke" in gData.shownCards:
                    if gData.shownCards.count("Duke") == 1:
                        if "Duke" in self.PotentialDeck:
                            # Loops through the weighted dictionary 
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Duke") >= 3:
                                        return False
                            return True 
                        else:
                            # Checks how many people have claimed to have the duke 
                            count = 0
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Duke") >= 3:
                                        count += 1
                                    if count == 2:
                                        return False 
                            # Randomly blocks 
                            if random() > .5:
                                return True 
                            else:
                                return False 
                    else: 
                    # Others might know where the Duke is too 
                        if "Duke" in self.PotentialDeck:
                            return False
                        else:
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Duke") >= 3:
                                        return False 
                            if random() > .5:
                                return True 
                            else:
                                return False 
                else:
                    # Same algorithm as above
                    if "Duke" in self.PotentialDeck:
                        count = 0 
                        for player in gData.players:
                            if player != self:
                                if player.playedMoves.count("Duke") >= 3:
                                    count += 1 
                                if count == 2:
                                    return False
                        return True 
                    else:
                        if random() > .5:
                            return True 
                        else:
                            return False 
                        
                        
                    
        elif move == "Steal":
            if "Captain" in self.hand or "Ambassador" in self.hand:
                # It's just game strategy to block if there are only two players left in the game 
                if len(AlivePlayers) == 2:
                    return True 
                # This is just for probabilistic purposes sometimes 
                elif random() < .1:
                    return False
                else: return True 
        
            else:
                # This is an opportunity to establish bluffs
                if gData.turnCount < 3:
                    if random() < .5:
                        return True 
                    else:
                        return False 
                elif "Captain" in gData.shownCards or "Ambassador" in gData.shownCards:
                    if gData.shownCards.count("Captain") + gData.shownCards.count("Ambassador") >= 3:
                        if random() < .25:
                            return True 
                        else:
                            return False
                else:
                    return False
    
    def willChallenge(self, data, gData, player = None, move = None):
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0
        AlivePlayers = [] 
        # Gets all of the players who are alive 
        for player in gData.players:
            if player.isAlive:
                AlivePlayers.append(player)
        
        #print("Will Challenge")
        
        if move == "Assasinate":
            if gData.shownCards.count("Assasin") == 3 or self.hand.count("Assasin") + gData.shownCards.count("Assasin") == 3:
                return True
            else:
                if "Assasin" in self.hand:
                    if "Assasin" in gData.shownCards:
                        if "Assasin" in self.PotentialDeck:
                            return True 
                        # This finds the probability that the other person has an assasin 
                        elif ( 2 * len(gData.players) - len(gData.shownCards))/(14 - len(gData.shownCards)) < .4:
                            return True
                        # If the other person has claimed Assasin multiple times you don't want to bluff and block     
                        elif player.playedMoves.count("Assasin") >= 3:
                            if gData.turnCount < 3:
                                return True 
                            return False 
                        else:
                            return False 
                    else:
                        return False 
                else:
                    if "Assasin" in gData.shownCards:
                        if gData.shownCards.count("Assasin") == 1:
                            if "Assasin" in self.PotentialDeck:
                                x = len(gData.players)
                                y = len(gData.shownCards)
                                if 24/91 - 2 * x - y/(14-y) < .1:
                                    return True 
                                return False 
                            else:
                                return False
                        else:
                            if "Assasin" in self.PotentialDeck:
                                return True 
                            else:
                                return False
        
        elif move == "Tax" or "Block Foreign Aid":
            if gData.shownCards.count("Duke") == 3:
                return True 
            # Should block only half the time in order to not give cards away
            elif "Duke" in self.hand:
                if self.hand.count("Duke") == 2:
                    if "Duke" in gData.shownCards:
                        return True 
                    elif random() < .75:
                        return True 
                    else:
                        return False 
                else:
                    if "Duke" in gData.shownCards:
                        if "Duke" in self.PotentialDeck:
                            return True 
                        elif random() < .7:
                            return True 
                        else:
                            return False
                    else:
                        return False 
            else:
                # Checks if it is worth bluffing a Duke 
                if "Duke" in gData.shownCards:
                    if gData.shownCards.count("Duke") == 1:
                        if "Duke" in self.PotentialDeck:
                            # Loops through the weighted dictionary 
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Duke") >= 3:
                                        return False
                            return True 
                        else:
                            # Checks how many people have claimed to have the duke 
                            count = 0
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Duke") >= 3:
                                        count += 1
                                    if count == 2:
                                        return False 
                            return True 
                    else: 
                    # Others might know where the Duke is too 
                        return False 
                else:
                    # Same algorithm as above
                    if "Duke" in self.PotentialDeck:
                        count = 0 
                        for player in gData.players:
                            if player != self:
                                if player.playedMoves.count("Duke") >= 3:
                                    count += 1 
                                if count == 2:
                                    return True 
                        return False 
                    else:
                        return False 
        
        elif move == "Steal":
            if gData.shownCards.count("Captain") == 3:
                return True 
            # Should block only half the time in order to not give cards away
            elif "Captain" in self.hand:
                if self.hand.count("Captain") == 2:
                    if "Captain" in gData.shownCards:
                        return True 
                    elif random() < .75:
                        return True 
                    else:
                        return False 
                else:
                    if "Captain" in gData.shownCards:
                        if "Captain" in self.PotentialDeck:
                            return True 
                        elif random() < .7:
                            return True 
                        else:
                            return False 
                    else:
                        return False 
            else:
                # Checks if it is worth bluffing a Duke 
                if "Captain" in gData.shownCards:
                    if gData.shownCards.count("Captain") == 1:
                        if "Captain" in self.PotentialDeck:
                            # Loops through the weighted dictionary 
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Captain") >= 3:
                                        return False
                            return True 
                        else:
                            # Checks how many people have claimed to have the duke 
                            count = 0
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Captain") >= 3:
                                        count += 1
                                    if count == 2:
                                        return False 
                            return True 
                    else: 
                    # Others might know where the Duke is too 
                        return False 
                else:
                    # Same algorithm as above
                    if "Captain" in self.PotentialDeck:
                        count = 0 
                        for player in gData.players:
                            if player != self:
                                if player.playedMoves.count("Captain") >= 3:
                                    count += 1 
                                if count == 2:
                                    return True 
                        return False 
                    else:
                        return False 
            
        
        elif move == "Exchange":
            if gData.shownCards.count("Ambassador") == 3:
                return True 
            # Should block only half the time in order to not give cards away
            elif "Ambassador" in self.hand:
                if self.hand.count("Ambassador") == 2:
                    if "Ambassador" in gData.shownCards:
                        return True 
                    elif random() < .75:
                        return True 
                    else:
                        return False 
                else:
                    if "Ambassador" in gData.shownCards:
                        if "Ambassador" in self.PotentialDeck:
                            return True 
                        elif random() < .7:
                            return True 
                        else:
                            return False
                    else:
                        return False 
            else:
                # Checks if it is worth bluffing a Duke 
                if "Ambassador" in gData.shownCards:
                    if gData.shownCards.count("Ambassador") == 1:
                        if "Ambassador" in self.PotentialDeck:
                            # Loops through the weighted dictionary 
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Ambassador") >= 3:
                                        return False
                            return True 
                        else:
                            # Checks how many people have claimed to have the duke 
                            count = 0
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Ambassador") >= 3:
                                        count += 1
                                    if count == 2:
                                        return False 
                            return True 
                    else: 
                    # Others might know where the Duke is too 
                        return False 
                else:
                    # Same algorithm as above
                    # Was captain before hand
                    if "Ambassador" in self.PotentialDeck:
                        count = 0 
                        for player in gData.players:
                            if player != self:
                                if player.playedMoves.count("Ambassador") >= 3:
                                    count += 1 
                                if count == 2:
                                    return True 
                        return False 
                    else:
                        return False 
            
        elif move == "Block Assasination":
            if gData.shownCards.count("Contessa") == 3:
                return True 
            # Should block only half the time in order to not give cards away
            elif "Contessa" in self.hand:
                if self.hand.count("Contessa") == 2:
                    if "Contessa" in gData.shownCards:
                        return True 
                    elif random() < .75:
                        return True 
                    else:
                        return False
                else:
                    if "Contessa" in gData.shownCards:
                        if "Contessa" in self.PotentialDeck:
                            return True 
                        elif random() < .7:
                            return True 
                        else:
                            return False 
                    else:
                        return False 
            else:
                # Checks if it is worth bluffing a Contessa 
                if "Contessa" in gData.shownCards:
                    if gData.shownCards.count("Contessa") == 1:
                        if "Contessa" in self.PotentialDeck:
                            # Loops through the weighted dictionary 
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Contessa") >= 3:
                                        return False
                            return True 
                        else:
                            # Checks how many people have claimed to have the Contessa 
                            count = 0
                            for player in gData.players:
                                if player != self:
                                    if player.playedMoves.count("Contessa") >= 3:
                                        count += 1
                                    if count == 2:
                                        return False 
                            return True 
                    else: 
                    # Others might know where the Duke is too 
                        return False 
                else:
                    # Same algorithm as above
                    if "Captain" in self.PotentialDeck:
                        count = 0 
                        for player in gData.players:
                            if player != self:
                                if player.playedMoves.count("Contessa") >= 3:
                                    count += 1 
                                if count == 2:
                                    return True 
                        return False 
                    else:
                        return False 
                
        elif move == "Block Stealing":
            if gData.shownCards.count("Assasin") + gData.shownCards.count("Ambassador") == 6:
                return True 
            else:
                if len(AlivePlayers) == 2:
                    for player in AlivePlayers:
                        if player != self:
                            if player.playedMoves.count("Ambassador") >= 3 or player.playedMoves.count("Captain") <= 3:
                                return True 
                    return False 
                elif len(AlivePlayers) != 2:
                    if "Captain" in self.hand or "Ambassador" in self.hand:
                        if "Ambassador" in self.hand:
                            if gData.shownCards.count("Ambassador") != 0:
                                if gData.shownCards.count("Captain") != 0:
                                    if random() > .2:
                                        return True 
                                    else:
                                        return False
                                else:
                                    return False 
                            else:
                                return False 
                        else:
                            return False 
                    else:
                        return False
                    
                                
        
    def pickTargetWrapper(f):
        def g(*args):
            result = f(*args)
            self = args[0]
            gData = args[1]
            if result == None:
                return result
            elif gData.players[result] == self or not gData.players[result].isAlive:
                for player in gData.players:
                    if player != self and player.isAlive:
                        return gData.players.index(player)
            else:
                return result
        return g
            
    @pickTargetWrapper
    def pickTarget(self, gData):
        # Tracks the coins and lives of all the players 
        coinsList = []
        livesList = [] 
        mostCoins = None 
        mostCoinsPlayer = None 
        mostLivesPlayer = None 
        # Runs through the player list and adds the information to the lists 
        for player in gData.players:
            if player != self:
                coinsList.append(player.coins)
                livesList.append(len(player.hand))
        
        # Finds the most amount of coins and which players has the most coins 
        mostCoins = max(coinsList)
        mostCoinsPlayer = coinsList.index(mostCoins)
        mostLivesPlayer = livesList.index(max(livesList))
        
        # The AI should always target players with the most lives and most coins 
        if livesList.count(2) > 1:
            if livesList[mostCoinsPlayer] == 2:
                return mostCoinsPlayer
            else:
                return mostLivesPlayer
        
        # If there is only one player with two lives he should always be targeted 
        elif livesList.count(2) == 1:
            targetPlayer = livesList.index(2)
            return targetPlayer
            
        # AI always targets the player with most coins if everybody has 1 life 
        else:
            targetPlayer = mostCoinsPlayer
            return targetPlayer 
    
    def run(self, gData, data):
        data.canMove = False
        target = None
        #print(self.otherPlayersAction)
        if not self.targetting and not self.runFlag1:
            move = self.chooseMove(gData)
            #move = self.move
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
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
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
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
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
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
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
            # Carries out the Tax Method 
            if move == "Tax":
                canMove, executeFn = primaryActions.tax(gData, self, data)
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
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
            # Carries out the Assasinate Method 
            if move == "Assasinate":
                # Check for target within the player list 
                self.targetting = True
                if self.targetting:
                    self.text = "Pick a player to assasinate"
                    player = self.pickTarget(gData)
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
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
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
            # Carries out the steal move 
            if move == "Steal":
                self.targetting = True
                if self.targetting:
                    self.text = "Pick a player to steal from"
                    player = self.pickTarget(gData)
                    if  str(player) in ["0", "1", "2", "3"]:
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
                #data.moveList.insert(0, ["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
                if not canMove:
                    self.assignInput(data, "")
                    return None
                else:
                    self.executeFn = executeFn
                    self.runFlag1 = True
                    self.move = move
                    data.server.send(("Move " + self.move + " " + str(self) + " " + str(self.target) + "\n").encode())
                    print("HEY")
                    data.moveList.insert(0,["Player%s played %s, target %s" % (str(self), self.move, str(self.target)), 950, 750])
                    data.textFlag = True
            # Carries out the coup action 
            if move == "Coup":
                # Gets the target 
                self.targetting = True
                if self.targetting:
                    self.text = "Pick a player to coup"
                    player = self.pickTarget(gData)
                    if  str(player) in ["0", "1", "2", "3"]:
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
                #data.moveList.insert(0,["Player%s played %s" % (str(self),move), 950, 750])
                print("Player%s played %s" % (str(self),move))
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
        print(gData.turnCount)
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
    
    def chooseMoveWrapper(f):
        def g(*args):
            result = f(*args)
            gData = args[1]
            self = args[0]
            maxCoins = 0
            for player in gData.players:
                if player != self:
                    if player.coins > maxCoins:
                        maxCoins = player.coins
            if maxCoins == 0 and result == "Steal":
                rand = random.randin(0, 1)
                if rand == 0:
                    return "Income"
                return "Foreign AId"
            return result
        return g
        
    @chooseMoveWrapper
    def chooseMove(self, gData):
        print("hello")
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return ""
        else:
            self.decisionCount = 0
        AlivePlayers = []
        coinsList = []
        myIndex = None 
        for player in gData.players:
            if player.isAlive:
                AlivePlayers.append(player)
        
        for player in range(len(AlivePlayers)):
            if AlivePlayers[player] == self:
                myIndex = player 
            coinsList.append(AlivePlayers[player].coins)
        maxCoins = max(coinsList)
        chance = random()
        # Moves should be random at the beginning to establish bluffing 
        if gData.turnCount < 3:
            if chance < .5:
                self.playedMoves.append("Tax")
                return "Tax"
            elif (chance > .5 and chance < .75):
                self.playedMoves.append("Ambassador")
                return "Exchange"
            else:
                return "Foreign Aid"
        # How to play if there are more than two players alive 
        elif len(AlivePlayers) != 2:
            if self.coins >= 3:
                if self.coins >= 7:
                    return "Coup"
                elif "Assasin" in self.hand:
                    return "Assasinate"
                elif len(self.PotentialDeck) == 0:
                    if "Ambassador" in self.hand:
                        return "Exchange" 
                    else:
                        count = 0 
                        for player in gData.players:
                            if player != self:
                                if player.playedMoves.count("Ambassador") >= 3:
                                    print("Abhi")
                                    return "Income"
                                else:
                                    return "Exchange"
                        return "Exchange"
                elif "Assasin" not in self.hand:
                    count = 0 
                    for player in gData.players:
                        if player != self:
                            if player.playedMoves.count("Duke") > 3:
                                count += 1
                    if count >= 1:
                        return "Income"
                    else:
                        return "Foreign Aid"
                else:
                    return "Income"
            else:
                if "Duke" in self.hand:
                    return "Tax"
                else:
                    count = 0 
                    for player in gData.players:
                        if player != self:
                            if player.playedMoves.count("Duke") > 3:
                                count += 1
                                continue
                        if count >= 1:
                            return "Income"
                    return "Foreign Aid"
        
        elif len(AlivePlayers) == 2:
            otherIndex = None 
            if self.coins >= 7:
                return "Coup"
                
            elif self.coins == maxCoins:
                if myIndex == 0:
                    otherIndex = 1 
                    if "Captain" in self.hand or "Duke" in self.hand:
                        if "Duke" in self.hand:
                            return "Tax"
                        elif "Captain" in AlivePlayers[1].hand or "Ambassador" in AlivePlayers[1].hand:
                            if "Duke" in AlivePlayers[1].hand:
                                if "Assasin" in self.hand and self.coins >= 3:
                                    return "Assasinate"
                                return "Income"
                            else:
                                return "Income"
                        else:
                            return "Steal"
                    else:
                        if self.coins >= 3 and "Assasin" in self.hand:
                            if "Contessa" not in AlivePlayers[1].hand:
                                return "Assasinate"
                            elif "Duke" in AlivePlayers[1].hand:
                                return "Income"
                            else:
                                return "Foreign Aid"
                        else:
                            return "Income"
                            
                elif myIndex == 1:
                    otherIndex = 0 
                    if "Captain" in self.hand or "Duke" in self.hand:
                        if "Duke" in self.hand:
                            return "Tax"
                        elif "Captain" in AlivePlayers[0].hand or "Ambassador" in AlivePlayers[0].hand:
                            if "Duke" in AlivePlayers[0].hand:
                                if "Assasin" in self.hand and self.coins >= 3:
                                    return "Assasinate"
                                return "Income"
                            return "Income"
                        else:
                            return "Steal"
                    else:
                        if self.coins >= 3 and "Assasin" in self.hand:
                            if "Contessa" not in AlivePlayers[0].hand:
                                return "Assasinate"
                            elif "Duke" in AlivePlayers[0].hand:
                                return "Income"
                            else:
                                return "Foreign Aid"
                        else:
                            return "Income"
            else:
                if myIndex == 0:
                    if "Captain" in self.hand or "Duke" in self.hand:
                        if "Captain" in self.hand and "Captain" not in AlivePlayers[1].hand and "Ambassador" not in AlivePlayers[1].hand:
                            return "Steal"
                        elif "Captain" in AlivePlayers[1].hand or "Ambassador" in AlivePlayers[1].hand:
                            if "Duke" in AlivePlayers[1].hand:
                                if "Assasin" in self.hand and self.coins >= 3:
                                    return "Assasinate"
                                return "Income"
                            else:
                                return "Income"
                        else:
                            return "Tax"
                    else:
                        if self.coins >= 3 and "Assasin" in self.hand:
                            if "Contessa" not in AlivePlayers[1].hand:
                                return "Assasinate"
                            elif "Duke" in AlivePlayers[1].hand:
                                return "Income"
                            else:
                                return "Assasinate"
                        else:
                            return "Income"
                else:
                    if "Captain" in self.hand or "Duke" in self.hand:
                        if "Captain" in self.hand and "Captain" not in AlivePlayers[0].hand and "Ambassador" not in AlivePlayers[0].hand:
                            return "Steal"
                        elif "Captain" in AlivePlayers[0].hand or "Ambassador" in AlivePlayers[0].hand:
                            if "Duke" in AlivePlayers[0].hand:
                                if "Assasin" in self.hand and self.coins >= 3:
                                    return "Assasinate"
                                return "Income"
                            else:
                                return "Income"
                        else:
                            return "Tax"
                    else:
                        if self.coins >= 3 and "Assasin" in self.hand:
                            if "Contessa" not in AlivePlayers[0].hand:
                                return "Assasinate"
                            elif "Duke" in AlivePlayers[0].hand:
                                return "Income"
                            else:
                                return "Assasinate"
                        else:
                            return "Income"
            pass
        else:
            return "Income"
        
    def exchange(self, gData, player, data, opposingPlayer = None):
        # User input asking which two cards they would like to keep
        if len(self.hand) == 1:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Exchange \n"
                card1 = gData.deck.pop(0)
                card2 = gData.deck.pop(0)
                self.possibleCards = [self.hand.pop(), card1, card2]
                player.firstPassExchange = False
                possibleCards = self.possibleCards
                player.text = "a card " + str(possibleCards)
                
                if "Captain" in possibleCards:
                    choice = "Captain"
                elif "Assasin" in possibleCards:
                    choice = "Assasin"
                elif "Ambassador" in possibleCards:
                    choice = "Ambassador"
                elif "Contessa" in possibleCards:
                    choice = "Contessa"
                elif "Duke" in possibleCards:
                    choice = "Duke"
                #choice = possibleCards[random.randint(0,2)]
                possibleCards.remove(choice)
                player.text = ""
                player.assignInput(data, "")
                self.PotentialDeck.append(possibleCards[0])
                self.PotentialDeck.append(possibleCards[1])
                gData.deck.append(possibleCards.pop(0))
                gData.deck.append(possibleCards.pop(0))
                self.hand = [choice]
                player.firstPassExchange = True
                return True
            return True, execute 
            #choice = input("Pick a card: ")
        elif len(self.hand) == 2:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Exchange \n"
                card1 = gData.deck.pop(0)
                card2 = gData.deck.pop(0)
                self.possibleCards = [self.hand.pop(), self.hand.pop(), card1, card2]
                player.firstPassExchange = False
                possibleCards = self.possibleCards
                player.text = "Choose two cards " + str(possibleCards)
                if "Captain" in possibleCards:
                    choice = "Captain"
                elif "Assasin" in possibleCards:
                    choice = "Assasin"
                elif "Ambassador" in possibleCards:
                    choice = "Ambassador"
                elif "Contessa" in possibleCards:
                    choice = "Contessa"
                elif "Duke" in possibleCards:
                    choice = "Duke"
                #choice = possibleCards[random.randint(0,3)]
                possibleCards.remove(choice)
                self.hand.append(choice)
                if "Captain" in possibleCards:
                    choice = "Captain"
                elif "Assasin" in possibleCards:
                    choice = "Assasin"
                elif "Ambassador" in possibleCards:
                    choice = "Ambassador"
                elif "Contessa" in possibleCards:
                    choice = "Contessa"
                elif "Duke" in possibleCards:
                    choice = "Duke"
                #choice = possibleCards[random.randint(0,2)]
                possibleCards.remove(choice)
                self.hand.append(choice)
                self.PotentialDeck.append(possibleCards[0])
                self.PotentialDeck.append(possibleCards[1])
                gData.deck.append(possibleCards.pop(0))
                gData.deck.append(possibleCards.pop(0))
                player.text = ""
                player.assignInput(data, "")
                player.firstPassExchange = True
                return True
            return True, execute
        
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
        self.decisionCount += 1
        if self.decisionCount < self.decisionTime:
            return None
        else:
            self.decisionCount = 0
        if move == "Tax":
            if "Duke" in self.hand:
                lostCard = "Duke"
                DukeIndex = self.hand.index("Duke")
                self.hand.pop(DukeIndex)
                return lostCard 
        elif move == "Steal":
            if "Captain" in self.hand:
                lostCard = "Captain"
                CaptainIndex = self.hand.index("Captain")
                self.hand.pop(CaptainIndex)
                return lostCard 
        elif move == "Assasinate":
            if "Assasin" in self.hand:
                lostCard = "Assasin"
                AssasinIndex = self.hand.index("Assasin")
                self.hand.pop(AssasinIndex)
                return lostCard 
        elif move == "Block Assasination":
            if "Contessa" in self.hand:
                lostCard = "Contessa"
                ContessaIndex = self.hand.index("Contessa")
                self.hand.pop(ContessaIndex)
                return lostCard 
        elif move == "Block Foreign Aid":
            if "Duke" in self.hand:
                lostCard = "Duke"
                DukeIndex = self.hand.index("Duke")
                self.hand.pop(DukeIndex)
                return lostCard 
        elif move == "Exchange":
            if "Ambassador" in self.hand:
                lostCard = "Ambassador"
                AmbassadorIndex = self.hand.index("Ambassador")
                self.hand.pop(AmbassadorIndex)
                return lostCard 
        elif move == "Block Stealing":
            if "Captain" or "Ambassador" in self.hand:
                if "Captain" in self.hand:
                    lostCard = "Captain"
                    CaptainIndex = self.hand.index("Captain")
                    self.hand.pop(CaptainIndex)
                    return lostCard 
                if "Ambassador" in self.hand:
                    lostCard = "Ambassador"
                    AmbassadorIndex = self.hand.index("Ambassador")
                    self.hand.pop(AmbassadorIndex)
                    return lostCard
        elif "Captain" in self.hand:
            CaptainIndex = self.hand.index("Captain")
            for card in self.hand:
                if self.hand.index(card) != CaptainIndex:
                    lostCard = card
                    self.hand.remove(card)
                    return lostCard 
        elif "Assasin" in self.hand:
            AssasinIndex = self.hand.index("Assasin")
            for card in self.hand:
                if self.hand.index(card) != AssasinIndex:
                    lostCard = card
                    self.hand.remove(card)
                    return lostCard
        if len(self.hand) == 1:
            lostCard = self.hand.pop()
            return lostCard
        randomIndex = rnd.randint(0,1)
        lostCard = self.hand[randomIndex]
        self.hand.pop(randomIndex)
        return lostCard 
            
    
        

        
    
    

# Taken from https://github.com/hexparrot/the-resistance-coup-ai/blob/master/heuristics.py


    

from DeckOperations import *
