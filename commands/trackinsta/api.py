
import instaloader
from dotenv import load_dotenv
import logging
import os
load_dotenv()

'''
Class for interacting with instagram
'''


class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.username = username

        

    
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
            # biography_mentions
            # biography_mentions = self.profile.biography_mentions

            return {
                "Username":self.username,
                "Full name":full_name,
                "Follower":follower,
                "Following":followee,
                "Private":isPrivate,
                "Bio":bio
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

                    self.L.load_session_from_file(os.getenv("INSTA_USERNAME"),"session-emi_lyitachi")
                except:
                    logging.error("Failed to load session for instagram")
                    return False
                return True if instaloader.Profile.from_username(self.L.context,self.username) else False
            except Exception as e:
                logging.error(e)
                return False

                

        
    def test(self):
        return self.profile.get_profile_pic_url()
