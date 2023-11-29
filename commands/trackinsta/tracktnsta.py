'''
Command : /trackinsta <instagram username> <option (optional)>

option:
    status:
    initial:
    history:
    remove:
    log:
    all?:
    checkout:?
    options?:
    help?:

'''


from  modules.CommandMaker.Base import CommandModel
from telegram.ext import ContextTypes,CallbackContext
from telegram import Update
from .api import Insta,Connector,TrackinstaTypes
from const import trackInsta_help_message,trackinsta_option_list
from configurations.settings import TRACKING_MODE,REPEAT_JOB_INTERVAL
from typing import Final
from .options import *

class TrackInsta(CommandModel):
    def __init__(self,update:Update,cxt:ContextTypes.DEFAULT_TYPE) -> None:
        self.update:Update = update
        self.cxt:ContextTypes.DEFAULT_TYPE = cxt
        self.args = self.cxt.args
        self.username = self.args[0]
        self.insta = Insta(self.username) # object for interacting with instagram api
        self.command = update.message.text.split(" ")[0][1:]
        self.valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"
        self.api = Connector(command=self.command,username=self.username)
        # required username
        self.status_option:Final = STATUS
        self.remove_option:Final = REMOVE
        self.initial_option:Final = INITIAL
        self.history_option:Final = HISTORY
        self.checkout_option:Final = CHECKOUT
        self.log_option:Final = LOG
        # no username required
        self.help_option = HELP
        self.tracking_list_option = ALL
        self.option_list_option = OPTIONS
        # configs
        self.TRACKING_MODE:Final = TRACKING_MODE
        # ////////////////////////////
        # required for job base class
        self.name = self.username
        # required for helper base class
        self.fileName = self.username
        super().__init__()

    def _validUserName(self) -> bool:
        for char in self.username:
            if char not in self.valid_characters:
                return False
        return True
    
    def _getLogs(self) -> list[tuple[str, tuple]]:
        return self._create_change_log(data=self.api.getPreviousData())

    def _remove(self):
        return self._cancel_job()
    
    '''Message Decorators'''
    # option = status
    def status_message(self) -> str:
        '''
        STATUS OF TRACKER
        full_name: USERNAME
        follower: 9999
        followee: 9999
        isPrivate: False
        bio: ''
        '''
        data = self.api.getStatus()
        title = f'Status of {self.username}\n\n'.upper()
        body = ""
        for d in data:
            for k,v in data[d].items():
                body += f'{k}: {v}\n'
        msg = title + body

        return msg
    # option = initial
    def initial_message(self) -> str:
        '''
        INITIAL VALUE OF TRACKER
        full_name: USERNAME
        follower: 9999
        followee: 9999
        isPrivate: False
        bio: ''
        '''
        data = self.api.getInitials()
        print(data)
        title = ''
        body = ""
        for d in data:
            for k,v in data[d].items():
                body += f'{k}: {v}\n'
        msg = title + body

        return msg

    # option = initial
    def _initialStatus(self,data) -> str:
        """
        Initials status of <username>
            full_name:name,
            follower:99,
            following:100,\n
            '''
        """
        title:str = f"Initials of {self.username}\n".upper()
        des:str = self._initialFormat(data)
        message = f"{title}\n{des}"
        return message
    
    # 
    def _changeDetected(self,data:list[tuple]) -> str:
        """
        Public activity detected for <username>
            follower:57554253 -> 57554329
            isPrivate:true -> false\n
            '''
        """
        title:str = f"Public activity detected for {self.username}"
        des = ""
        print(f"Change Data:{data}")
        for attr in data: 
            # eg:follower:99->100
            des += f"{attr[0]}:{attr[1]} -> {attr[2]},\n"
        message = f"{title}\n{des}"
        return message
    
    # option (username) = trackinsta?
    def _tracking_list_message(self) -> str:
        '''
        Active Trackers
        1. tracker 1
        2. tracker 2
        3. tracker 3
        Total:3
        '''
        all_tracker = self._getAllJobs()
        if len(all_tracker) == 0:
            return "You have no active tracker"
        
        msg = f"Active trackers\n"
        for index,jobs in enumerate(all_tracker):
            msg += f"{index+1}. {jobs.name.split('_')[1]}\n"
        msg += f"Total:{len(all_tracker)}"
        return msg
        
    # option = history
    def _history_message(self):
        '''
        TRACKING HISTORY OF <TRACKER>
        Monday 22:59:05 2023-11-20
        full_name: USERNAME
        follower: 999
        followee: 999
        isPrivate: False
        bio: BIO IF USER
        -------------------
        -------------------
        -------------------
        '''
        data = self.api.getHistory()
        if len(data) < 1:
            return "No history found!!"
        title = f"Tracking History of {self.username}\n\n".upper()
        body = ""
        for index,d in enumerate(data):
            time = self._timestamp_to_readable_format(float(d))
            body += time + "\n"
            for k,v in data[d].items():
                body +=  f"{k}: {v}\n"
            body += "-"*30 + '\n' if index+1 != len(data) else ""
        msg = title + body
        return msg
        ...
    # option = checkout (username optional)
    def _checkout_option_message(self,data,isTracking:bool):    
        '''
        TITLE:TITLE
        Monday 22:59:05 2023-11-20
        full_name: USERNAME
        follower: 999
        followee: 999
        isPrivate: False
        bio: BIO IF USER
        INFO:INFO
        '''
        title = "You are not tracking this user".upper() if not isTracking else ""
        info = "You are tracking this user".upper() if isTracking else ""
        if data != None:
            des:str = self._initialFormat(data)
            message = f"{title}\n\n{des}\n{info}"
            return message
        else:
            return 'USER NOT FOUND'

    # option = log
    def _log_option_message(self):
        logs = self._getLogs()
        print(logs)
        if len(logs) == 0:
            return "Logs not available.No activity detected"
        title = f'change history of {self.username}\n\n'.upper()
        body = ""
        for index,activity in  enumerate(logs):
            body += self._timestamp_to_readable_format(float(activity[0])) + '\n'
            for change,frm,to in activity[1]:
                body += f"{change}: {frm} -> {to}\n"
            body += "-"*30 + '\n' if index+1 != len(logs) else ""
        msg = title + body

        return msg



    '''Command manual provider'''
    # username = help?
    def _help_message(self):
        return trackInsta_help_message
    # username = options?
    def _option_list(self):
        return trackinsta_option_list
    
    # Main function
    async def run(self):
        '''
        username required : options (remove,initial,history,status,debug)
        no username required : options (help?,trackinsta?)

        only get the first parameter after username skip others 
        '''
        '''If special username is used.special user name ends with `?` '''
        if len(self.args) <= 1 and self.username.endswith("?"):

            if self.username == self.help_option:
                await self.update.effective_message.reply_text(self._help_message(),parse_mode='MarkdownV2')
                return
            elif self.username == self.tracking_list_option:
                msg = self._tracking_list_message()
                await self.update.effective_message.reply_text(msg)
                return
            elif self.username == self.option_list_option:
                msg = self._option_list()
                await self.update.effective_message.reply_text(msg,parse_mode='MarkdownV2')
                return
            else:
                await self.update.effective_message.reply_text(f"Invalid option `{self.username}`")
                return

            
        # '''if any option given'''
        elif len(self.args) > 1:
            option:str = self.args[1].lower()
            '''options will only run if the user is in tracking'''
            if self._is_job_exits():
                '''Remove the tracker for given user (/trackinsta <username> remove)'''
                if option == "remove":
                    success = self._remove()
                    if success:
                        self.api.delete_tracker()
                        self._removeFile()
                        await self.update.effective_message.reply_text("Tracker successfully cancelled!") 
                        return
                # '''See the first store data'''
                elif option == self.initial_option :
                    await self.update.effective_message.reply_text(self.initial_message())
                    return
                
                # '''See all store data'''
                elif option == self.history_option :
                    await self.update.effective_message.reply_text(self._history_message())
                    return
                
                # '''See last store data'''
                elif option == self.status_option :
                    await self.update.effective_message.reply_text(self.status_message())
                    return
                
                # '''See live status of a user info (tracker required)'''
                elif option == self.checkout_option:
                    await self.update.effective_message.reply_text(self._checkout_option_message(self.insta.checkout(),True))
                    return
                
                # '''See change log of a user info'''
                elif option == self.log_option:
                    await self.update.effective_message.reply_text(self._log_option_message())
                    return
                

                else:
                    await self.update.effective_message.reply_text(f"Invalid option `{option}`")
                    return

            # '''Detailed info on all tracking'''
            elif option == 'debug' and self.username == self.tracking_list_option:
                data = self._getAllJobs()
                await self.update.effective_message.reply_text(str(data))
                return
            
            elif option == self.checkout_option and not self.username.endswith('?'):
                await self.update.effective_message.reply_text(self._checkout_option_message(self.insta.checkout(),False))
                return

            else:
                await self.update.effective_message.reply_text("You are not tracking this user")
                return


        '''check for invalid char in username'''
        if not self._validUserName():
            await self.update.effective_message.reply_text(f"Invalid username {self.username}") 
            return
        '''Check if already tracking this user '''
        if self._is_job_exits():
            await self.update.effective_message.reply_text(f"Already Tracking {self.username}") 
            return 

        '''If username not exist'''
        if not self.insta.lookup():
            await self.update.effective_message.reply_text(f"Something went wrong.Check if user '{self.username}' exist") 
            return
        
        '''Id found'''
        '''Tracking user and sending its data to db'''
        user_insta_data = self.insta.publicData(initial=True)
        trackerObj = TrackinstaTypes(**user_insta_data)
        '''Send the first result when start tracking'''
        send_data = self.api.add_tracker(data=trackerObj)
        if  send_data.status_code == 200:
            await self.update.effective_message.reply_text(f"Tracking user {self.username}") 
            await self.update.effective_message.reply_text(self._initialStatus(user_insta_data))    
            self._createDataFile() 
        else:
            await self.update.effective_message.reply_text(f"Failed to add track for {self.username}") 
            return

        

        '''Add user in job queue'''
        async def callback(cxt:CallbackContext):
            ''' getting public instagram data for id (name, follower, followee,bio etc..)'''
            new_data = self.insta.publicData()
            '''Load previously stored data'''
            storedData = self.api.last_stored_log()
            '''Verify whether any earlier data has been stored, and if so, compare it with the new data'''
            if len(storedData) > 0:
                _ , last_value = list(storedData.items())[0]
                print(f'new data {new_data} ||||| last val {last_value}')
                if self._is_diff(last_value,new_data):
                    '''Get different values'''
                    diff_val = self._get_diff_val(last_value,new_data)
                    await self.update.effective_message.reply_text(self._changeDetected(diff_val))
                else:
                    return
            '''Append new data'''
            dataObject = TrackinstaTypes(**new_data)
            self.api.add_log(data=dataObject)
            
        '''How often the job should run
           daily at given time or after a interval(s) later
           Default daily
        '''
        if self.TRACKING_MODE.lower() == "daily":
            self._add_daily_job(callback)
        elif self.TRACKING_MODE.lower() == "repeat":
            self._add_repeating_job(callback,interval=REPEAT_JOB_INTERVAL) # 3 hour
        else:
            self._add_daily_job(callback)


