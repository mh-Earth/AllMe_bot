
import instaloader
from dotenv import load_dotenv
import logging
# import os
load_dotenv()

'''
Class for interacting with instagram
'''


class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.username = username
        # self.L.login(os.getenv("INSTA_USERNAME"),os.getenv("INSTA_PASS"))

        

    
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
            # post
            # post = self.profile.get_posts()
            # bio
            bio = self.profile.biography
            # biography_mentions
            # biography_mentions = self.profile.biography_mentions

            return {
                "Full name":full_name,
                "Follower":follower,
                "Followee":followee,
                "Private":isPrivate,
                "Bio":bio
            }

        else:
            logging.info(f"'{self.username}' Not Found!!")
            return 
    
    def lookup(self):
        try:
             instaloader.Profile.from_username(self.L.context,self.username)
             return True
        except Exception as e:
            logging.error(e)
            return False
            

        
    def test(self):
        return self.profile.get_profile_pic_url()

if __name__ == "__main__":
    test = Insta("afnan.aksa")
    print(test.publicData())