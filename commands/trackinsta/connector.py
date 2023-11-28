import requests
import json
from dataclasses import dataclass
from time import time
# from configurations.settings import DB_API_TOKEN
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


class BaseConnector:

    def __init__(self,command:str ,username:str) -> None:
        self.command = command
        self.username = username
        self.dbPath = f"https://allme-bot-strapi.onrender.com/api/{self.command}s"
        self.idLocation = 'data[0].id'
        self.logFiled = "logs"
        self.DB_API_TOKEN = '6e48cd3c19bda1817afad46c90f267d046bfc0e2c1c2895d829f9363c1518847ca381763848741bba5e21cc493c748e4ff5e92e29ced64c7c75f864f1111e2a1c3cb82851b1a49f2ef1476fa72135179345b6c7089d8cd4d3958c1eae8789e182cb6d5fcdfd8dceba59c3b9bc0f0efa8796fb34789704d7fdfbcd4772261e4ec'
    
    def _username_to_id(self) -> int:
        url = f"{self.dbPath}?{self._filter_username(self.username)}"
        print(url)
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        return data['data'][0]['id']
    
    def _get_initial(self) -> dict:
        url = f"{self.dbPath}?{self._filter_username(self.username)}&{self._type_filter('initial')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=initial
        print(url)
        headersList = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headersList)
        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled][0]

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

    def _get_last_data(self) -> dict:
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
    def _get_all(self) -> list[dict]:

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
        Id = self._username_to_id()
        url = f"{self.dbPath}/{Id}"
        # http://localhost:1337/api/trackinstas/:id
        username,full_name,bio,follower,following,isPrivate,dType,timestamp,dp = data.data()
        dType = 'continuous'

        previous_data = self._get_all()

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
        Id = self._username_to_id()
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




# c = Connector("trackinsta","emi_lyitachi2")
# data = TrackinstaTypes(username=c.username,follower=3,following=17,dType='continuous',timestamp=str(time()))
# initial = c.get_initial()

class Connector(BaseConnector):
    def __init__(self, command: str, username: str) -> None:
        super().__init__(command, username)

    def format(self,data:dict):
        username = data['username']
        full_name = data['full_name']
        follower =  data['followers']
        following =  data['followings']
        isPrivate = data['isPrivate']
        bio = data['bio']
        timestamp = data['timestamp']

        # print(data[i]['timestamp'])
        converted = {
            timestamp : {
                'Username' : username,
                'Full name':full_name if full_name != None else "",
                'Follower':follower,
                'Following':following,
                'isPrivate':isPrivate,
                'bio':bio if bio != None else ''

            }
        }
        return converted
    
    def getInitials(self) -> dict:
        return self.format(self._get_initial())
    
    def getStatus(self) -> dict:
        return self.format(self._get_last_data())
    def getHistory(self) -> dict[dict]:
        all_logs = self._get_all()
        converted = {}
        for logs in all_logs:
            converted.update(self.format(logs))
        return converted
            
        
        # print(converted)
            
connec = Connector('trackinsta','emi_lyitachi2')
print(connec.getHistory())

