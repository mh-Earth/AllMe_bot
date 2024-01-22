'''Base class for interacting with Instaloader module'''
import instaloader
from instaloader.structures import Profile
import logging
import requests
from configurations.settings import INSTA_USERNAME
from db.dataModels import TrackinstaDataModel
import uuid
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


    def _gen_uid(self)->str:
        return str(uuid.uuid4())
    
    def checkout(self) -> TrackinstaDataModel:
        return self.publicData(self.lookup())


    def publicData(self,profile:Profile) -> TrackinstaDataModel | None:
        # full name
        full_name = profile.full_name
        # follower
        follower = profile.followers
        # followee
        followee = profile.followees
        # isPrivate
        isPrivate = profile.is_private
        # bio
        bio = profile.biography
        # DP
        dp = profile.profile_pic_url
        
        verified = profile.is_verified


        data = {
            'uid':self._gen_uid(),
            "username":self.username,
            "full_name":full_name,
            "follower":follower,
            "following":followee,
            "isPrivate":isPrivate,
            "bio": bio if bio != "" else None,
            "verified":verified,
            "dp": dp,
        }
        logging.debug(f'Data for job:{data}')
        return TrackinstaDataModel(**data)
    

    def lookup(self) -> Profile:
        try:
            return instaloader.Profile.from_username(self.L.context,self.username)
        except Exception as e:
            logging.error(e)
            try:
                logging.warning(f"{e}. Trying to load session")
                try:
                    if INSTA_USERNAME != None:
                        self.L.load_session_from_file(INSTA_USERNAME,f"session-{INSTA_USERNAME}")
                    else:
                        logging.warning("Can not load session.No INSTA-USERNAME defined ")
                        return False
                except Exception as e:
                    logging.error(f"Failed to load session for instagram ({e})")
                    return False
                
                return instaloader.Profile.from_username(self.L.context,self.username)
                # return True if instaloader.Profile.from_username(self.L.context,self.username) else False
            except Exception as e:
                logging.error(e)
                return False
