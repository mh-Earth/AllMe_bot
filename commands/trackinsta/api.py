
import instaloader
from dotenv import load_dotenv
import logging
import requests
import json
from dataclasses import dataclass
from configurations.settings import INSTA_USERNAME,DB_PATH
from time import time
load_dotenv()

@dataclass
class TrackinstaTypes:
    username:str
    follower:int
    following:int
    full_name:str=None
    bio:str=None
    isPrivate:bool=False
    dp:str=None

    def data(self):
        return {
            'username':self.username,
            'full_name':self.full_name,
            'bio':self.bio,
            'follower':self.follower,
            'following':self.following,
            'isPrivate':self.isPrivate,
            'dp':self.dp
        }


'''
Class for interacting with instagram
'''
class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.username = username

    '''Same as getPublic data bt with profile picture'''
    def checkout(self):
        is_id_exits = self.lookup()
        if is_id_exits:
            self.profile = instaloader.Profile.from_username(self.L.context, self.username)
            # full name
            full_name = self.profile.full_name
            # follower
            follower = self.profile.followers
            # followee
            followee = self.profile.followees
            # isPrivate
            isPrivate = self.profile.is_private
            # bio
            bio = self.profile.biography
            # DP
            DP = self.profile.profile_pic_url
            # biography_mentions = self.profile.biography_mentions
            profile_url = f"https://www.instagram.com/{self.username}/"


            return {
                "username":self.username,
                "full_name":full_name,
                "follower":follower,
                "following":followee,
                "isPrivate":isPrivate,
                "bio": bio,
                "dp": DP,
            }

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return 
    
    def publicData(self,initial:bool=False):
        is_id_exits = self.lookup()
        if is_id_exits:
            self.profile = instaloader.Profile.from_username(self.L.context, self.username)
            # full name
            full_name = self.profile.full_name
            # follower
            follower = self.profile.followers
            # followee
            followee = self.profile.followees
            # isPrivate
            isPrivate = self.profile.is_private
            # bio
            bio = self.profile.biography
            dp = self.profile.profile_pic_url if initial else None

            return {
                "username":self.username,
                "full_name":full_name,
                "follower":follower,
                "following":followee,
                "isPrivate":isPrivate,
                "bio": bio,
                'dp':dp

                }

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return 
    
    def lookup(self):
        try:
            return True if instaloader.Profile.from_username(self.L.context,self.username) else False
        except Exception as e:
            logging.error(e)
            try:
                logging.warning(f"{e}. Trying to load session")
                try:

                    self.L.load_session_from_file(INSTA_USERNAME,"session-emi_lyitachi")
                except:
                    logging.error("Failed to load session for instagram")
                    return False
                return True if instaloader.Profile.from_username(self.L.context,self.username) else False
            except Exception as e:
                logging.error(e)
                return False

'''CONNECTOR TO BACKEND'''
class BaseConnector:

    def __init__(self,command:str ,username:str) -> None:
        self.command = command
        self.username = username
        self.dbPath = f"{DB_PATH}/api/{self.command}s"
        self.idLocation = 'data[0].id'
        self.logFiled = "logs"
        self.DB_API_TOKEN = '6e48cd3c19bda1817afad46c90f267d046bfc0e2c1c2895d829f9363c1518847ca381763848741bba5e21cc493c748e4ff5e92e29ced64c7c75f864f1111e2a1c3cb82851b1a49f2ef1476fa72135179345b6c7089d8cd4d3958c1eae8789e182cb6d5fcdfd8dceba59c3b9bc0f0efa8796fb34789704d7fdfbcd4772261e4ec'
    
    @staticmethod
    def _tick():
        return str(time())
    
    def _username_to_id(self) -> int:
        url = f"{self.dbPath}?{self._filter_username(self.username)}"
        logging.info(url)
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[_username_to_id] [code:{res.status_code}] {res.text}')
            return
        
        data = json.loads(res.text)
        return data['data'][0]['id']
    
    def _get_initial(self) -> dict:
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._type_filter('initial')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=initial
        logging.info(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[_get_initial] [code:{res.status_code}] {res.text}')
            return


        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled][0]

        if len(initials) == 0:
            return {'error':'No initials found'}
        else:
            return initials
    
    def get_continuous(self):
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._type_filter('continuous')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=continuous
        logging.info(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"

        }
        res = requests.get(url,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[get_continuous] [code:{res.status_code}] {res.text}')
            return

        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled]

        if len(initials) == 0:
            return {'error':'No initials found'}
        else:
            return initials

    def _get_last_data(self) -> dict:
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._populate(self.logFiled)}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate=data
        logging.info(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[_get_last_data] [code:{res.status_code}] {res.text}')
            return

        data = json.loads(res.text)
        data = data['data'][0]['attributes']['logs'][-1]

        return data
    def _get_all(self) -> list[dict]:

        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._populate(self.logFiled)}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate=data
        logging.info(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[_get_all] [code:{res.status_code}] {res.text}')
            return
        data = json.loads(res.text)
        data = data['data'][0]['attributes'][self.logFiled]
        # print(data)

        return data
    
    # Add tracker
    def add_tracker(self,data:TrackinstaTypes) -> requests.Response:
        url = f"{self.dbPath}"
        (username,full_name,bio,follower,following,isPrivate,dp) = data.data().values()
        dType = 'initial'
        timestamp = self._tick()
        logging.info(url)
        # http://localhost:1337/api/trackinstas
        payloads = {
            "data": {
                "username": username,
                "logs": [
                {
                    "username": username,
                    "full_name": full_name,
                    "bio": bio,
                    "follower": follower,
                    "following": following,
                    "isPrivate": isPrivate,
                    "type":dType,
                    "timestamp":timestamp,
                    "dp": dp
                }
                ]
            }
        }
        payloads = json.dumps(payloads)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        "Content-Type": "application/json" 
        }
        try:
            res = requests.post(url,data=payloads,headers=headersList)
            if res.status_code == 200:
                return res
            elif res.status_code == 400:
                raise ValueError
            else:
                logging.error(res.text)
                return res

        except ValueError as e:
            new_data = {
                    "username": username,
                    "full_name": full_name,
                    "bio": bio,
                    "follower": follower,
                    "following": following,
                    "isPrivate": isPrivate,
                    "dp": dp
            }
            new_trackinstaObj = TrackinstaTypes(**new_data)
            res = self.add_log(data=new_trackinstaObj)
            if res.status_code != 200:
                logging.error(f'[add_tracker] [code:{res.status_code}] {res.text}')
                return

            return res

    
    def add_log(self,data:TrackinstaTypes) -> requests.Response:
        Id = self._username_to_id()
        url = f"{self.dbPath}/{Id}"
        # http://localhost:1337/api/trackinstas/:id
        (username,full_name,bio,follower,following,isPrivate,dp) = data.data().values()
        timestamp = self._tick()
        dType = 'continuous'

        previous_data = self._get_all()
        previous_data.append({
            "username": username,
            "full_name": full_name if full_name != '' else None,
            "bio": bio,
            "follower": follower,
            "following": following,
            "isPrivate": isPrivate,
            "type": dType,
            "timestamp":timestamp,
            "dp": None

        })
        payloads = {
            "data": {
                "logs":previous_data
            }
        }
        payloads = json.dumps(payloads)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        "Content-Type": "application/json" 
        }

        res = requests.put(url,data=payloads,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[add_log] [code:{res.status_code}] {res.text}')
            return
        return res

    def delete_tracker(self) -> requests.Response:
        Id = self._username_to_id()
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        }
        url = f'{self.dbPath}/{Id}'
        res = requests.delete(url,headers=headersList)
        if res.status_code != 200:
            logging.error(f'[delete_tracker] [code:{res.status_code}] {res.text}')
            return
        return res
    
    def _filter_username(self,username):
        return f"filters[username][$eq]={username}"
    def _type_filter(self,type:str):
        return f"populate[{self.logFiled}][filters][type][$eq]={type}"
    def _populate(self,filed:str="*"):
        return f'populate={filed}'




class Connector(BaseConnector):
    def __init__(self, command: str, username: str) -> None:
        super().__init__(command, username)

    def format(self,data:dict):
        username = data['username']
        full_name = data['full_name']
        follower =  data['follower']
        following =  data['following']
        isPrivate = data['isPrivate']
        bio = data['bio']
        timestamp = data['timestamp']
        dp = data['dp']


        # print(data[i]['timestamp'])
        converted = {
            timestamp : {
                'Username' : username,
                'Full name':full_name if full_name != None else "",
                'Follower':int(follower),
                'Following':int(following),
                'isPrivate':isPrivate,
                'Bio':bio,
                'DP':dp

            }
        }
        return converted
    

    def format_raw(self,data:dict):
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
                'full_name':full_name if full_name != None else "",
                'follower':int(follower),
                'following':int(following),
                'isPrivate':isPrivate,
                'bio':bio,
                'dp':dp

            }
        }
        return converted
    
    def getInitials(self) -> dict:
        return self.format(self._get_initial())
    
    def last_stored_log(self) -> dict:
        return self.format_raw(self._get_last_data())

    
    def getStatus(self) -> dict:
        return self.format(self._get_last_data())
    def getHistory(self) -> dict[dict]:
        all_logs = self._get_all()
        converted = {}
        for logs in all_logs:
            converted.update(self.format(logs))
        return converted
    def getPreviousData(self) -> dict[dict]:
        all_logs = self._get_all()
        converted = {}
        for logs in all_logs:
            converted.update(self.format_raw(logs))
        return converted
            
        
        # print(converted)