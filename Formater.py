from json import loads


class Base():
    

    def dict_to_str(self,data:dict):
        formated_str = ""
        for key, value in data.items():
            formated_str += f"{key}:{value},\n"
        return formated_str
    
    
    def str_to_str(self,data:str) -> str:
        '''Json formated string'''
        try:
            data = loads(data)
            for key, value in data.items():
                formated_str += f"{key}:{value},\n"
            return formated_str
        except Exception as e:
            print(e)
            return data
    
    def to_str(self,data:any):
        return str(data)

    # def trackInstaFormaterStr(self,data:str):
    #     # formated_str = f"Change detected for {username}\n"

        