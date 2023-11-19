from Formater import Base

class TrackInstaMessage(Base):
    def __init__(self,username) -> None:
        super().__init__()
        self.username = username
    

    def initial(self,data) -> str:
        title:str = f"Initials of {self.username}"
        des:str = self.dict_to_str(data)

        message = f"{title}\n{des}"

        return message
        
    '''Changed Detected'''
    def changeDeteced(self,data:list[tuple]) -> str:
        '''Decorate the data 
        Exp:
        """
        Public activity deteced for <username>
        follwer:57554253 -> 57554329
        isPrivate:true -> false
        """
        '''
        # ''' data = list[tuple]] '''

        title:str = f"Public activity deteced for {self.username}"
        des = ""
        for attr in data:
            # eg:follwer:99->100
            des += f"{attr[0]}:{attr[1]} -> {attr[2]},\n"

        

        message = f"{title}\n{des}"
        return message
    