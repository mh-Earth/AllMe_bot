from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt
import random
from .api import BaseConnector
from matplotlib import colormaps

class ActivityPlot:
    '''
    activity (scatter plot) = x-axis conditions y-axis time (0-24 or 12am-12pm)
    condition 1: if private activity will be follower up and following up
    condition 2: if not private activity will be following up
    condition 3: bio change, username change, full-name change,privacy change
    '''

    def __init__(self,user_id:int,tracker_name:str) -> None:
        self.api = BaseConnector()
        self.user_id = user_id
        self.tracker_name = tracker_name

        
    def _timestamp_to_readable_format(self,timestamp:float) -> str:
        return  datetime.fromtimestamp(timestamp).strftime('%H:%m')


    def _add_noise(self,n:int):
        return n+(random.random())
    def chose_colormap(self) -> str:
        return random.choice(list(colormaps))

    def plot(self):
        hour = []
        minute = []
        timestamp = self.api.get_tracker_data_by_column(self.user_id,self.tracker_name,'timestamp')
        timestamp = list(map(self._timestamp_to_readable_format,timestamp))

        timestamp.sort()
        for time in timestamp:
            h,s = time.split(":")
            hour.append(int(h))
            minute.append(int(s))
                

        all_acts = [hour.count(i) for i in set(hour)]
        # time = list(set(time))

        activity = []
        for c in all_acts:
            for i in range(c):
                activity.append(c)


        def add_minute_to_time():
            hour_with_minute = []
            for i,h in enumerate(hour):
                hour_with_minute.append((h+(minute[i]/100))+random.random())
            return hour_with_minute

        time = add_minute_to_time()

        # activity = list(map(self._add_noise,activity))


        # create the plot
        plt.title(f"activity of {self.tracker_name}".upper())
        plt.scatter(time,activity,alpha=0.75,s=90,cmap=self.chose_colormap(),linewidths=1,c=activity,edgecolors='black')

        plt.tight_layout()

        plt.xticks([i for i in range(0,25)])
        plt.yticks([i for i in range(0,max(all_acts)+3)])

        plt.colorbar().set_label("Activity count around all day")
        

        plt.xlabel('Time (00-24) -->')
        plt.ylabel('Activity -->')
        plt.grid(True, linestyle='--', alpha=0.7)
        

        # Save the plot to a BytesIO object
        plot = BytesIO()
        plt.savefig(plot, format='png')
        plot.seek(0)
        plt.clf()

        return plot


class FFPlot:

    def __init__(self,user_id:int,tracker_name:str) -> None:
        self.api = BaseConnector()
        self.user_id = user_id
        self.tracker_name = tracker_name


    def plot(self):
        
        continue_data = self.api._get_continuous(self.user_id,self.tracker_name)
        following = []
        followers = []
        for data in continue_data:
            following.append(data['following'])
            followers.append(data['follower'])
            

        fig,(axi1,axi2) = plt.subplots(1,2)
        fig.suptitle(f"Follower and following of {self.tracker_name}")
        axi1.plot(followers, label='follower',c="r")
        axi1.set_title("Follower")

        axi2.set_title("Following")
        axi2.plot(following, label='following',c="g")
        # # plt.
        axi2.legend()
        axi1.legend()

        # Save the plot to a BytesIO object
        plot = BytesIO()
        plt.savefig(plot, format='png')
        plot.seek(0)
        plt.clf()

        return plot
    def follower(self):
        
        continue_data = self.api._get_continuous(self.user_id,self.tracker_name)
        followers = [data['follower'] for data in continue_data]
            

        plt.title(f"Followers of {self.tracker_name}")
        plt.plot(followers, label='follower',c="g")
        plt.legend()

        # Save the plot to a BytesIO object
        plot = BytesIO()
        plt.savefig(plot, format='png')
        plot.seek(0)
        plt.clf()

        return plot
    
    def following(self):
        
        continue_data = self.api._get_continuous(self.user_id,self.tracker_name)
        following = [data['following'] for data in continue_data]
            

        plt.title(f"Followings of {self.tracker_name}")
        plt.plot(following, label='following',c="g")
        plt.legend()

        # Save the plot to a BytesIO object
        plot = BytesIO()
        plt.savefig(plot, format='png')
        plot.seek(0)
        plt.clf()

        return plot
    
    def both(self):
        
        continue_data = self.api._get_continuous(self.user_id,self.tracker_name)
        following = [data['following'] for data in continue_data]
        followers = [data['follower'] for data in continue_data]
            

        plt.title(f"Followings of {self.tracker_name}")
        plt.plot(followers, label='follower',c="g")
        plt.plot(following, label='following',c="r")
        plt.legend()

        # Save the plot to a BytesIO object
        plot = BytesIO()
        plt.savefig(plot, format='png')
        plot.seek(0)
        plt.clf()

        return plot
