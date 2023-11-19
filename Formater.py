from json import loads

class TrackinstaFormater():
    
    
    def changed(self,username:str,data:dict) -> str:
        formated_str = f"Change detected for {username}\n"
        for key, value in data.items():
            formated_str += f"{key}:{value},\n"

        return formated_str
    
    def trackInstaFormater(self,data:dict) -> str:
        for key, value in data.items():
            formated_str += f"{key}:{value},\n"

        return formated_str

    def trackInstaFormaterStr(self,data:str):
        # formated_str = f"Change detected for {username}\n"
        try:

            data = loads(data)
            for key, value in data.items():
                formated_str += f"{key}:{value},\n"

            return formated_str
        except Exception as e:
            print(e)
            return data
        