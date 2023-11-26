# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
from dotenv import load_dotenv
import os
from time import sleep
from configurations.settings import NUMBER,API_ID,API_HASH
load_dotenv()
# get your api_id, api_hash, token
# from telegram as described above
api_id = API_ID
api_hash = API_HASH
message = "Host is running..."

# your phone number
phone = NUMBER

# creating a telegram session and assigning
# it to a variable client
client = TelegramClient('session', api_id, api_hash)

# connecting and building the session
client.connect()

# in case of script ran first time it will
# ask either to input token or otp sent to
# number or sent or your telegram id 
if not client.is_user_authorized():

	client.send_code_request(phone)
	
	# signing in the client
	client.sign_in(phone, input('Enter the code: '))

while True:
	try:
		# receiver user_id and access_hash, use
		# my user_id and access_hash for reference
		receiver = InputPeerUser(6540965739, 0)

		# sending message using telegram client
		client.send_message(receiver, message, parse_mode='html')
	except Exception as e:
		
		# there may be many error coming in while like peer
		# error, wrong access_hash, flood_error, etc
		print(e);
		client.disconnect()
	sleep(60)

# disconnecting the telegram session 
