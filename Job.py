
from telegram.ext import ContextTypes
import datetime

# Job name = instratacking_username
class Job():
    def __init__(self , name:str ,commandName:str ,context:ContextTypes.DEFAULT_TYPE) -> None:
        self.cxt:ContextTypes.DEFAULT_TYPE = context 
        # acts as job id
        self.job_name = f"{commandName}_{name}"
        self.commandName = commandName

    
    def remove_job_if_exists(self):
        # """Remove job with given name. Returns whether job was removed."""
        current_jobs = self.cxt.job_queue.get_jobs_by_name(self.commandName)

        for job in current_jobs:
            if job.chat_id == self.job_name:
                job.schedule_removal()
                return True
        return False
        ...
    
    def add_job_daily(self,callback):
        """Add a job to the queue."""
        time = datetime.time(12, 0, 0) # 12:00 pm
        # datetime.datetime.now()
        self.cxt.job_queue.run_daily(callback=callback, time=time, chat_id=self.job_name, name=self.commandName)
    
    def add_job_repeating(self,callback,interval:int):
        # interval in second (run every insterval second later)
        self.cxt.job_queue.run_repeating(callback=callback, interval=interval, chat_id=self.job_name, name=self.commandName)
        ...
    
    def remove(self)-> bool:
        """Remove the job if the user changed their mind."""
        return self.remove_job_if_exists()

    
    def getAllJobs(self):
        return self.cxt.job_queue.get_jobs_by_name(name=self.commandName)
        
    
    def is_job_exits(self):
        all_jobs = self.cxt.job_queue.get_jobs_by_name(name=self.commandName)
        for jobs in all_jobs:
            if jobs.chat_id == self.job_name:
                return True
        return False
    
    


if __name__ == "__main__":
    pass