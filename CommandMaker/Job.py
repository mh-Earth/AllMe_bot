
from datetime import datetime,time
import logging
from tzlocal import get_localzone
import pytz
from dotenv import load_dotenv
from os import getenv
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
        self.local_timezone = get_localzone()
        load_dotenv()
        
    
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
        time_zone = get_localzone()
        hour,minute,second = map(int,getenv("DAILY_JOB_TIME").split("_"))
        desired_time = time(hour,minute,second)  # 12:00:00

        # Set the desired time zone (replace 'America/New_York' with your desired time zone)
        desired_timezone = pytz.timezone(str(time_zone))

        # Get the current date
        current_date = datetime.now()

        # Combine the current date, desired time, and desired time zone
        desired_datetime = datetime.combine(current_date, desired_time).replace(tzinfo=desired_timezone)

        # datetime.datetime.now()
        logging.info(f'New daily job added time={desired_datetime} time_zone={time_zone} command_used=/{self.command} {self.name}')
        self.cxt.job_queue.run_daily(callback=callback, time=desired_datetime, chat_id=self.job_name, name=self.command)
    
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