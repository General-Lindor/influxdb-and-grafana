import os
import psutil
from time import sleep
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point

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
    
    def write(self, value):
        self.write_api.write(bucket = self.BUCKET, record = value)
    
    def add(self, point, field, getter):
        self.points = merge(self.points, {point : {field : getter}})
    
    def tick(self):
        for point, fields in self.points.items():
            for field, getter in fields.items():
                value = getter()
                newpoint = Point(point).field(field, value)
                self.write(value)
                print("point: " + repr(point) + ",	field: " + repr(field) + ",	value: " + repr(value))
    
    #should parallelize this method
    def run(self, condition = True, duration = 1):
        while condition:
            self.tick()
            sleep(duration)

engine = influxdb()
engine.add("CPU", "Auslastung", lambda: psutil.cpu_percent(interval = 1))
engine.add("CPU", "Frequenz", lambda: psutil.cpu_freq().current)
engine.run()