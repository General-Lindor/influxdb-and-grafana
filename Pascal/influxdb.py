import os
import psutil
from time import sleep
from time import time
import math
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point
import threading

#if __name__ == "__main__

iterables = (list, tuple, set)
#merge two python objects; if they're not compatible, return the second
def merge(first, second):
    
    #get types
    type_first = type(first)
    type_second = type(second)
    
    #both are dicts
    if (type_first == dict) and (type_second == dict):
        for key, value in second.items():
            first[key] = merge(first.get(key), value)
    
    #both are iterable
    elif (type_first in iterables) and (type_second in iterables):
        newlist = []
        for element in second:
            if not (element in first):
                newlist.append(element)
        first = type_first(list(first).extend(newlist))
    
    #both are incompatible
    else:
        first = second
    
    #and out
    return first

__location__ = lambda: os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
ftype = type(lambda: 3)
class influxdb():
    def __init__(self):
        os.system(os.path.join(__location__(), "startDB.bat"))
        #os.system("C:/users/admin/Desktop/influx.bat")
        
        load_dotenv()
        self.URL = os.getenv("INFLUXDB_URL")
        self.BUCKET = os.getenv("INFLUXDB_BUCKET")
        self.TOKEN = os.getenv("INFLUXDB_TOKEN")
        self.ORG = os.getenv("INFLUXDB_ORG")
        
        self.client = InfluxDBClient(url = self.URL, token = self.TOKEN, org = self.ORG)
        self.write_api = self.client.write_api()
        self.delete_api = self.client.delete_api()
        self.query_api = self.client.query_api()
        
        #structure: {point  : {field  : getter}}
        #types:     {string : {string : lambda}}
        self.points = {}
    
    def query(self, q):
        return self.query_api.query(query = q)
    
    def write(self, influxpoint):
        self.write_api.write(bucket = self.BUCKET, record = influxpoint)
    
    def delete(self, measurement, field, start, end):
        delete_api.delete(start, "now()", f'_measurement={measurement}', bucket = self.BUCKET, org = self.ORG)
    
    def add(self, point, field, getter):
        m = merge(self.points, {point : {field : getter}})
        self.points = m
    
    def tick(self):
        for point, fields in self.points.items():
            for field, getter in fields.items():
                value = getter()
                influxpoint = Point(point).field(field, value)
                self.write(influxpoint)
                #print("point: " + repr(point) + ",	field: " + repr(field) + ",	value: " + repr(value))
    
    def __run(self, condition, duration):
        while condition:
            self.tick()
            sleep(duration)
    
    def run(self, condition = True, duration = 0):
        x = threading.Thread(target = self.__run, args = (condition, duration), daemon = False)
        #x = self.__run(condition, duration)
        x.start()

def sin():
    return math.sin(time())

"""
>>> import psutil
>>> psutil.sensors_temperatures()
{'acpitz': [shwtemp(label='', current=47.0, high=103.0, critical=103.0)],
 'asus': [shwtemp(label='', current=47.0, high=None, critical=None)],
 'coretemp': [shwtemp(label='Physical id 0', current=52.0, high=100.0, critical=100.0),
              shwtemp(label='Core 0', current=45.0, high=100.0, critical=100.0)]}
>>>
>>> psutil.sensors_fans()
{'asus': [sfan(label='cpu_fan', current=3200)]}
>>>
>>> psutil.sensors_battery()
sbattery(percent=93, secsleft=16628, power_plugged=False)
>>>
"""

engine = influxdb()
engine.add("CPU", "Auslastung", lambda: float(psutil.cpu_percent(interval = 1)))
engine.add("CPU", "Frequenz", lambda: float(psutil.cpu_freq().current))
#sensors temperature is currently not implemented on windows
#engine.add("CPU", "temperature", lambda: psutil.sensors_temperatures()["coretemp"].current)
engine.add("Functions", "sine", sin)
engine.run()

#Execute Flux Queries Example
query_api = engine.query_api

ver = "data" # This variable would actually come from a function
params = {
    "pVersion": ver,
}
queryAll = '''data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and ((r._field == "Auslastung") or (r._field == "Frequenz")))
    |> group(columns: ["_field"], mode: "by")
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_results") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

queryA = '''data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and (r._field == "Auslastung"))
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_resultsA") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

queryF = '''data = from(bucket: "system_monitoring")
    |> range(start: -15m)
    |> filter(fn: (r) => (r._measurement == "CPU") and (r._field == "Frequenz"))
    |> keep(columns: ["_time", "_field", "_value"])
    |> yield(name: "_resultsF") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

import matplotlib.pyplot as plot
import pandas


def normalize_df(df):
    return df/df.iloc[0,:]

def numerize(data):
    try:
        return pandas.to_numeric(data)
    except Exception as e:
        try:
            return float(data)
        except Exception as ex:
            return data

#fig, ((ax1, ax2)) = plot.subplots(ncols=2, nrows=1, figsize=(15, 6))
fig, ((ax1, ax2)) = plot.subplots(ncols=2, nrows=1)

ax1.set_xlabel("Zeit", fontsize=12)
ax1.set_ylabel("CPU-Auslastung", fontsize=12)

ax2.set_xlabel("Zeit", fontsize=12)
ax2.set_ylabel("CPU-Frequenz", fontsize=12)

plot.title('System Monitoring')
plot.legend(loc='upper left', fontsize=12)
plot.tight_layout()
plot.style.use('bmh')
plot.grid(True)

while True:
    try:
        ax1.clear()
        ax2.clear()
        
        dfA = query_api.query_data_frame(query=queryA, params=params)
        dfF = query_api.query_data_frame(query=queryF, params=params)
        
        dfA = dfA.drop(columns=["result", "table", "_field"])
        dfF = dfF.drop(columns=["result", "table", "_field"])
        
        dfA = dfA.set_index("_time")
        dfF = dfF.set_index("_time")
        
        dfA.apply(numerize)
        dfF.apply(numerize)
        
        ax1.plot(dfA)
        ax2.plot(dfF)
    except Exception as e:
        print(e)
    plot.pause(0.1)
    #sleep(0.1)