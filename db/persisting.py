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
    pop = random.random() * 100
    if pop > 90:
        return generate_random_url()
    return None

def is_bio_change():
    pop = random.random() * 100
    if pop > 90:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return None
# random.randint(6000000000,6999999999)
user_id = '20'
name = 'meherab h'
user_name = name.replace(" ",".")

def resister():
    uid=connector._gen_uuid()

    data = TrackinstaDataModel(
        uid=uid,
        username=user_name,
        follower=random.randint(1,1000),
        following=random.randint(1,1000),
        full_name=name,
        bio=is_bio_change(),
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
            bio=is_bio_change(),
            dp=is_url_change(),
            isPrivate=True
        )

        connector.add_continues(user_id,user_name,uid)
        connector.add_trackerData(data)

def change_last_dp(user_id,tracker_name):
    data_ids = connector.get_continues(user_id,tracker_name).text.split(',')
    data_ids.reverse()
    for ids in data_ids:
        dp = connector.get_tracker_data(ids).text['dp']
        if dp == None:
            continue
        else:
            last_do_id = ids # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
            break
        
    trackerdata = connector.get_tracker_data_obj(last_do_id)
    trackerdata.text.dp = 'https://media.istockphoto.com/id/1455965102/photo/beautiful-sunrise-bursting-through-the-eucalyptus-trees-as-it-rises-over-a-mountain-beside-a.jpg?s=1024x1024&w=is&k=20&c=wYGK__qz9i8M7NfBvkNtkfbWNoiBxDLGi64PQjOo_wY='

    connector.session.commit()
    ...
    
def change_last_bio(user_id,tracker_name):
    data_ids = connector.get_continues(user_id,tracker_name).text.split(',')
    data_ids.reverse()
    for ids in data_ids:
        dp = connector.get_tracker_data(ids).text['bio']
        if dp == None:
            continue
        else:
            last_do_id = ids # ('ec504cd0-a476-468c-807f-0151af132894', 'https://RdehaeGHZI.com')
            break
        
    trackerdata = connector.get_tracker_data_obj(last_do_id)
    trackerdata.text.bio = 'Bio change!!'

    connector.session.commit()

# resister()
# populate_demo()
    
change_last_dp(6540965739,'blackpinkofficial')
change_last_bio(6540965739,'blackpinkofficial')