from datetime import datetime
import time
import pandas as pd

### CHANGE THESE TO CHANGE THE TIME RANGE ###
lower_bound = datetime(2018,1,3)
upper_bound = datetime(2018,1,10)
############################################


def get_weather():
    weather_df = pd.read_csv("data/weather_data.csv")
    weather_types = set()
    weather_dict = {}
    for i,r in weather_df.iterrows():
        wt = r['HOURLYPRSENTWEATHERTYPE']
        dt = datetime.strptime(r['DATE'],"%Y-%m-%d %H:%M")
        weather = set()
        if type(wt) is str:
            wt = wt.replace("|","")
            wt = wt.strip()
            wt = wt.split(" ")
            for w in wt:
                if w=="+RA:02":
                    weather.add("heavy rain")
                elif w=="-RA:02":
                    weather.add("light rain")
                elif w=="BR:1":
                    weather.add("mist")
                elif w=="FG:2" or w=="FG:30" or w=="FG:05":
                    weather.add("fog")
                elif w=="HZ:05" or w=="HZ:7":
                    weather.add("haze")
                elif w=="RA:02" or w=="RA:61" or w=="RA:62" or w=="RA:63":
                    weather.add("rain")
                elif w=="FU:05":
                    weather.add("smoke")
                else:
                    print("Warning: unidentified weather type. Code: {}".format(w))
        else:
            weather.add("clear")
        weather_dict[(dt.date(),dt.hour)] = list(weather)
    return weather_dict

lb = int(time.mktime(lower_bound.timetuple()))
ub = int(time.mktime(upper_bound.timetuple()))

weather_dict = get_weather()

streets_df = pd.read_csv("data/street_grid.csv")
cur_time = lb
while cur_time <= ub:
    time = datetime.fromtimestamp(cur_time)
    hour = time.hour
    day_of_week = time.weekday()
    weather = weather_dict[(time.date(),hour)]
    print("{}: {} - {}".format(day_of_week,hour,weather))
    cur_time += 60*60



df = pd.read_csv("data/jams.csv")
section = df[(df['pub_millis'] >= lb*1000) & (df['pub_millis'] <= ub*1000)]


