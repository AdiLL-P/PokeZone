import random
import pokebase
from replit import db
from User import pokeadder,adddex
pok =dict(db["pokezoned1"])
donos = ['10080','10081','10082','10083','10084','10147','10148']
leggie = ["144","145","146","150","243","244","245","249","250","377","378","379","380","381","382","383","393","384","480","481","482","483","484","485","486","487","488","638","639","640","641","642","643","644","645","646","716","717","718","785","786","787","788","789","790","791","792","800","888","889","890","891","892","893","894","895","896","897","898",'10227','10226']
mythic = ["151","251","385","386","489","490","491","492","493","494","647","648","649","719","720","721","801","802","807","808","809"]
ub = ["793","794","795","796","797","798","799","803","804","805","806"]
galar = ['10159','10160','10161','10162','10163','10164','10165','10166','10167','10168','10169','10170','10171','10172','10173','10174','10176','10177']
alola = ['10091','10092','10100','10101','10102','10103','10104','10105','10106','10107','10108','10109','10110','10111','10112','10113','10114','10115']
special = ["10223"]
natures = {
  'Adamant' : ['atk','spatk'],
  'Bashful' : [None,None],
  'Bold' : ['defen','atk'],
  'Brave' : ['atk','speed'],
  'Calm' : ['spdef','atk'],
  'Careful' : ['spdef','spatk'],
  'Docile' : [None,None],
  'Gentle' : ['spdef','defen'],
  'Hardy' : [None,None],
  'Hasty' : ['speed','defen'],
  'Impish' : ['defen','spatk'],
  'Jolly' : ['speed','spatk'],
  'Lax' : ['defen','spdef'],
  'Lonely' : ['atk','defen'],
  'Mild' : ['spatk','defen'],
  'Modest' : ['spatk','atk'],
  'Naive' : ['speed','spdef'],
  'Naughty' : ['atk','spdef'],
  'Quiet' : ['spatk','speed'],
  'Quirky' : [None,None],
  'Rash' : ['spatk','spdef'],
  'Relaxed' : ['defen','speed'],
  'Sassy' : ['spdef','speed'],
  'Serious' : [None,None],
  'Timid' : ['speed','atk']
}

normal =[]
for i in pok.keys():
   if (i not in leggie) and (i not in mythic) and (i not in ub) and (i not in alola) and (i not in galar) and (i not in special):
     normal.append(i)
key = random.choices([normal,special,alola,galar,ub,mythic,leggie],weights=[50,0,5,5,0,0,0],k = 100)
keys = []
for i in key:
  keys+=i
for i in range(2):
  keys+=mythic
keys+=leggie
keys+=ub
random.shuffle(keys)

def getPoke():#randomly returns a poke for random spawns
  pokenum = random.choice(keys)
  link=""+pokenum+".png"
  name = list(pok[pokenum])

  return [link,name]

orgi = list(db.keys())#contains name of all pokemon 
new = []#contains name of all pokemons in lower case
for i in orgi:
  new.append(i.lower())
def getdex(pkname,shiny =False):#returns dex of pokemon
    if pkname.lower() == "pokezoned1":return
    if pkname.lower() == 'primal rayquaza':
       return ['Primal Rayquaza','https://cdn.discordapp.com/attachments/853907239257899030/892654619010953216/primal_rayquaza_by_tomycase_d7zi7me-pre-removebg-preview.png','1000','Dragon Flying','180','193','110','189','111','142','11']      
    if pkname.lower() in new:
      index = new.index(pkname.lower())
      allst = list(db[orgi[index]])
      link = ''
      if allst[0] in donos:
        if shiny == True:
          link=""+allst[0]+".png"
        else:
          link = ""+allst[0]+".png"
      else:
        if shiny == True:
          link=""+allst[0]+".png"
        else:    
          link=""+allst[0]+".png"
      num = allst[0]
      typ = ''
      if allst[2]=='':
         typ = allst[1]
      else:
        typ = allst[1]+' | '+allst[2]
      totstat =allst[3]
      hp = allst[4]
      attack = allst[5]
      defen = allst[6]
      spatk =  allst[7]
      spdef =  allst[8]
      speed = allst[9]
      generation = allst[10]
      name = orgi[index]
      try:
        if int(num)<=898:
          flavor = pokebase.pokemon_species(pkname.lower())
          text = flavor.flavor_text_entries[1].flavor_text
          text = text.replace('\n',' ')
        else:
          text = ''
      except:
        text = ''  
      if shiny:
        name = "🌟 "+name
      return [name,link,num,typ,totstat,hp,attack,defen,spatk,spdef,speed,generation,text]
    else: return False  

def byId(id,by = False):#returns names of poke at a certain id
  if not id.isdigit():
    return
  names = ''
  if id in pok.keys():  
    names = list(pok.get(id))
    if by:
      return names[6]
    index =names[6]
    names.remove(index)
    try:
      names.remove(index)
    except:pass
    return names
  else:
    return False
def redeem(pkname,by = False):#this function returns name/link for redeem
  if pkname.lower() in new:
    index = new.index(pkname.lower())
    allst = list(db[orgi[index]])
    if by == False:
      if int(allst[0])>898:
        return False
    link=""+allst[0]+".png"
    if by == True:
      name = orgi[index]#gets the most/pokes general used name
    else:
      name = list(pok[allst[0]])#gets all name(alt name)
    return[link,name,allst[0]]
  else:
    return None#returns none is invalid pokemon name has been entered
    
def statmaker(iv,base,lvl):
  return  int(0.01*(2*base+iv)*lvl +5)
def hpmaker(iv,base,lvl):
  return int(0.01*(2*base+iv)*lvl +lvl+10)
#hp=None,atk=None,def=None,spa=None,spd=None,spe=None
async def addPoke(idd,pkname,lvl,shiny = False,all100 = False,*,hp=None,atk=None,defen=None,spa=None,spd=None,spe=None):#makes data for adding it to your database
  if pkname.lower() == 'pokezoned1':return
  data =  getdex(pkname,shiny)
  name = data[0]
  num = data[2]
  link = data[1]
  typ = data[3]
  nature = random.choice(list(natures.keys()))
  if all100:
    hpiv = 31
    atkiv = 31
    defiv = 31
    spatkiv = 31
    spdefiv = 31
    speediv = 31
  else:
    if hp is None: 
      hpiv = random.randint(1,31)
    else:
      hpiv = hp
    if atk is None:
      atkiv = random.randint(1,31)
    else:
      atkiv = atk
    if defen is None:
      defiv = random.randint(1,31)
    else:
      defiv = defen
    if spa is None:
      spatkiv = random.randint(1,31)
    else:
      spatkiv = spa
    if spd is None:
      spdefiv = random.randint(1,31)
    else:
      spdefiv = spd
    if spe is None:
      speediv = random.randint(1,31)
    else:
      speediv = spe
  hp =  hpmaker(hpiv,int(data[5]),lvl)
  atk = statmaker(atkiv,int(data[6]),lvl)
  defen = statmaker(defiv,int(data[7]),lvl)
  spatk = statmaker(spatkiv,int(data[8]),lvl)
  spdef = statmaker(spdefiv,int(data[9]),lvl)
  speed = statmaker(speediv,int(data[10]),lvl)
  totiv = (hpiv +atkiv + defiv + spatkiv + spdefiv + speediv)*100/(31*6)
  totiv = round(totiv,2)
  data = {'ids':-1,'name':name,'link':link,'typ':typ,'hp':hp,'atk':atk,'defen':defen,'spatk':spatk,'spdef':spdef,'speed':speed,'lvl':lvl,'hpiv':hpiv,'atkiv':atkiv,'defiv':defiv,'spatkiv':spatkiv,'spdefiv':spdefiv,'speediv':speediv,'totiv':totiv,'nature':nature}
  yield totiv
  await naModify(idd,data)
  if int(num)<=898:
    await adddex(idd,int(num)) 

async def naModify(idd,data):
  name = data['name']
  if '🌟 ' in name:
    name = name.replace('🌟 ','')
  dxdata = getdex(name)
  lvl  = data['lvl']
  data['hp'] =  hpmaker(data['hpiv'],int(dxdata[5]),lvl)
  data['atk'] = statmaker(data['atkiv'],int(dxdata[6]),lvl)
  data['defen'] = statmaker(data['defiv'],int(dxdata[7]),lvl)
  data['spatk'] = statmaker(data['spatkiv'],int(dxdata[8]),lvl)
  data['spdef'] = statmaker(data['spdefiv'],int(dxdata[9]),lvl)
  data['speed'] = statmaker(data['speediv'],int(dxdata[10]),lvl)
  nstat = natures[data['nature']]
  inc = nstat[0]
  dec = nstat[1]
  if not inc==None:
    print(inc)
    data[inc] = int(data[inc]*110/100)
  if not dec==None:
    print(dec)
    data[dec]  = int(data[dec]*90/100)
  await pokeadder(idd,data)

async def statModify(idd,dtpok,pk ='',newlvl=0):
  pk = pk.strip()
  shiny = False
  if pk == '':
    name = dtpok['name']
    if '🌟 ' in name:
      name = name.replace('🌟 ','')
      shiny = True
  else:
    if '🌟 ' in pk:
      pk = pk.replace('🌟 ','')
      shiny = True
      dtpok['name'] = '🌟 '+pk
      name = pk
      shiny = True
    else:
      dtpok['name'] = pk
      name = pk 
  data =  getdex(name,shiny)
  if newlvl ==0:
    lvl = dtpok['lvl']
  else:
    dtpok['lvl']= newlvl
    lvl = newlvl
  dtpok['hp'] =  hpmaker(dtpok['hpiv'],int(data[5]),lvl)
  dtpok['atk'] = statmaker(dtpok['atkiv'],int(data[6]),lvl)
  dtpok['defen'] = statmaker(dtpok['defiv'],int(data[7]),lvl)
  dtpok['spatk'] = statmaker(dtpok['spatkiv'],int(data[8]),lvl)
  dtpok['spdef'] = statmaker(dtpok['spdefiv'],int(data[9]),lvl)
  dtpok['speed'] = statmaker(dtpok['speediv'],int(data[10]),lvl)
  dtpok['link'] = data[1]
  await pokeadder(idd,dtpok)

def getmega(pk,xy=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if xy =='':
    pk = 'Mega '+pk
  else:
    xy = xy.upper()
    pk = 'Mega '+pk+' '+xy
  if pk in orgi:
    return True
  else:
    return False

def getprimal(pk,primal=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if primal =='':
    pk = 'Primal '+pk
  else:
    primal = primal.upper()
    pk = 'primal '+pk+' '+primal
  if pk in orgi:
    return True
  else:
    return False

def getcomplete(pk,complete=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if complete =='':
    pk = 'Complete '+pk
  else:
    complete = complete.upper()
    pk = 'complete '+pk+' '+complete
  if pk in orgi:
    return True
  else:
    return False

def getunbound(pk,unbound=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if unbound =='':
    pk = pk+" Unbound"
  else:
    unbound = unbound.upper()
    pk = 'Unbound '+pk+' '+unbound
  if pk in orgi:
    return True
  else:
    return False

def getgmax(pk,gmax=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if gmax =='':
    pk = 'Gigantamax '+pk
  else:
    gmax = gmax.upper()
    pk = 'Gigantamax '+pk+' '+gmax
  if pk in orgi:
    return True
  else:
    return False

def get10(pk,ten=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if ten =='':
    pk = pk+' 10%'
  else:
    ten = ten.upper()
    pk = '10% '+pk+' '+ten
  if pk in orgi:
    return True
  else:
    return False

def getultra(pk,ultra=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if ultra == '':
    pk = 'Ultra '+pk
  else:
    ultra = ultra.upper()
    pk = 'Ultra '+pk+' '+ultra
  if pk in orgi:
    return True
  else:
    return False

def getdawn(pk,dawn=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if dawn == '':
    pk = 'Dawn '+pk
  else:
    dawn = dawn.upper()
    pk = 'Dawn '+pk+' '+dawn
  if pk in orgi:
    return True
  else:
    return False

def getdusk(pk,dusk=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if dusk == '':
    pk = 'Dusk '+pk
  else:
    dusk = dusk.upper()
    pk = 'Dusk '+pk+' '+dusk
  if pk in orgi:
    return True
  else:
    return False

def getorigin(pk,origin=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if origin == '':
    pk = 'Origin '+pk
  else:
    origin = origin.upper()
    pk = 'Origin '+pk+' '+origin
  if pk in orgi:
    return True
  else:
    return False

def getsun(pk,sun=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if sun == '':
    pk = 'Radiant Sun '+pk
  else:
    sun = sun.upper()
    pk = 'Radiant Sun '+pk+' '+sun
  if pk in orgi:
    return True
  else:
    return False

def getmoon(pk,moon=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if moon == '':
    pk = 'Full Moon '+pk
  else:
    moon = moon.upper()
    pk = 'Full Moon '+pk+' '+moon
  if pk in orgi:
    return True
  else:
    return False

def getice(pk,ice=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if ice == '':
    pk = 'Ice Rider '+pk
  else:
    ice = ice.upper()
    pk = 'Ice Rider '+pk+' '+ice
  if pk in orgi:
    return True
  else:
    return False

def getshadow(pk,shadow=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if shadow == '':
    pk = 'Shadow Rider '+pk
  else:
    moon = shadow.upper()
    pk = 'Shadow Rider '+pk+' '+moon
  if pk in orgi:
    return True
  else:
    return False

def getsword(pk,sword=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if sword == '':
    pk = 'Crowned Sword '+pk
  else:
    sword = sword.upper()
    pk = 'Crowned Sword '+pk+' '+sword
  if pk in orgi:
    return True
  else:
    return False

def getshield(pk,shield=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if shield == '':
    pk = 'Crowned Shield '+pk
  else:
    shield = shield.upper()
    pk = 'Crowned Shield '+pk+' '+shield
  if pk in orgi:
    return True
  else:
    return False

def getemax(pk,emax=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if emax == '':
    pk = 'Eternamax '+pk
  else:
    emax = emax.upper()
    pk = 'Eternamax '+pk+' '+emax
  if pk in orgi:
    return True
  else:
    return False

def getattack(pk,attack=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if attack == '':
    pk = 'Attack '+pk
  else:
    attack = attack.upper()
    pk = 'Attack '+pk+' '+attack
  if pk in orgi:
    return True
  else:
    return False

def getdefence(pk,attack=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if attack == '':
    pk = 'Defence '+pk
  else:
    attack = attack.upper()
    pk = 'Defence '+pk+' '+attack
  if pk in orgi:
    return True
  else:
    return False

def getspeed(pk,attack=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if attack == '':
    pk = 'Speed '+pk
  else:
    attack = attack.upper()
    pk = 'Speed '+pk+' '+attack
  if pk in orgi:
    return True
  else:
    return False

def getash(pk,ash=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if ash == '':
    pk = 'Ash-'+pk
  else:
    ash= ash.upper()
    pk = "Ash-"+pk+' '+ash
  if pk in orgi:
    return True
  else:
    return False 

def getblack(pk,ash=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if ash == '':
    pk = 'Black '+pk
  else:
    ash= ash.upper()
    pk = "Black "+pk+' '+ash
  if pk in orgi:
    return True
  else:
    return False

def getwhite(pk,ash=''):
  if "🌟 " in pk:
    pk = pk[2:len(pk)+1]
  if ash == '':
    pk = 'White '+pk
  else:
    ash= ash.upper()
    pk = "White "+pk+' '+ash
  if pk in orgi:
    return True
  else:
    return False

