import random
from faker import Faker
import uuid
from Base import Base,TrackinstaDataModel

fake = Faker()
connector = Base()
import random
import string

def generate_random_url(length=10):
    # Generate a random string of alphanumeric characters
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    # Combine the random string with the base URL
    random_url = f"https://{random_string}.com"
    
    return random_url

def is_url_change():
    pop = random.randint(0,100)
    if pop > 90:
        return generate_random_url()
    return None

user_id = random.randint(6000000000,6999999999)
name = fake.name()
user_name = name.replace(" ",".")

def resister():
    uid=connector._gen_uuid()

    data = TrackinstaDataModel(
        uid=uid,
        username=user_name,
        follower=random.randint(1,1000),
        following=random.randint(1,1000),
        full_name=name,
        dp=is_url_change(),
        isPrivate=True
    )

    connector.resister(
        username='meherab',
        first_name='meherab',
        last_name="hossain",
        user_id=user_id,
        TrackerDataModel=data
    )

def populate_demo():

    for i in range(100):
        uid=connector._gen_uuid()

        data = TrackinstaDataModel(
            uid=uid,
            username=user_name,
            follower=random.randint(1,1000),
            following=random.randint(1,1000),
            full_name=name,
            dp=is_url_change(),
            isPrivate=True
        )

        connector.add_continues(6969696969,user_name,uid)
        connector.add_trackerData(data)

# def add_new_tracker():
#     data = TrackinstaDataModel(
#         uid=uid,
#         username=user_name,
#         follower=random.randint(1,1000),
#         following=random.randint(1,1000),
#         full_name=name,
#         dp=is_url_change(),
#         isPrivate=True
#     )
#     connector.add_trackerData()

resister()
populate_demo()