# blackjack
import random

# how to make this - ?
# have list of numbers from 1 to 13
# 1 is ace, 11 is jack, 12 is queen, 13 is king
# probably use dictionary ? could use that
# variable for dealer, variable for player.
# choose two random cards from for dealer, assign two as variable list. print first item in list
# to let user know what that value is.
# choose two random cards for user, assign to list
# print both of user's cards. prompt them to hit or stand.
# if user hits, add anothe random value. check if ov er 21
# when stand, then show dealer's cards and in real time check if 16 or under. if is, take hit
# find total values, add numbers if over 21 then bust.
# if value is 1 (ace), see what total value of cards is if 11 is added total, and what total is if 1.
# if total with 11 is over 21, then add 1 to total. if not, then add 11
# ask if they want to play again yes or no
# put game in while true loop, to keep questions and game going.

# EDGE CASES 7 ace queen, ace 10, idk whats happening ace 7?, oh its when I get ace first. ace 9
# edge case to fix is when ace is the first one.

cards = {
    "ace": 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    "jack": 10,
    "queen": 10,
    "king": 10,
}


def aceCheck(list):
    aceTotal = 0
    for i in list:
        if i[0] != "ace":
            aceTotal += i[1]
    for i in list:
        if i[0] == "ace":
            aceTotal += 11
            if aceTotal > 21:
                aceTotal -= 10
    return aceTotal


while True:
    print("Welcome to Blackjack! When you're ready, type in play to start. If you want to leave, type exit.")
    inp = input(":")
    if inp == "exit":
        break;
    elif inp != "play":
        continue
    else:
        print("Let's get started.")

        dealerCards = [random.choice(list(cards.items())), random.choice(list(cards.items()))]
        userCards = [random.choice(list(cards.items())), random.choice(list(cards.items()))]

        dealerTotal = 0
        userTotal = 0

        print(f"The dealer's shown card is: {dealerCards[0][0]}\n")
        print(f"Your cards are: {userCards[0][0]} {userCards[1][0]}")

        while True:
            userTotal = aceCheck(userCards)
            print("\nDo you want to hit, or stand?")
            desc1 = input("Type hit or stand: ")
            if desc1 == "hit":
                userCards.append(random.choice(list(cards.items())))
                userTotal = aceCheck(userCards)
                print(f"Your cards are:")
                for i in userCards:
                    print(f"{i[0]}", end=" ")
                if userTotal > 21:
                    print("\nBust! Better luck next time.")
                    break
            elif desc1 == "stand":
                break
            else:
                print("Invalid input. Try again.")
                continue

        if userTotal > 21:
            break
        print(f"Your total is {userTotal}.")
        print("The dealer will now flip their card.")
        print(f"The dealer's cards are:")
        for i in dealerCards:
            print(f"{i[0]}", end=" ")
        dealerTotal = aceCheck(dealerCards)
        while True:
            if dealerTotal < 17:
                dealerCards.append(random.choice(list(cards.items())))
                dealerTotal = aceCheck(dealerCards)
                print("\nThe dealer hits again.")
                print(f"The dealer's cards are:")
                for i in dealerCards:
                    print(f"{i[0]}", end=" ")
                print("")
            else:
                break
        print(f"\nThe dealer's total is: {dealerTotal}")
        if dealerTotal > 21:
            print("The dealer busted! you win.")
        elif dealerTotal < userTotal:
            print("You win! you beat the dealer.")
        else:
            print("You lose, the dealer beat you :(")

        input("\nThats the game! Click enter to run the game again.")
