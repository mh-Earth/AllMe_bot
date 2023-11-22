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
"""
commands_usages:Final = {
    "/wiki":"/wiki <your search>",
    '/trackinsta':"/trackinsta <insta profile url> <option>"
}

trackInsta_help_message = '''
**Add a tracker to an Instagram private ID**

Usage: `/trackinsta <username> <option>`

**Options:**
\- `status`: Get the status of a tracker \(`/trackinsta tracker_name\[username\] status`\)
\- `initial`: Get the initials of a tracker \(`/trackinsta tracker_name\[username\] initial`\)
\- `history`: Get the history of a tracker \(`/trackinsta tracker_name\[username\] history`\)
\- `trackinsta\?`: Get all active trackers \(`/trackinsta trackinsta\?`\)
\- `remove`: Remove a tracker \(`/trackinsta tracker_name\[username\] remove`\)
\- `help\?`: Get this menu \(`/trackinsta help\?`\)

'''