from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler,MessageHandler,filters,ContextTypes
from const import help_menu,commands_usages
from commands.trackinsta.tracktnsta import TrackInsta
from commands.wiki.wiki import Wiki
import logging
import coloredlogs
from utils.decorators import admin_only,indev,beta
from configurations.settings import BOT_USERNAME,LOGGING_LEVEL,BOT_TOKEN

# logging.basicConfig(level=logging.DEBUG)
coloredlogs.install(level=LOGGING_LEVEL.upper(), fmt='%(asctime)s [%(funcName)s] [%(levelname)s]  %(message)s', datefmt='%Y-%m-%d %H:%M:%S', colors={'DEBUG': 'green', 'INFO': 'blue', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red'})
logging.getLogger('httpx').setLevel(logging.ERROR)


class Main():

    _TOKEN:Final = BOT_TOKEN

    @staticmethod
    # @indev
    async def start_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
        logging.warning(f"User {update.effective_user.first_name} started the bot")
        await update.message.reply_text("Hello Sir...")

    @indev
    async def help_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(help_menu)

    @staticmethod
    @admin_only
    async def custom_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
        await update.effective_message.reply_text(f'{context.chat_data}')

    @staticmethod
    @beta
    async def trackinsta_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
        command = TrackInsta(update,context)
        await command.run()

    @staticmethod
    async def wikipedia_command(update:Update,context:ContextTypes.DEFAULT_TYPE):
        wiki = Wiki(update,context)
        await wiki.run()
    
    # response

    @staticmethod
    def handel_response(text:str) -> str:
        processed:str = text.lower()
        # print(processed)

        if processed in commands_usages:
            return commands_usages[processed]
        else:
            return "I do not understand what you wrote..."


    async def handel_message(self,update:Update , context:ContextTypes.DEFAULT_TYPE):
        message_type:str = update.message.chat.type
        text : str = update.message.text

        logging.info(f"User ({update.message.chat.id} in {message_type}) : {text}")

        if message_type == "group":
            return
        
        else:
            response= self.handel_response(text)
        try:

            # if its a normal message not a special command
            await update.message.reply_text(response)
        except Exception:
            # if its a spacial command
            await response(update)



    # @staticmethod
    # async def error(update:Update,context:ContextTypes.DEFAULT_TYPE):
    #     # await update.effective_message.reply_text(f"Update cause error {context.error}")
    #     logging.error(f"Update cause error {context.error}")
    #     logging.debug(f"Update {update} cause error {context.error}")

if __name__ == "__main__":
    logging.info("Starting the bot...")
    bot = Main()
    App = Application.builder().token(bot._TOKEN).build()

    # commands
    
    App.add_handler(CommandHandler('start',bot.start_command))
    App.add_handler(CommandHandler('help',bot.help_command))
    App.add_handler(CommandHandler('custom',bot.custom_command))
    # updater command
    App.add_handler(CommandHandler('wiki',bot.wikipedia_command,has_args=True,))
    App.add_handler(CommandHandler('trackinsta',bot.trackinsta_command,has_args=True))

    # Messages
    App.add_handler(MessageHandler(filters.TEXT,bot.handel_message))

    # Error
    # App.add_error_handler(bot.error)


    # Polls the bot
    logging.info("Polling...")
    App.run_polling(poll_interval=1)

 