from sys import exit

def main():

    change = getMoney()

    coins(change)


def getMoney():
    while True:
        money = input("Number: ")
        try:
            money = float(money)
            if (money > 0):
                break
        except:
            continue
    money = round(money * 100)
    return money


def coins(money):

    # Number of 25 cent coins required
    cents25 = money // 25
    money -= (cents25 * 25)

    # Number of 10 cent coins required
    cents10 = money // 10
    money -= (cents10 * 10)

    # Number of 5 cent coins required
    cents5 = money // 5
    money -= (cents5 * 5)

    # Number of 1 cent coins required
    cents1 = money

    total = cents25 + cents10 + cents5 + cents1
    print(f"{total}")


main()