from .Formatter import BaseFormatter
from .Helper import BaseHelper
from .Job import JobController
from abc import ABC,abstractclassmethod

class CommandModel(BaseFormatter,BaseHelper,JobController,ABC):

    @abstractclassmethod
    async def run(self):
        ...

class CommandBase(ABC):

    @abstractclassmethod
    async def run(self):
        ...