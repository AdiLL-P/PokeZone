import disnake
import datetime
import json
from disnake.ext import commands
import random
import asyncio
from User import setredeem,setbal,checkExist,incvote,getcrates,getvote,setcrates,setshard,getpref
from poke import addPoke,byId,normal,leggie,mythic,galar,alola

class Daily(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
      lol =  open('shiny.json','r')
      if len(lol.read()) !=0:
        lol.seek(0)
        data = json.load(lol)
        guild = self.bot.get_guild(852097339442331649)
        role = guild.get_role(888747355682267166)
        for id in data:
          member = guild.get_member(id)
          await member.remove_roles(role)
      lol.close()
      lol = open('shiny.json','w')
      lol.close()

    async def rmvrole(self,member,role):
      with open('shiny.json','r') as lol:
        if len(lol.read()) == 0:
          data = [member.id]
        else:
          lol.seek(0)
          data = json.load(lol)
          data.append(member.id)
      with open('shiny.json','w') as lol:
        json.dump(data,lol)
      await asyncio.sleep(3600)
      await member.remove_roles(role)
      with open('shiny.json','r+') as lol:
        data = json.load(lol)
        data.remove(member.id)
      with open('shiny.json','w') as lol:
        json.dump(data,lol)

    async def voteres(self,id,guild):
      user = self.bot.get_user(id)
      await incvote(id)
      votes = await getvote(id)
      reward = None
      if votes<5:
        await setcrates(id,'bronze',1)
        reward = 'bronze'
      elif votes<10:
        await setcrates(id,'silver',1)
        reward = 'silver'
      elif votes%20 ==0:
        await setcrates(id,'diamond',1)
        reward = 'diamond'
      elif votes%10 == 0:
        member = guild.get_member(id)
        if member is not None:
          role = guild.get_role(888747355682267166)
          await member.add_roles(role)
          asyncio.create_task(self.rmvrole(member,role))
          reward = 'shiny'
          print(f'User has access to shiny spawn for 1 hour:\n----------\nUser: {member.name}\n----------')
      else:
        await setcrates(id,'golden',1)
        reward = 'golden'

      if reward is not None:
        if reward == 'shiny':
          try:
            await user.send('Thanks for voting , You have gained access to Shiny catching for 1 hour')
          except:
            pass
        else:
          try:
            await user.send(f'Thanks for voting , You have recieved a {reward.title()} crate')
          except:
            pass
      channel = self.bot.get_channel(889057960930725908)
      embed = disnake.Embed(title = f'{user.name} has Upvoted!',colour = 0x2F3136,timestamp=datetime.datetime.utcnow())
      await channel.send(embed = embed)
    @commands.Cog.listener()
    async def on_message(self,msg):
      if msg.channel.id == 878498137357025280:
        if msg.content.isdigit():
          if await checkExist(msg.content):
            id = int(msg.content)
            asyncio.create_task(self.voteres(id,msg.guild)
            )
          else:
            msg.author.send("Please start the bot and vote later !")
    
    @commands.command()
    async def daily(self,ctx):
      crates = await getcrates(ctx.author.id)
      vote = await getvote(ctx.author.id)
      embed = disnake.Embed(
      title="Voting Rewards",
      description=f"""**[Vote the bot every 12 hours to get rewards!](https://top.gg/bot/832266727022395402/vote)**
Vote the bot multiple days in a streak and give you a chance at better rewards!

Vote Us by **[Clicking Here!](https://top.gg/bot/832266727022395402/vote)**
**Voting Streak**
{'<:Pz_Green_tick:873247568870662184>'*(vote if vote<7 else 7)}{'<:Pz_redx:873247207124508742>'*((7-vote) if vote<7 else 0)}
Current Voting Streak: `{vote}` votes!

**Your Rewards**
<:bronze_crate:889015428066734101> ・ Bronze Crate: { crates['bronze']}
<:silver_crate:889017053971902474> ・ Silver Crate: { crates['silver']}
<:golden_crate:889019160342982676> ・ Golden Crate: { crates['golden']}
<:daimond_crate:889019093804539914> ・ Diamond Crate: { crates['diamond']}


**Crate Opening : P!crate open [Bronze | Silver | Gold | Diamond]**
        
Once you have voted, you will get Dm from the bot & Rewards will automatically get redeemed to your account.""",color=0xffdf00)
      embed.set_footer(text="text",icon_url=ctx.author.avatar.url)
      embed.set_footer(text=f'Requested by {ctx.author.name}') 
      await ctx.send(embed=embed)
  

    @commands.command()
    async def crates(self,ctx):
      crates = await getcrates(ctx.author.id)
      embed = disnake.Embed(title=ctx.author.name+"'s Crates",description=f"""<:bronze_crate:889015428066734101> | Bronze Crate: { crates['bronze']}
<:silver_crate:889017053971902474> | Silver Crate: { crates['silver']}
<:golden_crate:889019160342982676> | Golden Crate: { crates['golden']}
<:daimond_crate:889019093804539914> | Diamond Crate: { crates['diamond']}""",color=0xffdf00)
      await ctx.send(embed=embed)
    
    @commands.command()
    async def votes(self,ctx): 
      if await checkExist(ctx.author.id):
        votes = await getvote(ctx.author.id)
        await ctx.send(f"**Your votes :** ` {votes} `")
      else:
        await ctx.send("You still need to start")
    

    @commands.group(name='crate',invoke_without_command=True)
    async def crate(self,ctx):
      crates = await getcrates(ctx.author.id)
      embed = disnake.Embed(title=ctx.author.name+"'s Crates",description=f"""<:bronze_crate:889015428066734101> | Bronze Crate: { crates['bronze']}
<:silver_crate:889017053971902474> | Silver Crate: { crates['silver']}
<:golden_crate:889019160342982676> | Golden Crate: { crates['golden']}
<:daimond_crate:889019093804539914> | Diamond Crate: { crates['diamond']}""",color=0xffdf00)
      await ctx.send(embed=embed)

    

    @crate.group(name='open',invoke_without_command=True)
    async def open(self,ctx):
      await ctx.send("Send in this format\n`P?crate open (crate_name)`")

    @open.command()
    async def bronze(self,ctx):
      crates = await getcrates(ctx.author.id)
      if crates['bronze']<=0:
        await ctx.send('You dont have enough crates')
      else:
        crate='bronze'
        reward=random.choice(['bal','poke'])
        if reward == 'bal':
          await setcrates(ctx.author.id,crate,-1)
          await setbal(ctx.author.id,300)
          embed = disnake.Embed(title='Bronze Crate',description='300 Zonal Coin',color=0xffdf00)
          await ctx.send(embed=embed)
        elif reward == 'poke':
          await setcrates(ctx.author.id,crate,-1)
          pkId = random.choice(normal)
          name = byId(pkId,by = True)
          lvl = random.randint(25,60)
          async for i in addPoke(ctx.author.id,name,lvl=lvl):
            embed = disnake.Embed(title='Bronze Crate',description=f'Level {str(lvl)} {name}',color=0xffdf00)
            await ctx.send(embed=embed)

    @open.command()
    async def silver(self,ctx):
      crates = await getcrates(ctx.author.id)
      if crates['silver']<=0:
        await ctx.send('You dont have enough crates')
      else:
        crate = 'silver'
        reward=random.choice(['bal','poke'])
        if reward == 'bal':
          await setcrates(ctx.author.id,crate,-1)
          await setbal(ctx.author.id,500)
          embed = disnake.Embed(title='Silver Crate',description='500 Zonal Coin',color=0xffdf00)
          await ctx.send(embed=embed)
        elif reward == 'poke':
          await setcrates(ctx.author.id,crate,-1)
          pkId = random.choice(normal)
          name = byId(pkId,by = True)
          lvl = random.randint(25,60)
          async for i in addPoke(ctx.author.id,name,lvl=lvl):
            embed = disnake.Embed(title='Silver Crate',description=f'Level {str(lvl)} {name}',color=0xffdf00)
            await ctx.send(embed=embed)
        # silver 500 - 900 zc  
    @open.command()
    async def golden(self,ctx):
      crates = await getcrates(ctx.author.id)
      if crates['golden']<=0:
        await ctx.send('You dont have enough crates')
      else:
        reward=random.choice(['bal','redeem','shard','poke','poke','poke','bal'])
        crate = 'golden'
        if reward == 'bal':
         await setcrates(ctx.author.id,crate,-1)
         await setbal(ctx.author.id,1000)
         embed = disnake.Embed(title='Golden Crate',description='1000 Zonal Coin',color=0xffdf00)
         await ctx.send(embed=embed)
        elif reward == 'poke':
           typ =random.choices(['normal','mythic','leggie','shiny'],weights=[30,5,4,1],k=10)
           typ = random.choice(typ)
           if typ == 'shiny':
            pkId = random.choice(normal)
            name = byId(pkId,by = True)
            lvl = random.randint(25,60)
            await setcrates(ctx.author.id,crate,-1)
            async for i in addPoke(ctx.author.id,name,lvl=lvl,shiny=True):
              embed = disnake.Embed(title='Golden Crate',description=f'⭐ {name}',color=0xffdf00)
              await ctx.send(embed=embed)
           else:
            if typ == 'normal':
              pkId = random.choice(normal)
            elif typ == 'mythic':
              pkId = random.choice(mythic)
            elif typ == 'leggie':
              pkId = random.choice(leggie)
            name = byId(pkId,by = True)
            lvl = random.randint(25,60)
            await setcrates(ctx.author.id,crate,-1)
            async for i in addPoke(ctx.author.id,name,lvl=lvl):
              embed = disnake.Embed(title='Golden Crate',description=f'Level {str(lvl)} {name}',color=0xffdf00)
              await ctx.send(embed=embed)
        elif reward == 'shard':
          await setcrates(ctx.author.id,crate,-1)
          await setshard(ctx.author.id,50)
          embed = disnake.Embed(title='Golden Crate',description='50 Shard',color=0x2F3136)
          await ctx.send(embed=embed)
        elif reward == 'redeem':
          await setcrates(ctx.author.id,crate,-1)
          await setredeem(ctx.author.id,1)
          embed = disnake.Embed(title='Golden Crate',description='1 Redeem',color=0xffdf00)
          await ctx.send(embed=embed)

    @open.command()
    async def diamond(self,ctx):
      crates = await getcrates(ctx.author.id)
      if crates['diamond']<=0:
        await ctx.send('You dont have enough crates')
      else:
        reward=random.choice(['bal','redeem','shard','poke','poke'])
        crate = 'diamond'
        if reward == 'bal':
         await setcrates(ctx.author.id,crate,-1)
         amt = random.randint(10000,20000)
         await setbal(ctx.author.id,amt)
         embed = disnake.Embed(title='Diamond Crate',description=f'{amt} Zonal Coin',color=0x2F3136)
         await ctx.send(embed=embed)
        elif reward == 'poke':
           typ =random.choices(['galar','alola','mythic','leggie','shiny'],weights=[5,5,4,3,1],k=10)
           typ = random.choice(typ)
           if typ == 'shiny':
            look = random.choices(['galar','alola','mythic','leggie'],weights=[5,5,4,3],k=1)
            lol = random.choice(look)
            if lol == 'galar': lol = galar
            elif lol == 'alola':lol = alola
            elif lol == 'mythic':lol = mythic
            elif lol == 'leggie':lol = leggie
            pkId = random.choice(lol)
            name = byId(pkId,by = True)
            lvl = random.randint(25,60)
            await setcrates(ctx.author.id,crate,-1)
            async for i in addPoke(ctx.author.id,name,lvl=lvl,shiny=True):
              embed = disnake.Embed(title='Daimond Crate',description=f'⭐ {name}',color=0xffdf00)
              await ctx.send(embed=embed)
           else:
            if typ == 'alola':
              pkId = random.choice(alola)
            elif typ == 'galar':
              pkId = random.choice(galar)
            elif typ == 'mythic':
              pkId = random.choice(mythic)
            elif typ == 'leggie':
              pkId = random.choice(leggie)
            name = byId(pkId,by = True)
            lvl = random.randint(25,60)
            await setcrates(ctx.author.id,crate,-1)
            async for i in addPoke(ctx.author.id,name,lvl=lvl):
              embed = disnake.Embed(title='Diamond Crate',description=f'Level {str(lvl)} {name}',color=0xffdf00)
              await ctx.send(embed=embed)
        elif reward == 'shard':
          await setcrates(ctx.author.id,crate,-1)
          amt = random.randint(100,500)
          await setshard(ctx.author.id,amt)
          embed = disnake.Embed(title='Diamond Crate',description=f'{amt} Shard',color=0xffdf00)
          await ctx.send(embed=embed)
        elif reward == 'redeem':
          await setcrates(ctx.author.id,crate,-1)
          amt = random.randint(1,3)
          await setredeem(ctx.author.id,amt)
          embed = disnake.Embed(title='Diamond Crate',description=f'{amt} Redeem',color=0xffdf00)
          await ctx.send(embed=embed)              

def setup(bot):
    bot.add_cog(Daily(bot)) 