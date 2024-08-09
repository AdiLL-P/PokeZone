import pymongo
import asyncio
import motor.motor_asyncio
import os
from dotenv.main import load_dotenv
load_dotenv()
pasw = os.environ['password']
name = os.environ['name']
clustor = os.environ['clustor']
client = pymongo.MongoClient("mongodb+srv://"+name+":"+pasw+clustor+".gqqt9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client['Bot']
client2 = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://"+name+":"+pasw+clustor+".gqqt9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db2 = client2['Bot']
loop = asyncio.get_event_loop()
async def id_creator(idd,id2,tim): #creates a user id
  try:
    if not await checkExist(idd):
      global collections
      idd = str(idd)
      user = db2[idd]
      await user.insert_one({'by':id2,'catches':0,'released':0,'shinies':0,'bal':0,'redeem':0,'select':-1,'shard':0,'invited':0,'time':tim})
      collections.append(idd)
      return True
    else: return False
  except:
    return False


collections = list( db.list_collection_names())
async def checkExist(idd):#checks if a id exists in mongodb or not
  if str(idd) in collections:
    return True
  else:
    return False

async def getbal(idd):#returns bal ko
  idd = str(idd)
  if idd in await db2.list_collection_names():
    user = db2[idd]
    a = await user.find_one({},{'_id':0,'bal':1})
    return a['bal']

async def setbal(idd,amount):#updating bal
  idd = str(idd)
  amount = int(amount)
  if idd in await db2.list_collection_names():
    user = db2[idd]
    old =await user.find_one({},{'_id':0,'bal':1})
    current = old['bal']
    newbal = current+amount
    new = {'$set':{'bal':newbal}}
    await user.update_one(old,new)
    return True
  else:
    return False
async def getredeem(idd):#your amount of redeem
  idd = str(idd)
  if idd in await db2.list_collection_names():
    user = db2[idd]
    a = await user.find_one({},{'_id':0,'redeem':1})
    return a['redeem']

async def setredeem(idd,amount):#updating redeem
  idd = str(idd)
  amount = int(amount)
  if idd in await db2.list_collection_names():
    user = db2[idd]
    old = await user.find_one({},{'_id':0,'redeem':1})
    current = old['redeem']
    newrr = current+amount
    new = {'$set':{'redeem':newrr}}
    await user.update_one(old,new)
    return True
  else:
    return False

async def pokeadder(idd,data):#takes data as dictionary . look in addpoke in poke.py
  idd = str(idd)
  user = db2[idd]
  NotFound = True
  c =1 
  async for i in user.find({},{'_id':0,'ids':1}).limit(2):
    if c ==1:
      dell = i
    if i !={}:
        NotFound = False
    c+=1
  if NotFound:
    data['ids'] = 1
    await user.insert_one(data)
    print("Added "+data['name']+" successfully to "+idd)
    inc = {'$inc':{'catches':1}}
    await user.update_one(dell,inc)
  else:
    if data['ids'] ==-1:
      current = None 
      async for i in user.find({},{'ids':1}).sort('ids',-1).limit(1):
        current=i['ids']
      data['ids'] = current+1
      await user.insert_one(data)
      print("Added "+data['name']+" successfully to "+idd)
      inc = {'$inc':{'catches':1}}
      await user.update_one(dell,inc)
    else:
      await user.find_one_and_replace({'ids':data['ids']},data)
    

async def lates(idd):#takes your id and returns the latest caught poke 
  idd = str(idd)
  user = db2[idd]
  NotFound = True
  async for i in user.find({},{'_id':0,'ids':1}).limit(2):
    if i !={}:
        NotFound = False
  if NotFound:
    return False
  current = None
  async for i in user.find({},{'_id':0}).sort('ids',-1).limit(1):
      current = i
  return current

async def selector(idd,arg):#selects a poke 
  current = None
  idd = str(idd)
  user = db2[idd]
  current = None
  async for i in user.find({},{'_id':0}).sort('ids',-1).limit(1):
    current = i 
  if arg > current['ids']:
    return False 
  old = await user.find_one({},{'_id':0,'select':1})
  new = {'$set':{'select':arg}}
  await user.update_one(old,new)
  return True

async def infoc(idd):#returns data of your selected poke else returns false
  idd = str(idd)
  user = db2[idd]
  hi = await user.find_one({},{'select':1})
  selected  = hi['select']
  if selected == -1:
    return False
  data= await user.find_one({'ids':selected},{'_id':0})
  return data

async def selected(idd):#returns select pokemon number
  idd = str(idd)
  user = db2[idd]
  hi = await user.find_one({},{'select':1})
  selected  = hi['select']
  return selected

async def infonum(idd,arg):#returns details of a pokemon at a certain number(arg)
  idd = str(idd)
  arg = int(arg)
  user = db2[idd]
  async for i in user.find({},{'_id':0}).sort('ids',-1).limit(1):
    current = i 
  if arg > current['ids']:
    return False
  data=await user.find_one({'ids':arg},{'_id':0})
  return data

clead = {}
rlead = {}
catlead = {}
relead = {}
shlead = {}
shalead = {}
cflag = True
rflag = True
catflag = True
reflag = True
shflag = True
shaflag = True
async def leader(what):#returns usersid along with their bal or redeem .depending on what is passed
    global rlead
    global clead
    global catlead
    global relead
    global shlead
    global shalead
    global catflag
    global reflag
    global shflag
    global shaflag
    global cflag
    global rflag
    uppass = False
    har = {}
    if what == 'redeem':
      yield rlead
      if rflag:
        rflag = False
        uppass = True
    elif what == 'catches':
      yield catlead
      if catflag:
        catflag = False
        uppass = True
    elif what == 'released':
      yield relead
      if reflag:
        reflag = False
        uppass = True
    elif what == 'shinies':
      yield shlead
      if shflag:
        shflag = False
        uppass = True
    elif what =='shard':
      yield shalead
      if shaflag:
        shaflag = False
        uppass = True
    else:
      what = 'bal'
      yield clead
      if cflag:
        cflag = False
        uppass = True
    if uppass:
      for i in await db2.list_collection_names():
        user = db2[i]
        bal = await user.find_one({},{what:1})
        if i == 'NoSpawns' or i == 'Prefix':
          continue
        bal = bal[what]
        har[str(i)] = bal
      if what == 'redeem': 
        rlead = har
        rflag = True
      elif what == 'bal':
        clead =har
        cflag = True
      elif what == 'catches': 
        catlead =har
        catflag = True
      elif what == 'released': 
        relead =har
        reflag = True
      elif what == 'shard': 
        shalead =har
        shaflag = True
      elif what == 'shinies': 
        shlead =har
        shflag = True

async def allPokes(idd):
  order =await getorder(idd)
  if order == None or order.lower() =='number' or order.lower() == 'id':
    order = "ids"
  elif order.lower() == 'level':
    order = 'lvl'
  elif order.lower() == 'iv':
    order = 'totiv'
  idd = str(idd)
  user = db2[idd]
  pokes = []
  NotFound = True
  async for i in user.find({},{'_id':0,'ids':1,'name':1,'lvl':1,'totiv':1}).sort(order,-1):
    if i!={}:
      NotFound = False
      pokes.append(i)
  if NotFound:
    return False
  else: 
    return pokes

async def getlatest(idd):#your latest job
    idd = str(idd)
    user =db2[idd]
    a = await user.find_one({},{'_id':0,'latest':1})
    return a['latest']

async def setlatest(idd,latest):#sets your latest job
    idd = str(idd)
    user = db2[idd]
    latest = int(latest)
    a = await user.find_one({},{'_id':0})
    await user.update_one(a,{'$set':{'latest':latest}})


async def setorder(idd,typ):#sets your order
  idd = str(idd)
  if not (typ.lower() == 'iv' or typ.lower() == 'number' or typ.lower() == 'level' or typ.lower() =='id'):
     return False
  else:
     user = db2[idd]
     a = await user.find_one({},{'_id':0})
     b = {'order':typ}
     await user.update_one(a,{'$set':b})
     return True

async def getorder(idd):#returns your order
  idd = str(idd)
  user = db2[idd]
  a = await user.find_one({},{'_id':0,'order':1})
  return a.get('order')
  
#resetts a user db and returns True if resetting is successful else Flase
async def change():
  global collections
  collections = await db2.list_collection_names()

async def resetdb(idd):
    idd = str(idd)
    if idd in collections:
        user = db2[idd]
        await user.drop()
        loop.create_task(change())
        return True
    else:
        return False
  

shs = {}
for user in db.list_collection_names():
  if user == 'NoSpawns' or user == 'Prefix':
    continue
  user_col = db[user]
  a = user_col.find_one({},{'_id':0,'sh':1,'shc':1,'vhc':1})
  if a == {}:
    shs[user] = None
  else:
    d1 = a['sh']
    d2 = a['shc']
    d3 = a['vhc']
    shs[user] = [d1,d2,d3]

async def getsh(idd):
    idd = str(idd)

    data = shs.get(idd,{})
    if data !={}:
      return data

    user = db2[idd]
    a = await user.find_one({},{'_id':0,'sh':1,'shc':1,'vhc':1})
    if a == {}:
        return None
    else:
      d1 = a['sh']
      d2 = a['shc']
      d3 = a['vhc']
      return [d1,d2,d3]

async def changesh(idd):
  user_col = db2[idd]
  a = await user_col.find_one({},{'_id':0,'sh':1,'shc':1,'vhc':1})
  if a == {}:
    shs[user] = None
  else:
    d1 = a['sh']
    d2 = a['shc']
    d3 = a['vhc']
    shs[user] = [d1,d2,d3]

async def setsh(idd,poke=None,shc=None,vhc = None):
  idd = str(idd)
  user = db2[idd]
  old = await user.find_one({},{'_id':0,'bal':1})
  if vhc!= None:
    old = await user.find_one({},{'_id':0,'shc':1,'vhc':1})
    oldshc = old['shc']
    oldvhc = old['vhc']
    if vhc>0:
      new = {'shc':vhc+oldshc,'vhc':vhc+oldvhc}
    else:
      new = {'vhc':0}
  elif poke!=None:
    oldsh = await getsh(idd)
    if oldsh == None or oldsh[0] != poke: 
      new = {'sh':poke,'shc':0,'vhc':0}
    else:
      new = {'sh':poke}
  elif shc!=None:
    old = await user.find_one({},{'_id':0,'shc':1,'vhc':1})
    oldshc = old['shc']
    new = {'shc':shc+oldshc}
  await user.update_one(old,{'$set':new})
  await changesh(idd)
  return True


def resettt(a):
  if a !='True':
    return False
  for idd in db.list_collection_names():
    user = db[idd]
    user.drop()
  global collections
  collections = db.list_collection_names()
  return True

async def pkremove(idd,pkID):
  idd = str(idd)
  pkID = int(pkID)
  user = db2[idd]
  await user.delete_one({'ids':pkID})


async def gapfiller(idd):
  change = 1
  prev = 0
  idd = str(idd)
  user = db2[idd]
  async for i in user.find({}).sort("ids"):
    if i.get('ids') == None:
      continue
    change = i['ids']-prev
    if change ==1:
      prev = i['ids']
    else:
      prev = i['ids']-change+1
      this = {'ids':i['ids']}
      that = {"$set":{'ids':i['ids']-change+1}}
      user.update_one(this,that)


async def setnosp(idd):
  idd = int(idd)
  a = db2["NoSpawns"]
  a.insert_one({'idd':idd})

async def getnosp():
 lis = []
 a = db2['NoSpawns']
 async for  i in a.find({},{'_id':0}):
   lis.append(i['idd'])
 return lis

async def removenosp(idd):
  idd = int(idd)
  a = db2['NoSpawns']
  await a.delete_one({'idd':idd})

async def getshard(idd):#returns shard 
  idd = str(idd)
  if idd in await db2.list_collection_names():
    user = db2[idd]
    a = await user.find_one({},{'_id':0,'shard':1})
    shards =  a.get('shard')
    if shards == None :
      return 0 
    else:
      return shards

async def setshard(idd,amount):#updating shard
  idd = str(idd)
  amount = int(amount)
  if idd in await db2.list_collection_names():
    user = db2[idd]
    old =await user.find_one({},{'_id':0})
    current = old.get('shard')
    if current == None: current = 0
    newshard = current+amount
    new = {'$set':{'shard':newshard}}
    await user.update_one(old,new)
    return True
  else:
    return False

async def setshiny(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    inc = {'$inc':{'shinies':1}}
    await user.update_one(data,inc)

async def getshiny(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    value = data.get('shinies')
    if value == None:
      return 0
    else:
      return value  

async def getcat(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    value = data.get('catches')
    if value == None:
      return 0
    else:
      return value

async def getrel(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    value = data.get('released')
    if value == None:
      return 0
    else:
      return value

async def setrel(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    inc = {'$inc':{'released':1}}
    await user.update_one(data,inc)

async def getinviter(idd):
  idd = str(idd)
  user = db2[idd]
  data = await user.find_one({},{'_id':0})
  return data.get('by')


async def getstart(idd):
  idd = str(idd)
  user = db2[idd]
  data = await user.find_one({},{'_id':0})
  return data.get('time')


async def getinv(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    value = data.get('invited')
    if value == None:
      return 0
    else:
      return value

async def setinv(idd):
    idd = str(idd)
    user = db2[idd]
    data = await user.find_one({},{'_id':0})
    inc = {'$inc':{'invited':1}}
    await user.update_one(data,inc)


async def setpref(idd,prefix):
  idd = str(idd)
  a = db2["Prefix"]
  exit = await a.find_one({idd:{'$exists':True}})
  if exit is None:
    await a.insert_one({idd:prefix})
  else:
    await a.update_one(exit,{'$set':{idd:prefix}})

async def getpref():
 lis = {}
 a = db2['Prefix']
 async for  i in a.find({},{'_id':0}):
  a =  list(i.items())[0]
  lis[int(a[0])] = a[1]
 return lis


async def getvote(idd):#your current number of votes
   idd = str(idd)
   user = db2[idd]
   data = await user.find_one({},{'votes':1})
   return data.get('votes',0)

async def incvote(idd):
  idd = str(idd)
  user = db2[idd]
  await user.update_one({},{'$inc':{'votes':1}})


async def getcrates(idd):
  idd = str(idd)
  user = db2[idd]
  data = await user.find_one({},{'crates':1})
  val= data.get('crates',{'bronze':0,'silver':0,'golden':0,'daimond':0})
  keys = val.keys()
  for i in ('bronze','silver','golden','daimond'):
    if i not in keys:
      val[i] = 0
  
  return val 

async def setcrates(idd,crate_name,amount:int):
  if type(amount) !=int:
    return False
  if crate_name not in ('bronze','silver','golden','daimond'):
    return False
  idd = str(idd)
  user = db2[idd]
  await user.update_one({},{'$inc':{f'crates.{crate_name}':amount}})


async def mydex(idd):
  idd = str(idd)
  user =db2[idd]
  data = await user.find_one({},{'_id':0,'mydex':1})
  return data.get('mydex',{})

async def dexmany(idd,pk_id):#how many have pokes have you caught of a specific id
  idd = str(idd)
  user = db2[idd]
  data = await user.find_one({},{'_id':0,f'mydex.{pk_id}':1})
  if data == {}:
    return 0
  return data['mydex'].get(str(pk_id),0)

async def adddex(idd,id_pk:int):
  idd = str(idd)
  user = db2[idd]
  await user.update_one({},{'$inc':{f'mydex.{id_pk}':1}})

