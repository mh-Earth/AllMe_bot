from dataclasses import dataclass

@dataclass(kw_only=True)
class TrackinstaDataModel:

    uid:str
    username:str
    follower:int
    following:int
    verified:bool
    full_name:str|None =None
    bio:str|None = None
    isPrivate:bool=False
    dp:str|None=None
    timestamp:float|None=None
    


    def __call__(self) -> dict:
         return {
            'uid':self.uid,
            'username':self.username,
            'full_name':self.full_name,
            'bio':self.bio,
            'follower':self.follower,
            'following':self.following,
            'isPrivate':self.isPrivate,
            'verified':self.verified,
            'dp':self.dp,
            'timestamp':self.timestamp
        }

    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            if not isinstance(self.__dict__[name], field_type):
                current_type = type(self.__dict__[name])
                raise TypeError(f"The field `{name}` was assigned by `{current_type}` instead of `{field_type}`")
