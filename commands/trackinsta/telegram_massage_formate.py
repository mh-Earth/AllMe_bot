from modules.CommandMaker.Formatter import BaseFormatter
from const import trackInsta_help_message,trackinsta_option_list
from .api import ConnectorUtils
from dataclasses import dataclass
from models.trackinsta.types import TrackinstaDataModel
from time import time
from utils.comparator import get_diff_val
from telegram.helpers import escape_markdown
@dataclass
class FuckIamSickOfNamingThinksFormat:
    username:str
    full_name:str
    follower:int
    following:int
    isPrivate:bool
    bio:str
    dp:str


'''Message Decorators'''
class TelegramMessageFormate(BaseFormatter):
    def __init__(self,username) -> None:
        self.username = username
        self.dbUtils = ConnectorUtils(username)
        self.ini_list = ['Username','Full Name','Follower','Following','Private','Bio','Dp']
        self.FormateKeys = FuckIamSickOfNamingThinksFormat(*self.ini_list)
    
    def __call__(self,data:dict[str:dict]):
        return self._format(data)
    
    @staticmethod
    def _escape_markdown_pre(text:str):
        return escape_markdown(text,version=2,entity_type='pre')
    @staticmethod
    def _escape_markdown(text:str):
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
        title = self._escape_markdown(f'Status of {self.username}\n\n'.upper())
        body = ""
        for d in data:
            for values in d.values():
                for k,v in values.items():
                    if k == self.FormateKeys.dp:
                        body += self._escape_markdown_pre(f'{k}: [Dp]({v})\n')
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
        if data == None:
            fData = self._format(self.dbUtils.getInitials())
        else:
            fData = self._format(self.extract_data_from_model(data))
        title = ''
        body = ''
        for data in fData:
            for d in data.values():
                for k,v in d.items():
                    if k == self.FormateKeys.dp:
                        body += self._escape_markdown_pre(f'{k}: [Dp]({v})\n')
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
        title:str = self._escape_markdown(f"Public activity detected for {self.username}")
        des = ""
        for key,old,new in data:
            if key == self.FormateKeys.dp.lower():
                if new != None:
                    des += f"{key} change:"
                    des += self._escape_markdown_pre(f'[old]({old})')
                    des +=self._escape_markdown(" -> ")
                    des += self._escape_markdown_pre(f"[new]({new})")
                    des += '\n'
            else:
                # eg:follower:99->100
                des += self._escape_markdown(f"{key}:{old} -> {new}\n")
        
        message = f"{title}\n{des}"
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
        data = self.api.getHistory()
        if len(data) < 1:
            return self._escape_markdown("No history found!!")
        title = self._escape_markdown(f"Tracking History of {self.username}\n\n".upper())
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
        title = "You are not tracking this user".upper() if not isTracking else ""
        info = "You are tracking this user".upper() if isTracking else ""
        if dataModel != None:
            data = self._format(self.extract_data_from_model(dataModel=dataModel))
            des = ''
            for d in data:
                for i in d.values():
                    for k,v in i.items():
                        if k == self.FormateKeys.dp:
                            des += self._escape_markdown_pre(f'{k}: [DP]({v})\n')
                        else:
                            des += self._escape_markdown(f'{k}: {v}\n')
            message = f"{title}\n\n{des}\n{info}"
            return message
        else:
            return 'USER NOT FOUND'
        

    @staticmethod
    def _create_change_log(data:dict[dict]) -> list[tuple[str,tuple]]:
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
        
        keys = [k for d in data for k in d.keys()]
        changes = []
        for i in range(len(data)-1):
            change = get_diff_val(data[i].get(keys[i]),data[i+1].get(keys[i+1]))
            if len(change) > 0:
                changes.append((keys[i+1],change))
        return changes
    
    # option = log
    def log_option(self):
        logs = self._create_change_log(self._format(self.dbUtils.getPreviousData()))
        if len(logs) < 1:
            return self._escape_markdown("Logs are not available.No activity detected")
        
        title = self._escape_markdown(f'change history of {self.username}\n\n'.upper())
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
                        body += self._escape_markdown_pre(f"{change}: [Dp change]({to})\n")
                        has_add = True
                    
                else:
                    body += self._escape_markdown(f"{change}: {frm} -> {to}\n")
                    has_add = True

            if not has_add:
                body = body[:len(body)-len(self._escape_markdown(f'{activity[0]}\n'))]


            body += "\-"*30 + "\n" if index+1 != len(logs) and has_add else ""

        if body == "":
            return self._escape_markdown("Logs are not available.No activity detected")
        else:
            msg = title + body
            return msg



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
                'bio':dataModel.bio,
                'dp':dataModel.dp

            }
        }