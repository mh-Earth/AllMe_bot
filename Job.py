
from telegram.ext import ContextTypes


# Job name = instratacking_username
class Job():
    def __init__(self , name:str ,context:ContextTypes.DEFAULT_TYPE) -> None:
        self.cxt:ContextTypes.DEFAULT_TYPE = context 
        # self.instra_username = username
        # self.instra:Insta = Insta(username=self.instra_username)
        self.job_name = name

    
    def if_job_exits(self):
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = self.cxt.job_queue.get_jobs_by_name(self.job_name)
        if not current_jobs:
            return False
        for job in current_jobs:
            job.schedule_removal()
        return True
        ...
    
    def add_job_daily(self,callback):
        """Add a job to the queue."""
        self.cxt.job_queue.run_repeating(callback=callback, interval=55, chat_id=self.cxt._user_id, name=self.job_name)
# 86400
    
    def add_job_repeating(self,callback):
        ...
    
    def remove(self):
        ...


if __name__ == "__main__":
    pass