'''
Command : /trackinsta <instagram username> < option (optional)>

option:
    status:
    initial:
    history:
    trackinsta?:
    remove:

'''


from  CommandMaker.Base import CommandModel
from telegram.ext import ContextTypes
from telegram import Update
from .api import Insta
import logging

class TrackInsta(CommandModel):
    def __init__(self,update:Update,cxt:ContextTypes.DEFAULT_TYPE) -> None:
        self.update:Update = update
        self.cxt:ContextTypes.DEFAULT_TYPE = cxt
        self.command = update.message.text.split(" ")[0][1:]
        self.args = self.cxt.args
        self.username = self.args[0]
        self.name = self.username
        self.fileName = self.name
        self.valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"
        super().__init__()

    def _validUserName(self) -> bool:
        for char in self.username:
            if char not in self.valid_characters:
                return False
        return True
    
    # get the first one
    def _getInitials(self):
        return list(self._loadStoreData().values())[0]
    # get the last one
    def _getStatus(self):
        return list(self._loadStoreData().values())[-1]
    # get all
    def _getHistory(self):
        return  list(self._loadStoreData().values())
    
    def _remove(self):
        return self._cancel_job()
    
    # Message Decorators
    def _initialStatus(self,data) -> str:
        """
        Initials status of <username>
            full_name:name,
            follower:99,
            followee:100,\n
            '''
        """
        title:str = f"Initials of {self.username}"
        des:str = self._dict_to_str(data)
        message = f"{title}\n{des}"
        return message
        
    def _changeDetected(self,data:list[tuple]) -> str:
        """
        Public activity detected for <username>
            follower:57554253 -> 57554329
            isPrivate:true -> false\n
            '''
        """
        title:str = f"Public activity detected for {self.username}"
        des = ""
        for attr in data:
            # eg:follower:99->100
            des += f"{attr[0]}:{attr[1]} -> {attr[2]},\n"
        message = f"{title}\n{des}"
        return message
    
    def _tracking_list_message(self) -> str:
        '''
        Active Trackers..
        1. tracker 1
        2. tracker 2
        3. tracker 3
        Total:3
        '''
        all_tracker = self._getAllJobs()
        msg = f"Active trackers for..\n"
        for index,jobs in enumerate(all_tracker):
            msg += f"{index+1}. {jobs.chat_id.split('_')[1]}\n"
        msg += f"Total:{len(all_tracker)}"
        return msg
        

    def _history_message(self,data:dict):
        ...
    

    async def run(self):


        '''special methods'''
        '''if only special method given as username'''
        '''Get all tracking'''
        if len(self.args) == 1:
            if self.username == "trackinsta?":
                msg = self._tracking_list_message()
                await self.update.effective_message.reply_text(msg)
                return

        '''
        options (remove,_initial,history,status,debug)
        only get the first parameter after username skip others 
        '''
        '''if any option given'''
        if len(self.args) > 1:
            option:str = self.args[1].lower()
            '''options will only run if the user is in tracking'''
            if self._is_job_exits():
                '''Remove the tracker for given user (/trackinsta <username> remove)'''
                if option == "remove":
                    success = self._remove()
                    if success:
                        await self.update.effective_message.reply_text("Tracker successfully cancelled!") 
                        self._removeFile()
                        return
                # '''See the first store data'''
                elif option == 'initial' :
                    await self.update.effective_message.reply_text(self._getInitials())
                    return
                
                # '''See all store data'''
                elif option == 'history' :
                    await self.update.effective_message.reply_text(self._getHistory())
                    return
                
                # '''See last store data'''
                elif option == 'status' :
                    await self.update.effective_message.reply_text(self._getStatus())
                    return
                # '''Detail info on all tracking'''

                else:
                    await self.update.effective_message.reply_text("Invalid option!!!")
                    return
                
            elif option == 'debug' and self.username == "trackinsta?":
                data = self._getAllJobs()
                await self.update.effective_message.reply_text(str(data))
                return
            
            else:
                await self.update.effective_message.reply_text("You are not tracking this user")
                return


        '''check for wrong username schema'''
        if not self._validUserName():
            await self.update.effective_message.reply_text(f"Invalid username {self.username}") 
            return
        '''Check if already tracking this user '''
        if self._is_job_exits():
            await self.update.effective_message.reply_text(f"Already Tracking {self.username}") 
            return 

        '''instance for interacting with instagram api'''
        insta = Insta(self.username)
        '''If username not exist'''
        if not insta.lookup():
            await self.update.effective_message.reply_text(f"Something went wrong.Check if user '{self.username}' exist") 
            return
        
        '''Id found'''
        await self.update.effective_message.reply_text(f"Tracking Instagram id {self.username}") 
        # create initial files (if file not exist )
        self._createDataFile()
        '''Send the first result when start tracking'''
        await self.update.effective_message.reply_text(self._initialStatus(insta.publicData()))


        '''Add user in job queue'''
        async def callback(cxt):
            ''' getting public instagram data for id (name, follower, followee,bio etc..)'''
            new_data = insta.publicData()
            '''Loading previously stored data'''
            storedData = self._loadStoreData()
            '''Verify whether any earlier data has been stored, and if so, compare it with the new data'''
            if len(storedData) > 0:
                _ , last_value = list(storedData.items())[-1]
                if self._is_diff(last_value,new_data):
                    '''Get different values'''
                    diff_val = self._get_diff_val(last_value,new_data)
                    await self.update.effective_message.reply_text(self._changeDetected(diff_val))
                else:
                    return
            '''Append new data'''
            self._storeNewData(data=new_data)

        self._add_repeating_job(callback,interval=50)
