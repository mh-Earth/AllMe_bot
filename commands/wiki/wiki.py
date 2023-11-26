from modules.CommandMaker.Base import CommandBase
import wikipediaapi
import logging


class Wiki(CommandBase):
    def __init__(self,update,context) -> None:
        self.update = update
        self.context = context
        self.wikipedia = wikipediaapi.Wikipedia('All Me bot')

    async def run(self):
    
        query:str = " ".join(self.context.args)
        await self.update.effective_message.reply_text(f"Searching for {query}....")

        try:
            page = self.wikipedia.page(query)
            if page.exists():
                result:str = page.summary[:2024] 
                await self.update.message.reply_text(f"According to wikipedia {result} \n For more:{page.fullurl}")

            else:
                await self.update.effective_message.reply_text("Sorry I couldn't find any info on this topic on wikipedia")
        

        except Exception as e:
            logging.error(e)
            await self.update.effective_message.reply_text("Sorry I couldn't find any info on this topic on wikipedia")
