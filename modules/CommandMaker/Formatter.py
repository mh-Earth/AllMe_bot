from json import loads
import logging
from datetime import datetime

class BaseFormatter():

    def _initialFormat(self,data:dict):
        '''coming soon'''
        formatted_str = ""
        data = self._toUpper(data)
        for key, value in data.items():
            formatted_str += f"{key}: {value}\n"
        return formatted_str
    
    @staticmethod
    def _toUpper(data:dict):
        username = data['username']
        full_name = data['full_name']
        follower =  data['follower']
        following =  data['following']
        isPrivate = data['isPrivate']
        bio = data['bio']
        dp =  data['dp']

        # print(data[i]['timestamp'])
        converted = {
            'Username' : username,
            'Full name':full_name,
            'Follower':follower,
            'Following':following,
            'isPrivate':isPrivate,
            'Bio':bio if bio != None else '',
            'Dp' if dp != None else None: dp

        }
        return converted
    
    
    def _str_to_str(self,data:str) -> str:
        '''Json formatted string'''
        try:
            data = loads(data)
            for key, value in data.items():
                formatted_str += f"{key}: {value},\n"
            return formatted_str
        except Exception as e:
            logging.error(e)
            return data
    
    def _to_str(self,data:any):
        return str(data)
    
    def _timestamp_to_readable_format(self,timestamp:float) -> str:
        """
        Converts a timestamp to a human-readable date and time format.

        Args:
            timestamp (float): The timestamp to convert.

        Returns:
            str: A string representing the formatted date and time.
        """
        return  datetime.fromtimestamp(timestamp).strftime('%A %H:%M:%S %Y-%m-%d')


    