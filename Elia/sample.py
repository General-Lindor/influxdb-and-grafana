import influxdb_client, os
from influxdb_client import Point
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("INFLUXDB_TOKEN")
ORG = os.getenv("INFLUXDB_ORG")
BUCKET = os.getenv("INFLUXDB_BUCKET")
URL = os.getenv("INFLUXDB_URL")

point = Point("WEATHER").tag("location", "Berlin").field("temperature", 21)

write_client = influxdb_client.InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_client.write(bucket=BUCKET, org=ORG, record=point)
