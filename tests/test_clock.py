import requests
from datetime import datetime

url = "http://127.0.0.1:8000/clock/"
myobj = {"id": "clock1", "interval": 300, "start": datetime.now().astimezone()}

x = requests.post(url, json=myobj)

print(x.text)


myobj = {"id": "clock1"}
url = "http://127.0.0.1:8000/clock/clock1"
x = requests.get(url, json=myobj)

print(x.text)
