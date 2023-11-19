from BaseHelper import Base
import os
# import json

class TrackinstaHelper(Base):
    def __init__(self,username:str) -> None:
        # super().__init__()
        self.username = username
        self.valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"
        self.command = 'trackinsta'
        self.fileName = username
    
    def validUserName(self) -> bool:
        for char in self.username:
            if char not in self.valid_characters:
                return False
        return True
    
    def if_tracking(self) -> bool:
        path:str = f'{self.parent_path}/data/{self.command}/{self.fileName}.json'
        if os.path.exists(path) and os.path.getsize(path) > 5:
            return True
    
    def if_file_exist(self) -> bool:
        path:str = f'{self.parent_path}/data/{self.command}/{self.fileName}.json'
        if os.path.exists(path):
            return True
        return False

    
    # get the first one
    def getInitials(self):
        return list(self.loadStoreData().values())[0]
    # get the last one
    def getStatus(self):
        return list(self.loadStoreData().values())[-1]
    # get all
    def getHistory(self):
        return  list(self.loadStoreData().values())
    
    

if __name__ == "__main__":

    trackinstaHelper = TrackinstaHelper(username="aksa")
    trackinstaHelper.createDataFile()
