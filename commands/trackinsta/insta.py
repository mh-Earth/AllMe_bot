'''Base class for interacting with Instaloader module'''
import instaloader
import logging
from configurations.settings import INSTA_USERNAME
from ..Types.trackinsta.types import TrackinstaDataModel

class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.username = username

    '''Same as getPublic data bt with profile picture'''
    def checkout(self) -> TrackinstaDataModel | None:
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
            dp = self.profile.profile_pic_url
            # biography_mentions = self.profile.biography_mentions
            profile_url = f"https://www.instagram.com/{self.username}/"


            data = {
                "username":self.username,
                "full_name":full_name if full_name != '' else None,
                "follower":follower,
                "following":followee,
                "isPrivate":isPrivate,
                "bio": bio,
                "dp": dp,
            }
            return TrackinstaDataModel(**data)

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return None
    
    def publicData(self) -> TrackinstaDataModel | None:
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
            # dp
            dp = self.profile.profile_pic_url

            data =  {
                "username":self.username,
                "full_name":full_name,
                "follower":follower,
                "following":followee,
                "isPrivate":isPrivate,
                "bio": bio,
                'dp':dp

                }
            return TrackinstaDataModel(**data)

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return None
    
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
