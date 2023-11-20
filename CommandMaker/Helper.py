import os 
import json
import time
from dataclasses import dataclass

'''Base class handling file relate works helper'''
'''Temporary class until db is here'''

@dataclass
class BaseHelper:
    commandName:str
    fileName:str

class BaseHelper:

    parent_path = str(os.path.dirname(__file__))

    def _tick(self) -> str:
        return str(time.time())

    def _createDataFile(self):
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

    def _storeNewData(self,data:dict):
        '''Store New data to json file'''
        # load the data as python dict
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","r") as f:
            x:dict = json.loads(f.read())
            
        # update the the dict
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
            x.update({self._tick():data})
            jsonData = json.dumps(x)
            f.write(jsonData)

    def _removeFile(self):
        '''remove command data file'''
        os.remove(f"{self.parent_path}\data\{self.command}\{self.fileName}.json")

    def _if_file_exist(self) -> bool:
        path:str = f'{self.parent_path}\data\{self.command}\{self.fileName}.json'
        if os.path.exists(path):
            return True
        return False


    @staticmethod
    def _compare_dicts(dict1, dict2):
        '''use to get difference between to dictionary'''
        # Find keys that are common to both dictionaries
        common_keys = set(dict1.keys()) & set(dict2.keys())

        # Find keys that are unique to each dictionary
        unique_keys_dict1 = set(dict1.keys()) - set(dict2.keys())
        unique_keys_dict2 = set(dict2.keys()) - set(dict1.keys())

        # Find values that are different for common keys
        diff_val = [(key, dict1[key], dict2[key]) for key in common_keys if dict1[key] != dict2[key]]

        # Create a dictionary of the differences
        differences = {
            'common_keys': common_keys,
            'unique_keys_dict1': unique_keys_dict1,
            'unique_keys_dict2': unique_keys_dict2,
            'different_values': diff_val
        }

        return differences
    
    @staticmethod
    def _get_diff_val(dict1, dict2) -> bool:
        '''same as compare_dicts '''

        # Find keys that are common to both dictionaries
        common_keys = set(dict1.keys()) & set(dict2.keys())

        # Find values that are different for common keys
        diff_val = [(key, dict1[key], dict2[key]) for key in common_keys if dict1[key] != dict2[key]]

        # return differences
        return diff_val

    
    @staticmethod
    def _is_diff(dict1, dict2):
        '''check if two dictionary are same or not'''

        # Check for changes in keys
        if set(dict1.keys()) != set(dict2.keys()):
            return True

        # Check for changes in values
        for key in dict1:
            if dict1[key] != dict2[key]:
                return True

        # No changes detected
        return False
