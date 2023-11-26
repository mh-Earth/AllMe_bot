from typing import Final
from commands.trackinsta.options import *

response_key:Final = {
    "/wiki":"/wiki <your search>",
    '/trackinsta':"/trackinsta <instagram username> <options>"
}

help_menu:Final = """
/start - start bot
/help - open this menu
/custom - random thing will happen
/wiki - search topic from wikipedia
/trackinsta - add a tracker to an Instagram private ID
"""
commands_usages:Final = {
    "/wiki":"/wiki <your search>",
    '/trackinsta':"Use `/trackinsta help?` to see manual"
}

trackInsta_help_message = f'''
**Add a tracker to an Instagram private ID**

Usage: `/trackinsta <username> <option>`

**Options:**
\- `{STATUS}`: Get the status of a tracker \(`/trackinsta tracker_name\[username\] status`\)
\- `{INITIAL}`: Get the initials of a tracker \(`/trackinsta tracker_name\[username\] initial`\)
\- `{HISTORY}`: Get the history of a tracker \(`/trackinsta tracker_name\[username\] history`\)
\- `{REMOVE}`: Remove a tracker \(`/trackinsta tracker_name\[username\] remove`\)
\- `{OPTIONS}`: Get available options \(/`/trackinsta options?`\)
\- `{CHECKOUT}`: checkout a users live info \(/trackinsta \<username\> checkout\)
\- `{LOG}`: Get activity history \(/trackinsta \<username\> checkout\)
\- `{ALL}`: Get all active trackers \(`/trackinsta trackinsta\?`\)
\- `{HELP}`: Get this menu \(`/trackinsta help\?`\)

'''
trackinsta_option_list = F'''
**Available options for trackinsta command**

\- `{STATUS}`: Get the status of a tracker 
\- `{INITIAL}`: Get the initials of a tracker 
\- `{HISTORY}`: Get the history of a tracker 
\- `{REMOVE}`: Remove a tracker 
\- `{CHECKOUT}`: Checkout a users live info
\- `{LOG}`: Get activity history
\- `{OPTIONS}`: Get this menu
\- `{ALL}`: Get all active trackers 
\- `{HELP}`: Get help menu

Usage: `/trackinsta <username> <option>`

'''
