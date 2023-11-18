from BaseHelper import Base

class TrackinstaHelper(Base):
    def __init__(self,username:str) -> None:
        # super().__init__()
        self.username = username
        self.valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._"
        self.command = 'trackinsta'
        self.fileName = username
    
    def validUserName(self) -> bool:
        for char in self.username:
            if char not in self.valid_characters:
                return False
        return True


if __name__ == "__main__":

    trackinstaHelper = TrackinstaHelper(username="aksa")
    trackinstaHelper.createDataFile()
