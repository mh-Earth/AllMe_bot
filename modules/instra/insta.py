
import instaloader
# from instaloader import Profile


class Insta():
    def __init__(self,username:str) -> None:
        self.L = instaloader.Instaloader()
        self.USERNAME = username
        

    
    def publicData(self):
        if self.lookup():
            self.profile = instaloader.Profile.from_username(self.L.context, self.USERNAME)
            # full name
            full_name = self.profile.full_name
            # follwer
            follwer = self.profile.followers
            # follwee
            followee = self.profile.followees
            # isPrivate
            isPrivate = self.profile.is_private
            # post
            # post = self.profile.get_posts()
            # bio
            bio = self.profile.biography
            # biography_mentions
            biography_mentions = self.profile.biography_mentions

            return {
                "full_name":full_name,
                "follwer":follwer,
                "followee":followee,
                "isPrivate":isPrivate,
                "bio":bio
            }

        else:
            return f"No profile found {self.USERNAME}"
    
    def lookup(self):
        try:
             instaloader.Profile.from_username(self.L.context,self.USERNAME)
             return True
        except Exception as e:
            return False

        
    def test(self):
        return self.profile.get_profile_pic_url()

if __name__ == "__main__":
    test = Insta("afnan.aksa")
    print(test.publicData())