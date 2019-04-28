####### This file is the main Client 
####### The game is drawn and Run Here
###### All images were taken from google images and the were resized

# Updated Animation Starter Code

from tkinter import *
from Deck_Run import *
from DeckOperations_Run import *
from HardAI import *
from AI import *
import socket 
import threading 
from queue import Queue
from random import shuffle 
#import winsound

####################################
# customize these functions
####################################

#####################  
#####################  Socket Handling 

HOST = "" # put your IP address here if playing on multiple computers
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")
    
#winsound.PlaySound('song.wav', winsound.SND_ALIAS | winsound.SND_ASYNC)


######################################### 15112 Run Function 
def init(data):
    # load data.xyz as appropriate
    data.fontSize = str(data.width//10)
    data.mode = "StartScreen"
    data.scrollY = 0 
    data.ImageWidthRules = 241 
    data.ImageHeightRules = 385 
    # data.numPlayers = len(newGame.players)
    data.numPlayers = 4
    data.color = ["DarkOrange1", "DarkOrange2", "DarkOrange3", "DarkOrange4"]
    data.count = 0  
    data.count2 = 0 
    data.shiftUp = False
    data.others = {}
    data.HardAINumber = 0 
    data.EasyAINumber = 0 
    ####
    
def localMultiplayerInit(data):
    #data.me = Player(data.newGame)
    #data.others = dict()
    data.moveList = [] 
    data.newTurn = True
    data.requiresInput = False
    data.input = ""
    data.input2 = ""
    data.input3 = ""
    data.input4 = ""
    data.text = ""
    data.text2 = ""
    data.text3 = ""
    data.text4 = ""
    data.textFlag = True
    
    data.newGame = GameData()
    data.Player0 = Player(data.newGame)
    data.Player1 = HardAI(data.newGame)
    data.Player2 = HardAI(data.newGame) 
    data.Player3 = HardAI(data.newGame)
    data.currPlayer = data.Player0
    data.getDecision = StringVar()
    data.decisionReq = Entry(data.root, textvariable=data.getDecision)
    data.decisionReq.pack()
    pass

def onlineMultiplayerInit(data):
    #data.me = Player(data.newGame)
    #data.others = dict()
    data.moveList = [] 
    data.input = ""
    data.text = ""
    data.shownCards = []
    if data.ID == "Player0":
        data.handState = [["Duke", "Duke"], ["Duke", "Duke"], ["Duke", "Duke"], ["Duke", "Duke"]]
        data.gameState = "[[True, 2, 2], [True, 2, 2], [True, 2, 2], [True, 2, 2], [0]]"
        data.newTurn = True
        data.requiresInput = False
        data.textFlag = True
        data.newGame = GameData()
        data.me = Player(data.newGame)
        others = len(data.others)
        for i in range(others):
            useless = Player(data.newGame)
        for j in range(3 - others):
            useless = HardAI(data.newGame)
        data.currPlayer = data.me
    else:
        data.isAlive = "False"
    data.getDecision = StringVar()
    data.decisionReq = Entry(data.root, textvariable=data.getDecision)
    data.decisionReq.pack()
    pass

def mousePressed(event, data):
    # use event.x and event.y
    # Put the buttons in mousepressed
    if data.mode == "StartScreen": startScreenMousePressed(event, data)
    if data.mode == "SetupScreen": setupScreenMousePressed(event, data)
    if data.mode == "EndScreen":
        if event.x in range(data.width//3, data.width//3 + 150) and event.y in range(data.height//2, data.height//2 + 150):
            localMultiplayerInit(data)
            data.mode = "LocalMultiplayer"
        elif event.x in range(2* data.width//3, 2 * data.width//3 + 150) and event.y in range(data.height//2, data.height//2 + 150):
            data.mode =="StartScreen"
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.mode == "RulesScreen": keyPressedRulesScreen(event,data)
    if data.mode == "EndScreen": 
        if event.char == "b":
            data.mode = "StartScreen"
    if data.mode == "LocalMultiplayer": 
        localMultiplayerKeyPressed(event, data)
    if data.mode == "OnlineMultiplayer": 
        onlineMultiplayerKeyPressed(event, data)
    pass

def timerFired(data):
    #data.Currcolor = data.color[data.count % len(data.color)]
    if data.mode == "LocalMultiplayer":
        localMultiplayerRun(data)
    elif data.mode == "OnlineMultiplayer":
        if data.ID == "Player0":
            onlineMultiplayerRun(data)
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        msg = msg.lstrip()
        index1 = msg.find(" ")
        command = msg[:index1]
        msg = msg[index1+1:]
        index2 = msg.find(" ")
        if index2 != -1:
            id = msg[:index2]
            if len(msg) > 2:
                payload = msg[index2+1:]
            else:
                payload = ""
        else:
            id = msg
            payload = ""
        if (command == "myIDis"):
            data.ID = id
        elif (command == "newPlayer"):
            try:
                if data.ID == "Player0":
                    data.others[id] = ""
            except:
                pass
        elif (command == "Playing"):
            if data.mode != "OnlineMultiplayer":
                onlineMultiplayerInit(data)
                data.mode = "OnlineMultiplayer"
        elif (command == "GameState"):
            data.gameState = payload
        elif (command == "HandState"):
            handStateStr = payload[2:-2]
            data.handState = []
            for hand in handStateStr.split("], ["):
                currHand = []
                for item in hand.split(", "):
                    currHand.append(item)
                data.handState.append(currHand)
        elif (command[:-1] == "Text"):
            if command[-1] == data.ID[-1]:
                if len(payload) == 5:
                    data.text = ""
                else:
                    data.text = payload[5:]
        elif (command == "Input"):
            if data.ID == "Player0":
                #Remove Later
                if payload in ["0", "1", "2", "3"]:
                    offset = id[-1]
                    payload = str((int(payload) + int(offset)) % 4)
                data.others[id] = payload
        elif (command == "Move"):
            data.textFlag = True
            payload = payload.split()
            move = payload[0]
            if move == "ForeignAid":
                move = "Foreign Aid"
            player = payload[1]
            if move == "Steal" or move == "Coup" or move == "Assasinate":
                target = payload[2]
                offset = data.ID[-1]
                player = str((int(player) - int(offset)) % 4)
                target = str((int(target) - int(offset)) % 4)
                data.moveList.insert(0,["Player%s played %s, target %s" % (player, move, target), 950, 750])
            else:
                #Remove Later
                if player in ["0", "1", "2", "3"]:
                    offset = data.ID[-1]
                    player = str((int(player) - int(offset)) % 4)
                data.moveList.insert(0,["Player%s played %s" % (player, move), 950, 750])
        elif (command == "Challenge"):
            data.textFlag = True
            if payload == "-1":
                data.moveList.insert(0,["No one challenges", 950, 750])
            else:
                #Remove Later
                if payload in ["0", "1", "2", "3"]:
                    offset = data.ID[-1]
                    payload = str((int(payload) - int(offset)) % 4)
                data.moveList.insert(0,["Player%s challenges" % (payload), 950, 750])
        elif (command == "Block"):
            data.textFlag = True
            if payload == "-1":
                data.moveList.insert(0,["No one blocks", 950, 750])
            else:
                #Remove Later
                if payload in ["0", "1", "2", "3"]:
                    offset = data.ID[-1]
                    payload = str((int(payload) - int(offset)) % 4)
                data.moveList.insert(0,["Player%s blocks" % (payload), 950, 750])
        elif (command == "Lost"):
            data.textFlag = True
            payload = payload.split()
            card = payload[0]
            player = payload[1]
            #Remove Later
            if player in ["0", "1", "2", "3"]:
                offset = data.ID[-1]
                player = str((int(player) - int(offset)) % 4)
            data.moveList.insert(0,["Player%s showed a %s" % (player, card), 950, 750])
        elif (command == "ShownCards"):
            payload = payload[1:-1]
            data.shownCards = []
            for card in payload.split(", "):
                data.shownCards.append(card)
        serverMsg.task_done()

def localMultiplayerRun(data):
    if data.mode == "LocalMultiplayer":
        if data.newTurn or data.repeatTurn:
            for player in data.newGame.players:
                player.updateData(data)
            if data.newTurn:
                data.currPlayer.text = "Choose a Move"
                for player in data.newGame.players:
                    player.updateAIData()
            data.newTurn = False
            if not data.currPlayer.isAlive:
                for player in data.newGame.players:
                    player.text = ""
                index = data.newGame.players.index(data.currPlayer) + 1
                data.currPlayer = data.newGame.players[index % len(data.newGame.players)]
                data.repeatTurn = False
                data.newTurn = True
            else:
                result = data.currPlayer.run(data.newGame, data)
                #print(data.currPlayer.name)
                if result == None:
                    data.repeatTurn = True
                else:
                    for player in data.newGame.players:
                        player.text = ""
                    index = data.newGame.players.index(data.currPlayer) + 1
                    data.currPlayer = data.newGame.players[index % len(data.newGame.players)]
                    data.repeatTurn = False
                    data.newTurn = True
            for player in data.newGame.players:
                player.updateData(data)
            deadCount = 0
            alive = ""
            for player in data.newGame.players:
                if not player.isAlive:
                    deadCount += 1
                else:
                    alive = player
            if deadCount == len(data.newGame.players) - 1:
                data.winner = alive
                data.mode = "EndScreen"
                
def onlineMultiplayerRun(data):
    if data.mode == "OnlineMultiplayer":
        if data.newTurn or data.repeatTurn:
            for player in data.newGame.players:
                player.updateData(data)
            if data.newTurn:
                data.currPlayer.text = "Choose a Move"
                for player in data.newGame.players:
                    player.updateAIData()
            data.newTurn = False
            if not data.currPlayer.isAlive:
                for player in data.newGame.players:
                    player.text = ""
                index = data.newGame.players.index(data.currPlayer) + 1
                data.currPlayer = data.newGame.players[index % len(data.newGame.players)]
                data.repeatTurn = False
                data.newTurn = True
            else:
                result = data.currPlayer.run(data.newGame, data)
                #print(data.currPlayer.name)
                if result == None:
                    data.repeatTurn = True
                else:
                    for player in data.newGame.players:
                        player.text = ""
                    index = data.newGame.players.index(data.currPlayer) + 1
                    data.currPlayer = data.newGame.players[index % len(data.newGame.players)]
                    data.repeatTurn = False
                    data.newTurn = True
            for player in data.newGame.players:
                player.updateData(data)
            gameState = []
            for player in data.newGame.players:
                playerList = []
                playerList.append(player.isAlive)
                playerList.append(player.coins)
                playerList.append(len(player.hand))
                gameState.append(playerList)
            gameState.append([data.newGame.players.index(data.currPlayer)])
            data.gameState = str(gameState)
            data.server.send(("GameState "+data.gameState + "\n").encode())
            handState = []
            for player in data.newGame.players:
                handState.append(player.hand)
            data.handState = handState
            data.server.send(("HandState "+str(data.handState)+ "\n").encode())
            data.server.send(("ShownCards "+str(data.newGame.shownCards)+ "\n").encode())
            data.server.send(("Playing Useless" + "\n").encode())
            deadCount = 0
            alive = ""
            for player in data.newGame.players:
                if not player.isAlive:
                    deadCount += 1
                else:
                    alive = player
            if deadCount == len(data.newGame.players) - 1:
                data.winner = alive
                data.mode = "EndScreen"

def redrawAll(canvas, data):
    # draw in canvas
    if data.mode == "StartScreen": startScreenRedrawAll(canvas, data)
    elif data.mode == "SetupScreen": setupScreenRedrawAll(canvas,data)
    elif data.mode == "RulesScreen": rulesScreenRedrawAll(canvas,data)
    elif data.mode == "LocalMultiplayer": localMultiplayerRedrawAll(canvas, data)
    elif data.mode == "OnlineMultiplayer": onlineMultiplayerRedrawAll(canvas, data)
        # canvas.create_rectangle(0,0,data.width,data.height,fill = "LightSkyBlue1")
    elif data.mode == "EndScreen":
        canvas.create_rectangle(0,0, data.width, data.height, fill = "White")
        canvas.create_text(200, 200, text = "WINNER: PLAYER " + str(data.newGame.players.index(data.winner)), fill = "Black", font = "Helvetica 27")
        data.decisionReq.destroy()
        canvas.create_rectangle(data.width/3, data.height/3, data.width/3 + 250, data.height/3 + 150, fill = "Gray")
        canvas.create_text(data.width/3 + 125, data.height/3 + 75, text = "Restart Local Multiplayer")
        canvas.create_rectangle(data.width/3, 2 * data.height/3, data.width/3 + 250,
        2* data.height/3 + 150, fill = "Gray")
        canvas.create_text(data.width/3 + 125, 2* data.height/3 + 75, text = "Start Screen")
    pass
    


#################3 Start Screen Methods 
def startScreenRedrawAll(canvas, data):
        # Creates the background 
        canvas.create_rectangle(0,0,data.width,data.height,fill = "White")
        #canvas.create_image(data.width//2, data.height//2, image =  data.startScreenBackGround)
        # Creates the Coup text 
        canvas.create_text(data.width/2, data.height/5, text = "Coup", font = ("Copper %s bold italic") % (data.fontSize), fill = "Grey")
        # Creates the 3 mode boxes 
        canvas.create_rectangle(data.width/4, 3* data.height/8, 3*data.width/4,4*data.height/8,
        fill = "Gray")
        canvas.create_rectangle(data.width/4,4*data.height/8, 3* data.width/4, 5*data.height/8,
        fill = "Gray")
        canvas.create_rectangle(data.width/4,5*data.height/8, 3*data.width/4, 6*data.height/8, 
        fill = "Gray")
        # Labels the 3 mode boxes 
        canvas.create_text(data.width/2, 3.5*data.height/8, text = "Online Multiplayer",
        font = ("Copper %s bold italic")% ("26"))
        canvas.create_text(data.width/2, 4.5*data.height/8, text = "Local Multiplayer",
        font = ("Copper %s bold italic") % ("26"))
        canvas.create_text(data.width/2, 5.5*data.height/8, text = "Rules",
        font = ("Copper %s bold italic") % ("26"))

def startScreenMousePressed(event, data):
    # Checks which mode was pressed on the start screen 
    
    if event.x in range(data.width//4, 3*data.width//4):
        if event.y in range(5*data.height//8,6*data.height//8):
            data.mode = "RulesScreen"
        elif event.y in range(4*data.height//8, 5*data.height//8):
            localMultiplayerInit(data)
            data.mode = "LocalMultiplayer"
        elif event.y in range(3*data.height//8, 4*data.height//8) and data.ID == "Player0":
            onlineMultiplayerInit(data)
            data.mode = "OnlineMultiplayer"
 
 #####################  Rules Screen Methods            
def rulesScreenRedrawAll(canvas, data):
    # 241,385 
    canvas.create_rectangle(0,0,4* data.width,4* data.height - data.scrollY,fill = "Black")
    cardList = ["Duke", "Assasin", "Contessa", "Captain" , "Ambassador"]
    x0, y0 = 300, 100 - data.scrollY
    for card in cardList:
        if card == "Duke":
            canvas.create_image(x0, y0, image = data.DukeGame2)
        elif card == "Contessa":
            canvas.create_image(x0, y0, image = data.ContessaGame2)
        elif card == "Captain":
            canvas.create_image(x0, y0, image = data.CaptainGame2)
        elif card == "Ambassador":
            canvas.create_image(x0, y0, image = data.AmbassadorGame2)
        elif card == "Assasin":
            canvas.create_image(x0, y0, image = data.AssasinGame2)
        
        x0 += 100
    canvas.create_image(500, 700 - data.scrollY, image = data.CoupRules)
    
def keyPressedRulesScreen(event,data):
    if event.keysym == "Up":
        if data.scrollY - 5 >= 0:
            data.scrollY -=15 
        else:
            data.scrollY = 0 
    elif event.keysym == "Down":
        data.scrollY += 15 
        print(data.scrollY)
    elif event.keysym == "b":
        data.mode = "StartScreen"


def drawGame(canvas, data, gData):
    for player in data.newGame.players:
        for card in player.hand:
            if card == "Duke":
                canvas.create_image()
            elif card == "Assasin":
                canvas.create_image()
            elif card == "Contessa":
               pass
               #canvas.create_image()
            elif card == "Ambassador":
                canvas.create_image()
            elif card == "Captain":
                canvas.create_image()
    pass

def drawScrollBar(canvas, data):
    canvas.create_rectangle(850, 0, 1000, 800, fill = "White")
    for move in data.moveList:
        if move == data.moveList[0]:
            pass
        elif data.textFlag == True:
            move[2] -= 20
            if move[2] < 200:
                data.moveList.remove(move)
        canvas.create_text(move[1] + 35, move[2] - 60, text = move[0], fill = "Black", font = "Helvetica 12", anchor = "se")
    data.textFlag = False
    pass

# 850, 800

################ Online Multiplayer
def parseGameState(gameState):
    gameState = gameState[2:-2]
    parsedState = []
    playerStates = gameState.split("], [")
    currPlayer = playerStates.pop()
    for playerState in playerStates:
        playerDict = {}
        playerState = playerState.split(", ")
        playerDict["Alive"] = playerState[0]
        playerDict["Coins"] = int(playerState[1])
        playerDict["CardNumber"] = int(playerState[2])
        parsedState.append(playerDict)
    parsedState.append(int(currPlayer))
    return parsedState

def onlineMultiplayerRedrawAll(canvas, data):
    # Need to draw both cards 
    #canvas.create_image(data.width/2, data.height/2, image = data.BackGround)
    #canvas.create_rectangle(0,0,1000,800, fill = "tomato2")
    canvas.create_image(425,500, image = data.castle)
    drawScrollBar(canvas, data)
    # drawShownCards(canvas, data)
    # 193 by 265 
    # for card in data.player0.hand:
    #     if card == "Duke":
    #         canvas.create_image(data.width/4, data.height - data.card.height(), image = data.Duke)
    #     elif card == "Assasin":
    #         canvas.create_image(data.width/4, data.height - data.card.height(), image = data.Assasin)
    #     elif card == "Ambassador":
    #         canvas.create_image(data.width/4, data.height - data.card.height(), image = data.Ambassador)
    #     elif card == "Contessa":
    #         canvas.create_image(data.width/4, data.height - data.card.height(), image = data.card)
    #     else:
    #         canvas.create_image(data.width/4, data.height - data.card.height(), image = data.Captain)
            
    if data.numPlayers == 4:
        canvas.create_image(data.width/4, data.height- data.card.height(), image = data.CoupBack)
        canvas.create_image(data.width/4, data.card.height()//2, image = data.CoupBack)
        canvas.create_image(3*data.width/4, data.height- data.card.height(), image = data.CoupBack)
        canvas.create_image(3*data.width/4, data.card.height()//2, image = data.CoupBack)
        drawShownCardsOnline(canvas,data)
    
    gameState = parseGameState(data.gameState)
    currPlayer = gameState.pop()
    myNumber = int(data.ID[-1])
    myHand = data.handState[myNumber]
    for i in range(myNumber):
        temp = gameState.pop(0)
        gameState.append(temp)
    currPlayer = (currPlayer - myNumber) % 4
    if data.ID == "Player0":
        data.shownCards = data.newGame.shownCards
    data.isAlive = gameState[0]["Alive"]
    #drawShownCardsOnline(canvas, data)
    if gameState[0]["Alive"] == "True":
        canvas.create_text(data.width//4, data.height//4 - 30, text = data.text, fill = "LightGreen", font = "Helvetica 26")
        canvas.create_text(data.width//4, data.height//4 - 60, text = "Coins: " + str(gameState[0]["Coins"]), fill = "Yellow", font = "Helvetica 26")
        canvas.create_text(data.width//4, data.height//4 - 90, text = "Cards: " + str(myHand), fill = "Yellow", font = "Helvetica 26")
        # drawShownCardsOnline(canvas, data)
        data.decisionReq.place(x=data.width//4, y=data.height//4, anchor="center")
    else:
        data.decisionReq.destroy()
        canvas.create_text(data.width//4, data.height//4 - 90, text = "Dead", fill = "Red", font = "Helvetica 26")
    if gameState[1]["Alive"] == "True":
        if currPlayer == 1:
            canvas.create_text(3*data.width//4, data.height//4 - 30, text = "Current Mover", fill = "LightGreen", font = "Helvetica 26")
        canvas.create_text(3*data.width//4, data.height//4 - 60, text = "Coins: " + str(gameState[1]["Coins"]), fill = "Yellow", font = "Helvetica 26")
        # drawShownCardsOnline(canvas, data)
        #canvas.create_text(3*data.width//4, data.height//4 - 90, text = "Cards: " + str(data.Player1.hand), fill = "Yellow", font = "Helvetica 26")
    else:
        canvas.create_text(3*data.width//4, data.height//4 - 90, text = "Dead", fill = "Red", font = "Helvetica 26")
    if gameState[2]["Alive"] == "True":
        if currPlayer == 2:
            canvas.create_text(data.width//4, 3*data.height//4 - 30, text = "Current Mover", fill = "LightGreen", font = "Helvetica 26")
        canvas.create_text(data.width//4, 3*data.height//4 - 60, text = "Coins: " + str(gameState[2]["Coins"]), fill = "Yellow", font = "Helvetica 26")
        #canvas.create_text(data.width//4, 3*data.height//4 - 90, text = "Cards: " + str(data.Player2.hand), fill = "Yellow", font = "Helvetica 26")
    else:
        canvas.create_text(data.width//4, 3*data.height//4 - 90, text = "Dead", fill = "Red", font = "Helvetica 26")
    if gameState[3]["Alive"] == "True":
        if currPlayer == 3:
            canvas.create_text(3*data.width//4, 3*data.height//4 - 30, text = "Current Mover", fill = "LightGreen", font = "Helvetica 26")
        canvas.create_text(3*data.width//4, 3*data.height//4 - 60, text = "Coins: " + str(gameState[3]["Coins"]), fill = "Yellow", font = "Helvetica 26")
        #canvas.create_text(3*data.width//4, 3*data.height//4 - 90, text = "Cards: " + str(data.Player3.hand), fill = "Yellow", font = "Helvetica 26")
    else:
        canvas.create_text(3*data.width//4, 3*data.height//4 - 90, text = "Dead", fill = "Red", font = "Helvetica 26")
    canvas.create_text(data.width//2, data.height//2, text = "Shown Cards: " + str(data.shownCards), fill = "White", font = "Helvetica 16")
    #drawShownCards(canvas, data)

def drawShownCards(canvas, data):
    x0 , y0  = 200, data.height/2 - 75 
    for card in data.newGame.shownCards:
        if card == "Duke":
            canvas.create_image(x0, y0, image = data.DukeGame2)
        elif card == "Contessa":
            canvas.create_image(x0, y0, image = data.ContessaGame2)
        elif card == "Captain":
            canvas.create_image(x0, y0, image = data.CaptainGame2)
        elif card == "Ambassador":
            canvas.create_image(x0, y0, image = data.AmbassadorGame2)
        elif card == "Assasin":
            canvas.create_image(x0, y0, image = data.AssasinGame2)
        
        x0 += 100

def drawShownCardsOnline(canvas, data):
    x0 , y0  = 200, data.height/2 - 75 
    for card in data.shownCards:
        if card == "Duke":
            canvas.create_image(x0, y0, image = data.DukeGame2)
        elif card == "Contessa":
            canvas.create_image(x0, y0, image = data.ContessaGame2)
        elif card == "Captain":
            canvas.create_image(x0, y0, image = data.CaptainGame2)
        elif card == "Ambassador":
            canvas.create_image(x0, y0, image = data.AmbassadorGame2)
        elif card == "Assasin":
            canvas.create_image(x0, y0, image = data.AssasinGame2)
        
        x0 += 100
    
def drawGame(canvas, data):
    # data.width/4 - 150, data.DukeGame.height()//2 + 50
   
    if len(data.Player0.hand) == 2:
        count = 0 
        for card in data.Player0.hand:
            if count == 0:
                if card == "Duke":
                    canvas.create_image(data.width/4 - 150, data.DukeGame.height()//2 + 50, image = data.DukeGame)
                elif card == "Assasin":
                    canvas.create_image(data.width/4 - 150, data.DukeGame.height()//2 + 50, image = data.AssasinGame)
                elif card == "Contessa":
                    canvas.create_image(data.width/4 - 150 , data.ContessaGame.height()//2 + 50, image = data.ContessaGame)
                #canvas.create_image()
                elif card == "Ambassador":
                    canvas.create_image(data.width/4 - 150, data.ContessaGame.height()//2 + 50, image = data.AmbassadorGame)
                elif card == "Captain":
                    canvas.create_image(data.width/4 - 150, data.CaptainGame.height()//2 + 50, image = data.CaptainGame)
            if count == 1:
                if card == "Duke":
                    canvas.create_image(data.width/4 - 25, data.DukeGame.height()//2 + 50, image = data.DukeGame)
                elif card == "Assasin":
                    canvas.create_image(data.width/4 - 25, data.DukeGame.height()//2 + 50, image = data.AssasinGame)
                elif card == "Contessa":
                    canvas.create_image(data.width/4 - 25, data.ContessaGame.height()//2 + 50, image = data.ContessaGame)
                #canvas.create_image()
                elif card == "Ambassador":
                    canvas.create_image(data.width/4 - 25, data.ContessaGame.height()//2 + 50, image = data.AmbassadorGame)
                elif card == "Captain":
                    canvas.create_image(data.width/4 - 25, data.CaptainGame.height()//2 + 50, image = data.CaptainGame)
            count += 1
    elif len(data.Player0.hand) == 1:
        card = data.Player0.hand[0]
        if card == "Duke":
            canvas.create_image(data.width/4 - 77.5, data.DukeGame.height()//2 + 50, image = data.DukeGame)
        elif card == "Assasin":
            canvas.create_image(data.width/4 - 77.5, data.DukeGame.height()//2 + 50, image = data.AssasinGame)
        elif card == "Contessa":
            canvas.create_image(data.width/4 - 77.5, data.ContessaGame.height()//2 + 50, image = data.ContessaGame)
        elif card == "Ambassador":
            canvas.create_image(data.width/4 - 77.5, data.ContessaGame.height()//2 + 50, image = data.AmbassadorGame)
        elif card == "Captain":
            canvas.create_image(data.width/4 - 77.5, data.CaptainGame.height()//2 + 50, image = data.CaptainGame)


################ Local Multiplayer     
def localMultiplayerRedrawAll(canvas, data):
    # Need to draw both cards 
    #canvas.create_image(data.width/2, data.height/2, image = data.BackGround)
    #canvas.create_rectangle(0,0,1000,800, fill = "tomato2")
    canvas.create_image(425,500, image = data.castle)
    drawScrollBar(canvas, data)
    
    if data.Player0.isAlive:
        drawGame(canvas, data)
        canvas.create_text(data.width//4 - 85, data.height//4 - 30, text = data.text, fill = "NavajoWhite", font = "Helvetica 20")
        canvas.create_text(data.width//4 - 85, data.height//4 - 60, text = "Coins: " + str(data.Player0.coins), fill = "White", font = "Helvetica 26", justify="center")
        data.decisionReq.place(x=data.width//4 - 85, y=data.height//4 + 20, anchor="center")
    else:
        data.decisionReq.destroy()
        
    if data.Player1.isAlive:
        if len(data.Player1.hand) == 2:
            canvas.create_image(3 * data.width/4 - 150, data.DukeGame.height()//2 + 50, image = data.CoupBack)
            canvas.create_image(3 * data.width/4 - 25, data.DukeGame.height()//2 + 50, image = data.CoupBack)
            pass
        
        elif len(data.Player1.hand) == 1:
             canvas.create_image(3 * data.width/4 - 75, data.DukeGame.height()//2 + 50, image = data.CoupBack)
        canvas.create_rectangle(3*data.width//4 - 160, data.height//4 - 90, 3*data.width//4 - 10, data.height//4, fill = "Black", outline = "White", width = 4)
        if data.currPlayer == data.Player1:
            canvas.create_text(3*data.width//4 - 85, data.height//4 - 30, text = "Current Mover", fill = "NavajoWhite", font = "Helvetica 20")
        canvas.create_text(3*data.width//4 - 85, data.height//4 - 60, text = "Coins: " + str(data.Player1.coins), fill = "White", font = "Helvetica 26")
        
    if data.Player2.isAlive:
        if len(data.Player2.hand) == 2:
            canvas.create_image(data.width/4 - 150, data.height - data.DukeGame.height() - 100, image = data.CoupBack)
            canvas.create_image(data.width/4 - 25, data.height - data.CoupBack.height() - 100, image = data.CoupBack)
        elif len(data.Player2.hand) == 1:
             canvas.create_image(data.width/4 - 75, data.height - data.CoupBack.height() - 100 , image = data.CoupBack)
        canvas.create_rectangle(data.width//4 - 160, 3*data.height//4 - 90, data.width//4 - 10, 3*data.height//4, fill = "Black", outline = "White", width = 4)
        if data.currPlayer == data.Player2:
            canvas.create_text(data.width//4 - 85, 3*data.height//4 - 30, text = "Current Mover", fill = "NavajoWhite", font = "Helvetica 20")
        canvas.create_text(data.width//4 - 85, 3*data.height//4 - 60, text = "Coins: " + str(data.Player2.coins), fill = "White", font = "Helvetica 26")
    
    if data.Player3.isAlive:
        if len(data.Player3.hand) == 2:
            canvas.create_image(3 * data.width/4 - 150, data.height - data.DukeGame.height() - 100 , image = data.CoupBack)
            canvas.create_image(3 * data.width/4 - 25, data.height - data.CoupBack.height() - 100, image = data.CoupBack)
        elif len(data.Player3.hand) == 1:
              canvas.create_image(3 * data.width/4 - 75, data.height - data.DukeGame.height() - 100, image = data.CoupBack)
        canvas.create_rectangle(3*data.width//4 - 160, 3*data.height//4 - 90, 3*data.width//4 - 10, 3*data.height//4, fill = "Black", outline = "White", width = 4)
        if data.currPlayer == data.Player3:
            canvas.create_text(3*data.width//4 - 85, 3*data.height//4 - 30, text = "Current Mover", fill = "NavajoWhite", font = "Helvetica 20")
        canvas.create_text(3*data.width//4 - 85, 3*data.height//4 - 60, text = "Coins: " + str(data.Player3.coins), fill = "White", font = "Helvetica 26")

    drawShownCards(canvas, data)
    
def localMultiplayerKeyPressed(event, data):
    if event.keysym == "Return":
        if data.Player0.isAlive:
            data.input = data.decisionReq.get()
            data.getDecision = StringVar()
            data.decisionReq = Entry(data.root, textvariable=data.getDecision)
            data.decisionReq.pack()

def onlineMultiplayerKeyPressed(event, data):
    if event.keysym == "Return":
        if data.ID == "True" and data.me.isAlive:
            data.input = data.decisionReq.get()
            data.getDecision = StringVar()
            data.decisionReq = Entry(data.root, textvariable=data.getDecision)
            data.decisionReq.pack()
            if data.ID != "Player0":
                data.server.send(("Input " + data.input + "\n").encode())
        elif data.isAlive == "True":
            data.input = data.decisionReq.get()
            data.getDecision = StringVar()
            data.decisionReq = Entry(data.root, textvariable=data.getDecision)
            data.decisionReq.pack()
            if data.ID != "Player0":
                data.server.send(("Input " + data.input + "\n").encode())

# use the run function as-is
###################### Setup Screen 

def setupScreenRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width, data.height, fill = "White")
    canvas.create_text(data.width/2 - 35, data.height/3, text = "Hard AI Players: ", fill = "Grey", font = "Helvetica 27")
    canvas.create_text(data.width/2 - 35, 2 * data.height/3, text = "Easy AI Players: ", fill = "Grey", font = "Helvetica 27")
    canvas.create_rectangle(70 + data.width/2, data.height/3 - 15, 85 + data.width/2, data.height/3 + 15, width = 2, fill = "White")
    canvas.create_rectangle(70 + data.width/2, 2 * data.height/3 - 15, 85 + data.width/2 , 2 * data.height/3 + 15, width = 2, fill = "White")
    canvas.create_text(77.5 + data.width/2, data.height/3, text = str(data.HardAINumber), fill = "Grey", font = "Helvetica 27")
    canvas.create_text(77.5 + data.width/2, 2 * data.height/3, text = str(data.EasyAINumber), fill = "Grey", font = "Helvetica 27")
    canvas.create_rectangle(800, 600 - 30, 900, 700 - 30, fill = "Grey")
    canvas.create_text(850, 650 - 30, text = "GO!", fill = "White", anchor = "center", font = "Helvetica 27")
    
def setupScreenMousePressed(event, data):
    if event.x in range(800, 900) and event.y in range(570, 670):
        data.mode = "LocalMultiplayer"
    pass 
        
####################################
# 112 Run Function
def run(width=300, height=300, serverMsg = None, server = None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server 
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    data.root = root 
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    data.canvas = canvas 
    init(data)
    # create the root and the canvas
    # set up events
    ## Card Pictures 
    #image = Image.open("Duke.gif")
    Duke = PhotoImage(file = "Duke_241x385.gif")
    data.Duke = Duke
    DukeGame = PhotoImage(file = "Duke_125x125.gif")
    data.DukeGame = DukeGame 
    Assasin = PhotoImage(file = "Assasin__241x385.gif")
    data.Assasin = Assasin 
    Captain = PhotoImage(file = "Captain__241x385.gif")
    data.Captain = Captain 
    Ambassador = PhotoImage(file = "Ambassador__241x385.gif")
    data.Ambassador = Ambassador 
    Contessa = PhotoImage(file = "Contessa125x125.gif")
    data.Contessa = Contessa 
    card = PhotoImage(file = "card.gif")
    data.card = card
    BackGround = PhotoImage(file = "BackGround1_1000x800.gif")
    data.BackGround = BackGround 
    RulesScreenBackGround = PhotoImage(file = "GrayBubbles_1000x800.gif")
    data.RulesBackground = RulesScreenBackGround 
    CoupBackGround = PhotoImage(file = "Coupbackground .gif")
    data.startScreenBackGround = CoupBackGround
    Castle = PhotoImage(file = "CastleBackground.gif")
    data.castle = Castle
    # data.EndBackGround = EndBackGround 
    ## https://www.google.com/search?biw=1254&bih=639&tbm=isch&sa=1&ei=z0vrWt7wIdLn_Qad0pXwCA&q=coup+cards&oq=coup+cards&gs_l=psy-ab.3..0l10.1156.3397.0.3440.11.11.0.0.0.0.73.591.10.10.0....0...1c.1.64.psy-ab..1.10.590...0i67k1j0i8i30k1j0i10k1.0.kWGZDNbNrp0#imgrc=scqCZZxwTPXiKM:
    AssasinGame = PhotoImage(file = "Assasin2.gif")
    data.AssasinGame = AssasinGame 
    DukeGame = PhotoImage(file = "Duke2.gif")
    data.DukeGame = DukeGame 
    AmbassadorGame = PhotoImage(file = "Ambassador2.gif")
    data.AmbassadorGame = AmbassadorGame 
    ContessaGame = PhotoImage(file = "Contessa2.gif")
    data.ContessaGame = ContessaGame 
    CaptainGame = PhotoImage(file = "Captain2.gif")
    data.CaptainGame = CaptainGame
    CoupBack = PhotoImage(file = "CoupBack.gif")
    data.CoupBack = CoupBack
    DukeGame2 = PhotoImage(file = "finalDuke.gif")
    data.DukeGame2 = DukeGame2 
    AmbassadorGame2 = PhotoImage(file = "finalAmbassador.gif")
    data.AmbassadorGame2 = AmbassadorGame2
    ContessaGame2 = PhotoImage(file = "finalContessa.gif")
    data.ContessaGame2 = ContessaGame2 
    AssasinGame2 = PhotoImage(file = "finalAssasin.gif")
    data.AssasinGame2 = AssasinGame2 
    CaptainGame2 = PhotoImage(file = "finalCaptain.gif")
    data.CaptainGame2 = CaptainGame2
    CoupRules = PhotoImage(file = "CoupRules .gif")
    data.CoupRules = CoupRules
    
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()


run(1000, 800, serverMsg, server)
