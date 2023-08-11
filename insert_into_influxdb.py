import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json
# Set up the InfluxDB connection
host = 'localhost' 
port = 8086 
username = 'mani'  
password = '11221122' 
org = 'custeye' 
bucket = 'bgp' 

client = InfluxDBClient(url=f"http://{host}:{port}", token='', org=org, username=username, password=password)

bucket="bgp"
write_api = client.write_api(write_options=SYNCHRONOUS)
 
with open("file_migration/all_neis_details_sharable_u.json", "r") as file:
    data = json.load(file)
# Loop through the data and create data points
for item in data["data"]:
    device_name = item["device_name"]
    vrf_name = item["vrf_name"]
    peer_address = item["peer_address"]
    received_value = int(item["received_prefixes"])
    advertised_value = int(item["advertised_prefixes"])

    # Create the data point
    point = (
        Point("bgpstat")
        .tag("device_name", device_name)
        .tag("vrf_name", vrf_name)
        .tag("peer_address", peer_address)
        .field("received_value", received_value)
        .field("advertised_value", advertised_value)
    )
    write_api.write(bucket=bucket, org="custeye", record=point)




query_api = client.query_api()
query = 'from(bucket:"bgp")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "bgpstat")'
result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

print(results)