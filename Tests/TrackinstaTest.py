import pyautogui as pg
from typing import Final
# from ..configurations.settings import INSTA_USERNAME

STATUS:Final="status"
INITIAL:Final="initial"
HISTORY:Final="history"
REMOVE:Final="remove"
CHECKOUT:Final="checkout"
LOG:Final="log"
OPTIONS:Final="options?"
ALL:Final="all?"
HELP:Final="help?"

options = [


    STATUS,INITIAL,HISTORY,CHECKOUT,LOG,OPTIONS,ALL,HELP,REMOVE
]

login_req = ["",STATUS,INITIAL,HISTORY,LOG,CHECKOUT,REMOVE,CHECKOUT]
not_login_req = [HELP,OPTIONS,ALL]
test_user = 'emi_lyitachi'
command = "/trackinsta"

from time import sleep

def openTelegram():
    sleep(2)
    telegramIcon = pg.locateCenterOnScreen('Tests\\images\\telegram_logo.PNG',confidence=.7)
    pg.click(telegramIcon)
    sleep(1)
    bot_account = pg.locateCenterOnScreen('Tests\\images\\bot_account.PNG',confidence=.7)
    pg.click(bot_account)
    print(bot_account)
    sleep(.5)
    textarea = pg.locateCenterOnScreen('Tests\\images\\textarea.PNG',confidence=.7)
    pg.click(textarea)
    sleep(.5)
def login_req_test():
    for options in login_req:
        pg.write(f"{command} {test_user} {options}")
        pg.press('enter')
        # sleep(1)
        

def no_login_req_test():
    for options in not_login_req:
        pg.write(f"{command} {options}")
        pg.press('enter')
        # sleep(1)

openTelegram()
login_req_test()
no_login_req_test()

# '''



# '''



