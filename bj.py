import numpy as np
from time import sleep
import os
from tqdm import tqdm
# 1 deck 52 card 4 x 13

deck = ["A♦", "A♣", "A♥", "A♠",
        "2♦", "2♣", "2♥", "2♠",
        "3♦", "3♣", "3♥", "3♠",
        "4♦", "4♣", "4♥", "4♠",
        "5♦", "5♣", "5♥", "5♠",
        "6♦", "6♣", "6♥", "6♠",
        "7♦", "7♣", "7♥", "7♠",
        "8♦", "8♣", "8♥", "8♠",
        "9♦", "9♣", "9♥", "9♠",
        "10♦", "10♣", "10♥", "10♠",
        "J♦", "J♣", "J♥", "J♠",
        "Q♦", "Q♣", "Q♥", "Q♠",
        "K♦", "K♣", "K♥", "K♠"]


hardtotal = [["H","H","H","H","H","H","H","H","H","H"],
             ["H","D","D","D","D","H","H","H","H","H"],
             ["D","D","D","D","D","D","D","D","H","H"],
             ["D","D","D","D","D","D","D","D","D","D"],
             ["H","H","S","S","S","H","H","H","H","H"],
             ["S","S","S","S","S","H","H","H","H","H"],
             ["S","S","S","S","S","H","H","H","H","H"],
             ["S","S","S","S","S","H","H","H","H","H"],
             ["S","S","S","S","S","H","H","H","H","H"],
             ["S","S","S","S","S","H","H","H","H","H"],
             ["S","S","S","S","S","S","S","S","S","S"]]

softtotal = [["H","H","H","D","D","H","H","H","H","H"],
             ["H","H","H","D","D","H","H","H","H","H"],
             ["H","H","D","D","D","H","H","H","H","H"],
             ["H","H","D","D","D","H","H","H","H","H"],
             ["H","D","D","D","D","H","H","H","H","H"],
             ["DS","DS","DS","DS","DS","S","S","H","H","H"],
             ["S","S","S","S","DS","S","S","S","S","S"],
             ["S","S","S","S","S","S","S","S","S","S"]]

splittotal = [["N","N","Y","Y","Y","Y","N","N","N","N"],
             ["N","N","Y","Y","Y","Y","N","N","N","N"],
             ["N","N","N","Y","Y","N","N","N","N","N"],
             ["N","N","N","N","N","N","N","N","N","N"],
             ["N","Y","Y","Y","Y","N","N","N","N","N"],
             ["Y","Y","Y","Y","Y","Y","N","N","N","N"],
             ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"],
             ["Y","Y","Y","Y","Y","N","Y","Y","N","N"],
             ["N","N","N","N","N","N","N","N","N","N"],
             ["Y","Y","Y","Y","Y","Y","Y","Y","Y","Y"]]
'''
H - Hit
S - Stand
D - Double if allowed, otherwise Hit
DS - Double if allowed, otherwise Stand
N - Don't Split
Y - Split
'''

finaldeck = []
playercards = []
dealercards = []
playercardsval = []
dealercardsval = [0]
numdecks = 6  # int(input()) default 6 for now
tiecount = 0
wincount = 0
losecount = 0
option = 0
defaultplayers = 0
inplay = True


def calval(cards,cardsval):  # to calculate and update the total value of the player's cards
    for c in range(len(cardsval)):  # initialise to 0 then count up
        cardsval[c] = 0
    for c in range(len(cards)):  # each player 2 cards, playercards[i][0][0]-> the first char of the 2d array
        if cards[c][0] == "A":  # for card value ace
            if len(cardsval) != 2:  # make sure val array has 2 index as ace have 2 values 1,11 -> [4]->[5,15]
                cardsval.append(cardsval[0])  # copy the first value
            cardsval[0] += 1
            cardsval[1] += 11
            if cardsval[1]==21:
                del cardsval[0]
        elif cards[c][0] == "K" or cards[c][0] == "Q" or cards[c][0] == "J":  # for card value king, queen, jack
            for x in range(len(cardsval)):  # in a case where there is ace in the deck [1,11] -> [11,21]
                cardsval[x] += 10
        else:  # for card value from 1-10 (digits)
            for x in range(len(cardsval)):  # in a case where there is ace in the deck [1,11] -> [4,14]
                cardsval[x] += int(cards[c][:-1])


def printcardval(cardsval, cards, numplayers, dcardsval, dcards):  # option 1 to show player, dealer start hand per rd
    for i in range(numplayers):
        print("Player " + str(i + 1)+": ", end="")
        for c in range(len(cards[i])):
            if c==len(cards[i])-1:  # last print number
                print(cards[i][c]+" → ",end="")
            else:
                print(cards[i][c], end=",")
        for x in range(len(cardsval[i])):
            if x==len(cardsval[i])-1:  # last print number
                print(cardsval[i][x])
            else:
                print(cardsval[i][x], end=",")
    print("Dealer: ", end="")
    for c in range(len(dcards)):
        if c == len(dcards) - 1:  # last print number
            print(dcards[c] + " → ", end="")
        else:
            print(dcards[c], end=",")
    for x in range(len(dcardsval)):
        if x == len(dcardsval) - 1:  # last print number
            print(dcardsval[x])
        else:
            print(dcardsval[x], end=",")


def printresult(cardsval, cards, numplayers, dcardsval, dcards):  # option 1 to show player, dealer final hand per rd
    global tiecount, losecount, wincount
    for i in range(numplayers):
        if dcardsval[0] > 21:
            win = True
            tie = False
        else:
            win = False
            tie = False
        if cardsval[i][0]>21:
            win = False
        print("Player " + str(i + 1)+": ", end="")
        for c in range(len(cards[i])):
            if c==len(cards[i])-1:  # last print number
                print(cards[i][c]+" → ",end="")
            else:
                print(cards[i][c], end=",")
        for x in range(len(cardsval[i])):
            if (cardsval[i][x]>dcardsval[0] and cardsval[i][x]<=21) or (dcardsval[0]>21 and cardsval[i][x]<=21):
                win = True
            if cardsval[i][x]==dcardsval[0] and cardsval[i][x]<=21:
                tie = True
            if x==len(cardsval[i])-1:  # last print number
                print(cardsval[i][x],end= " ")
            else:
                print(cardsval[i][x], end=",")
        if tie:
            print("Tie")
            tiecount += 1
        else:
            if win:
                print("Win")
                wincount += 1
            else:
                print("Lose")
                losecount += 1

    print("Dealer: ", end="")
    for c in range(len(dcards)):
        if c == len(dcards) - 1:  # last print number
            print(dcards[c] + " → ", end="")
        else:
            print(dcards[c], end=",")
    for x in range(len(dcardsval)):
        if x == len(dcardsval) - 1:  # last print number
            print(dcardsval[x])
        else:
            print(dcardsval[x], end=",")
    print("Overall: wins:" + str(wincount) + " lose:" + str(losecount) + " tie:" + str(tiecount))
    print("Win percentage: " + "{:.2f}".format(wincount / (wincount + losecount + tiecount) * 100) + "%")
    print("lose percentage: " + "{:.2f}".format(losecount / (wincount + losecount + tiecount) * 100) + "%")
    print("Tie percentage: " + "{:.2f}".format(tiecount / (wincount + losecount + tiecount) * 100) + "%")


def printpercentage(cardsval, numplayers, dcardsval):  # option 1
    global tiecount, losecount, wincount

    for i in range(numplayers):
        if dcardsval[0] > 21:
            win = True
            tie = False
        else:
            win = False
            tie = False
        if cardsval[i][0]>21:
            win = False
        for x in range(len(cardsval[i])):
            if (cardsval[i][x]>dcardsval[0] and cardsval[i][x]<=21) or (dcardsval[0]>21 and cardsval[i][x]<=21):
                win = True
            if cardsval[i][x]==dcardsval[0] and cardsval[i][x]<=21:
                tie = True
        if tie:
            tiecount += 1
        else:
            if win:
                wincount += 1
            else:
                losecount += 1
    print("Overall: wins:" + str(wincount) + " lose:" + str(losecount) + " tie:" + str(tiecount))
    print("Win percentage: " + "{:.2f}".format(wincount / (wincount + losecount + tiecount) * 100) + "%")
    print("lose percentage: " + "{:.2f}".format(losecount / (wincount + losecount + tiecount) * 100) + "%")
    print("Tie percentage: " + "{:.2f}".format(tiecount / (wincount + losecount + tiecount) * 100) + "%")


def printfinal(cardsval, numplayers, dcardsval): # when reach goal every player cardval<=21
    global tiecount, losecount, wincount
    for i in range(numplayers):
        if dcardsval[0] > 21:
            win = True
            tie = False
        else:
            win = False
            tie = False
        if cardsval[i][0]>21:
            win = False
        for x in range(len(cardsval[i])):
            if (cardsval[i][x]>dcardsval[0] and cardsval[i][x]<=21) or (dcardsval[0]>21 and cardsval[i][x]<=21):
                win = True
            if cardsval[i][x]==dcardsval[0] and cardsval[i][x]<=21:
                tie = True

        if tie:
            tiecount += 1
        else:
            if win:
                wincount += 1
            else:
                losecount += 1


def checkace(cards):
    for i in range(len(cards)):
        if cards[i][0] == "A":
            return True
    return False


def checkpair(cards):
    if len(cards)!=2:
        return False
    if cards[0][0]!= cards[1][0]:
        return False
    return True


def dcardindex(card):
    if card == "A":
        return 11
    elif card == "K" or card == "Q" or card == "J":
        return 10
    else:
        return int(card)


def choice(cards, cardsval, dcard, deck):
    global numplayers
    for c in range(numplayers):
        while True:
            pair = checkpair(cards[c])
            if pair:  # player's 2 cards with pairs
                dval = dcardindex(dcard[0][:-1])
                cval = round(cardsval[c][-1]/2)
                decision = splittotal[cval-2][dval-2]
                if decision == "Y":  # if split
                    newhand = [cards[c][-1]]  # create an array for additional stack while appending the recent card
                    del cards[c][-1]
                    newhand.append(deck[0])  # add a card from the deck to the new hand
                    del deck[0]
                    # as cards[] contain all the players cards
                    # insert the new hand at the position of the current hand, pushing the current hand behind
                    cards.insert(c,newhand)
                    cardsval.insert(c,[0])
                    calval(cards[c], cardsval[c])  # update new cardsval[c] value
                    cards[c+1].append(deck[0])  # add a card from the deck to the hand
                    del deck[0]
                    calval(cards[c+1], cardsval[c+1])  # update new cardsval[c+1] value
                    numplayers +=1   # since there is additional hand, assumed it as an additional player
            soft = checkace(cards[c])
            if soft:  # player's cards with ace
                # reach bj soft (cardsval[c][-1]==21) or bust/ace hard (cardsval[c][0]>10) just stand
                if cardsval[c][-1]==21 or cardsval[c][0]>10:
                    break
                dval = dcardindex(dcard[0][:-1])  # get index of dealercard
                cval = cardsval[c][0]  # get index of playercard
                decision = softtotal[cval-3][dval-2]
                if decision == "H":  # soft hit
                    cards[c].append(deck[0])
                    calval(cards[c],cardsval[c])
                    del deck[0]
                if decision == "D":  # double if allowed, otherwise hit
                    if len(cards[c]) == 2:  # double
                        cards[c].append(deck[0])
                        calval(cards[c],cardsval[c])
                        del deck[0]
                        break
                    else:  # hit
                        cards[c].append(deck[0])
                        calval(cards[c],cardsval[c])
                        del deck[0]
                if decision == "DS":  # double if allowed, otherwise stand
                    if len(cards[c]) == 2:  # double
                        cards[c].append(deck[0])
                        calval(cards[c],cardsval[c])
                        del deck[0]
                    break
                if decision == "S":  # stay
                    break
            else:
                if cardsval[c][-1]>17:  # card value bigger than 17 stand
                    break
                dval = dcardindex(dcard[0][:-1])
                if cardsval[c][0]<8:
                    cval = 8
                else:
                    cval = cardsval[c][0]
                decision = hardtotal[cval-8][dval-2]  ##!!!!
                if decision == "H":
                    cards[c].append(deck[0])
                    calval(cards[c],cardsval[c])
                    del deck[0]
                if decision == "D":  # double if allowed, otherwise hit
                    if len(cards[c]) == 2: # double
                        cards[c].append(deck[0])
                        calval(cards[c],cardsval[c])
                        del deck[0]
                        break
                    else:  # hit
                        cards[c].append(deck[0])
                        calval(cards[c],cardsval[c])
                        del deck[0]
                if decision == "S":
                    #print("Stay")
                    break

def dealerturn(card,cardval,deck):
    while True:
        if cardval[0]>16:  # dealer stand at 17
            break
        card.append(deck[0])
        calval(card,cardval)
        del deck[0]

def printprogress(current,total):
    percent = 100 * (current/float(total))
    print("Games Completed: |" + "█" * int(percent/2) + " " * int((100 - percent)/2) + "|", end="")  # '█' - hold alt and press 219 on numpad: /2 is used to reduce size
    print(str(current) + "/" + str(total))


while inplay:
    print("Welcome to the Black Jack simulator")
    print("Option 1: Full details with player and dealer hands and result after each round")
    print("Option 2: Full result after each round")
    print("Option 3: Final result")
    while option<1 or option>3:
        try:
            option = int(input("Your option:"))
        except Exception as e:
            print("Error")
    while defaultplayers<1 or defaultplayers>7:
        try:
            defaultplayers = int(input("Number of Players:"))
        except Exception as e:
            print("Error")

    numgames = int(input("How Many Games:"))
    final = False

    #pbar = tqdm(desc="Games Completed",total=numgames, ncols=70, leave=False) if numgames>999 else numgames  # tqdm(range(numtrial), ncols=70)<- did not used this as it affects option 1/2
    for n in tqdm(range(numgames), desc="Games completed", ncols=80):
        numplayers = defaultplayers
        playercards.clear()
        dealercards.clear()
        playercardsval.clear()
        dealercardsval = [0]

        if len(finaldeck)<(numdecks*52/2):  # if current deck contains less than half of original reshuffle deck
            finaldeck.clear()
            for i in range(numdecks):  # compile num of decks
                finaldeck.extend(deck)
            np.random.shuffle(finaldeck)  # shuffle pile

        for i in range(numplayers):  # initialise player arrays
            playercards.append([])
            playercardsval.append([0])
        for i in range(2):  # serve the cards
            for p in range(numplayers):
                playercards[p].append(finaldeck[0])
                del finaldeck[0]
            dealercards.append(finaldeck[0])
            del finaldeck[0]

        for i in range(numplayers):
            calval(playercards[i], playercardsval[i])  # calculate and update player card value
        calval(dealercards, dealercardsval)  # calculate and update dealer card value

        match option:
            case 1:
                # print()
                sleep(0.1)  # !!!! important so that progress bar is updated and shown before clear screen
                os.system('cls')
                print("Round " + str(n + 1))
                print("Start Hand")
                printcardval(playercardsval,playercards,numplayers,dealercardsval,dealercards)
                print()
                print("Result")
            case 2:
                sleep(0.1)  # !!!! important so that progress bar is updated and shown before clear screen
                os.system('cls')
                print("Round "+str(n+1)+" Result")

        choice(playercards,playercardsval,dealercards,finaldeck)
        if dealercardsval[0]<17 or dealercardsval[-1]!=21:
            dealerturn(dealercards,dealercardsval,finaldeck)
        match option:
            case 1:
                printresult(playercardsval,playercards,numplayers,dealercardsval,dealercards)
                #printprogress(n+1, numgames)

            case 2:
                printpercentage(playercardsval,numplayers,dealercardsval)
                #printprogress(n+1, numgames)

            case 3:
                final = True
                printfinal(playercardsval,numplayers,dealercardsval)
    if final:
        print()
        print("Overall: wins:" + str(wincount) + " lose:" + str(losecount) + " tie:" + str(tiecount))
        print("Win percentage: " + "{:.2f}".format(wincount / (wincount + losecount + tiecount) * 100) + "%")
        print("lose percentage: " + "{:.2f}".format(losecount / (wincount + losecount + tiecount) * 100) + "%")
        print("Tie percentage: " + "{:.2f}".format(tiecount / (wincount + losecount + tiecount) * 100) + "%")

    if input("Try again? y/n:").lower() == "y":
        inplay = True
        os.system('cls')
        option = 0
        defaultplayers = 0
    else:
        inplay = False