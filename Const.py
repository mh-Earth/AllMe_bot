from telegram import Sticker
from typing import Final

hidden_commands = {
    "roll a dice": "Will roll a dice",
    "seehiddens": "See this menu"
}
def seeHiddens():
    return hidden_commands

respponce_key:Final = {
    # "hello":"Hi there ",
    # "hi":"Hi there ",
    # "how are you":"I am fine.Wby?",
    # "what is your name":"My name is Ada Lovelace but you can call me loveless",
    "/wiki":"/wiki <your search>",
    '/trackinsta':"/trackinsta <instagram username>"
    # hidden commands
}

help_menu:Final = """
/start - start bot
/help - open this menu
/custom - random thing will happen
/wiki - search topic from wikipedia
"""
commands_uesgs:Final = {
    "/wiki":"/wiki <your search>",
    '/trackinsta':"/trackinsta <insta profile url>"
}
