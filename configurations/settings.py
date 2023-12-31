from dotenv import load_dotenv
from typing import Final
from os import environ
load_dotenv()

BOT_TOKEN:Final=environ.get("BOT_TOKEN")
API_ID:Final=environ.get('API_ID')
API_HASH:Final=environ.get('API_HASH')
USER_ID:Final=environ.get('USER_ID')
CHAT_ID:Final=environ.get('CHAT_ID')
BOT_USERNAME:Final=environ.get('BOT_USERNAME')
INSTA_USERNAME:Final=environ.get('INSTA_USERNAME')
INSTA_PASS:Final=environ.get('INSTA_PASS')
NUMBER:Final=environ.get('NUMBER')
LIST_OF_ADMINS:Final=list(map(int,(environ.get('LIST_OF_ADMINS').split(','))))
DAILY_JOB_TIME:Final=environ.get('DAILY_JOB_TIME')
LOGGING_LEVEL:Final=environ.get('LOGGING_LEVEL')
TRACKING_MODE:Final=environ.get('TRACKING_MODE')
LIST_OF_TEST_USER:Final = list(map(int,(environ.get('LIST_OF_TEST_USER').split(','))))
REPEAT_JOB_INTERVAL:Final=int(environ.get('REPEAT_JOB_INTERVAL'))
DB_NAME=environ.get('DB_NAME')