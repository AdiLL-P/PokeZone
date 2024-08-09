from disnake.ext import commands
import random
import disnake
import asyncio
from poke import redeem,addPoke,byId,normal
from User import setbal,setredeem,checkExist,resettt,resetdb,getshard,setshard,getbal,getredeem,getlatest,setlatest,allPokes,infonum,pkremove,gapfiller,setcrates
class Dev(commands.Cog):
  def __init__(self,bot) -> None:
        self.bot= bot
        self.owners = []
        
  @commands.slash_command(name = 'givepoke',description = 'Dev only Command',guild_ids = [852097339442331649],options = [
    disnake.Option(name = 'user_name',description = 'hpiv',type = disnake.OptionType.user,required = True),
    disnake.Option(name = 'pokemon_name',description = 'hpiv',type = disnake.OptionType.string,required = True),
    disnake.Option(name = 'hpiv',description = 'hpiv',type = disnake.OptionType.integer),
    disnake.Option(name = 'attack_iv',description = 'hpiv',type = disnake.OptionType.integer),
    disnake.Option(name = 'defense_iv',description = 'hpiv',type = disnake.OptionType.integer),
    disnake.Option(name = 'spatk_iv',description = 'hpiv',type = disnake.OptionType.integer),
    disnake.Option(name = 'spdef_iv',description = 'hpiv',type = disnake.OptionType.integer),
    disnake.Option(name = 'speed_iv',description = 'hpiv',type = disnake.OptionType.integer)
  ])
  async def givepoke(self,inter,user_name,pokemon_name,hpiv=None,attack_iv=None,defense_iv=None,spatk_iv=None,spdef_iv=None,speed_iv=None,lvl =35):
      if inter.author.id not in self.owners:
        await inter.response.send_message("**Oops ! <a:developer_shiny:876786616251859054>  it's a Developer Command**",ephemeral = True)
        return
      poke = pokemon_name.strip()
      if 'shiny' in poke:
        poke = poke.replace('shiny','')
        shiny = True
      elif 'Shiny' in poke:
        poke = poke.replace('Shiny','')
        shiny = True
      else:
        shiny = False
      poke = poke.strip()
      idd = user_name.id
      if not await checkExist(idd):
        await inter.response.send_message("Mentioned Person is not user of bot",ephemeral = True)
        return 
      if poke.lower()== 'addy' or poke.lower()=='alxen':
        all = ['a','a']
        all[1] = poke.lower().title()
      else:
        all = redeem(poke,by = True)
      async for i in addPoke(idd,poke,lvl,shiny,hp=hpiv,atk=attack_iv,defen=defense_iv,spa=spatk_iv,spd=spdef_iv,spe=speed_iv):
        shv = ''
        if shiny: shv = 'Shiny'
        try:
          lol = "<:Pz_Green_tick:873247568870662184> **Congratulations**  "+user_name.name+"** You recieved a Level "+str(lvl)+' '+shv+' '+all[1]+'**'
          await inter.response.send_message(lol)
        except:
          lol = "`<:Pz_Green_tick:873247568870662184> Congratulations "+user_name.name+" You recieved a Level "+str(lvl)+' '+shv+' '+all[1]+'`'
          await inter.response.send_message(lol) 

  @commands.command()
  async def give_poke(self,ctx,name,*poke):
      lc = [512275263158222868,751859605797208185]
      if ctx.author.id not in lc:
        return
      poke = list(poke)
      if 'shiny' in poke:
        poke.remove('shiny')
        shiny = True
      else:
        shiny = False
      poke = ' '.join(poke)
      idd = ''.join([i for i in name if i.isdigit()])
      if not await checkExist(idd):
        await ctx.send("Mentioned Person is not user of bot")
        return
      all = redeem(poke,by = True)
      lvl = 100
      async for i in addPoke(idd,poke,lvl,shiny,all100=True):
        shv = ''
        if shiny: shv = 'Shiny'
        await ctx.send("`Congratulations "+ctx.guild.get_member(int(idd)).name+" You recieved a Level "+str(lvl)+' '+shv+' '+all[1]+'`')
  
  @commands.command()
  async def resetall(self,ctx,arg):
    lc = [751859605797208185,512275263158222868]
    if ctx.author.id not in lc:
      await ctx.send("**Oops! <a:developer_shiny:876786616251859054>  Only Devs can reset your profile**")
      return
    if resettt(arg):
      await ctx.send("```GG ```")
    else:
      await ctx.send("`ERROR 404`")

  @commands.command()
  async def reset(self,ctx,arg):
    if ctx.author.id not in self.owners:
      await ctx.send("Sorry")
      return
    idd = ''.join([i for i in arg if i.isdigit()])
    if await resetdb(idd):
      await ctx.send("```ID: "+idd+" <:Pz_Green_tick:873247568870662184> has been sucessfully Reseted```") 
    else:
      await ctx.send("Person is not a user of bot")

  @commands.command()
  async def invites(self,ctx):
    lc = [751859605797208185,512275263158222868]
    if ctx.author.id not in lc:
      await ctx.send("Sorry")
      return 
    embed = disnake.Embed(title = "Click here",url = "https://discord.com/api/oauth2/authorize?client_id=832266727022395402&permissions=1611000897&scope=bot" , colour = disnake.colour.red())
    embed.set_footer(text=f'Requested By {ctx.author.name}')
    await ctx.send(embed=embed)

  
  @commands.command()
  async def givedev(self,ctx,member:disnake.Member):
    lc = []
    if ctx.author.id not in lc:
      return
    if not await checkExist(member.id):
      return
    else:
      await ctx.send("You have recieved dev perms !")
      self.owners.append(member.id)
  @commands.command()
  async def removedev(self,ctx,member:disnake.Member):
    lc = []
    if ctx.author.id not in lc:
      return
    if not await checkExist(member.id):
      return
    else:
      await ctx.send("Removed !")
      self.owners.remove(member.id)
  
  @commands.command()
  async def giveaway(self,ctx,arg='coins',users =0,data = 0):
    if ctx.author.id not in self.owners:
      await ctx.send("Only devs can use this command")
      return
    lchan = ctx.channel
    if users ==0:
      users = random.randint(1,6)
    else:
      users = int(users)
    def check(me):
      return me.channel == lchan
    if data ==0:
      call = 'random'
    else:
      data = int(data)
      call = str(data)
    await ctx.send("Next "+str(users)+" people will get "+call+" "+arg)
    got = []
    count =0
    while count<int(users):
      try:
        msg = await self.bot.wait_for('message',check =check,timeout = 1000)
      except asyncio.TimeoutError:
          await ctx.send("Oops! Timeout for giveaway")
          break
      if arg.lower() == 'coins':
          if data == 0:
            data = random.randint(random.randint(10000,15000),random.randint(40000,100000))#amount of bal
      elif arg.lower() == 'redeems':
          if data == 0:
            data = random.randint(1,10)#amount of redeem 
      idd = msg.author.id
      if idd in got:
          continue
      if arg.lower() == 'coins':
        if await setbal(idd,data):
          await ctx.send(msg.author.mention+"You have won "+str(data))
          got.append(idd)
          count+=1
      if arg.lower() == 'redeem':
        if await setredeem(idd,data):
          await ctx.send(msg.author.mention+"You have won "+str(data)+" redeems.")
          got.append(idd)
          count+=1
  @commands.group(invoke_without_command=True,aliases = ['devsus'])
  async def dev(self,ctx):
    await ctx.send("DEV Exclusive commands!")

  @dev.command()
  async def bal(self,ctx,member:disnake.Member,*args):
    if ctx.author.id in self.owners:
      bal = await getbal(member.id)
      await ctx.send(f"{member.name}'s balance: {bal}")
    else:
      await ctx.send('You are not developer to sus a user')

  @dev.command()
  async def redeem(self,ctx,member:disnake.Member,*args):
    if ctx.author.id in self.owners:
      bal = await getredeem(member.id)
      await ctx.send(f"{member.name}'s redeem: {bal}")
    else:
      await ctx.send('You are not developer to sus a user')

  @dev.command()
  async def shard(self,ctx,member:disnake.Member,*args):
    if ctx.author.id in self.owners:
      bal = await getshard(member.id)
      await ctx.send(f"{member.name}'s shards: {bal}")
    else:
      await ctx.send('You are not developer to sus a user')

  @dev.command()
  async def pk(self,ctx,member:disnake.Member,*args):
    if ctx.author.id in self.owners:
      if not await checkExist(ctx.author.id):
          return
      current = 0
      broke = True
      channel = ctx.channel
      auth = ctx.author
      a =await allPokes(member.id)
      if a ==False:
          await ctx.send("NO pokemon")
          return
      des = ''
      for i in a :
          des+= '`'+i['name']+ ' '+'`ID: '+str(i['ids'])+' • Level-'+str(i['lvl'])+' • IV: '+str(i['totiv'])+'%'
          des+='\n'
          current+=1
          if current ==20:
              break
      embed = disnake.Embed(title = member.name+" Pokemons",description = des,color=disnake.Colour.blue())
      embed.set_footer(text="Type (next) To view next page or Type (back) To view Previous Page")
      msg = await ctx.send(embed = embed)
      await setlatest(auth.id,msg.id)
      while await getlatest(auth.id) == msg.id:
            def check(m):
                return m.channel == channel and m.author == auth and (m.content.lower() == 'next' or m.content.lower()=='back' or m.content.lower() == 'n' or m.content.lower() == 'b')
            try:    
                msgs = await self.bot.wait_for('message',check = check,timeout = 60.0)
            except asyncio.TimeoutError:
                return
            mess = msgs.content
            if await getlatest(auth.id) == msg.id:
                des = ''
                if mess.lower() =='next' or mess.lower() == 'n':
                    await msgs.delete()
                    count = 0
                    hehe = 0
                    for i in a :
                        if count>=current:
                            hehe+=1
                            des+= '`'+i['name']+' '+'` ID: '+str(i['ids'])+' •  Level-'+str(i['lvl'])+' • IV: '+str(i['totiv'])+'%'
                            des+='\n'
                            current+=1
                        if hehe ==20:
                            broke = False
                            break
                        else : broke = True
                        count+=1
                if mess.lower() =='back' or mess.lower() == 'b':
                    await msgs.delete()
                    count = 0
                    data = None
                    if broke:
                      data = current-40+20-(hehe)-1
                      broke = not broke
                    else:
                      data = current-40
                    hehe = 0
                    for i in a:
                        if count>data:
                            hehe+=1
                            des+= '`'+i['name']+' '+'` ID: '+str(i['ids'])+' •  Level-'+str(i['lvl'])+' • IV: '+str(i['totiv'])+'%'
                            des+='\n'
                        if hehe ==20:
                            break
                        count+=1
                    current-=hehe
                embed2 = disnake.Embed(title = auth.name+ " Pokemons",description = des,color=disnake.Colour.blue())
                embed2.set_footer(text="Type `next` To View Next Page or Type `back` To View Previous Page")
                editable = channel.get_partial_message(await getlatest(auth.id))
                await editable.edit(embed =embed2)
    else:
      await ctx.send('You are not developer to sus a user')
  
  @dev.command(aliases = ['release'])
  async def free(self,ctx,arg1:disnake.Member,arg2):
    if not ctx.author.id  in self.owners:
      await ctx.send("You are not a developer to sus a user")
      return
    idd = arg1.id 
    if not await checkExist(idd):
      await ctx.send("Mentioned person is not a member of bot")
      return
    pk = await infonum(idd,arg2)
    if pk == False:
      await ctx.send("he does'nt have any pokemon at that number")
      return
    name = pk['name']
    mess = await ctx.send(f'{ctx.author.mention} Are you sure you want to release {name} for 50 credits !')
    await mess.add_reaction('<:Pz_Green_tick:873247568870662184>')
    await mess.add_reaction('<:redx:873247207124508742>')
    def check(reaction,user):
      emoji = str(reaction.emoji)
      return user.id == ctx.author.id and (emoji == '<:Pz_Green_tick:873247568870662184>' or emoji == '<:Pz_redx:873247207124508742>')
    try:
      reaction,user = await self.bot.wait_for('reaction_add',timeout = 60.0 ,check = check)
      if str(reaction.emoji) == '<:Pz_Green_tick:873247568870662184>':
        await ctx.send('You released this pokemon')
        await setbal(idd,50)
        await pkremove(idd,arg2)
        await gapfiller(idd)
      elif str(reaction.emoji) == '<:Pz_redx:873247207124508742>':
        await ctx.send("The release of pokemon was cancelled")
    except asyncio.TimeoutError:
      await ctx.send("Timeout for Interaction")

  @commands.command()
  async def give_random(self,ctx,arg1:disnake.Member,arg2 = None):
      if not ctx.author.id in self.owners:
        return
      shiny = True
      if arg2 == "shiny":
        shiny = True
      elif arg2 == 'normal':
        shiny = False
      else:
        await ctx.send('Please enter a valid give type')
        return
      if not await checkExist(arg1.id):
        await ctx.send("Mentioned person is not a user of bot")
        return
      pkId = random.choice(normal)
      name = byId(pkId,by = True)
      lvl = random.randint(25,60)
      async for i in addPoke(arg1.id,name,lvl=lvl,shiny=shiny):
        shv = ''
        if shiny:
          shv ="Shiny"
        await ctx.send("<:Pz_Green_tick:873247568870662184> **Congratulations**  "+arg1.name+"** You recieved a Level "+str(lvl)+' '+shv+' '+name+'**')
  
  @commands.command()
  async def givecrate(self,ctx,arg:disnake.Member,arg2,amount:int):
    if ctx.author.id not in self.owners:
      return
    arg2 = arg2.lower()
    if await setcrates(arg.id,arg2,amount) == False:
      await ctx.send('Please enter a valid crate name')
    else:
      s =''
      if amount!=1:
        s = 's'
      await ctx.send(f'{arg.name} has been given {amount} {arg2.title()} crate{s}')
 
def setup(bot):
    bot.add_cog(Dev(bot)) 