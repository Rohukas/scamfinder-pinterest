import datetime
import json


time_format = "%a, %d %b %Y %H:%M:%S +%f"


with open("output.json") as f:
    data = f.read()

search = json.loads(data)

up_to_date = []
for item in search:
    created_at = datetime.datetime.strptime(item['created_at'], time_format)
    if created_at > datetime.datetime(2020, 1, 6):
        print(item['link'])
