import os 
import json
import time
from dataclasses import dataclass
from db.types import TrackinstaDataModel
'''Class for storing data to a local file storage (temporary)'''

@dataclass
class LocalStorage:
    command:str
    fileName:str

class LocalStorage:

    parent_path = str(os.path.dirname(__file__))
    def __init__(self,command,username) -> None:
        self.command:str = command
        self.fileName:str = username

    def _tick(self) -> str:
        return str(time.time())

    def createDataFile(self):
        """if file and folder has already been created"""
        if os.path.exists(fr"{self.parent_path}\data\{self.command}\{self.fileName}.json"):
            # print(f"Already tracking {self.fileName}")
            return
        
        '''if only folder has created'''
        if os.path.exists(fr"{self.parent_path}\data\{self.command}"):
            with open(fr"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
                f.write("{}")

        # '''create folder and file'''
        else:
            os.makedirs(self.parent_path + fr"\data\{self.command}")
            with open(fr"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
                f.write("{}")

    def _loadStoreData(self) -> dict:
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","r") as f:
            data = json.loads(f.read())
            # print(data)            
        return data

    def storeNewData(self,data:dict):
        '''Store New data to json file'''
        # load the data as python dict
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","r") as f:
            x:dict = json.loads(f.read())
            
        # update the the dict
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
            x.update({self._tick():data})
            jsonData = json.dumps(x)
            f.write(jsonData)
    @staticmethod
    def extra_data_from_model(model:TrackinstaDataModel|None):

        return {'username':model.username,'full_name':model.full_name,'follower':model.follower,'following':model.following,'isPrivate':model.isPrivate,'bio':model.bio,}
        
        

    def _removeFile(self):
        '''remove command data file'''
        os.remove(f"{self.parent_path}\data\{self.command}\{self.fileName}.json")

    def _if_file_exist(self) -> bool:
        path:str = f'{self.parent_path}\data\{self.command}\{self.fileName}.json'
        if os.path.exists(path):
            return True
        return False
    
#     print(data)