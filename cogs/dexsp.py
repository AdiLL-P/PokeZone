from disnake.ext import commands
from disnake.ext import tasks
import random
import disnake
from User import getredeem,setredeem,checkExist,setbal,lates,infoc,infonum,getsh,setsh,setlatest,getlatest,getnosp,setnosp,removenosp,pkremove,gapfiller,setrel,getcat,getinviter,setshiny
from poke import getPoke,getdex,byId,redeem,addPoke
import asyncio
class spaw:
  def __init__(self,lol):
    self.count = lol
    self.poke = None
    self.temp = None
  def what(self,c=1):
    if self.count >= 15:
      self.count = 1
      return True
    else:#pip install git+https://github.com/EQUENOS/disnake@master
      self.count+=c
      return False
  def getts(self):
    a = getPoke()
    self.temp = a[1]
    return a[0]
  def setPk(self):
    self.poke = self.temp
    self.temp = None
gID =   [852097339442331649]
class spd(commands.Cog):
  def __init__(self,bot):
   self.bot = bot
   self.spawn = {}
   self.OTO = random.choices([1, 2], k=25)
   self.tf = random.choices([True, False], k=25)
   self.disabled = []
   self.gID = [852097339442331649]
   self.t = 1
  @commands.Cog.listener()
  async def on_ready(self):
    self.disabled = await getnosp()
  @commands.Cog.listener()
  async def on_message(self,message):
    if message.content.startswith('<@832266727022395402>') or message.content.startswith('<@!832266727022395402>'):
      embed = disnake.Embed(title='POKEZONE',description=f'_`Hello! {message.author.name} I am Pokezone, a discord bot based on pokemon where you can catch,trade,evolve,duel and can do many more things with your pokemon.For our event info .Please type p?event`_',color=0xFFDF00)
      embed.add_field(name='__MY PREFIX__',value='`P?`',inline=False)
      embed.add_field(name='__MY SERVER__',value='[CLICK HERE]()')
      embed.add_field(name='__INVITE ME__',value='[CLICK HERE]()')
      await message.channel.send(embed=embed)
    if message.guild is None:
      return
    if message.channel.id in self.disabled:
      return
    if message.author == self.bot.user:
      return
    if message.author.bot:
      return
    if message.channel.id in [852565395579994112]:
      if not self.timed.is_running():
        self.timed.start()
    chandID = message.channel.id
    if chandID == 888722361027801098:
      c = 1.5
    else:
      c = 1
    if chandID not in self.spawn:
      self.spawn[chandID] = spaw(2)
    elif self.spawn[chandID].what(c):
      ul = self.spawn[chandID].getts()
      embed = disnake.Embed(
        title = "A wild pokémon has Just Spawned!",
        description = "Guess the pokémon аnd type `P?catch <pokémon>` to cаtch it!",
        colour = 0xFFDF00
      )
      embed.set_image(url=ul)
      a = self.bot.get_command("hint")
      try:
        a.reset_cooldown(self.spawn[chandID].hint)
      except:pass
      await message.channel.send(embed=embed)
      await asyncio.sleep(0.3)
      self.spawn[chandID].setPk()
  @tasks.loop(seconds =500)
  async def timed(self):
    for i in (852565395579994112,879649426824646657,880323047482064926):
      if i not in self.spawn:
        self.spawn[i] = spaw(2)
      ul = self.spawn[i].getts()
      embed = disnake.Embed(
        title = "A wild pokémon has Just Spawned!",
        description = "Guess the pokémon аnd type `P?catch <pokémon>` to cаtch it!",
        colour = 0x2F3136
      )
      embed.set_image(url=ul)
      a = self.bot.get_command("hint")
      try:
        a.reset_cooldown(self.spawn[i].hint)
      except:pass
      chnl = self.bot.get_channel(i)
      await chnl.send(embed = embed)
      await asyncio.sleep(0.3)
      self.spawn[i].setPk()
    self.t+=1  
    if self.t>=10:
      self.timed.stop()
      self.t =1
    

  @commands.command()
  async def disable(self,ctx,arg):
    if arg == 'spawn':
      if ctx.channel.permissions_for(ctx.author).manage_channels:
        await setnosp(ctx.channel.id)
        await ctx.send('Pokemon spawns has been disabled in this channel')
        self.disabled = await getnosp()
      else:
        await ctx.send("You dont seem to have permission to manage channels")

  @commands.command()
  async def enable(self,ctx,arg):
    if arg == 'spawn':
      if ctx.channel.permissions_for(ctx.author).manage_channels:
        await removenosp(ctx.channel.id)
        await ctx.send('Pokemon spawns has been enabled in this channel')
        self.disabled = await getnosp()
      else:
        await ctx.send("You dont seem to have permission to manage channels")
      
  
  @commands.command(aliases=["DeX","Dex","DEX","pokedex","Pokedex"])
  async def dex(self,ctx,*arg):
      if arg ==():
        cog = self.bot.get_cog('Dex')
        await cog.ok(ctx.author,ctx.channel)
        return
      arg = list(arg)
      if 'shiny' in arg:
        arg.remove('shiny')
        arg = ' '.join(arg)
        all =getdex(arg,shiny = True)
      else:
        arg = ' '.join(arg)
        all = getdex(arg)
      if all == False:
        await ctx.send("This Pokemon doesn't seem to exist")
        return
    #name,link,num,typ,totstat,hp,attack,defen,spatk,spdef,speed,generation
      embed = disnake.Embed(
      title = '#'+all[2]+'-'+all[0],
      description =all[12],
      colour = disnake.Colour.random(seed=None)
      )
      names = ''
      if byId(all[2]) == False:
        names = 'No alternative names'
      else: names = ' | '.join(byId(all[2]))
      base = '**HP**:'+all[5]+'\n'+'**Attack**:'+all[6]+'\n'+'**Def**:'+all[7]+'\n'+'**Sp.Atk**:'+all[8]+'\n'+'**Sp.Def**:'+all[9]+'\n'+'**Speed**:'+all[10]+'\n'+'**Total Stats**:'+all[4]
      embed.add_field(name = "Alternative Names",value = names)
      embed.add_field(name = "Base Stats" ,value = base )
      embed.add_field(name = "Generation :",value= all[11],inline=True )
      embed.add_field(name = "Type:",value= all[3])
      embed.set_author(name ='Professor Cerice',url   ="https://discord.gg/SUMUNTCehH",icon_url = 'https://cdn.discordapp.com/attachments/512275320645353502/867373806539898890/Professor_Cerise_JN.png')
      embed.set_image(url = all[1])
      await ctx.send(embed=embed)
  

  @commands.max_concurrency(1,per = commands.BucketType.channel,wait = True)
  @commands.command(aliases=['c', 'C', 'Catch', 'cAtch', 'caTch', 'catCh', 'catcH', 'CATCH'])
  async def catch(self,ctx,*arg):
    if ctx.channel.id in self.disabled:
      await ctx.send("Pokemon catching has been disabled here !")
      return
    chanId = ctx.channel.id
    current = self.spawn[chanId].poke
    ids = ctx.author.id
    arg = ' '.join(arg)
    if not await checkExist(ids):
      await ctx.send(ctx.author.mention+" You still need to start")
      return
    lvl = random.randint(1,40)
    if lvl >30:
      lvl = random.randint(10,40)
    if type(current)== str:
      if arg == 'coins' or arg == 'coin' or arg == 'Coin' or arg == 'Coins':
        await ctx.send('Congratulation !! '+ctx.author.mention+' You have won '+str(current)+' coins')
        self.bot.loop.create_task(setbal(ctx.author.id,int(current)))
        self.spawn[chanId].poke = None
      return
    llis = []
    try:
      for i in current:
        llis.append(i.lower())
    except:
      await ctx.send("There is no wild Pokemon here ! ")
      return
    if ctx.author.id == 751859605797208185:
      arg = llis[6]
    if arg.lower() in llis:
      index = llis.index(arg.lower())
      self.spawn[chanId].poke = None
      temp = current[6]
      if ctx.channel.id == 888722361027801098:
          name = current[index]
          ifshiny  = random.choices([True,False],weights= [1,10],k=100)
          shiny = random.choice(ifshiny)
          if shiny:
            async for iv in addPoke(ids,temp,lvl,shiny=shiny):
              await ctx.send(f"<:1M_Green_tick:873247568870662184> **Congratulations** !! {ctx.author.mention} **You have caught a level {str(lvl)} {name}**, `IV: {str(iv)}%`""\n""\n""**This Colour Doesn't Seems Regular 🌟**")
              await setshiny(ctx.author.id)
          else:
            async for iv in addPoke(ids,temp,lvl):
              await ctx.send(f"<:1M_Green_tick:873247568870662184> **Congratulations !! {ctx.author.mention} You have caught a level {str(lvl)} {name}**, `IV: {str(iv)}%`")
          await asyncio.sleep(1)
          catch = await getcat(ctx.author.id)
          if catch==10 or catch ==100 or catch ==1000:
            if catch ==10 or catch ==1000:
              await setbal(ctx.author.id,5000)
            inv = await getinviter(ctx.author.id)
            if inv!=None:
              try:
                dm = self.bot.get_user(int(inv))
                await dm.send("You have recieved One redeem as per invite event !\nHappy Playing\nRegards\nPokezone Team")
              except:
                await ctx.send(f"<@{inv}> <:Pz_Green_tick:873247568870662184>  You have succesfully recieved One redeem as per invite event")
              await setredeem(inv,1)
          return
      shus = await getsh(ctx.author.id)
      if shus == None or shus[0] != temp:
        name = current[index]
        async for iv in addPoke(ids,temp,lvl):
          #await ctx.send("Congratulations !! **"+ctx.author.mention+"** You have caught a level "+str(lvl)+' '+name+", IV: "+str(iv)+"% ")
          await ctx.send(f"<:1M_Green_tick:873247568870662184> **Congratulations !! {ctx.author.mention} You have caught a level {str(lvl)} {name}**, `IV: {str(iv)}%`")
        await asyncio.sleep(1)
        catch = await getcat(ctx.author.id)
        if catch == 10 or catch ==100 or catch ==1000:
          if catch == 10 or catch == 1000:
            await setbal(ctx.author.id,5000)
          inv = await getinviter(ctx.author.id)
          if inv!= None:
            try:
              dm = self.bot.get_user(int(inv))
              await dm.send("You have recieved One redeem as per invite event!\nHappy Playing\nRegards,\nPokezone Team")
            except:
              await ctx.send(f"<@{inv}> <:Pz_Green_tick:873247568870662184>  You have succesfully recieved One redeem as per invite event")
            await setredeem(inv,1)
      else:
        vhcus = shus[2]
        l2 = random.randint(151,300)
        l1 = random.randint(1,150)
        w2 = random.randint(l1,l2)
        chance = random.choices([True,False],weights=[vhcus,w2],k=100)
        chance = random.choice(chance)
        name = current[index]
        if chance:
          async for iv in addPoke(ids,temp,lvl,shiny=True):
            await ctx.send(f"<:1M_Green_tick:873247568870662184> **Congratulations** !! ""{ctx.author.mention} **You have caught a level {str(lvl)} {name}**, `IV: {str(iv)}%`""\n""\n""**This Colour Doesn't Seems Regular 🌟**")
          await setsh(ctx.author.id,vhc = 0)
          await setshiny(ctx.author.id)
          await asyncio.sleep(1)
          catch = await getcat(ctx.author.id)
          if catch==10 or catch ==100 or catch ==1000:
            if catch ==10 or catch ==1000:
              await setbal(ctx.author.id,5000)
            inv = await getinviter(ctx.author.id)
            if inv!=None:
              try:
                dm = self.bot.get_user(int(inv))
                await dm.send("You have recieved One redeem as per invite event !\nHappy Playing\nRegards\nPokezone Team")
              except:
                await ctx.send(f"<@{inv}> <:Pz_Green_tick:873247568870662184>  You have succesfully recieved One redeem as per invite event")
              await setredeem(inv,1)
        else:
          async for iv in addPoke(ids,temp,lvl):
            await ctx.send(f"<:1M_Green_tick:873247568870662184> **Congratulations !! {ctx.author.mention} You have caught a level {str(lvl)} {name}**, `IV: {str(iv)}%`")
          await setsh(ctx.author.id,vhc = 1)
          await asyncio.sleep(1)
          catch = await getcat(ctx.author.id)
          if catch==10 or catch ==100 or catch ==1000:
            inv = await getinviter(ctx.author.id)
            if catch ==10 or catch ==1000:
              await setbal(ctx.author.id,5000)
            if inv!=None:
              try:
                dm = self.bot.get_user(int(inv))
                await dm.send("You have recieved One redeem as per invite event ! \nHappy Playing\nRegards,\nPokezone Team")
              except:
                await ctx.send(f"<@{inv}> <:Pz_Green_tick:873247568870662184>  You have succesfully recieved One redeem as per invite event")
              await setredeem(inv,1)
      await setbal(ids,30)
    else: await ctx.send(f"<:redx:873247207124508742> {ctx.author.mention} This is Wrong Name of this Pokemon, Try `P?hint` Get a hint for the wild pokémon.")
  
  @commands.command()
  @commands.cooldown(rate = 1,per = 30.0 ,type = commands.BucketType.channel)
  async def hint(self,ctx,arg = None ):
    if ctx.channel.id in self.disabled:
      return
    self.spawn[ctx.channel.id].hint = ctx
    current = self.spawn[ctx.channel.id].poke
    if current == None:
      await ctx.send("There is no wild Pokemon ! Kinda sus")
      return
    lc = [512275263158222868,751859605797208185,769073090604171345]
    if ctx.author.id in lc and arg == 'dev':
      await ctx.send(current)
    else:
      if type(current) == str:
        return
      pknam = current[6]
      ch = '-'
      hint = ''
      j = 0
      lc = 0
      cc = 0
      while j < len(pknam):
        if len(pknam) - j == 2:
          if lc > cc: hint += ch
          else: hint += pknam[j]
          j += 1
        elif random.choice(self.tf):
          hint += pknam[j]
          lc += 1
          j += 1
        else:
          l = random.choice(self.OTO)
          hint += ch * l
          cc += l
          j += l
      await ctx.send("The wild Pokemon is "+hint+" !")
  @hint.error
  async def hmm(self,ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
      await ctx.send("Sush ! move quietly , The command is on cooldown ")

  @commands.command(aliases = ['r'])
  async def redeem(self,ctx,*arg):
   if ctx.channel.id in self.disabled:
     await ctx.send("Pokemon spawns have been disabled in this channel")
     return
   if await getredeem(ctx.author.id)>0:
    arg = list(arg)
    if "spawn" in arg or 's' in arg:
      if 'spawn' in arg:
        arg.remove('spawn')
      elif 's' in arg:
        arg.remove('s')
      if 'coin' in arg or 'coins' in arg or 'Coin' in arg or 'Coins' in arg:
        embed = disnake.Embed(title = "You chose to decide you luck... lets see",color=0x2F3136)
        embed.set_image(url = 'https://cdn.disnakeapp.com/attachments/835885318234177636/854767052714934282/images__2_-removebg-preview.png')
        embed.set_footer(text="Type P?catch coin to get coins. Amount Will Depend On Your Luck!!")
        if ctx.channel.id not in self.spawn:
          self.spawn[ctx.channel.id] = spaw(1)
        self.spawn[ctx.channel.id].poke = str(random.randint(random.randint(10000,15000),random.randint(15000,100000)))
        await setredeem(ctx.author.id,-1)
        a = self.bot.get_command("hint")
        a.reset_cooldown(ctx)
        await ctx.send(embed = embed)
        return
      arg = ' '.join(arg)
      all = redeem(arg)
      if all ==None:
        await ctx.send("That pokemon doesn't seem exist")
        return
      if all == False:
        await ctx.send("That pokemon is not redeemable")
        return
      if ctx.channel.id not in self.spawn:
        self.spawn[ctx.channel.id] = spaw(1)
      embed = disnake.Embed(title = "A wild pokémon has Just Spawned!",description= 'Guess the pokémon аnd type `P?catch <pokémon>` to cаtch it!',color=0x2F3136)
      embed.set_image(url = all[0])
      await ctx.send(embed = embed)
      self.spawn[ctx.channel.id].poke = all[1]
      a = self.bot.get_command("hint")
      a.reset_cooldown(ctx)
      await setredeem(ctx.author.id,-1)
    else:
      lvl = random.randint(1,40)
      if lvl>30:
        lvl = random.randint(10,30)
      arg = ' '.join(arg)
      all = redeem(arg)
      if all ==None:
        await ctx.send("That pokemon doesn't seem to exist")
        return
      if all ==False:
        await ctx.send('That pokemon is not redeemable')
        return
      llst = []
      for i in all[1]:
        llst.append(i.lower())
      index = llst.index(arg.lower())
      async for i in addPoke(ctx.author.id,all[1][6],lvl):
        iv = i
      await ctx.send("<:Pz_Green_tick:873247568870662184> **Congratulations "+ctx.author.mention+" You recieved a Level "+str(lvl)+' '+all[1][index]+' IV:'+str(iv)+'**')
      await setredeem(ctx.author.id,-1)
   else:
       await ctx.send(ctx.author.mention+" You dont have enough redeems")
  

    
  @commands.group(aliases=["i","I"],invoke_without_command = True)
  async def info(self,ctx,arg = None):
    if ctx.channel.id in self.disabled:
      return
    auth = ctx.author
    channel = ctx.channel
    if not await checkExist(auth.id):
      await ctx.sed("You dont seem to be a member of BOT . Please try P?start")
      return
    async def sender(args,edit = False):
      if args == 'c':
        data = await infoc(ctx.author.id)
        if data == False:
          await ctx.send("There is no selected Pokemon")
          return
      elif args.isdigit():
        data = await infonum(ctx.author.id,args)
        if data == False:
          await ctx.send("You dont have a pokemon at that number")
          return
      pkId = data['ids']
      data2 = await lates(ctx.author.id)
      embed = disnake.Embed(title = "Level "+str(data['lvl'])+" "+ data['name'],color=0x9acd32)#str(data['ids'])
      stats ='**HP**:'+str(data['hp'])+'    **IV:**'+str(data['hpiv'])+'/31\n'+'**Attack**:'+str(data['atk'])+'    **IV**:'+str(data['atkiv'])+'/31\n'+'**Defense**:'+str(data['defen'])+'    **IV**:'+str(data['defiv'])+'/31\n'+'**Sp.Atk**:'+str(data['spatk'])+'    **IV**:'+str(data['spatkiv'])+'/31\n'+'**Sp.Def**:'+str(data['spdef'])+'    **IV**:'+str(data['spdefiv'])+'/31\n'+'**Speed**:'+str(data['speed'])+'    **IV**:'+str(data['speediv'])+'/31''\n**Total IV**: '+str(data['totiv'])+"%"
      embed.add_field(name = "__INFORMATION__",value = "**Nature**: "+data['nature']+'\n'+'**Types**: '+data['typ'])
      embed.add_field(name = "__STATS__" ,value = stats,inline = False )
      embed.set_image(url = data['link'])
      embed.set_footer(text="Displaying Pokemon: "+str(data['ids'])+"/"+str(data2['ids'])+"\nType (n / b) or  (next / back) ")
      embed.set_thumbnail(url = ctx.author.avatar.url)
      if not edit:
        msg = await ctx.send(embed = embed)
        await setlatest(auth.id,msg.id)
        return [msg,pkId]
      else:
        editable = channel.get_partial_message(await getlatest(auth.id))
        await editable.edit(embed =embed)
        await setlatest(auth.id,editable.id)
        return [editable,pkId]

    if arg == None:
      alls = await sender('c')
      msg = alls[0]
      pkId = alls[1]
    elif arg.isdigit():
      alls = await sender(arg)
      msg = alls[0]
      pkId = alls[1]
    else:
      await ctx.send("Number of a pokemon should be a integer")
      return 
    while True:
      def check(m):
        return m.channel == channel and m.author == auth and (m.content.lower() == 'next' or m.content.lower()=='back' or m.content.lower() == 'n' or m.content.lower() == 'b')
      try:    
        msgs = await self.bot.wait_for('message',check = check,timeout = 60.0)
      except asyncio.TimeoutError:
        return
      cont = msgs.content
      idoflatest = await getlatest(ctx.author.id)
      if idoflatest != msg.id:
        return
      if (cont.lower() == 'next' or cont.lower() =='n'):
        await msgs.delete()
        naya = await lates(auth.id)
        if pkId<naya['ids']:
          alls = await sender(str(pkId+1),edit = True)
          msg = alls[0]
          pkId = alls[1]
        else:
          await ctx.send("No further pokemons were found")
      elif (cont.lower()== 'back' or cont.lower() == 'b'):
        await msgs.delete()
        if pkId>1:
          alls = await sender(str(pkId-1),edit = True)
          msg = alls[0]
          pkId = alls[1]
        else:
          await ctx.send("No further pokemons were found")

  @info.command(aliases=["l","L"])
  async def latest(self,ctx):
    if ctx.channel.id in self.disabled:
      return
    auth = ctx.author
    channel = ctx.channel
    if not await checkExist(auth.id):
      await ctx.send("You dont seem to be a member of BOT . Please try P?start")
      return
    async def sender(args = None,edit=False,allpkc = 0):
      if args == None:
        data = await lates(ctx.author.id)
      elif args.isdigit():
        data = await infonum(ctx.author.id,args)
      pkId = data['ids']
      embed = disnake.Embed(title = "Level "+str(data['lvl']) +" "+data['name'],color=0x9acd32)
      stats = '**HP**:'+str(data['hp'])+'    **IV**:'+str(data['hpiv'])+'/31\n'+'**Attack**:'+str(data['atk'])+'    **IV**:'+str(data['atkiv'])+'/31\n'+'**Defense**:'+str(data['defen'])+'    **IV**:'+str(data['defiv'])+'/31\n'+'**Sp.Atk**:'+str(data['spatk'])+'    **IV**:'+str(data['spatkiv'])+'/31\n'+'**Sp.Def**:'+str(data['spdef'])+'    **IV**:'+str(data['spdefiv'])+'/31\n'+'**Speed**:'+str(data['speed'])+'    **IV**:'+str(data['speediv'])+'/31''\n**Total IV**: '+str(data['totiv'])+"%"
      embed.add_field(name = "__INFORMATION__",value = "**Nature:** "+data['nature']+"\n**Types**: "+data['typ'])
      embed.add_field(name = "__STATS__" ,value = stats,inline = False )
      embed.set_image(url = data['link'])
      embed.set_thumbnail(url = ctx.author.avatar.url)
      if not edit:
        embed.set_footer(text="Displaying Pokemon: "+str(data['ids'])+"/"+str(data['ids'])+"\nType (n / b) or  (next / back) ")
        msg = await ctx.send(embed=embed)
        await setlatest(auth.id,msg.id)
        return [msg,pkId]
      else:
        embed.set_footer(text="Displaying Pokemon: "+str(data['ids'])+"/"+str(allpkc)+"\nType (n / b) or  (next / back) ")
        editable  = channel.get_partial_message(await getlatest(auth.id))
        await editable.edit(embed = embed)
        await setlatest(auth.id,editable.id)
        return [editable,pkId]
    alls = await sender()
    msg = alls[0]
    pkId = alls[1]
    while True:
      def check(m):
        return m.channel == channel and m.author == auth and (m.content.lower() == 'next' or m.content.lower()=='back' or m.content.lower() == 'n' or m.content.lower() == 'b')
      try:
        msgs = await self.bot.wait_for('message',check = check,timeout = 60.0)
      except asyncio.TimeoutError:
        return
      idoflatest = await getlatest(ctx.author.id)
      cont = msgs.content
      if idoflatest != msg.id:
        return
      if (cont.lower() == 'next' or cont.lower() =='n'):
        await msgs.delete()
        naya = await lates(auth.id)
        if pkId< naya['ids']:
          alls = await sender(str(pkId+1),edit = True,allpkc = naya['ids'])
          msg = alls[0]
          pkId = alls[1]
        else:
          await ctx.send("No further pokemons were found")
      elif (cont.lower()== 'back' or cont.lower() == 'b'):
        await msgs.delete()
        naya = await lates(auth.id)
        if pkId>1:
          alls = await sender(str(pkId-1),edit = True,allpkc = naya['ids'])
          msg = alls[0]
          pkId = alls[1]
        else:
          await ctx.send("No further pokemons were found")

  @commands.command()
  async def redirect(self,ctx,arg:disnake.TextChannel):
    if ctx.channel.permissions_for(ctx.author).manage_channels:
      pass
  @commands.command(aliases = ['release'])
  async def free(self,ctx,arg):
    idd = ctx.author.id
    if not await checkExist(idd):
      await ctx.send("You are not a member of bot, Please try p?start")
      return
    pk = await infonum(idd,arg)
    if pk == False:
      await ctx.send("You dont have any pokemon at that number")
      return
    name = pk['name']
    mess = await ctx.send(f'{ctx.author.mention} Are you sure you want to release {name} for 50 credits !')
    await mess.add_reaction('<:Pz_Green_tick:873247568870662184>')
    await mess.add_reaction('<:redx:873247207124508742>')
    def check(reaction,user):
      emoji = str(reaction.emoji)
      return user.id == idd and (emoji == '<:Pz_Green_tick:873247568870662184>' or emoji == '<:Pz_redx:873247207124508742>')
    try:
      reaction,user = await self.bot.wait_for('reaction_add',timeout = 60.0 ,check = check)
      if str(reaction.emoji) == '<:Pz_Green_tick:873247568870662184>':
        await ctx.send('You released this pokemon')
        await setbal(idd,50)
        await pkremove(idd,arg)
        await gapfiller(idd)
        await setrel(idd)
      elif str(reaction.emoji) == '<:Pz_redx:873247207124508742>':
        await ctx.send("The release of pokemon was cancelled")
    except asyncio.TimeoutError:
      await ctx.send("Timeout for Interaction")    
def setup(bot):
  bot.add_cog(spd(bot))