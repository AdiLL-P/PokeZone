import json
from replit import db
dic = {}
for i in db.keys():
  if i == 'pokezoned1':
    continue
  dic[i] = list(db[i])


with open('stats.json','w') as lol:
  json.dump(dic,lol,indent=4)