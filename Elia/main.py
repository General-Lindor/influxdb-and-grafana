from multiprocessing import Process
import os, time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
from typing import List
import psutil
from time import sleep
from random import randint

load_dotenv()
TOKEN = os.getenv("INFLUXDB_TOKEN")
ORG = os.getenv("INFLUXDB_ORG")
BUCKET = os.getenv("INFLUXDB_BUCKET")
URL = os.getenv("INFLUXDB_URL")

class InfluxDBWriteClient:
    def __init__(self):
        self.client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        
        self.io = psutil.net_io_counters()
        self.bytes_sent = self.io.bytes_sent
        self.bytes_recv = self.io.bytes_recv

    def start_writing(self) -> None:
        p1 = Process(target=self._write_cores)
        p2 = Process(target=self._write_network_usage)
        p1.start()
        p2.start()

    def _write_cores(self) -> None:
        while True:
            sleep(1)
            measurements: List[float] = []

            for idx, value in enumerate(psutil.cpu_percent(percpu=True)):
                measurements.append({
                    "measurement": f'Core {idx + 1}',
                    "fields": {"cpu_percentage": value}
                    })

            self.write_api.write(bucket=BUCKET, org=ORG, record=measurements)

    def _write_network_usage(self) -> None:
        while True:
            sleep(1)

            new_io = psutil.net_io_counters()
            upload_speed = new_io.bytes_sent - self.bytes_sent
            download_speed = new_io.bytes_recv - self.bytes_recv
            
            measurement = {
                    "measurement": 'Upload',
                    "fields": {"MB/s": round(upload_speed / (1024 ** 2), 2)}
                    }, {
                    "measurement": 'Download',
                    "fields": {"MB/s": round(download_speed / (1024 ** 2), 2)}
                    }
            
            self.write_api.write(bucket=BUCKET, org=ORG, record=measurement)
            self.bytes_sent = new_io.bytes_sent
            self.bytes_recv = new_io.bytes_recv



def main() -> None:
    write_client = InfluxDBWriteClient()
    write_client.start_writing()

if __name__ == '__main__':
    main()