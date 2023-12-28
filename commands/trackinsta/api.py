import logging
from pprint import pprint
# from configurations.settings import DB_API_TOKEN,DB_PATH
from time import time
from models.trackinsta.types import TrackinstaDataModel
from db.Base import Base
from db.standard_response import StandardResponse
from telegram import Update

'''CONNECTOR TO BACKEND'''
class BaseConnector:


    def __init__(self) -> None:
        self.connector = Base()

    
    @staticmethod
    def _tick():
        return str(time())
    
    def _get_last_found_dp(self,user_id:int,tracker_name:str) -> tuple:
        'Get the last store dp'
        # Get all continues data's
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')
        # reversed the list
        data_ids.reverse()
        for ids in data_ids:
            dp = self.connector.get_tracker_data(ids).text['dp']
            if dp == None:
                continue
            else:
                return (ids,dp) # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
        
        # return (ids,dp)
    
    def _get_last_found_bio(self,user_id:int,tracker_name:str) -> tuple:
        'Get the last store bio'
        # Get all continues data's
        data_ids = self.connector.get_continues(user_id,tracker_name).text.split(',')
        # reversed the list
        data_ids.reverse()
        for ids in data_ids:
            bio = self.connector.get_tracker_data(ids).text['bio']
            if bio == None:
                continue
            else:
                return (ids,bio) # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
        
        # return (ids,dp)
        



    def _get_initial(self,user_id:int,tracker_name:str) -> dict:
        'Get the initial data'
        # Get initial data id
        initial_data = self.connector.get_tracker_data(self.connector.get_initial(user_id,tracker_name).text).text
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
        'Get the last store dp'
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
        # 'full_name': 'afnan.aksa',
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1070664,
        # 'username': 'afnan.aksa'},
        # ...........
        # ...........
        # {'bio': None,
        # 'dp': None,
        # 'follower': 835,
        # 'following': 757,
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1218953,
        # 'username': 'afnan.aksa'}]   
        '''
        return data

    def _get_last_data(self,user_id:int,tracker_name:str,has_last_dp:bool=True,has_last_bio:bool=True) -> dict:
        'Get the last store data (with or not with last stored dp)'
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
        # 'full_name': 'afnan.aksa',
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1070664,
        # 'username': 'afnan.aksa'},
        # ...........
        # ...........
        # {'bio': None,
        # 'dp': None,
        # 'follower': 835,
        # 'following': 757,
        # 'isPrivate': True,
        # 'timestamp': 1703680581.1218953,
        # 'username': 'afnan.aksa'}]   
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
            self.connector.add_continues(tele_user.id,data.username,data.uid)
            self.connector.add_trackerData(data_model=data)
            return StandardResponse.success("Already tracking this user")
            
        else:
            logging.critical("Fuck!! someone hacked me!!!!!!!!!!")
            return StandardResponse.standard_error("Fuck!! someone hacked me!!!!!!!!!!")


    # # # pprint(b.add_trackerData(data))
    def add_tracker_data(self,update:Update,data:TrackinstaDataModel) -> StandardResponse:
        tele_user = update.effective_user
        user_id = tele_user.id
        username_aka_trackername = data.username
        uid = data.uid
        # step 1: Find the tracker in db with user_id and tracker_name (primary keys)
        tracker = self.connector.find_tracker(user_id,username_aka_trackername)
        # step 1.1: if instagram user name is not change (instagram username is tracker_name)
        if tracker.code == 200:
            # add data to data table
            '''Compare dps to check if dp as changed or not'''
            last_found_dp = self._get_last_found_dp(user_id,username_aka_trackername)[1]
            if data.dp == last_found_dp:
                data.dp = None
            else:
                data.dp = last_found_dp           
            '''Compare bio's to check if bio as changed or not'''
            last_found_bio = self._get_last_found_bio(user_id,username_aka_trackername)[1]
            if data.bio == last_found_bio:
                data.bio = None
            else:
                data.bio = last_found_bio           
                

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
            print("User name change maybe??")
            ...
            

    def remove_tracker(self,user_id,tracker_name):
        # find the tracker
        r_tracker = self.connector.find_tracker(user_id,tracker_name)
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

            self.connector.remove_tracker(user_id,tracker_name)
            return StandardResponse.success(text=f'Total {total_ids}, Success {success}, Failed {total_ids-success}')
        
        logging.error(f'No Tracker found with (user_id:{user_id}, tracker_name:{tracker_name})')
        return StandardResponse.null_error(f'No Tracker found with (user_id:{user_id}, tracker_name:{tracker_name})')
    
    def get_all_active_tracker(self,user_id):
        return self.connector.get_all_tracker(user_id=user_id)


class Converter:

    def format(self,data:dict):
        username = data['username']
        full_name = data['full_name']
        follower =  data['follower']
        following =  data['following']
        isPrivate = data['isPrivate']
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
        if self.connector.get_active_trackers_count(user_id) >= self.connector.MAX_TRACKER_LIMIT:
            return StandardResponse.limit_reached("Max tracker limits reached!")
        else:
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

            


if __name__ == "__main__":
    # conn = Connector('trackinsta','emi_lyitachi')
    # data = {
    #     "username":conn.username,
    #     "full_name":'full_name',
    #     "follower":12,
    #     "following":32,
    #     "isPrivate":True,
    #     "bio": None,
    #     "dp": 'url changed again',
    #     }
    
    # dataModel = TrackinstaDataModel(**data)
    # # print(conn.add_tracker(data=dataModel))
    # print(conn.getPreviousData())
        
        # print(converted)
    bc = BaseConnector()
    bc._get_last_found_dp(6969696969,'afnan.aksa')