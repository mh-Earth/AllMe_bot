from json import loads
import logging
from datetime import datetime

class BaseFormatter():

    def _dict_to_str(self,data:dict):
        '''coming soon'''
        formatted_str = ""
        for key, value in data.items():
            formatted_str += f"{key}:{value},\n"
        return formatted_str
    
    
    def _str_to_str(self,data:str) -> str:
        '''Json formatted string'''
        try:
            data = loads(data)
            for key, value in data.items():
                formatted_str += f"{key}:{value},\n"
            return formatted_str
        except Exception as e:
            logging.error(e)
            return data
    
    def _to_str(self,data:any):
        return str(data)
    
    def timestamp_to_readable_format(self,timestamp:int) -> str:
        """
        Converts a timestamp to a human-readable date and time format.

        Args:
            timestamp (float): The timestamp to convert.

        Returns:
            str: A string representing the formatted date and time.
        """
        return  datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    