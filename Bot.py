from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler,MessageHandler,filters,ContextTypes
import wikipediaapi
from dotenv import load_dotenv
from Const import help_menu,commands_uesgs
from modules.trackinsta.tracktnsta import Trackinsta
import os
load_dotenv()


class Bot():

    TOKEN:Final = os.getenv("BOT_TOKEN")
    BOT_USERNAME:Final = os.getenv("BOT_USERNAME")
    USER_ID:Final = int(os.getenv("USER_ID"))

    def __init__(self) -> None:
        self.wiki=wikipediaapi.Wikipedia('Ada lovelace')
        self.DataPath = "/data"


    # Commands
    async def start_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        if context._user_id == self.USER_ID:
            # return
            await update.message.reply_text("Hello Sir...")
        else:
            return


    async def help_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(help_menu)

    async def custom_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):
        print(type(context._user_id))
        await update.effective_message.reply_text(update.message.chat_id)

    async def trackinsta_command(self,update:Update, context:ContextTypes.DEFAULT_TYPE):

        if context._user_id == self.USER_ID:
            await Trackinsta(update,context)

                
                
    async def wikipedia_command(self,update:Update,context:ContextTypes.DEFAULT_TYPE):
        if context._user_id == self.USER_ID:
            query:str = " ".join(context.args)
            await update.effective_message.reply_text(f"Searching for {query}....")

            try:
                page = self.wiki.page(query)
                if page.exists():
                    result:str = page.summary[:2024] 
                    await update.message.reply_text(f"Accodding to wikipedia {result} \n For more:{page.fullurl}")

                else:
                    await update.effective_message.reply_text("Sorry I couldn't find any info on this toopic on wikipedia")
            

            except Exception as e:
                print(e)
                await update.effective_message.reply_text("Sorry I couldn't find any info on this topic on wikipedia")


    # response
    def handel_response(self,text:str) -> str:
        processed:str = text.lower()
        # print(processed)

        if processed in commands_uesgs:
            return commands_uesgs[processed]
        else:
            return "I do not understand what you wrote..."

    async def handel_message(self,update:Update , context:ContextTypes.DEFAULT_TYPE):
        message_type:str = update.message.chat.type
        text : str = update.message.text

        print(f"User ({update.message.chat.id} in {message_type} : {text})")

        if message_type == "group":
            return
        
        else:
            response= self.handel_response(text)
        try:

            # if its a normal message not a special command
            await update.message.reply_text(response)
        except Exception:
            # if its a spicial command
            await response(update)



    async def error(self,update:Update,context:ContextTypes.DEFAULT_TYPE):
        print(f"Update {update} cause error {context.error}")

if __name__ == "__main__":
    print("Starting the bot...")
    bot = Bot()
    App = Application.builder().token(bot.TOKEN).build()

    # commands
    
    App.add_handler(CommandHandler('start',bot.start_command))
    App.add_handler(CommandHandler('help',bot.help_command))
    App.add_handler(CommandHandler('custom',bot.custom_command))
    # updater command
    App.add_handler(CommandHandler('wiki',bot.wikipedia_command,has_args=True))
    App.add_handler(CommandHandler('trackinsta',bot.trackinsta_command,has_args=True))

    # Messages
    App.add_handler(MessageHandler(filters.TEXT,bot.handel_message))

    # Error
    App.add_error_handler(bot.error)

    # Polls the bot
    print("Polling...")
    App.run_polling(poll_interval=1)

