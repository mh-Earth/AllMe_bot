from dotenv import load_dotenv
from typing import Final
from os import environ
load_dotenv()

BOT_TOKEN:Final=environ.get("BOT_TOKEN")
LIST_OF_ADMINS:Final=list(map(int,(environ.get('LIST_OF_ADMINS',000).split(','))))
DAILY_JOB_TIME:Final=environ.get('DAILY_JOB_TIME','20_25_0')
INSTA_USERNAME:Final=environ.get('INSTA_USERNAME',None)
LOGGING_LEVEL:Final=environ.get('LOGGING_LEVEL','INFO')
TRACKING_MODE:Final=environ.get('TRACKING_MODE','repeat')
LIST_OF_TEST_USER:Final = list(map(int,(environ.get('LIST_OF_TEST_USER',000).split(','))))
REPEAT_JOB_INTERVAL:Final=int(environ.get('REPEAT_JOB_INTERVAL',1800))
MAX_TRACKER_LIMIT=int(environ.get('MAX_TRACKER_LIMIT',3))
MAX_DATA_TO_STORE_LIMIT=int(environ.get('MAX_DATA_TO_STORE_LIMIT',100))