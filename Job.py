
from telegram.ext import ContextTypes
import datetime

# Job name = instratacking_username
class Job():
    def __init__(self , name:str ,commandName:str ,context:ContextTypes.DEFAULT_TYPE) -> None:
        self.cxt:ContextTypes.DEFAULT_TYPE = context 
        self.job_id = f"{commandName}_{name}"
        self.commandName = commandName

    
    def remove_job_if_exists(self):
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
        time = datetime.time(12, 0, 0)
        self.cxt.job_queue.run_daily(callback=callback, time=time, chat_id=self.job_name, name=self.commandName)
    
    def add_job_repeating(self,callback,interval:int):
        # interval in second
        self.cxt.job_queue.run_repeating(callback=callback, interval=interval, chat_id=self.job_id, name=self.commandName)
        ...
    
    def remove(self)->str:
        """Remove the job if the user changed their mind."""
        job_removed = self.remove_job_if_exists()
        text = True if job_removed else False
        return text
    
    def getAllJobs(self):
        return self.cxt.job_queue.get_jobs_by_name(name=self.commandName)
        
    
    def is_job_exits(self):
        all_jobs = self.cxt.job_queue.get_jobs_by_name(name=self.commandName)
        for jobs in all_jobs:
            if jobs.chat_id == self.job_id:
                return True
        return False
    
    


if __name__ == "__main__":
    pass