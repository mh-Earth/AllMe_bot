from telegram import Update
from telegram.ext import ContextTypes
from .trackinstaHelper import TrackinstaHelper
from Job import Job
from .api import Insta
from .Template import TrackInstaMessage


async def Trackinsta(update:Update,context:ContextTypes.DEFAULT_TYPE):

    username:str = context.args[0]
    commandName = 'trackinsta'
    helper = TrackinstaHelper(username)
    formater = TrackInstaMessage(username=username)
    j = Job(username,commandName,context)


    '''special methods'''
    '''if only special method given as username'''
    '''Get all tracking'''
    if len(context.args) == 1:
        if username == "trackinsta?":
            all_jobs = j.getAllJobs()
            s = f"Total {len(all_jobs)}\n"
            for index,jobs in enumerate(all_jobs):
                s += f"{index}. {jobs.chat_id}\n"
            await update.effective_message.reply_text(s)
            return

    '''
    options (remove,initial,history,status,debug)
    only get the first perameter after username skip others 
    '''
    '''if any option given'''
    if len(context.args) > 1:
        arg = context.args[1].lower()
        '''options will only run if the user is in tracking'''
        if j.is_job_exits():
            '''Remove the tracker for given user (/trackinsta <username> remove)'''
            if arg == "remove":
                success = j.remove()
                if success:
                    await update.effective_message.reply_text("Tracker successfully cancelled!") 
                    helper.removeFile()
                    return
            # '''See the first store data'''
            elif arg == 'initial' :
                await update.effective_message.reply_text(helper.getInitials())
                return
            
            # '''See all store data'''
            elif arg == 'history' :
                await update.effective_message.reply_text(helper.getHistory())
                return
            
            # '''See last store data'''
            elif arg == 'status' :
                await update.effective_message.reply_text(helper.getStatus())
                return
            # '''Detail info on all tracking'''

            else:
                await update.effective_message.reply_text("Invaild option!!!")
                return
            
        elif arg == 'debug' and username == "trackinsta?":
            data = j.getAllJobs()
            await update.effective_message.reply_text(str(data))
            return
        
        else:
            await update.effective_message.reply_text("You are not tracking this user")
            return


    '''cheak for wrrong username schema'''
    if not helper.validUserName():
        await update.effective_message.reply_text(f"Invalied username {username}") 
        return
    '''Check if already tracking rhis user '''
    if j.is_job_exits():
        await update.effective_message.reply_text(f"Already Tracking {username}") 
        return 

    '''instance for insteracting with instagram api'''
    insta = Insta(username)
    '''If username exist'''
    if not insta.lookup():
        await update.effective_message.reply_text(f"Something went wrrong.Check if user '{username}' exist") 
        return
    
    '''Id found'''
    await update.effective_message.reply_text(f"Tracking Instagram id {username}") 
    # create initial files (if file exist )
    helper.createDataFile()
    '''Send the first result when start tracking'''
    await update.effective_message.reply_text(formater.initial(insta.publicData()))
    '''Add user in job queue'''
    async def alarm(cxt):
        ''' getting public instagram data for id (follwer ,followee,bio etc..)'''
        new_data = insta.publicData()
        '''Loding previouly stored data'''
        storedData = helper.loadStoreData()
        '''Verify whether any earlier data has been stored, and if so, compare it with the new data'''
        if len(storedData) > 0:
            _ , last_value = list(storedData.items())[-1]
            if helper.is_diff(last_value,new_data):
                '''Get different values'''
                diff_val = helper.get_diff_val(last_value,new_data)
                await update.effective_message.reply_text(formater.changeDeteced(diff_val))
            else:
                return
        '''Append new data'''
        helper.storeNewData(data=new_data)
    j.add_job_daily(alarm)

