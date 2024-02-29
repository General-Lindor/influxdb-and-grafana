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
        os.system(os.path.join(__location__(), "influx.bat"))
        #os.system("C:/users/admin/Desktop/influx.bat")
        load_dotenv()
        self.BUCKET = os.getenv("INFLUXDB_BUCKET")
        self.client = InfluxDBClient(url = os.getenv("INFLUXDB_URL"), token = os.getenv("INFLUXDB_TOKEN"), org = os.getenv("INFLUXDB_ORG"))
        self.write_api = self.client.write_api()
        
        #structure: {point  : {field  : getter}}
        #types:     {string : {string : lambda}}
        self.points = {}
    
    def write(self, influxpoint):
        self.write_api.write(bucket = self.BUCKET, record = influxpoint)
    
    def add(self, point, field, getter):
        m = merge(self.points, {point : {field : getter}})
        print(m)
        self.points = m
    
    def tick(self):
        for point, fields in self.points.items():
            for field, getter in fields.items():
                value = getter()
                influxpoint = Point(point).field(field, value)
                self.write(influxpoint)
                print("point: " + repr(point) + ",	field: " + repr(field) + ",	value: " + repr(value))
    
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

engine = influxdb()
engine.add("CPU", "Auslastung", lambda: psutil.cpu_percent(interval = 1))
engine.add("CPU", "Frequenz", lambda: psutil.cpu_freq().current)
engine.add("Functions", "sine", sin)
engine.run()
while True:
    pass

#Execute Flux Queries Example
"""
query_api = client.query_api()

ver = "data" # This variable would actually come from a function
params = {
    "pVersion": ver,
}
query =                      '''from(bucket: "db")
                                |> range(start: -200d)
                                |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
                                |> filter(fn: (r) => r._measurement == "test_result")
                                |> filter(fn: (r) => r.version == pVersion)
                                |> keep(columns: ["_time", "test", "run", "status_tag", "duration_sec", "version"])'''

df = query_api.query_data_frame(query=query, params=params)
"""