from typing import Final


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

trackInsta_help_message = '''
**Add a tracker to an Instagram private ID**

Usage: `/trackinsta <username> <option>`

**Options:**
\- `status`: Get the status of a tracker \(`/trackinsta tracker_name\[username\] status`\)
\- `initial`: Get the initials of a tracker \(`/trackinsta tracker_name\[username\] initial`\)
\- `history`: Get the history of a tracker \(`/trackinsta tracker_name\[username\] history`\)
\- `remove`: Remove a tracker \(`/trackinsta tracker_name\[username\] remove`\)
\- `options`: Get available options \(/`/trackinsta options?`\)
\- `trackinsta\?`: Get all active trackers \(`/trackinsta trackinsta\?`\)
\- `help\?`: Get this menu \(`/trackinsta help\?`\)

'''
trackinsta_option_list = '''
**Available options for trackinsta command**

\- `status`: Get the status of a tracker 
\- `initial`: Get the initials of a tracker 
\- `history`: Get the history of a tracker 
\- `remove`: Remove a tracker 
\- `options`: Get this menu
\- `trackinsta\?`: Get all active trackers 
\- `help\?`: Get help menu

Usage: `/trackinsta <username> <option>`

'''
