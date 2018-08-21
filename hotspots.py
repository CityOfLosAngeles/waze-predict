from datetime import datetime
import time
import pandas as pd
from cover_path import cover_path, increment
from ast import literal_eval
from pprint import pprint
import json

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

weather_dict = get_weather()

def index_streets():
    print("Indexing streets.")
    streets_df = pd.read_csv("data/street_grid.csv")
    streets = {}
    ind = {}

    index = 0
    m = len(streets_df)
    for i,r in streets_df.iterrows():
        if i%10000==0:
            print("{} of {}".format(i,m))
        # target = (r['streets'], r['type'], r['intersection'], {})
        street = literal_eval(r['coordinates'])
        if street not in streets:
            streets[street] = index
            ind[index] = street
            index += 1

    print("done indexing streets.")
    return (streets, ind, index+1)

streets, index, array_len = index_streets()


"""
cur_time = lb
while cur_time <= ub:
    time = datetime.fromtimestamp(cur_time)
    hour = time.hour
    day_of_week = time.weekday()
    weather = weather_dict[(time.date(),hour)]
    print("{}: {} - {}".format(day_of_week,hour,weather))
    cur_time += 60*60
"""


# creates snapshots of the city
# each the keys are times and hours
# the output is the indexed grid (1 for jammed, 0 for not jammed)
def construct_snapshots():
    print("Constructing snapshots.")
    jams_df = pd.read_csv("data/jams.csv")

    states = {}

    for i,r in jams_df.iterrows():
        if i%5000 == 0:
            print("{} of {}".format(i,len(jams_df['street'])))
        time = datetime.fromtimestamp(r['pub_millis']/1000)
        hour = time.hour
        day_of_week = time.weekday()
        weather = weather_dict[(time.date(),hour)]
        path = literal_eval(r['line'])
        key = (time.date(),time.hour)
        if key not in states:
            states[key] = [0] * array_len

        covered_path = cover_path(path)
        for s in covered_path:
            # we are just going to throw out our data that didn't get caught by our grid
            # sorry :(
            # this is a tiny part (~0.5%) of the data anyways
            if s in streets:
                states[key][streets[s]] = 1
    print("Done constructing snapshots.")
    return states

states = construct_snapshots()

def check_states(states):
    for k in states:
        bad = 0
        good = 0
        for s in states[k]:
            if s == 0:
                bad += 1
            elif s == 1:
                good += 1
            else:
                print("BIZARRE RESULT. INVESTIGATE.")
        print("{}: {} unjammed, {} jammed".format(k,bad,good))

# check_states(states)


# using timed snapshots, aggregate buckets so we can get
# an idea of frequency at different times and locations
def construct_buckets(states):
    print("Constructing buckets.")
    buckets = {}
    index = 0
    m = len(states.keys())
    for key in states:
        if index%100 == 0:
            print("{} of {}".format(index,m))
        index += 1
        date,hour = key
        day_of_week = date.weekday()
        if day_of_week < 5:
            day_of_week = "weekday"
        elif day_of_week < 6:
            day_of_week = "saturday"
        else:
            day_of_week = "sunday"
        new_key = (day_of_week,hour)
        if new_key not in buckets:
            buckets[new_key] = [0] * array_len
        for i in range(array_len):
            buckets[new_key][i] += states[key][i]
    print("done constructing buckets")
    return buckets

buckets = construct_buckets(states)

def check_buckets(buckets):
    for k in sorted(buckets.keys()):
        print(k)
        dist = {}
        for s in buckets[k]:
            if s in dist:
                dist[s] += 1
            else:
                dist[s] = 1
        for k in sorted(dist.keys()):
            print("{}: {}".format(k,dist[k]))
        print()

def int_to_day(n):
    if n == 0:
        return "Monday"
    elif n == 1:
        return "Tuesday"
    elif n == 2:
        return "Wednesday"
    elif n == 3:
        return "Thursday"
    elif n == 4:
        return "Friday"
    elif n == 5:
        return "Saturday"
    elif n == 6:
        return "Sunday"
    else:
        return "Error"

def make_geojsons(buckets,index):
    for k in sorted(buckets.keys()):
        geojson = {}
        geojson['type'] = "FeatureCollection"
        features = []
        for i in range(len(buckets[k])):
            if buckets[k][i] > 0:
                square = index[i]
                x,y = increment(square)
                feature = {}
                feature['type'] = "Feature"
                feature['geometry'] = {}
                feature['geometry']['type'] = "Polygon"
                feature['geometry']['coordinates'] = [
                    [
                        [x[0], y[0]],
                        [x[1], y[0]],
                        [x[1], y[1]],
                        [x[0], y[1]],
                        [x[0], y[0]]
                    ]
                ]
                feature['properties'] = {}
                feature['properties']['incidents'] = buckets[k][i]
                features.append(feature)
        geojson['features'] = features
        filename = "geojsons/{}-{}.geojson".format(k[0],k[1])
        with open(filename, "w") as f:
            f.write(json.dumps(geojson, indent = 4))

make_geojsons(buckets,index)

