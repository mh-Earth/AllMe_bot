
from dotenv import load_dotenv
import logging
import requests
import json
from time import time
from dataclasses import dataclass
load_dotenv()
import logging
import coloredlogs
coloredlogs.install(level='INFO', fmt='%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S', colors={'DEBUG': 'green', 'INFO': 'blue', 'WARNING': 'yellow', 'ERROR': 'red', 'CRITICAL': 'bold_red'})





@dataclass(kw_only=True)
class TrackinstaDataModel:
    username:str
    follower:int
    following:int
    full_name:str|None =None
    bio:str|None = None
    isPrivate:bool=False
    dp:str|None=None
    timestamp:str|None = None
    dType:str|None = None
    


    def __call__(self) -> dict:
         return {
            'username':self.username,
            'full_name':self.full_name,
            'bio':self.bio,
            'follower':self.follower,
            'following':self.following,
            'isPrivate':self.isPrivate,
            'dp':self.dp
        }

    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")



'''CONNECTOR TO BACKEND'''
class BaseConnector:

    def __init__(self,pluralApiId:str='trackinstas') -> None:
        self.pluralApiId = pluralApiId
        self.DB_PATH = 'http://localhost:1337'
        self.dbPath = f"{self.DB_PATH}/api/{self.pluralApiId}s"
        self.idLocation = 'data[0].id'
        self.logFiled = "logs"
        self.DB_API_TOKEN = '37599b9d92f3c4daae9a293318a16d3d14dba192431a0e9e5811855953100b1b1257d5c783964b9e7f228dd39fd9c89b7dfddd922923e44633e9ca5b2d0a90877045a3292b5e73f43487d995a9467a4013cc9c538a6760afdccbec68e100a4683f94e39417953a9963bc4740b1d3984f8129039d4e5d7a82c302d2ceba5df2ac'
        self.dTypes:list[str] = ['initial','continuous']
    
    @staticmethod
    def _tick():
        return str(time())
    
    def _username_to_id(self,identifier:str|int) -> int:
        url = f"{self.dbPath}?{self._filter_username(identifier)}"
        logging.info(f'[GET] {url}')
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[_username_to_id] [code:{res.status_code}] {res.text}')
            return
        
        data = json.loads(res.text)
        return data['data'][0]['id']
    
    def _get_last_found_dp(self,identifier:str|int) -> dict:
        url = f'{self.dbPath}?{self._filter_username(identifier)}&populate[logs][filters][dp][$null]&populate[logs][fields][0]=dp'
        logging.info(f'[GET] {url}')
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[_get_dp] [code:{res.status_code}] {res.text}')
            return
        data = json.loads(res.text)
        # print(data)
        dp:list[dict] = data['data'][0]['attributes'][self.logFiled]

        return dp[-1]



    def _get_initial(self,identifier:str|int) -> TrackinstaDataModel:
        url = f"{self.dbPath}?{self._filter_username(identifier)}&{self._dType_filter('initial')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=initial
        logging.info(f'[GET] {url}')
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[_get_initial] [code:{res.status_code}] {res.text}')
            return


        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled][0]

        if len(initials) == 0:
            return {'error':'No initials found'}
        else:
            # print(initials)
            return initials
    
    def _get_continuous(self,identifier:str|int):
        url = f"{self.dbPath}?{self._filter_username(identifier)}&{self._dType_filter('continuous')}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate[data][filters][type][$eq]=continuous
        logging.info(f'[GET] {url}')
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"

        }
        res = requests.get(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[get_continuous] [code:{res.status_code}] {res.text}')
            return

        data = json.loads(res.text)
        initials = data['data'][0]['attributes'][self.logFiled]

        if len(initials) == 0:
            return {'error':'No initials found'}
        else:
            return initials

    def _get_last_data(self,identifier:str|int) -> dict:
        url = f"{self.dbPath}?{self._filter_username(identifier)}&{self._populate(self.logFiled)}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate=data
        logging.info(f'[GET] {url}')
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[_get_last_data] [code:{res.status_code}] {res.text}')
            return

        data = json.loads(res.text)
        data = data['data'][0]['attributes']['logs'][-1]

        return data
    def _get_all(self,identifier:str|int) -> list[dict]:

        url = f"{self.dbPath}?{self._filter_username(identifier)}&{self._populate(self.logFiled)}"
        # http://localhost:1337/api/trackinstas?filters[username][$eq]=emi_lyitachi&populate=data
        logging.info(f'[GET] {url}')
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}"
        }
        res = requests.get(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[_get_all] [code:{res.status_code}] {res.text}')
            return
        data = json.loads(res.text)
        data = data['data'][0]['attributes'][self.logFiled]
        # print(data)

        return data
    
    # Add tracker
    def add_tracker(self,data:TrackinstaDataModel) -> requests.Response:
        (username,full_name,bio,follower,following,isPrivate,dp) = data().values()
        url = f"{self.dbPath}"
        # http://localhost:1337/api/trackinstas
        dType = self.dTypes[0]
        timestamp = self._tick()
        logging.info(f'[POST] {url}')


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
                    "dType":dType,
                    "timestamp":timestamp,
                    "dp": dp                 }
                ]
            }
        }
        payloads = json.dumps(payloads)
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        "Content-Type": "application/json" 
        }
        try:
            res = requests.post(url,data=payloads,headers=headers)
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
            new_trackinstaObj = TrackinstaDataModel(**new_data)
            res = self.add_log(data=new_trackinstaObj)
            if res.status_code != 200:
                logging.error(f'[add_tracker] [code:{res.status_code}] {res.text}')
                return

            return res

    
    def add_log(self,data:TrackinstaDataModel) -> requests.Response:

        (username,full_name,bio,follower,following,isPrivate,dp) = data().values()
        Id = self._username_to_id(identifier=username)
        url = f"{self.dbPath}/{Id}"
        # http://localhost:1337/api/trackinstas/:id

        '''Compare dp urls to check if dp as changed or not'''
        last_found_dp = self._get_last_found_dp(identifier=username)['dp']

        timestamp = self._tick()
        dType = self.dTypes[1]
        previous_data = self._get_all(identifier=username)
        previous_data.append({
            "username": username,
            "full_name": full_name if full_name != '' else None,
            "bio": bio,
            "follower": follower,
            "following": following,
            "isPrivate": isPrivate,
            "dType": dType,
            "timestamp":timestamp,
            "dp": dp if last_found_dp != dp else None


        })
        payloads = {
            "data": {
                "logs":previous_data
            }
        }
        payloads = json.dumps(payloads)
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        "Content-Type": "application/json" 
        }
        logging.info(f'[PUT] {url}')
        res = requests.put(url,data=payloads,headers=headers)
        if res.status_code != 200:
            logging.error(f'[add_log] [code:{res.status_code}] {res.text}')
            return
        return res

    def remove_tracker(self,identifier:str|int) -> requests.Response:
        Id = self._username_to_id(identifier=identifier)
        headers = {
        "Authorization": f"Bearer {self.DB_API_TOKEN}",
        }
        url = f'{self.dbPath}/{Id}'
        logging.info(f'[DELETE] {url}')
        res = requests.delete(url,headers=headers)
        if res.status_code != 200:
            logging.error(f'[delete_tracker] [code:{res.status_code}] {res.text}')
            return
        return res
    
    def _filter_username(self,identifier:str|int):
        return f"filters[username][$eq]={identifier}"
    def _dType_filter(self,dType:str):
        return f"populate[{self.logFiled}][filters][dType][$eq]={dType}"
    def _populate(self,filed:str="*"):
        return f'populate={filed}'

class Connector(BaseConnector):
    pass



class ConnectorUtils(BaseConnector):
    def __init__(self, command: str, username: str) -> None:
        super().__init__(command)
        self.username = username


    

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
    
    def getInitials(self) -> dict:
        return self.format(self._get_initial(self.username))
    
    def last_stored_log(self) -> dict:
        return self.format(self._get_last_data(self.username))

    
    def getStatus(self) -> dict:
        return self.format(self._get_last_data(self.username))
    
    def getPreviousData(self) -> dict[dict]:
        all_logs = self._get_all(self.username)
        converted = {}
        for logs in all_logs:
            converted.update(self.format(logs))
        return converted
            


if __name__ == "__main__":
    conn = ConnectorUtils('trackinsta','emi_lyitachi')
    data = {
        "username":conn.username,
        "full_name":'full_name',
        "follower":12,
        "following":32,
        "isPrivate":True,
        "bio": None,
        "dp": 'url changed again',
        }
    
    dataModel = TrackinstaDataModel(**data)
    # print(conn.add_tracker(data=dataModel))
    # print(conn.getPreviousData())

    ini_list = ['Username','Full Name','Follower','Following','Private','Bio','Dp']
    init_dict = conn.getInitials().items()
    f = {}
    for k,v in init_dict:
        # print(k,v)
        final_dict = dict(zip(ini_list, list(v.values())))
        f.update({
            k:final_dict
        })
    
    print(f)
    

    
        
        # print(converted)