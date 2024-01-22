
# Telegram Bot

A Telegram bot written in python for tracking a Instagram ID



## Usage

```
pip3 install -r req.txt
```
```
python3 Bot.py
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

Required

`BOT_TOKEN`: [Get Bot Token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)

Optional

`LIST_OF_ADMINS`:Default '000'

`DAILY_JOB_TIME`:Default '20_25_0' (08:25:00 pm)

`INSTA_USERNAME`:Default None

`LOGGING_LEVEL`: Default 'INFO'

`TRACKING_MODE`: Default 'repeat' (daily|repeat)

`LIST_OF_TEST_USER`: Default '000'

`REPEAT_JOB_INTERVAL`: Default 1800(s) (30 minute)

`MAX_TRACKER_LIMIT`: Default 3

`MAX_DATA_TO_STORE_LIMIT`: Default 100


## Project Dropped for lack of instagram api to get user info.

