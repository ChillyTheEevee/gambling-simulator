import random

# Da wheel
wheel = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
         21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 0, "00"]

money = 500

print("Roulette!")
print("Place bets on a color or on numbers to win money based off the odds")


# Betting loop
while money > 0:
    print(f"Current money: ${money}")

    # Input for bet size
    bet = int(input("Enter your bet size: "))

    if bet > money:
        print("You don't have enough funds for this bet.")
        continue

    # Input for bet type
    bet_type = input("Do you want to bet on 'number' or 'color'? ").lower()

    if bet_type == 'number':
        bet_numbers_input = input("Enter numbers (comma-separated): ")
        bet_numbers = [int(num.strip()) for num in bet_numbers_input.split(",")]
    elif bet_type == 'color':
        bet_color = input("Enter a color ('red', 'black', or 'green'): ").lower()
        if bet_color not in ['red', 'black', 'green']:
            print("Please enter 'red', 'black', or 'green'.")
            continue
        bet_numbers = []
    else:
        print("Choose 'number' or 'color'.")
        continue

    # Spin the wheel
    result = random.choice(wheel)

    if result in [0, "00"]:
        result_color = "green"
    elif result % 2 == 1:
        result_color = "red"
    else:
        result_color = "black"

    print(f"\nThe wheel landed on: {result} ({result_color})")

    # number betting results
    winnings = 0
    if bet_type == 'number':
        if result in bet_numbers:
            payout_odds = (len(bet_numbers) / 38)
            winnings = bet - (bet * (payout_odds))
            winnings = round(winnings)
            print(f"Congratulations! You won ${winnings} on number {result}.")
        else:
            print(f"L, {result}")

    # color betting results
    if bet_type == 'color':
        if bet_color == result_color:
            winnings = bet
            print(f"Congratulations! You won ${winnings} on {result_color}.")
        else:
            print(f"L, {result_color}")

    # 0 or 00 payout
    if result in [0, "00"]:
        winnings = bet * 36
        winnings = round(winnings)
        print(f"Congratulations! You won ${winnings} on green.")

    if winnings > 0:
        money += (winnings * .95)
    else:
        money -= bet

    print(f"Remaining money: ${money}\n")

    # See if game continues
    if money <= 0:
        print("You're out of money!")
        break
    keep_playing = input("Do you want to keep playing? (yes/no): ").lower()
    if keep_playing != "yes":
        print("Thanks for playing!")
        break
