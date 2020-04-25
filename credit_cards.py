import sys
from random import *
import time
import os
os.system('color') # apparently this makes colors work for windows users

main = ""
cvc = ""
date = ""
margin = " "*8
seconds = ""

failure_words = ["Bollocks", "Bugger", "ffs", "Shite", "Damn", "Goddammit", "Gah", "Nope", "Boo", "Dagnabbit", "For goodness' sake", "Nuh-uh", "Nah", "Negative"]
success_words = ["Woohooo!", "No way", "PARTY!", "Hell yeah", "Well done", "Good job", "Awww yeah", "Indeed", "Hurrah", "Whoopee", "Hooray", "You're a master", "Nice", "Awesome", "Amazing", "Keep up the good work", "Keep it up"]
names = ["John Smith", "Gamithra M.", "Donald Trump", "Foo Bar", "Jane Doe", "David", "Karl Marx", "Abe Lincoln", "Elon Musk", "Steve Jobs", "S. Wozniak", "Willy Wonka", "Bill Gates", "Henry Ford"]
banks = [u'\u263B', u'\u262F', u'\u2605', u'\u2622', u'\u2665', u'\u266B', u'\u2691', u'\u2654']

# failure and success colors
fc = u"\u001b[38;5;124m"
sc = u"\u001b[38;5;76m"
cd = u"\u001b[0m" # default color
cbg = ""

def print_card():
    global main, date, cvc, cbg, cd, banks

    cl = str(16 + randint(0,5) * 36 + randint(0, 20)) # magic values to make sure the colours are on the darker side
    cbg = u"\u001b[48;5;" + cl + "m" # colored background
    ctx = u"\u001b[38;5;" + cl + "m" # colored text (for the corners)
    cch = u"\u001b[48;5;136m"
    name = names[randint(0, len(names)-1)]

    card_front = [ctx + u'\u259F' + cd + cbg +" "*26 + cd + ctx + u'\u2599' + cd, \
                  cbg + " "*24 + banks[randint(0, len(banks)-1)] + " "*3 + cd, \
                  cbg + " "*28 + cd, \
                  cbg + " "*3 + cch + " "*4 + cbg + " "*21 + cd, \
                  cbg + " "*28 + cd, \
                  cbg + "   "+ main + "      " + cd, \
                  cbg + "   "+ name + (14-len(name))*" " + date + "      " + cd, \
                  ctx + u'\u259C' + cd + cbg +" "*26 + cd + ctx + u'\u259B' + cd, \
                  ]

    card_back = [ctx + u'\u259F' + cd + cbg +" "*26 + cd + ctx + u'\u2599' + cd, \
                  cd + " "*28 + cd, \
                  cd + " "*28 + cd, \
                  cbg + " "*28 + cd, \
                  cbg + " "*3 + u"\u001b[48;5;231m" + u"\u001b[38;5;16m" + " "*8 + cvc + cbg + " "*14 + cd, \
                  cbg + " "*28 + cd, \
                  cbg + " "*28 + cd, \
                  ctx + u'\u259C' + cd + cbg +" "*26 + cd + ctx + u'\u259B' + cd, \
                  ]


    for i in range(len(card_front)):
        print(margin + card_front[i] + "   " + card_back[i])

    print("")

def ask():
    global main, date, cvc, seconds
    print(margin + "Memorize as many digits as you can!")
    print("")

    main = ""

    # add numbers that start with zero
    for i in range(4):
        main += str(randint(1000,9999))
        if i < 3: main += "-"

    cvc = str(randint(100, 999))

    expires_day = randint(1, 12)
    if expires_day < 10:
        expires_day = "0" + str(expires_day)
    date  = str(expires_day) + "/" + str(randint(20, 28))


    sys.stdout.write("\r")
    print_card()
    if seconds != "":
        for remaining in range(seconds, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write(margin + "    {:2d} seconds remaining.".format(remaining))
            sys.stdout.flush()
            time.sleep(1)
    else:
        input(margin + "Press Enter when you're done!")
    os.system('cls' if os.name == 'nt' else "printf '\033c'")



def calc_score(a, b, date=False):
    score = 0
    if date:
        if a[0:2] == b[0:2]:
            score += 1
        if a[3:5] == b[3:5]:
            score += 1
    else:
        for i in range(min(len(a), len(b))):
            if a[i] != "-" or a[i] == "/":
                if a[i] == b[i]:
                    score += 1

    return score



def success():
    global sc, cd
    return sc + success_words[randint(0, len(success_words)-1)] + "!" + cd

def failure():
    global fc, cd
    return fc + failure_words[randint(0, len(failure_words)-1)] + "!" + cd

def guess():
    global main, date, cvc, cbg, cd


    for i in range(4):
        print("")

    guess_main = input(margin + cbg + "What was the credit card number? \n" + cd + margin + "Format: xxxx-xxxx-xxxx-xxxx\n"+ margin)
    score_main = calc_score(guess_main, main)
    if guess_main == main:
        print(margin + success() + " You got it right!")
    elif score_main > 0:
        print(margin + failure() + " It was " + main + ", but you got " + str(score_main) + " digits right!")
    else:
        print(margin + failure() + " It was " + main + ".")
    print("")

    guess_cvc = input(margin + cbg + "What was the CVC?\n" + cd + margin + "Format: xxx\n"+margin)
    score_cvc = calc_score(guess_cvc, cvc)
    if guess_cvc == cvc:
        print(margin + success() + " That's correct.")
    elif score_cvc > 0:
        print(margin + failure() + " It was " + cvc + ", but you got " + str(score_cvc) + " digits right!")
    else:
        print(margin + failure() + " It was " + cvc + ".")
    print("")

    guess_date = input(margin + cbg + "What was the expiry date?\n" + cd + margin + "Format: xx/xx\n"+margin)
    score_date = calc_score(guess_date, date, date=True)
    if guess_date == date:
        print(margin + success() + " That's it.")
    elif score_date > 0:
        print(margin + failure() + " It was " + date + ", but you got " + str(score_date) + " digits right!")
    else:
        print(margin + failure() + " It was " + date + ".")

    print("")
    print(margin + u"\u001b[48;5;231m" + u"\u001b[38;5;16m" + " Score for this round: " + str(int((score_main + score_cvc + score_date)/21*100)) + "% " + cd)

    print("")
    print("")

    print(margin + "Too easy? To set a time limit, just run:\n"+margin+"'python3 credit_card.py [seconds]'!")
    print("")

    print(margin + u"\u001b[38;5;22m" + "made by @gamithra" + cd)
    play_again = input(margin + "Press Enter to play again - or 'q' to quit!")
    if play_again == "q":
        print(margin + "See you again soon :-)")
    else:
        play()


def play():
    global seconds
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    if len(sys.argv) > 1:
        seconds = int(sys.argv[1])
    for i in range(4):
        print("")

    ask()
    guess()

if __name__ ==  "__main__":
    play()


