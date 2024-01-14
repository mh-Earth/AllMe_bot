import uuid
import logging
from configurations.settings import MAX_DATA_TO_STORE_LIMIT,MAX_TRACKER_LIMIT

try:

    from .connect import session
    from .models import TrackinstaData,User,Trackers
    from .dataModels import TrackinstaDataModel
    from .standard_response import StandardResponse
except ImportError:
    from connect import session
    from models import TrackinstaData,User,Trackers
    from dataModels import TrackinstaDataModel
    from standard_response import StandardResponse


class Base:
    MAX_DATA_LIMIT = MAX_DATA_TO_STORE_LIMIT
    MAX_TRACKER_LIMIT = MAX_TRACKER_LIMIT
    NO_TRACKER_FOUND_BY_USERID_AND_NAME = 'No Tracker found with (user_id:{0}, tracker_name:{1})'

    def __init__(self) -> None:
        self.session = session
        pass
    
    def _gen_uuid(self) ->str:
        return str(uuid.uuid4())

    def _to_dict(self,result:TrackinstaData) -> dict:

        to_dict = {
            'username':result.username,
            'full_name':result.full_name,
            'follower':result.follower,
            'following':result.following,
            'isPrivate':result.isPrivate,
            'verified':result.verified,
            'bio':result.bio,
            'dp':result.dp,
            'timestamp':result.timestamp
        }
        return to_dict

    def get_initial(self,user_id:int, tracker_name:str) -> StandardResponse:
        logging.debug(f'Queuing tracker ({user_id},{tracker_name} for initial_ids)')
        # if tracker exits
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        if tracker:
            return StandardResponse.success(text=tracker.initial_data)
        logging.error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))
        return StandardResponse.null_error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))

    def get_continues(self,user_id:int, tracker_name:str) -> StandardResponse:
        logging.debug(f'Queuing tracker ({user_id},{tracker_name} for continues_ids)')
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        if tracker:
            return StandardResponse.success(text=tracker.continues_data)
        logging.error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))
        return StandardResponse.null_error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))

        
    def add_tracker(self,tracker_name:str,initial_data:str,user_id:int=None) -> StandardResponse:
        # check for one user max tracker limit
        if self.get_active_trackers_count(user_id) >= self.MAX_TRACKER_LIMIT:
            logging.info(f'Max Tracker limit reached for {user_id}')
            return StandardResponse.limit_reached("Max tracker limits reached!")
        
        # check if tracker with same primary keys (user_id,tracker) exits
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).count()
        if tracker > 0:
            logging.error(f'Tracker:{tracker_name} user_id:{user_id} already exits!!!')
            return StandardResponse(500,f'Tracker:{tracker_name} user_id:{user_id} already exits!!!')
        # Add tracker
        tracker = Trackers(
            user_id=user_id,
            tracker_name=tracker_name,
            initial_data=initial_data,
            continues_data=initial_data,
        )
        self.increase_active_trackers_count(user_id)
        self.session.add(tracker)
        self.session.commit()
        return StandardResponse.success()

    def find_tracker(self,user_id:int,tracker_name:str) -> StandardResponse:
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        if tracker:
            return StandardResponse.success(tracker=tracker)
        else:
            return StandardResponse.null_error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))



    def add_continues(self,user_id,tracker_name,new_continues_data) -> StandardResponse:
        # continues data are long string of TrackerData ids "uuid4,uuid4,uuid4..."

        # step 1:Get Tracker entry
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        # step 1.1:
        if tracker:
            # step 2:Get the continues data
            old_data = tracker.continues_data
            # step 3:Add new data to old data string
            new_data = old_data + f',{new_continues_data}'
            # step 4:Store the new data string
            tracker.continues_data = new_data
            # step 5:Commit the change
            self.session.commit()
            return StandardResponse.success()
        logging.error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))
        return StandardResponse.standard_error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))

    def remove_continues(self,user_id,tracker_name,continues_data) -> StandardResponse:
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        continues_ids = tracker.continues_data.split(',')
        try:
            continues_ids.remove(continues_data)
        except ValueError:
            return StandardResponse.null_error(f'Id:{continues_data} not in {tracker}')
        new_continues_data = ",".join(continues_ids)
        tracker.continues_data = new_continues_data
        self.session.commit()
        return StandardResponse.success()


        
        
    def add_initial(self,user_id,tracker_name,new_initial_data):
        '''
         this will over-write the old initial data
        '''
        # step 1:Get Tracker entry
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        # step 1.1:
        if tracker:
            # step 2:change old initial data
            tracker.initial_data = new_initial_data
            # step 3:Commit the change
            self.session.commit()
            return StandardResponse.success()
        logging.error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))
        StandardResponse.null_error( self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))

    def add_trackerData(self,data_model:TrackinstaDataModel) -> StandardResponse:

        '''
        Add tracker instagram data. UNIQUE=False
        '''
        try:
            trackerdata = TrackinstaData(**data_model())
            self.session.add(trackerdata)
            self.session.commit()
            return StandardResponse.success(self._to_dict(trackerdata))
        except Exception as e:
            return StandardResponse.standard_error(e)
    
    def remove_trackerData(self,uid:str):
        
        try:
            data = self.session.query(TrackinstaData).filter_by(uid=uid).first()
            self.session.delete(data)
            self.session.commit()
            return StandardResponse.success()
        except Exception as e:
            return StandardResponse.standard_error(e)


    
    def get_tracker_data(self,uid:str)-> StandardResponse:
        logging.debug(f'Getting tracker data : {uid}')
        data = self.session.query(TrackinstaData).filter_by(uid=uid).first()
        if data:
            return StandardResponse.success(self._to_dict(data))
        logging.error(f'No entry found Uid:{uid}')
        return StandardResponse.null_error(text=f'No entry found Uid:{uid}')

    
    def get_tracker_data_obj(self,uid:str)-> StandardResponse:
        logging.debug(f'Getting tracker data object : {uid}')
        data = self.session.query(TrackinstaData).filter_by(uid=uid).first()
        if data:
            return StandardResponse.success(data)
        logging.error(f'No entry found Uid:{uid}')
        return StandardResponse.null_error(text=f'No entry found Uid:{uid}')



    def add_user(self,user_id:int,first_name:str,last_name:str,trackers:list[TrackinstaData]) -> StandardResponse:

        # check if user with same id already exits
        users = self.session.query(User).filter_by(user_id=user_id).count()
        if users > 0:
            logging.error(f'User with user ID:{user_id} already exits!!!')
            return StandardResponse.duplication_error(f'User with user ID:{user_id} already exits!!!')
        # 
        try:
            user = User(
                user_id=user_id,
                first=first_name,
                last=last_name,
                trackers=trackers,
                active_tracker=0
            )
            self.session.add(user)
            self.session.commit()
            return StandardResponse.success()
        except Exception as e:
            return StandardResponse.standard_error(e)
    
    def if_user(self,user_id:int) -> bool:
        user = self.session.query(User).filter_by(user_id=user_id).count()
        if user > 0:
            return True
        return False

    def get_all_tracker(self,user_id) -> StandardResponse:
        '''Get all trackers for a users'''    
        trackers = self.session.query(Trackers).filter_by(user_id=user_id)
        return StandardResponse.success([tracker.tracker_name for tracker in trackers])
    
    def get_active_trackers_count(self,user_id:int) -> int:
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user.active_tracker
    
    def set_active_trackers_count(self,user_id:int,count:int) -> StandardResponse:
        user = self.session.query(User).filter_by(user_id=user_id).first()
        user.active_tracker = count
        self.session.commit()
        return StandardResponse.success()
    
    def increase_active_trackers_count(self,user_id):
        try:
            user = self.session.query(User).filter_by(user_id=user_id).first()
            user.active_tracker += 1
            self.session.commit()
        except Exception as e:
            logging.error(f"An error course while increasing the active_trackers count. Error {e}")
            return StandardResponse.standard_error(e)
    def decrease_active_trackers_count(self,user_id):
        try:
            user = self.session.query(User).filter_by(user_id=user_id).first()
            user.active_tracker -= 1
            self.session.commit()
        except Exception as e:
            logging.error(f"An error course while decreasing the active_trackers count. Error {e}")
            return StandardResponse.standard_error(e)
    
    def increase_total_data_count(self,user_id:int,tracker_name:str):
        try:
            tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name) .first()
            tracker.total_data += 1
            self.session.commit()
        except Exception as e:
            logging.error(f"An error course while increasing the total_data count. Error {e}")
            return StandardResponse.standard_error(e)
        return StandardResponse.success()
    def decrease_total_data_count(self,user_id:int,tracker_name:str):
        try:
            tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name) .first()
            tracker.total_data -= 1
            self.session.commit()
        except Exception as e:
            logging.error(f"An error course while decreasing the total_data count. Error {e}")
            return StandardResponse.standard_error(e)
        return StandardResponse.success()



    def resister(self,username:str,user_id:int,first_name:str,last_name:str,TrackerDataModel:TrackinstaDataModel) -> StandardResponse:
        '''
        Resister a user in User Table and add a new tracker with all data necessary

        '''
        user = self.session.query(User).filter_by(user_id=user_id).count()
    
        if user > 0:
            logging.error(f'User with user id {user_id} already exits')
            return StandardResponse.duplication_error(f'User with user id {user_id} already exits')
        
        try:
            TrackerData = TrackinstaData(**TrackerDataModel())

            tracker = Trackers(
                tracker_name=TrackerData.username,
                initial_data=TrackerData.uid,
                continues_data=TrackerData.uid

            )

            user = User(
                username=username,
                user_id=user_id,
                first=first_name,
                last=last_name,
                trackers=[tracker],
                active_tracker=1

            )

            self.session.add_all([TrackerData,user])
            self.session.commit()
            return StandardResponse.success()
        except Exception as e:
            return StandardResponse.standard_error(e)
        
    def remove_tracker(self,user_id:int,tracker_name:str) -> StandardResponse:
        tracker = self.session.query(Trackers).filter_by(user_id=user_id).filter_by(tracker_name=tracker_name).first()
        if tracker:
            self.session.delete(tracker)
            self.decrease_active_trackers_count(user_id)
            self.session.commit()
            logging.info(f"Tracker {tracker} delete")
            return StandardResponse.success(f"Tracker {tracker} delete")
        else:
            logging.error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))
            return StandardResponse.null_error(self.NO_TRACKER_FOUND_BY_USERID_AND_NAME.format(user_id,tracker_name))

            


