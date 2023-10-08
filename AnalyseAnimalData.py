import json


f = open("data.json", "r", encoding="utf-8")
data = f.read()
f.close()

dict = json.loads(data)

names = dict.keys
