from dotenv import load_dotenv
from typing import Final
from os import environ
load_dotenv()

BOT_TOKEN:Final=environ.get("BOT_TOKEN")
LIST_OF_ADMINS:Final=list(map(int,(environ.get('LIST_OF_ADMINS').split(','))))
DAILY_JOB_TIME:Final=environ.get('DAILY_JOB_TIME')
INSTA_USERNAME:Final=environ.get('INSTA_USERNAME')
LOGGING_LEVEL:Final=environ.get('LOGGING_LEVEL')
TRACKING_MODE:Final=environ.get('TRACKING_MODE')
LIST_OF_TEST_USER:Final = list(map(int,(environ.get('LIST_OF_TEST_USER').split(','))))
REPEAT_JOB_INTERVAL:Final=int(environ.get('REPEAT_JOB_INTERVAL'))
# DATABASE
# DATABASE_HOST=environ.get('DATABASE_HOST')
# DATABASE_USERNAME=environ.get('DATABASE_USERNAME')
# DATABASE_NAME=environ.get('DATABASE_NAME')
# DATABASE_PASSWORD=environ.get('DATABASE_PASSWORD')
# 
MAX_TRACKER_LIMIT=int(environ.get('MAX_TRACKER_LIMIT'))
MAX_DATA_TO_STORE_LIMIT=int(environ.get('MAX_DATA_TO_STORE_LIMIT'))