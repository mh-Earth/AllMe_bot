
import instaloader
from dotenv import load_dotenv
import logging
import os
from configurations.settings import INSTA_USERNAME
load_dotenv()

'''
Class for interacting with instagram
'''


class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.username = username

    '''Same as getPublic data bt with profile picture'''
    def checkout(self):
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
            # DP
            DP = self.profile.profile_pic_url
            # biography_mentions = self.profile.biography_mentions
            profile_url = f"https://www.instagram.com/{self.username}/"


            return {
                "Username":self.username,
                "Full name":full_name,
                "Follower":follower,
                "Following":followee,
                "Private":isPrivate,
                "Bio":bio,
                "DP":DP,
                "URL": profile_url
            }

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return 
    
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

            return {
                "Username":self.username,
                "Full name":full_name,
                "Follower":follower,
                "Following":followee,
                "Private":isPrivate,
                "Bio":bio,
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

                    self.L.load_session_from_file(INSTA_USERNAME,"session-emi_lyitachi")
                except:
                    logging.error("Failed to load session for instagram")
                    return False
                return True if instaloader.Profile.from_username(self.L.context,self.username) else False
            except Exception as e:
                logging.error(e)
                return False

