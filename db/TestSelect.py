from connect import session
from models import Trackers,User,TrackinstaData
from sqlalchemy import select

# result = select(User).where(User.username.in_(['John','cathy']))
# result = session.scalars(result)

# for user in result:
#     print(user.comments)

# allUser = session.query(Trackinsta).all()

# for user in allUser:
#     print(user.tracker_name)

state = select(Trackers).join(User.trackers).where(
    Trackers.tracker == 'afnan'
)

result = session.scalars(state)

# print(result)
for res in result:
    print(res)

