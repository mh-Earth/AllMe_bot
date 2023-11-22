from telegram.ext import Updater,ContextTypes,CallbackContext
from os import getenv
from dotenv import load_dotenv
from CommandMaker.Base import CommandBase
import logging

class Loadalljobs(CommandBase):
    def __init__(self,update:Updater,context:ContextTypes.DEFAULT_TYPE) -> None:
        self.update = update
        self.cxt = context
        self.admins = [6540965739]

        ...
    
    async def run(self):
        if self.cxt._user_id in self.admins:
            await self.update.effective_message.reply_text('loading jos..')
            return
        
        await self.update.effective_message.reply_text('I do not understand what you wrote...')
        logging.warning(f"User ID {self.cxt._user_id} attempted to access the admin command. Command:{self.update.message.text}")


