import requests
from datetime import date, datetime

urlbase = "http://127.0.0.1:8000/clock/"
test_clock = "clock1"


def make():
    url = urlbase
    myobj = {"id": "clock1", "interval": 300, "start": str(datetime.now().astimezone())}

    return requests.post(url, json=myobj)


def get():
    url = f"{urlbase}{test_clock}"
    return requests.get(url)


def now():
    url = f"{urlbase}{test_clock}now"
    return requests.get(url)


def tick():
    url = f"{urlbase}{test_clock}tick"
    return requests.put(url)


def reset():
    url = f"{urlbase}{test_clock}reset"
    return requests.put(url)


print(make().text)
print(get().text)
print(now().text)
print(tick().text)
print(get().text)
print(reset().text)
print(get().text)
