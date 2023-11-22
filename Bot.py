from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler,MessageHandler,filters,ContextTypes
import wikipediaapi
from dotenv import load_dotenv
from const import help_menu,commands_usages
from commands.trackinsta.tracktnsta import TrackInsta
import os
import logging
import coloredlogs


load_dotenv()

# logging.basicConfig(level=logging.DEBUG)
coloredlogs.install(level='INFO', fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', colors={'DEBUG': 'green', 'INFO': 'blue', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red'})


class Bot():

    _TOKEN:Final = os.getenv("BOT_TOKEN")
    _BOT_USERNAME:Final = os.getenv("BOT_USERNAME")
    _USER_ID:Final = int(os.getenv("USER_ID"))

    def __init__(self) -> None:
        self.wiki=wikipediaapi.Wikipedia('Ada lovelace')
        self.DataPath = "/data"


    # Commands
    async def start_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        if context._user_id == self._USER_ID:
            logging.warning(f"User {context._user_id} started the bot")
            await update.message.reply_text("Hello Sir...")
        else:
            logging.warning(f"User ID {context._user_id} tried to access the bot")
            return


    async def help_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(help_menu)

    async def custom_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        await update.effective_message.reply_text(update.message.chat_id)

    async def trackinsta_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):

        if context._user_id == self._USER_ID:
            command = TrackInsta(update,context)
            await command.run()
        else:
            logging.warning(f"User ID {context._user_id} tried to access the bot")

                
                
    async def wikipedia_command(self,update:Update,context:ContextTypes.DEFAULT_TYPE):
        if context._user_id == self._USER_ID:
            query:str = " ".join(context.args)
            await update.effective_message.reply_text(f"Searching for {query}....")

            try:
                page = self.wiki.page(query)
                if page.exists():
                    result:str = page.summary[:2024] 
                    await update.message.reply_text(f"According to wikipedia {result} \n For more:{page.fullurl}")

                else:
                    await update.effective_message.reply_text("Sorry I couldn't find any info on this topic on wikipedia")
            

            except Exception as e:
                logging.error(e)
                await update.effective_message.reply_text("Sorry I couldn't find any info on this topic on wikipedia")
        
        else:
            logging.warning(f"User ID {context._user_id} tried to access the bot")



    # response
    def handel_response(self,text:str) -> str:
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



    async def error(self,update:Update,context:ContextTypes.DEFAULT_TYPE):
        logging.error(f"Update cause error {context.error}")
        logging.debug(f"Update {update} cause error {context.error}")

if __name__ == "__main__":
    logging.info("Starting the bot...")
    bot = Bot()
    App = Application.builder().token(bot._TOKEN).build()
    # App.job_queue.start()

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
    App.add_error_handler(bot.error)

    # Polls the bot
    logging.info("Polling...")
    App.run_polling(poll_interval=1)

 