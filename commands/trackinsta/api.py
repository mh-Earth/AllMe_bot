import logging
from time import time
from db.dataModels import TrackinstaDataModel
from db.Base import Base
from db.standard_response import StandardResponse
from telegram import Update
from utils.comparator import are_images_same
from .messages import SPECIAL_CRITICAL,USER_NAME_CHANGE,MAX_TRACKER_LIMIT_REACHED
'''CONNECTOR TO BACKEND'''
class BaseConnector:


    def __init__(self) -> None:
        self.connector = Base()

    
    @staticmethod
    def _tick():
        return str(time())
    
    def _get_last_found_dp(self,user_id:int,tracker_name:str) -> tuple:
        'Get the last store dp'
        logging.debug(f"Getting last found dp for user_id:{user_id} tracker_name:{tracker_name}")
        # Get all continues data's
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')
        # reversed the list
        data_ids.reverse()
        for ids in data_ids:
            dp = self.connector.get_tracker_data(ids).text['dp']
            if dp == None:
                continue
            else:
                logging.debug(f"Last dp found at {ids}")
                return (ids,dp) # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
        logging.debug(f"No dp found ({user_id,tracker_name})")
        return (None,None)
        
        # return (ids,dp)
    def _get_initial_found_dp(self,user_id:int,tracker_name:str) -> tuple:
        'Get the last store dp'
        logging.debug(f"Getting initial dp for user_id:{user_id} tracker_name:{tracker_name}")
        # Get all continues data's
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')

        for ids in data_ids:
            dp = self.connector.get_tracker_data(ids).text['dp']
            if dp == None:
                continue
            else:
                logging.debug(f"Initial dp found at {ids}")
                return (ids,dp) # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
        logging.debug(f"No dp found ({user_id,tracker_name})")
        return (None,None)
        
        # return (ids,dp)
    
    def _get_last_found_bio(self,user_id:int,tracker_name:str) -> tuple:
        'Get the last store bio'
        logging.debug(f"Getting last found bio for user_id:{user_id} tracker_name:{tracker_name}")
        # Get all continues data's
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')
        # reversed the list
        data_ids.reverse()
        for ids in data_ids:
            bio = self.connector.get_tracker_data(ids).text['bio']
            if bio == None:
                continue
            else:
                logging.debug(f"Last bio found at {ids}")
                return (ids,bio) # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
        logging.debug(f"No bio found ({user_id,tracker_name})")
        return (None,None)        
        # return (ids,dp)


    def _get_initial(self,user_id:int,tracker_name:str) -> dict:
        'Get the initial data'
        logging.debug(f"Getting initials for user_id:{user_id} tracker_name:{tracker_name}")
        # Get initial data id
        initial_data = self.connector.get_tracker_data(self.connector.get_initial(user_id,tracker_name).text).text
        initial_dp = self._get_initial_found_dp(user_id,tracker_name)[1]
        initial_data['dp'] = initial_dp
        '''
         {'bio': None,
         'dp': None,
         'follower': 193,
         'following': 847,
         'full_name': 'fullname',
         'isPrivate': True,
         'timestamp': 1703679632.5298285,
         'username': 'user.name'}
        '''
        return initial_data

        
    
    def _get_continuous(self,user_id:int,tracker_name:str) -> dict:

        logging.debug(f"Getting continuous for user_id:{user_id} tracker_name:{tracker_name}")
        # Get all continues data's
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')[1:]
        data = []
        for ids in data_ids:
            data.append(self.connector.get_tracker_data(ids).text)
        '''
        # [{'bio': None,
        # 'dp': None,
        # 'follower': 10,
        # 'following': 795,
        # 'full_name': 'username',
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1070664,
        # 'username': 'username'},
        # ...........
        # ...........
        # {'bio': None,
        # 'dp': None,
        # 'follower': 835,
        # 'following': 757,
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1218953,
        # 'username': 'username'}]   
        '''
        return data

    def _get_last_data(self,user_id:int,tracker_name:str,has_last_dp:bool=True,has_last_bio:bool=True) -> dict:
        'Get the last store data (with or not with last stored dp)'
        logging.debug(f"Getting last store data for user_id:{user_id} tracker_name:{tracker_name} has_last_dp:{has_last_dp} has_last_bio:{has_last_bio}")
        # Get last continues data's id
        last_data_id = self.connector.get_continues(user_id,tracker_name).text.split(',')[-1]
        # id to data dict
        last_data =  self.connector.get_tracker_data(last_data_id).text

        if has_last_dp:
            last_found_dp = self._get_last_found_dp(user_id,tracker_name)[1]
            last_data['dp'] = last_found_dp
        if has_last_bio:
            last_found_bio = self._get_last_found_bio(user_id,tracker_name)[1]
            last_data['bio'] = last_found_bio
        
        return last_data


    def _get_all(self,user_id:int,tracker_name:str) -> dict:
        # 'Get the all store data (both initial, continues)'
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')
        data = []
        for ids in data_ids:
            data.append(self.connector.get_tracker_data(ids).text)
        '''
        # [{'bio': None,
        # 'dp': None,
        # 'follower': 10,
        # 'following': 795,
        # 'full_name': 'username',
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1070664,
        # 'username': 'username'},
        # ...........
        # ...........
        # {'bio': something,
        # 'dp': something,
        # 'follower': 835,
        # 'following': 757,
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1218953,
        # 'username': 'username'}]   
        '''
        return data
 
    
    # Add tracker
    def add_new_tracker(self,update:Update,data:TrackinstaDataModel) -> StandardResponse:
        tele_user = update.effective_user
        # check if user exits
        is_user = self.connector.if_user(tele_user.id)
        # check if this user already tracking this user
        is_tracking = data.username in self.connector.get_all_tracker(tele_user.id).text

        if not is_user and not is_tracking:
            logging.debug(f"Registering new user user data {tele_user.username} ")
            success = self.connector.resister(
                username=tele_user.username,
                user_id=tele_user.id,
                first_name=tele_user.first_name,
                last_name=tele_user.last_name,
                TrackerDataModel=data
            
            )
            return success

        elif is_user and not is_tracking:
            # add initial data
            logging.debug(f"Adding new tracker for {tele_user.username} tracker={data.username} ")
            trackerdata = self.connector.add_trackerData(data)
            if trackerdata.code == 200:
                tracker_success = self.connector.add_tracker(
                    initial_data=data.uid,
                    tracker_name=data.username,
                    user_id=tele_user.id
                )
                if tracker_success.code == 200:
                    return StandardResponse.success()
                else:
                    # rollback
                    self.connector.remove_trackerData(data.uid)
                    return tracker_success


        elif is_user and is_tracking:
            logging.debug(f"Resuming tracker for {tele_user.username} tracker={data.username} ")
            # self.add_tracker_data(update,data)
            return StandardResponse.success()
            
        else:
            logging.critical(SPECIAL_CRITICAL)
            return StandardResponse.standard_error(SPECIAL_CRITICAL)


    # # # pprint(b.add_trackerData(data))
    def add_tracker_data(self,update:Update,data:TrackinstaDataModel) -> StandardResponse:
        tele_user = update.effective_user
        user_id = tele_user.id
        username_aka_trackername = data.username
        uid = data.uid
        logging.debug(f"Adding tracker data uid:{uid} ,user_id:{user_id}, tracker_name:{username_aka_trackername} ")
        # step 1: Find the tracker in db with user_id and tracker_name (primary keys)
        tracker = self.connector.find_tracker(user_id,username_aka_trackername)
        # step 1.1: if instagram user name is not change (instagram username is tracker_name)
        if tracker.code == 200:
            # add data to data table
            '''Compare dps to check if dp as changed or not'''
            try:
                iD,last_found_dp = self._get_last_found_dp(user_id,username_aka_trackername)
            except TypeError:
                last_found_dp = None

            if data.dp == last_found_dp:
                data.dp = None
            else:
                if are_images_same(last_found_dp,data.dp):
                    self.connector.get_tracker_data_obj(iD).text.dp = None

            '''Compare bio's to check if bio as changed or not'''
            try:
                # if _get_last_found_bio returns None
                last_found_bio = self._get_last_found_bio(user_id,username_aka_trackername)[1]
            except TypeError:
                last_found_bio = None
                
            if data.bio == last_found_bio:
                data.bio = None
                

            add_data = self.connector.add_trackerData(data)
            if add_data.code == 200:
                # store data id to tracker table
                add_data_id = self.connector.add_continues(user_id,username_aka_trackername,uid)
                if add_data_id.code == 200:
                    return StandardResponse.success()
                else:
                    # Rollback
                    self.connector.remove_trackerData(uid)
                

            ...
        # step 1.2: if instagram user name is change (instagram username is tracker_name)
        elif tracker.code == 404:
            # step 1.2.2:check if user
            print(USER_NAME_CHANGE)
            ...
            

    def remove_tracker(self,user_id,tracker_name):
        # find the tracker
        r_tracker = self.connector.find_tracker(user_id,tracker_name)
        logging.debug(f"Deleting tracker (user_id:{user_id}, tracker_name:{tracker_name}) ")
    
        # connector.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        if r_tracker.code == 200:
            # Get all continues
            continues_ids = r_tracker.kwargs['tracker'].continues_data.split(',')
            total_ids = len(continues_ids)
            success = 0
            # remove all continues id (or do I 😏)
            for ids in continues_ids:
                res = self.connector.remove_trackerData(ids)
                if res.code == 200:
                    success += 1

            remove_tracker = self.connector.remove_tracker(user_id,tracker_name)
            logging.debug(f'Tracker removed code:{remove_tracker.code}.(Total {total_ids}, Success {success}, Failed {total_ids-success})')
            return StandardResponse.success(text='Tracker removed code')
        
        logging.error(f'No Tracker found with (user_id:{user_id}, tracker_name:{tracker_name})')
        return StandardResponse.null_error(f'No Tracker found with (user_id:{user_id}, tracker_name:{tracker_name})')
    
    def get_all_active_tracker(self,user_id):
        return self.connector.get_all_tracker(user_id=user_id)
    
    def get_tracker_data_by_column(self,user_id:int,tracker_name:str,column_name:str) -> list:
        logging.debug(f'Getting {column_name} column from user_id:{user_id} tracker_name:{tracker_name}')
        continue_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')
        column_data = []
        for ids in continue_ids:
            time = self.connector.get_tracker_data(ids).text
            time = time[column_name]
            column_data.append(time)
        
        return column_data




class Converter:
    def format(self,data:dict):
        username = data['username']
        full_name = data['full_name']
        follower =  data['follower']
        following =  data['following']
        isPrivate = data['isPrivate']
        verified = data['verified']
        bio = data['bio']
        dp = data['dp']
        timestamp = data['timestamp']

        # print(data[i]['timestamp'])
        converted = {
            timestamp : {
                'username' : username,
                'full_name':full_name,
                'follower':follower,
                'following':following,
                'isPrivate':isPrivate,
                'verified':verified,
                'bio':bio,
                'dp':dp

            }
        }
        return converted


class Connector(BaseConnector,Converter):
    def __init__(self,user_id:int,username:str) -> None:
        super().__init__()
        self.user_id = user_id
        self.tracker_name = username
    

    def tracker_limit(self,user_id):
        if self.connector.if_user(user_id):
            if self.connector.get_active_trackers_count(user_id) >= self.connector.MAX_TRACKER_LIMIT and not self.connector.find_tracker(self.user_id,self.tracker_name):
                return StandardResponse.limit_reached(MAX_TRACKER_LIMIT_REACHED)
            else:
                return StandardResponse.success()
        return StandardResponse.success()
     
    def get_last_log(self,has_last_dp:bool=True,has_last_bio:bool=True):
        return self.format(self._get_last_data(user_id=self.user_id,tracker_name=self.tracker_name, has_last_dp=has_last_dp,has_last_bio=has_last_bio))

        
    def get_users_all_active_tracker(self):
        return self.get_all_active_tracker(self.user_id)    

class ConnectorUtils(BaseConnector,Converter):
    def __init__(self, user_id, username:str) -> None:        
        super().__init__()
        self.user_id = user_id
        self.tracker_name = username
    
    def getInitials(self) -> dict:
        return self.format(self._get_initial(self.user_id,self.tracker_name))

    
    def getStatus(self) -> dict:
        return self.format(self._get_last_data(self.user_id,self.tracker_name))
    
    def getPreviousData(self) -> dict[dict]:
        all_logs = self._get_all(self.user_id,self.tracker_name)
        converted = {}
        for logs in all_logs:
            converted.update(self.format(logs))
        return converted
    
    def getLogData(self) -> dict[dict]:
        all_logs = self._get_continuous(self.user_id,self.tracker_name)
        converted = {}
        for logs in all_logs:
            converted.update(self.format(logs))
        return converted

        