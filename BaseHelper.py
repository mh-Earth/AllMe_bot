import os 
import json
from datetime import datetime

'''Base class for all modules helper'''
class Base():

    parent_path = str(os.path.dirname(__file__))

    def now_time(self,) -> str:
        return datetime.now().strftime("%d|%m|%Y|%H|%M|%S")

    def createDataFile(self):
        if os.path.exists(fr"{self.parent_path}\data\{self.command}\{self.fileName}.json"):
            print(f"Allready tracking {self.fileName}")
            return
        
        if os.path.exists(fr"{self.parent_path}\data\{self.command}"):
            with open(fr"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
                f.write("{}")


        else:
            os.makedirs(self.parent_path + fr"\data\{self.command}")
            with open(fr"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
                f.write("{}")

    def loadStoreData(self) -> dict:
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","r") as f:
            data = json.loads(f.read())
        
        return data

    def storeNewData(self,data:dict):
        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","r") as f:
            x:dict = json.loads(f.read())

        with open(f"{self.parent_path}\data\{self.command}\{self.fileName}.json","w") as f:
            x.update({self.now_time():data})
            jsonData = json.dumps(x)
            f.write(jsonData)

    @staticmethod
    def compare_dicts(dict1, dict2):
        # Find keys that are common to both dictionaries
        common_keys = set(dict1.keys()) & set(dict2.keys())

        # Find keys that are unique to each dictionary
        unique_keys_dict1 = set(dict1.keys()) - set(dict2.keys())
        unique_keys_dict2 = set(dict2.keys()) - set(dict1.keys())

        # Find values that are different for common keys
        different_values = [(key, dict1[key], dict2[key]) for key in common_keys if dict1[key] != dict2[key]]

        # Create a dictionary of the differences
        differences = {
            'common_keys': common_keys,
            'unique_keys_dict1': unique_keys_dict1,
            'unique_keys_dict2': unique_keys_dict2,
            'different_values': different_values
        }

        return differences
    
    @staticmethod
    def get_diff(dict1, dict2):
        # Check for changes in keys
        if set(dict1.keys()) != set(dict2.keys()):
            return True

        # Check for changes in values
        for key in dict1:
            if dict1[key] != dict2[key]:
                return True

        # No changes detected
        return False
