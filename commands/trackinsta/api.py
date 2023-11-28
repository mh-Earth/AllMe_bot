
import instaloader
from dotenv import load_dotenv
import logging
import os
import requests
import json
from dataclasses import dataclass
from configurations.settings import INSTA_USERNAME
load_dotenv()



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
                "Username":self.username,
                "Full name":full_name,
                "Follower":follower,
                "Following":followee,
                "Private":isPrivate,
                "Bio":bio,
                "DP":DP,
                "URL": profile_url
            }

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return 
    
    def publicData(self):
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

            return {
                "Username":self.username,
                "Full name":full_name,
                "Follower":follower,
                "Following":followee,
                "Private":isPrivate,
                "Bio":bio,
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

@dataclass
class TrackinstaTypes:
    username:str
    follower:int
    following:int
    dType:str
    timestamp:str
    full_name:str=None
    bio:str=None
    isPrivate:bool=False
    dp:str=None

    def data(self):
        return [
            self.username,
            self.full_name,
            self.bio,
            self.follower,
            self.following,
            self.isPrivate,
            self.dType,
            self.timestamp,
            self.dp
        ]


class Connector:

    def __init__(self,command:str ,username:str) -> None:
        self.command = command
        self.username = username
        self.dbPath = f"https://allme-bot-strapi.onrender.com/api/{self.command}s"
        self.idLocation = 'data[0].id'
        self.logFiled = "logs"
        self.DB_API_TOKEN = '6e48cd3c19bda1817afad46c90f267d046bfc0e2c1c2895d829f9363c1518847ca381763848741bba5e21cc493c748e4ff5e92e29ced64c7c75f864f1111e2a1c3cb82851b1a49f2ef1476fa72135179345b6c7089d8cd4d3958c1eae8789e182cb6d5fcdfd8dceba59c3b9bc0f0efa8796fb34789704d7fdfbcd4772261e4ec'
    
    def username_to_id(self) -> int:
        url = f"{self.dbPath}?{self._filter_username(self.username)}"
        print(url)
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        return data['data'][0]['id']
    
    def get_initial(self):
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._type_filter('initial')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=initial
        print(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled]

        if len(initials) == 0:
            return {'error':'No initials found'}
        else:
            return initials
    
    def get_continuous(self):
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._type_filter('continuous')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=continuous
        print(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"

        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled]

        if len(initials) == 0:
            return {'error':'No initials found'}
        else:
            return initials

    def get_last_data(self):
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._populate(self.logFiled)}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate=data
        print(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        data = data['data'][0]['attributes']['logs'][-1]

        return data
    def get_all(self) -> list[dict]:

        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._populate(self.logFiled)}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate=data
        print(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        data = data['data'][0]['attributes'][self.logFiled]

        return data
    
    # Add tracker
    def add_tracker(self,data:TrackinstaTypes) -> int:
        url = f"{self.dbPath}"
        username,full_name,bio,follower,following,isPrivate,dType,timestamp,dp = data.data()
        dType = 'initial'
        print(url)
        # http://localhost:1337/api/trackinstas
        payloads = {
            "data": {
                "username": username,
                "logs": [
                {
                    "username": username,
                    "full_name": full_name,
                    "bio": bio,
                    "followers": follower,
                    "followings": following,
                    "isPrivate": isPrivate,
                    "type": dType,
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
        res = requests.post(url,data=payloads,headers=headersList)
        return res.status_code
    
    def update_tracker(self,data:TrackinstaTypes):
        Id = self.username_to_id()
        url = f"{self.dbPath}/{Id}"
        # http://localhost:1337/api/trackinstas/:id
        username,full_name,bio,follower,following,isPrivate,dType,timestamp,dp = data.data()
        dType = 'continuous'

        previous_data = self.get_all()

        previous_data.append({
            "username": username if username != None else None,
            "full_name": full_name if full_name != None else None,
            "bio": bio if bio != None else None,
            "followers": follower if follower != None else None,
            "followings": following if following != None else None,
            "isPrivate": isPrivate if isPrivate != None else None,
            "type": dType,
            "timestamp":timestamp if timestamp != None else None,
            "dp": dp if dp != None else None

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
        return res.status_code

    def delete_tracker(self):
        Id = self.username_to_id()
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        }
        url = f'{self.dbPath}/{Id}'
        res = requests.delete(url,headers=headersList)

        return res.status_code
    
    def _filter_username(self,username):
        return f"filters[username][$eq]={username}"
    def _type_filter(self,type:str):
        return f"populate[{self.logFiled}][filters][type][$eq]={type}"
    def _populate(self,filed:str="*"):
        return f'populate={filed}'


