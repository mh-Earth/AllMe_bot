
from telegram.ext import ContextTypes
import datetime
import logging
from dataclasses import dataclass

# Job name = instratacking_username
'''
Base class for handling telegram job queue

Job schema:
|------------------------------------------------|
| ssn | name (command)     | chat id (job_name)  |
|------------------------------------------------|
|  1  | trackinsta         | trackinsta_username |
|------------------------------------------------|
|  2  | some_command_name  | command_name        |
|------------------------------------------------|

'''

# @dataclass
# class Job:
#     cxt:ContextTypes.DEFAULT_TYPE
#     command:str
#     job_name:str


class JobController:
    def __init__(self) -> None:
        self.job_name = f"{self.command}_{self.name}"
        
    
    def _remove_job_if_exists(self) -> bool:
        """Remove job with given name. Returns whether job was removed."""
        current_jobs = self.cxt.job_queue.get_jobs_by_name(self.command)
        for job in current_jobs:
            if job.chat_id == self.job_name:
                job.schedule_removal()
                return True
        return False
        ...
    
    def _add_daily_job(self,callback):
        """Add a job to the queue that is run daily in a given time."""
        time = datetime.time(12, 0, 0) # 12:00 pm
        # datetime.datetime.now()
        logging.info(f'New daily job added time={time} command=/{self.command} {self.name}')
        self.cxt.job_queue.run_daily(callback=callback, time=time, chat_id=self.job_name, name=self.command)
    
    def _add_repeating_job(self,callback,interval:int):
        """Add a repeating job to the queue,run every (interval) seconds later."""
        # interval in second (run every interval second later)
        logging.info(f'New repeating job added interval={interval} command:/{self.command} {self.name}')
        job = self.cxt.job_queue.run_repeating(callback=callback, interval=interval, chat_id=self.job_name, name=self.command)
        # self.c
    
    def _cancel_job(self)-> bool:
        """Remove the job if the user changed their mind."""
        return self._remove_job_if_exists()
    
    def _getAllJobs(self) -> tuple:
        '''Return all jobs by job name from job queue'''
        return self.cxt.job_queue.get_jobs_by_name(name=self.command)
        
    def _is_job_exits(self)->bool:
        '''check if a job (by name) is in job queue '''
        all_jobs = self.cxt.job_queue.get_jobs_by_name(name=self.command)
        for jobs in all_jobs:
            if jobs.chat_id == self.job_name:
                return True
        return False
    
    


if __name__ == "__main__":
    pass