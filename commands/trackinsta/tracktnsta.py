'''
Command : /trackinsta <instagram username> <option (optional)>

option:
    status:
    initial:
    remove:
    log:
    plot:
    act:
    all?:
    checkout:?
    options?:
    help?:

'''

import logging
from modules.CommandMaker.Base import CommandModel
from telegram.ext import ContextTypes,CallbackContext
from telegram import InputFile, Update
from .insta import Insta
from .api import Connector
from .telegram_massage_formate import TelegramMessageFormate
from configurations.settings import TRACKING_MODE,REPEAT_JOB_INTERVAL
from typing import Final
from .options import *
from .plot import ActivityPlot,FFPlot
from utils.comparator import is_diff
from .schema import Detection

class TrackInsta(CommandModel):
    def __init__(self,update:Update,cxt:ContextTypes.DEFAULT_TYPE) -> None:
        self.update:Update = update
        self.cxt:ContextTypes.DEFAULT_TYPE = cxt
        self.args = self.cxt.args
        self.username = self.args[0]
        self.user_id = self.cxt._user_id
        self.command = update.message.text.split(" ")[0][1:] # [1:] for removing the '/' from /command
        self.api = Connector(user_id=self.user_id,username=self.username)
        self.insta = Insta(self.username) # object for interacting with instagram api
        self.formatter = TelegramMessageFormate(self.user_id, username=self.username)
        # self.localStorage = LocalStorage(self.command,self.username)
        self.valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"
        # required username
        self.status_option:Final = STATUS
        self.remove_option:Final = REMOVE
        self.initial_option:Final = INITIAL
        self.checkout_option:Final = CHECKOUT
        self.log_option:Final = LOG
        self.history_option = HISTORY
        self.plot_option = PLOT
        self.activity_option = ACTIVITY
        # no username required
        self.help_option = HELP
        self.tracking_list_option = ALL
        self.option_list_option = OPTIONS
        # configs
        self.TRACKING_MODE:Final = TRACKING_MODE
        self.REPEAT_JOB_INTERVAL = REPEAT_JOB_INTERVAL
        # ////////////////////////////
        # required for job base class
        self.name = self.username
        # //////////////////////////
        super().__init__()

    def _validUserName(self) -> bool:
        for char in self.username:
            if char not in self.valid_characters:
                return False
        return True

    def _remove(self):
        return self._cancel_job()

    def tracking_list_message(self) -> str:
        '''
        Active Trackers
        1. tracker 1
        2. tracker 2
        3. tracker 3
        Total:3
        '''
        all_tracker = self._getAllJobs(self.user_id)
        
        if len(all_tracker) == 0:
            return "You have no active tracker"
        
        msg = f"Active trackers\n"
        for index,jobs in enumerate(all_tracker):
            msg += f"{index+1}. {jobs.name.split('&')[1]}\n"
        msg += f"Total:{len(all_tracker)}"
        return msg
        
    # Main function
    async def run(self):
        '''
        username required : options (remove,initial,status,debug)
        no username required : options (help?,all?,option?)
        hybrid : checkout

        only get the first parameter after username skip others 
        '''
        '''If special username is used.special user name ends with `?` '''
        if len(self.args) <= 1 and self.username.endswith("?"):

            if self.username == self.help_option:
                await self.update.effective_message.reply_markdown_v2(self.formatter.help_message())
                return
            elif self.username == self.tracking_list_option:
                await self.update.effective_message.reply_text(self.tracking_list_message())
                return
            elif self.username == self.option_list_option:
                await self.update.effective_message.reply_markdown_v2(self.formatter.option_list())
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
                if option == self.remove_option:
                    success = self._remove()
                    if success:
                        remove_tracker = self.api.remove_tracker(user_id=self.user_id,tracker_name=self.username)
                        if remove_tracker.code == 200:
                            await self.update.effective_message.reply_text(f"Tracker removed from `{self.username}`") 
                            
                            return
                        await self.update.effective_message.reply_text(f"Something went wrong.Failed to remove tracker for {self.username}") 
                        return

                # '''See the first store data'''
                elif option == self.initial_option :
                    await self.update.effective_message.reply_markdown_v2(self.formatter.initial())
                    return
                
                # '''See last store data'''
                elif option == self.status_option :
                    await self.update.effective_message.reply_markdown_v2(self.formatter.status())
                    return
                
                # '''See live status of a user info (tracker required)'''
                elif option == self.checkout_option:
                    await self.update.effective_message.reply_markdown_v2(self.formatter.checkout_option(self.insta.checkout(),True))
                    return
                
                # '''See change log of a user info'''
                elif option == self.log_option:
                    logs = self.formatter.log_option()
                    if len(logs) > self.formatter.TELEGRAM_MAX_MESSAGE_LENGTH:
                        from io import BytesIO
                        # Create a BytesIO object to store the text content
                        file_stream = BytesIO()
                        # Write the text content to the BytesIO object
                        file_stream.write(logs.replace("\\",'').encode('utf-8'))
                        # Move the file cursor to the beginning of the BytesIO object
                        file_stream.seek(0)
                        # Send the BytesIO object as a document
                        await self.cxt.bot.send_document(chat_id=self.cxt._chat_id, document=InputFile(file_stream, filename=f'{self.username}_logs.txt'))
                        return
                    await self.update.effective_message.reply_markdown_v2(logs,disable_web_page_preview=True)
                    return
                # '''See change log of a user info'''
                elif option == self.history_option:
                    history = self.formatter.history_message()
                    if len(history) > self.formatter.TELEGRAM_MAX_MESSAGE_LENGTH:
                        from io import BytesIO
                        # Create a BytesIO object to store the text content
                        file_stream = BytesIO()
                        # Write the text content to the BytesIO object
                        file_stream.write(history.replace("\\",'').encode('utf-8'))
                        # Move the file cursor to the beginning of the BytesIO object
                        file_stream.seek(0)
                        # Send the BytesIO object as a document
                        await self.cxt.bot.send_document(chat_id=self.cxt._chat_id, document=InputFile(file_stream, filename=f'{self.username}_history.txt'))
                        return
                    
                    await self.update.effective_message.reply_text(history,disable_web_page_preview=True)
                    return
                elif option == self.plot_option:
                    try:
                        what_to_plot = self.args[2].lower()
                    except IndexError:
                        what_to_plot = 'all'
                    if what_to_plot.lower() == 'follower':
                        plot = FFPlot(self.user_id,self.username).follower()
                        await self.cxt.bot.send_photo(chat_id=self.cxt._chat_id, photo=InputFile(plot, filename='activity.png'))
                        return 
                    elif what_to_plot.lower() == 'following':
                        plot = FFPlot(self.user_id,self.username).following()
                        await self.cxt.bot.send_photo(chat_id=self.cxt._chat_id, photo=InputFile(plot, filename='activity.png'))
                        return 
                    elif what_to_plot.lower() == 'both':
                        plot = FFPlot(self.user_id,self.username).both()
                        await self.cxt.bot.send_photo(chat_id=self.cxt._chat_id, photo=InputFile(plot, filename='activity.png'))
                        return 
                    else:
                        plot = FFPlot(self.user_id,self.username).following()
                        await self.cxt.bot.send_photo(chat_id=self.cxt._chat_id, photo=InputFile(plot, filename='activity.png'))
                        return 

                elif option == self.activity_option:
                    try:
                        colormap = self.args[2].lower()
                        if colormap.lower() in ['colormaps','colormap']:
                            await self.update.effective_message.reply_text(self.formatter.colormap_message())
                            return
                    except IndexError:
                        colormap = None
                    activity = ActivityPlot(self.user_id,self.username).plot(colormap=colormap)
                    await self.cxt.bot.send_photo(chat_id=self.cxt._chat_id, photo=InputFile(activity, filename='activity.png'))
                    return                

                else:
                    await self.update.effective_message.reply_text(f"Invalid option `{option}`")
                    return

            # '''Detailed info on all tracking'''
            elif option == 'debug' and self.username == self.tracking_list_option:
                data = self._getAllJobs(user_id=-1)
                await self.update.effective_message.reply_text(str(data))
                return
            
            elif option == self.checkout_option and not self.username.endswith('?'):
                await self.update.effective_message.reply_markdown_v2(self.formatter.checkout_option(self.insta.checkout(),False))
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

        '''If username exist'''
        if not self.insta.lookup():
            await self.update.effective_message.reply_text(f"Something went wrong.Check if user '{self.username}' exist") 
            return
        
        '''check limits for having tracker'''
        limit = self.api.tracker_limit(self.user_id)
        if limit.code != 200:
            await self.update.effective_message.reply_text(limit.text) 
            return
        '''Id found'''
        '''Tracking user and sending its data to db'''
        user_insta_data = self.insta.publicData()
        '''Send the first result when start tracking'''
        send_data = self.api.add_new_tracker(self.update, data=user_insta_data)
        if  send_data.code == 200:
            await self.update.effective_message.reply_text(f"Tracking user {self.username}")
            await self.update.effective_message.reply_markdown_v2(self.formatter.initial(data=user_insta_data))
            # self.localStorage.createDataFile()
            # self.localStorage.storeNewData(self.localStorage.extra_data_from_model(user_insta_data))
        else:
            await self.update.effective_message.reply_text(f"Failed to add track for {self.username}") 
            logging.error(send_data.text)
            return

        '''Add user in job queue'''
        '''How often the job should run
           daily at given time or after a interval(s) later
           Default daily
        '''
        if self.TRACKING_MODE.lower() == "daily":
            self._add_daily_job(self.callback)
        elif self.TRACKING_MODE.lower() == "repeat":
            self._add_repeating_job(self.callback,interval=self.REPEAT_JOB_INTERVAL) # 3 hour
        else:
            self._add_daily_job(self.callback)

    async def callback(self,cxt:CallbackContext):
        ''' getting public instagram data for id (name, follower, followee,bio etc..)'''
        new_data =  self.insta.publicData()
        extracted_new_data = [v for k,v in self.formatter.extract_data_from_model(new_data).items()][0]
        '''Load previously stored data'''
        storedData = self.api.get_last_log()
        last_value = [v for k,v in storedData.items()][0]
        '''Verify whether any earlier data has been stored, and if so, compare it with the new data'''
        # print(f'new data {extracted_new_data} ||||| last val {last_value}')
        if is_diff(last_value,extracted_new_data):
            '''Get different values'''
            diff_val = Detection(last_value,extracted_new_data).activity()
            if len(diff_val) != 0:
                await self.update.effective_message.reply_markdown_v2(self.formatter.changeDetected(diff_val),disable_web_page_preview=True)
                self.api.add_tracker_data(update=self.update,data=new_data)

            elif not new_data.verified:
                '''Append new data'''
                self.api.add_tracker_data(update=self.update,data=new_data)
            
            # self.localStorage.storeNewData(self.localStorage.extra_data_from_model(new_data))

