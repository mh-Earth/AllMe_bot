
import logging
from modules.CommandMaker.Formatter import BaseFormatter
from const import trackInsta_help_message,trackinsta_option_list
from .api import ConnectorUtils
from dataclasses import dataclass
from db.dataModels import TrackinstaDataModel
from time import time
from utils.comparator import get_diff_val
from telegram.helpers import escape_markdown
from .messages import STATUS_OPTION_TITLE
from .messages import INITIAL_OPTION_TITLE
from .messages import CHANGE_DETECTED_MESSAGE
from .messages import HISTORY_OPTION_TITLE
from .messages import CHECKOUT_OPTION_INFO
from .messages import CHECKOUT_OPTION_TITLE
from .messages import LOG_OPTION_TITLE
from .messages import NO_LOG_MESSAGE

@dataclass
class FuckIamSickOfNamingThinksFormat:
    username:str
    full_name:str
    follower:int
    following:int
    isPrivate:bool
    verified:bool
    bio:str
    dp:str


'''Message Decorators'''
class TelegramMessageFormate(BaseFormatter):
    def __init__(self,user_id:int, username:str) -> None:
        self.user_id = user_id
        self.username = username
        self.dbUtils = ConnectorUtils(user_id, username)
        self.ini_list = ['Username','Full Name','Follower','Following','Private','Verified','Bio','Dp']
        self.FormateKeys = FuckIamSickOfNamingThinksFormat(*self.ini_list)
    
    def __call__(self,data:dict[str:dict]):
        return self._format(data)
    
    @staticmethod
    def _escape_markdown_pre(text:str) -> str:
        logging.debug('escaping markdown')
        return escape_markdown(text,version=2,entity_type='pre')
    @staticmethod
    def _escape_markdown(text:str) -> str:
        logging.debug('escaping markdown')
        return escape_markdown(text,version=2)

    def _format(self,data:dict[str:dict]) -> list[dict[str,dict]]:
        formatted = []
        for timestamp,v in data.items():
            time = self._timestamp_to_readable_format(float(timestamp))
            final_dict = dict(zip(self.ini_list, list(v.values())))
            formatted.append({
                time:final_dict
            })
        
        return formatted

    # option = status
    def status(self) -> str:
        '''
        STATUS OF TRACKER
        full_name: USERNAME
        follower: 9999
        followee: 9999
        isPrivate: False
        bio: BIO
        '''
        data = self._format(self.dbUtils.getStatus())
        title = self._escape_markdown(STATUS_OPTION_TITLE.format(self.username).upper())
        body = ""
        logging.debug(f'Creating status message with data = {data}')
        for d in data:
            for values in d.values():
                for k,v in values.items():
                    if k == self.FormateKeys.dp:
                        body += self._escape_markdown_pre(f'{k}: [Dp]({v})\n')

                    elif k == self.FormateKeys.isPrivate:
                        if v:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                        else:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')

                    elif k == self.FormateKeys.verified:
                        if v:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                        else:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')

                    elif k == self.FormateKeys.bio:
                        if v==None or v=='':
                            body += self._escape_markdown_pre(f'{k}: No bio found 💤\n')
                        else:
                            body += self._escape_markdown(f'{k}: {v}\n')
                    else:
                        body += self._escape_markdown(f'{k}: {v}\n')


                
        msg = title + body

        return msg
    # option = initial
    def initial(self,data:TrackinstaDataModel=None) -> str:
        '''
        INITIAL VALUE OF TRACKER
        full_name: USERNAME
        follower: 9999
        followee: 9999
        isPrivate: False
        bio: ''
        '''
        logging.debug(f'Creating initial message with data = {data}')
        if data == None:
            fData = self._format(self.dbUtils.getInitials())
        else:
            fData = self._format(self.extract_data_from_model(data))
        title = INITIAL_OPTION_TITLE
        body = ''
        for data in fData:
            for d in data.values():
                for k,v in d.items():
                    if k == self.FormateKeys.dp:
                        body += self._escape_markdown_pre(f'{k}: [Dp]({v})\n')
                                        # Use emoji for true false instead of bool value
                    elif k == self.FormateKeys.isPrivate:
                        if v:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                        else:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')

                    elif k == self.FormateKeys.verified:
                        if v:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                        else:
                            body += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                    
                    elif k == self.FormateKeys.bio:
                        if v==None or v=='':
                            body += self._escape_markdown_pre(f'{k}: No bio found on profile 💤\n')
                        else:
                            body += self._escape_markdown(f'{k}: {v}\n')

                    else:
                        body += self._escape_markdown(f'{k}: {v}\n')


        msg = title + body
        return msg

    def changeDetected(self,data:list[tuple]) -> str:
        """
        Public activity detected for <username>
            follower:57554253 -> 57554329
            isPrivate:true -> false\n
            '''
        """
        title:str = self._escape_markdown(CHANGE_DETECTED_MESSAGE.format(self.username))
        des = ""
        logging.debug(f'Change detected. Formatting data. data = "{data}"')
        for key,old,new in data:
            if key == self.FormateKeys.dp.lower():
                des += f"{key} change:"
                des += self._escape_markdown_pre(f'[old]({old})')
                des +=self._escape_markdown(" -> ")
                des += self._escape_markdown_pre(f"[new]({new})")
                des += '\n'

            if key == self.FormateKeys.bio.lower():
                logging.debug(f'Change {key}')
                if new != None:
                    des += self._escape_markdown(f"{key}:{old} -> {new}\n")
                
            elif key == self.FormateKeys.isPrivate:
                body += self._escape_markdown_pre(f'{key}: {self.bool_to_emoji(old)} -> {self.bool_to_emoji(new)} \n')

            elif key == self.FormateKeys.verified:
                body += self._escape_markdown_pre(f'{key}: {self.bool_to_emoji(old)} -> {self.bool_to_emoji(new)} \n')
            
            else:
                logging.debug(f'Change {key}')
                if key in ['dp','bio']:
                    pass
                else:
                    des += self._escape_markdown(f"{key}:{old} -> {new}\n")
                    
                # eg:follower:99->100
        
        message = f"{title}\n{des}"
        logging.debug(f"change message created.\n message ='{message}'")
        return message
    
    # option (username) = trackinsta?

        
    # option = history
    def history_message(self,key:str=None):
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
        data = self.dbUtils.getPreviousData()
        logging.debug(f'Creating history message from data = {data}')
        if len(data) < 1:
            return self._escape_markdown("No history found!!")
        title = self._escape_markdown(HISTORY_OPTION_TITLE.format(self.username).upper())
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
    def checkout_option(self,dataModel:TrackinstaDataModel,isTracking:bool):    
        '''
        TITLE:TITLE
        full_name: USERNAME
        follower: 999
        followee: 999
        isPrivate: False
        bio: BIO IF USER
        INFO:INFO
        '''
        title = CHECKOUT_OPTION_TITLE.upper() if isTracking else CHECKOUT_OPTION_INFO.upper()
        # info = CHECKOUT_OPTION_INFO.upper() if isTracking else ""
        if dataModel != None:
            data = self._format(self.extract_data_from_model(dataModel=dataModel))
            des = ''
            for d in data:
                for i in d.values():
                    for k,v in i.items():
                        if k == self.FormateKeys.dp:
                            des += self._escape_markdown_pre(f'{k}: [DP]({v})\n')
                        
                        # Use emoji for true false instead of bool value
                        elif k == self.FormateKeys.isPrivate:
                            if v:
                                des += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                            else:
                                des += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')

                        elif k == self.FormateKeys.verified:
                            if v:
                                des += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')
                            else:
                                des += self._escape_markdown_pre(f'{k}: {self.bool_to_emoji(v)} \n')

                        elif k == self.FormateKeys.bio:
                            if v==None or v=='':
                                des += self._escape_markdown_pre(f'{k}: No bio found on profile 💤\n')
                            else:
                                des += self._escape_markdown(f'{k}: {v}\n')

                        else:
                            des += self._escape_markdown(f'{k}: {v}\n')
            message = f"{title}\n\n{des}"
            return message
        else:
            return 'USER NOT FOUND'
        

    @staticmethod
    def _create_change_log(data:list[dict]) -> list[tuple[str,tuple]]:
        '''
        Create a change log of changes overtime\n
        Format:\n
        [
            (timestamp:str [(what_changes:str , to:str | int from:str | int)]),\n
            (timestamp:str [(what_changes:str , to:str | int from:str | int)]),\n
        ]\n
        """\n
        """
        '''
        logging.debug('Creating change log')
        keys = [k for d in data for k in d.keys()]
        logging.debug(f'Change log keys: {keys}')
        changes = []
        for i in range(len(data)-1):
            change = get_diff_val(data[i].get(keys[i]),data[i+1].get(keys[i+1]))
            if len(change) > 0:
                changes.append((keys[i+1],change))
        logging.debug(f'Success.Change log = "{changes}"')
        return changes
    
    # option = log
    def log_option(self):
        logging.debug('Creating logging message')
        logs = self._create_change_log(self._format(self.dbUtils.getLogData()))
        if len(logs) < 1:
            logging.debug(f'Log message length {len(logs)}')
            return self._escape_markdown(NO_LOG_MESSAGE)
        
        title = self._escape_markdown(LOG_OPTION_TITLE.format(self.username).upper())
        body = ""
        self.previous_dp = None
        for index,activity in  enumerate(logs):
            body += self._escape_markdown(f'{activity[0]}\n')
            has_add = False
            for change,frm,to in activity[1]:
                if change == self.FormateKeys.dp:
                    self.previous_dp = frm
                    if to != None:
                        # body += self._escape_markdown_pre(f"{change}: [From]({frm})")
                        # body += self._escape_markdown(" -> ")
                        body += self._escape_markdown_pre(f"{change}: Dp change\n")
                        has_add = True
                    
                else:
                    body += self._escape_markdown(f"{change}: {frm} -> {to}\n")
                    has_add = True

            if not has_add:
                body = body[:len(body)-len(self._escape_markdown(f'{activity[0]}\n'))]


            body += "\-"*30 + "\n" if index+1 != len(logs) and has_add else ""

        if body == "":
            return self._escape_markdown(NO_LOG_MESSAGE)
        else:
            msg = title + body
            return msg

    # plot colormap message
    def colormap_message(self) -> str:
        from matplotlib import colormaps
        colormaps = list(colormaps)
        title = 'Available colormaps for plot\n'
        des = ''
        for index,color in enumerate(colormaps):
            des += f'{index+1}. {color}\n'
        
        message = title + des
        return message


    '''Command manual provider'''
    # username = help?
    def help_message(self):
        return escape_markdown(trackInsta_help_message,version=2)
    # username = options?
    def option_list(self):
        return escape_markdown(trackinsta_option_list,version=2)
    
    @staticmethod
    def extract_data_from_model(dataModel:TrackinstaDataModel):
        if type(dataModel) == list:
            raise ValueError('dataModel can to be a list')
        
        return {
            str(time()) if dataModel.timestamp else str(time()) : {
                'username' : dataModel.username,
                'full_name':dataModel.full_name,
                'follower':dataModel.follower,
                'following':dataModel.following,
                'isPrivate':dataModel.isPrivate,
                'verified':dataModel.verified,
                'bio':dataModel.bio,
                'dp':dataModel.dp

            }
        }