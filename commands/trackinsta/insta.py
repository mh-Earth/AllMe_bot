'''Base class for interacting with Instaloader module'''
import instaloader
import logging
import requests
from configurations.settings import INSTA_USERNAME
from models.trackinsta.types import TrackinstaDataModel

class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.username = username
        session = requests.Session()
        session.headers.update({
            "Host": "www.instagram.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Sec-GPC": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1"
        })
        self.L.context._session = session  # Set Instaloader's session to the custom session


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
