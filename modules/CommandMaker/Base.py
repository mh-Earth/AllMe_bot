from .Job import JobController
from abc import ABC,abstractclassmethod

class CommandModel(JobController,ABC):

    @abstractclassmethod
    async def run(self):
        ...

class CommandBase(ABC):

    @abstractclassmethod
    async def run(self):
        ...