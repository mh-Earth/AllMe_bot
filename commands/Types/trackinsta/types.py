from dataclasses import dataclass


@dataclass(kw_only=True)
class TrackinstaDataModel:
    username:str
    follower:int
    following:int
    full_name:str|None =None
    bio:str|None = None
    isPrivate:bool=False
    dp:str|None=None
    timestamp:str|None = None
    dType:str|None = None
    


    def __call__(self) -> dict:
         return {
            'username':self.username,
            'full_name':self.full_name,
            'bio':self.bio,
            'follower':self.follower,
            'following':self.following,
            'isPrivate':self.isPrivate,
            'dp':self.dp
        }

    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
    # def __repr__(self) -> str:
    #     return [value for value in TrackinstaDataModel.__dict__.keys() if not value.startswith('__')]

if __name__ == "__main__":
    data = {
        "username":'meherab',
        "full_name":'full_name',
        "follower":12,
        "following":32,
        "isPrivate":True,
        "bio": None,
        "dp": None,
        }
    a = TrackinstaDataModel(**data)
    (username,full_name,bio,follower,following,isPrivate,dp) = a().values()
    print(username,full_name,bio,follower,following,isPrivate,dp)

    
    b = TrackinstaDataModel(**a())

    print(TrackinstaDataModel.__dict__.keys())
    print([value for value in TrackinstaDataModel.__dict__.keys() if not value.startswith('__')])
    

    @dataclass
    class FuckIamSickOfThinkingNameFormat:
        username:str
        full_name:str
        follower:int
        following:int
        isPrivate:bool
        bio:str
        dp:str


    ini_list = ['Username','Full Name','Follower','Following','Private','Bio','Dp']
    FormateKeys = FuckIamSickOfThinkingNameFormat(*ini_list)
    print(FormateKeys.bio)

