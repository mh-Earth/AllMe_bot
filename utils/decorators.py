from functools import wraps
from configurations.settings import LIST_OF_ADMINS,LIST_OF_TEST_USER
from telegram.ext import ContextTypes
from telegram import Update
import logging


def admin_only(func):
    @wraps(func)
    async def wrapped(update:Update,context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        user_id = context._user_id
        if user_id not in LIST_OF_ADMINS:
            logging.warning("User ID {} tried to use admin command `{}`".format(user_id,update.effective_message.text))
            return
        return await func(update,context,*args,**kwargs)
    
    return wrapped

def restricted(func):
    @wraps(func)
    async def wrapped(update:Update,context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        user_id = context._user_id
        if user_id not in LIST_OF_TEST_USER:
            logging.warning("User ID {} tried to use restricted command `{}`".format(user_id,update.effective_message.text))
            return
        return await func(update,context,*args,**kwargs)
    
    return wrapped

def beta(func):
    @wraps(func)
    async def wrapped(update:Update,context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        user_id = context._user_id
        if user_id not in LIST_OF_TEST_USER:
            logging.warning("User ID {} tried to use in-dev command `{}`".format(user_id,update.effective_message.text))
            return
        else:
            logging.info(f'[Running Command] ({update.message.text}) from {update.effective_user.username}')
            return await func(update,context,*args,**kwargs)

    return wrapped

def production(func):
    @wraps(func)
    async def wrapped(update:Update,context:ContextTypes.DEFAULT_TYPE,*args,**kwargs):
        logging.info(f'[Running Command] ({update.message.text}) from {update.effective_user.username} ({update.effective_user.first_name} {update.effective_user.last_name})')
        return await func(update,context,*args,**kwargs)

    return wrapped




