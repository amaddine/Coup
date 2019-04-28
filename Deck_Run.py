##### This is the actions setup

class primaryActions(object):
    actions = {"Income": ["Duke", "Captain", "Ambassador", "Assasin", "Contessa"], 
                    "Foreign Aid": ["Duke", "Captain", "Ambassador", "Assasin", "Contessa"], 
                    "Steal": ["Captain"],
                    "Coup" : ["Duke", "Captain", "Ambassador", "Assasin", "Contessa"],
                    "Assasinate" : ["Assasin"],
                    "Exchange": ["Ambassador"], 
                    "Tax": ["Duke"] }
    
    @staticmethod
    def income(gData, player, data, opposingPlayer = None):
        if player.coins >= 10:
            player.text = "You can only coup\nChoose a Move"
            return False, None
        else:
            def execute(player = player, opposingPlayer = opposingPlayer):
                player.coins += 1 
                message = "Income \n"
                return True
            return True, execute

    @staticmethod 
    def coup(gData, player, data, opposingPlayer = None):
        if player.coins < 7:
            player.text = "You don't have enough coins\nChoose a Move"
            return False, None
        elif opposingPlayer == None:
            player.text = "You must pick a player to coup\nChoose a Move"
            return False, None
        elif not opposingPlayer.isAlive:
            player.text = "The Player is already dead\nChoose a Move"
            return False, None
        else:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Coup \n"
                card = opposingPlayer.loseACard(data)
                if card == None:
                    return None
                else:
                    opposingPlayer.assignInput(data, "")
                    player.coins -= 7
                    gData.shownCards.append(card)
                    return True
            return True, execute

    @staticmethod
    def foreignAid(gData, player, data, opposingPlayer = None):
        # Adds two to coin total
        if player.coins >= 10:
            player.text = "You can only coup\nChoose a Move"
            return False, None
        else:
            def execute(player = player, opposingPlayer = opposingPlayer):
                player.coins += 2
                message = "ForeignAid \n"
                return True
            return True, execute

    @staticmethod
    def tax(gData, player, data, opposingPlayer = None):
        # Adds three to coin total
        if player.coins >= 10:
            player.text = "You can only coup\nChoose a Move"
            return False, None
        else:
            def execute(player = player, opposingPlayer = opposingPlayer):
                player.coins += 3 
                message = "Tax \n"
                return True
            return True, execute
            
    @staticmethod
    def steal(gData, player, data, opposingPlayer = None):
        if not opposingPlayer.isAlive:
            player.text = "The Player is already dead\nChoose a Move"
            return False, None
        elif opposingPlayer.coins == 0:
            player.text = "The Player doesn't have enough coins\nChoose a Move"
            return False, None
        elif player.coins >= 10:
            player.text = "The Player can only coup\nChoose a Move"
            return False, None
        else:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Steal \n"
                if opposingPlayer.coins >= 2:
                    opposingPlayer.coins -=2 
                    player.coins += 2 
                else:
                    opposingPlayer.coins -= 1
                    player.coins += 1 
                return True
            return True, execute
        
    @staticmethod
    def assasinate(gData, player, data, opposingPlayer = None):
        # If other player challenges they lose both thier cards 
        # Else they block
        # Else they block and lose both cards  
        # Else they lose a card 
        if player.coins < 3:
            player.text = "You dont have enough coins\nChoose a Move"
            return False, None
        elif player.coins >= 10:
            player.text = "The Player can only coup\nChoose a Move"
            return False, None
        elif not opposingPlayer.isAlive:
            player.text = "The Player is already dead\nChoose a Move"
            return False, None
        else:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Assasinate \n"
                card = opposingPlayer.loseACard(data)
                if card == None:
                    return None
                else:
                    opposingPlayer.assignInput(data, "")
                    player.coins -= 3 
                    gData.shownCards.append(card)
                    return True
            return True, execute
      
    @staticmethod
    def exchange(gData, player, data, opposingPlayer = None):
        # User input asking which two cards they would like to keep
        if player.coins >= 10:
            player.text = "The Player can only coup"
            return False, None
        if len(player.hand) == 1:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Exchange \n"
                if player.firstPassExchange:
                    card1 = gData.deck.pop(0)
                    card2 = gData.deck.pop(0)
                    player.possibleCards = [player.hand.pop(), card1, card2]
                player.firstPassExchange = False
                possibleCards = player.possibleCards
                player.text = "Choose a card\n" + str(possibleCards)
                choice = player.input
                if choice == "":
                    return None
                if choice not in possibleCards:
                    player.text = "Choose a legal card\n" + str(possibleCards)
                    return None
                possibleCards.remove(choice)
                player.text = ""
                player.assignInput(data, "")
                gData.deck.append(possibleCards.pop(0))
                gData.deck.append(possibleCards.pop(0))
                player.hand = [choice]
                player.firstPassExchange = True
                return True
            return True, execute 
            #choice = input("Pick a card: ")
        elif len(player.hand) == 2:
            def execute(player = player, opposingPlayer = opposingPlayer):
                message = "Exchange \n"
                if player.firstPassExchange:
                    card1 = gData.deck.pop(0)
                    card2 = gData.deck.pop(0)
                    player.possibleCards = [player.hand.pop(), player.hand.pop(), card1, card2]
                player.firstPassExchange = False
                possibleCards = player.possibleCards
                player.text = "Choose two cards \n" + str(possibleCards)
                choice = player.input
                if choice == "":
                    return None
                cardList = choice.split(" ")
                if len(cardList) != 2:
                    player.text = "Choose two legal cards\n" + str(possibleCards)
                    return None
                for card in cardList:
                    if card not in possibleCards:
                        player.text = "Choose two legal cards\n" + str(possibleCards)
                        return None
                possibleCards.remove(cardList[0])
                player.hand.append(cardList[0])
                possibleCards.remove(cardList[1])
                player.hand.append(cardList[1])
                gData.deck.append(possibleCards.pop(0))
                gData.deck.append(possibleCards.pop(0))
                player.text = ""
                player.assignInput(data, "")
                player.firstPassExchange = True
                return True
            return True, execute
            #def e
        ###### Finish this exchange method 
        

class secondaryActions(object):
    actions = {"Block Stealing": ["Captain", "Ambassador"],
            "Block Assasination": ["Contessa"],
            "Block Foreign Aid": ["Duke"], 
            }
        
from DeckOperations_Run import *
        
        
    