'''
schema for public activity detection
1. if the id is private
    - full name change
    - bio change
    - following up
    - follower up
    - dp change
    - privacy change

2. if the id is not private
    - full name change
    - bio change
    - following up
    - dp change
    - privacy change
'''

from pprint import pprint
from main.utils.comparator import get_diff_val
import logging

class Detection:
    def __init__(self,last_val:dict,new_val:dict) -> None:
        self.last_val = last_val
        self.new_val = new_val


    def account_type(self):
        # private or not private
        return 'private' if self.last_val['isPrivate'] == True else 'not-private'
    
    def get_diff_vals(self):
        return get_diff_val(self.last_val,self.new_val)
        

    def activity(self):
        activities = self.get_diff_vals()
        if self.account_type() == 'private':
            for change in activities:
                key,old,new = change
                # only keep follower up 📈
                if key == 'follower':
                    if new < old:
                        activities.remove(change)

                # only keep  following up 📈                       
                elif key == 'following':
                    if new < old:
                        activities.remove(change)
            logging.debug(activities)
            return activities
            
        elif self.account_type() == 'not-private':
            for change in activities:
                key,old,new = change
                # remove any follower up down activity
                if key == 'follower':
                    activities.remove(change)
                # remove any follower or following down activity
                if key == 'following':
                    if new < old:
                        activities.remove(change)
            
            logging.debug(activities)
            return activities

if __name__ == '__main__':
    val1 ={
            'uid':'122334',
            "username":'afnan.aksa',
            "full_name":'afnan aksa',
            "follower":122,
            "following":22,
            "isPrivate":False,
            "bio": None,
            "dp": None,
            }
    val2 = {
            'uid':'122334',
            "username":'afnan.aksa',
            "full_name":'Afnan aksa',
            "follower":122,
            "following":23,
            "isPrivate":False,
            "bio": None,
            "dp": None,
            }
    
    d = Detection(val1,val2)
    pprint(d.activity())
