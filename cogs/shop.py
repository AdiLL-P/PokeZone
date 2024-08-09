from disnake.ext import commands
import disnake
from poke import natures,statModify,naModify,getmega,getprimal,getcomplete,getunbound,getgmax,get10,getultra,getdusk,getdawn,getorigin,getmoon,getsun,getshadow,getice,getshield,getsword,getemax,getspeed,getattack,getdefence,getash,getblack,getwhite
from User import infoc,getbal,setbal,checkExist,getshard,setshard,setredeem

natlc = {}
for i in natures.keys():
  natlc[i.lower()] = natures[i] 
class Shop(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    self.shop=[{'name':'Candy','price':80,'Description':'To Evolve Poke''\n''Level 1 - 70 Price = 80''\n''Level 71 - 100 Price = 100''\n'},{'name':'Natures','price':150,'Description':'With Changing Natures You Can Increase Stats By 10%'}]

  @commands.group(invoke_without_command = True)
  async def buy(self,ctx):
    pass
  
  @buy.command()
  async def nature(self,ctx,arg):
    idd = ctx.author.id
    if arg.lower() in natlc:
      data = await infoc(idd)
      if data['nature'].lower() == arg.lower():
        await ctx.send("You already have this nature")
      elif await getbal(idd) >= 150:
        data['nature'] = arg.lower().title()
        await naModify(idd,data)
        await setbal(idd,-150)
        await ctx.send("You have bought "+data['nature']+" for your "+data['name'])
      else:
        await ctx.send("You dont have enough bal to buy that nature")
    else:
      await ctx.send("That nature doesn't exist")    

  @buy.command(aliases = ['Candy'])
  async def candy(self,ctx,amt):
    idd = ctx.author.id
    data = await infoc(idd)
    if data == False:
      await ctx.send("Please select a pokemon to buy candies")
      return
    malvl =100- data['lvl']
    clvl = data['lvl']
    if not amt.isdigit():
      await ctx.send("Amount should be in digits")
      return
    amt= int(amt)
    if amt <=0:
      return
    elif amt>malvl:
      await ctx.send("Amount exceeds the max level")
    else:
      totamt = 0
      cc=1
      while cc<=amt:
        if clvl<=70:
          totamt+=70
          clvl+=1
          cc+=1
        elif clvl>70 and clvl<=100:
          totamt+=100
          clvl+=1
          cc+=1
      if await getbal(idd)>=totamt:
        newlvl = data['lvl']+amt
        await setbal(idd,-totamt)
        data = await infoc(ctx.author.id)
        embed = disnake.Embed(title=ctx.author.name,description="You have successfully bought "+str(amt)+" levels for your "+data['name'],color=disnake.Colour.blue())
        embed.set_thumbnail(url=data['link'])
        await ctx.send(embed=embed)
        #("You have successfully bought "+str(amt)+" levels for your "+data['name'])
        await statModify(idd,data,newlvl= newlvl)
      else:
        await ctx.send("You dont have enough coins to buy level")
  @buy.command()
  async def mega(self,ctx,xy=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getmega(data['name'],xy):
      await ctx.send("This Mega is not available for selected pokemon")
    elif await getbal(idd)<1000:
      await ctx.send("You dont have enough coins to buy Mega")
    else:
      await ctx.send("You have bought mega for your "+data['name'])
      await statModify(idd,data,'Mega '+data['name']+' '+xy.upper())
      await setbal(idd,-1000)

  @buy.command()
  async def primal(self,ctx,primal=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getprimal(data['name'],primal):
      await ctx.send("This Primal is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy This Form")
    else:
      await ctx.send("You have bought primal form for your "+data['name'])
      await statModify(idd,data,'Primal '+data['name']+' '+primal.upper())
      await setbal(idd,-2000) 

  @buy.command()
  async def complete(self,ctx,complete=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getcomplete(data['name'],complete):
      await ctx.send("complete form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy This form")
    else:
      await ctx.send("You have bought complete form for your "+data['name'])
      await statModify(idd,data,'Complete '+data['name']+' '+complete.upper())
      await setbal(idd,-2000) 

  @buy.command()
  async def unbound(self,ctx,unbound=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getunbound(data['name'],unbound):
      await ctx.send("Unbound form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought unbound form for your "+data['name'])
      await statModify(idd,data,data['name']+' Unbound'+unbound.upper())
      await setbal(idd,-2000) 

  @buy.command()
  async def gigantamax(self,ctx,gmax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getgmax(data['name'],gmax):
      await ctx.send("Gigantamax form is not available for selected pokemon")
    elif await getbal(idd)<30000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Gigantamax form for your "+data['name'])
      await statModify(idd,data,'Gigantamax '+data['name']+gmax.upper())
      await setbal(idd,-30000)

  @buy.command(name='10%')
  async def tenpercent(self,ctx,ten=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not get10(data['name'],ten):
      await ctx.send("10% form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought 10% form for your "+data['name'])
      await statModify(idd,data,data['name']+' 10%'+ten.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def ultra(self,ctx,ultra=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getultra(data['name'],ultra):
      await ctx.send("Ultra form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought ultra form for your "+data['name'])
      await statModify(idd,data,'Ultra '+data['name']+ultra.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def dusk(self,ctx,dusk=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getdusk(data['name'],dusk):
      await ctx.send("Dusk form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought dusk form for your "+data['name'])
      await statModify(idd,data,'Dusk '+data['name']+dusk.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def dawn(self,ctx,dawn=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getdawn(data['name'],dawn):
      await ctx.send("Dawn form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Dawn form for your "+data['name'])
      await statModify(idd,data,'Dawn '+data['name']+dawn.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def origin(self,ctx,origin=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getorigin(data['name'],origin):
      await ctx.send("Origin form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Origin form for your "+data['name'])
      await statModify(idd,data,'Origin '+data['name']+origin.upper())
      await setbal(idd,-2000)

  @buy.group(name='full',invoke_without_command=True)
  async def full(self,ctx):
    pass  

  @full.command()
  async def moon(self,ctx,moon=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getmoon(data['name'],moon):
      await ctx.send("Full Moon form is not available for selected pokemon")
    elif await getbal(idd)<3000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Full Moon form for your "+data['name'])
      await statModify(idd,data,'Full Moon '+data['name']+moon.upper())
      await setbal(idd,-3000)

  @buy.group(name='radiant',invoke_without_command=True)
  async def radiant(self,ctx):
    pass      

  @radiant.command()
  async def sun(self,ctx,sun=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getsun(data['name'],sun):
      await ctx.send("Radiant Sun form is not available for selected pokemon")
    elif await getbal(idd)<3000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Radiant Sun form for your "+data['name'])
      await statModify(idd,data,'Radiant Sun '+data['name']+sun.upper())
      await setbal(idd,-3000)

  @buy.group(name='rider',invoke_without_command=True)
  async def rider(self,ctx):
    pass    

  @rider.command(name='ice')
  async def ice_subcommand(self,ctx,ice=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getice(data['name'],ice):
      await ctx.send("Ice Rider form is not available for selected pokemon")
    elif await getbal(idd)<3000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Ice Rider form for your "+data['name'])
      await statModify(idd,data,'Ice Rider '+data['name']+ice.upper())
      await setbal(idd,-3000)

  @rider.command(name='shadow')
  async def shadow_subcommand(self,ctx,shadow=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getshadow(data['name'],shadow):
      await ctx.send("Shadow Rider form is not available for selected pokemon")
    elif await getbal(idd)<3000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Shadow Rider form for your "+data['name'])
      await statModify(idd,data,'Shadow Rider '+data['name']+shadow.upper())
      await setbal(idd,-3000)

  @buy.group(name='crowned',invoke_without_command=True)
  async def crowned(self,ctx):
    pass

  @crowned.command(name='sword')
  async def sword_subcommand(self,ctx,sword=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getsword(data['name'],sword):
      await ctx.send("Crowned Sword form is not available for selected pokemon")
    elif await getbal(idd)<3000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Crowned Sword form for your "+data['name'])
      await statModify(idd,data,'Crowned Sword '+data['name']+sword.upper())
      await setbal(idd,-3000)

  @crowned.command(name='shield')
  async def shield_subcommand(self,ctx,shield=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getshield(data['name'],shield):
      await ctx.send("Crowned Shield form is not available for selected pokemon")
    elif await getbal(idd)<3000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Crowned Shield form for your "+data['name'])
      await statModify(idd,data,'Crowned Shield '+data['name']+shield.upper())
      await setbal(idd,-3000)      

  @buy.command()
  async def eternamax(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getemax(data['name'],emax):
      await ctx.send("Eternamax form is not available for selected pokemon")
    elif await getbal(idd)<40000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Eternamax form for your "+data['name'])
      await statModify(idd,data,'Eternamax '+data['name']+emax.upper())
      await setbal(idd,-40000)

  @buy.command()
  async def attack(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getattack(data['name'],emax):
      await ctx.send("Attack form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Attack form for your "+data['name'])
      await statModify(idd,data,'Attack '+data['name']+emax.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def defence(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getdefence(data['name'],emax):
      await ctx.send("Defence Form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Defence form for your "+data['name'])
      await statModify(idd,data,'Defence '+data['name']+emax.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def speed(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getspeed(data['name'],emax):
      await ctx.send("Speed form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Speed form for your "+data['name'])
      await statModify(idd,data,'Speed '+data['name']+emax.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def ash(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getash(data['name'],emax):
      await ctx.send("Ash form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Ash form for your "+data['name'])
      await statModify(idd,data,'Ash-'+data['name']+emax.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def black(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getblack(data['name'],emax):
      await ctx.send("Black form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought Black form for your "+data['name'])
      await statModify(idd,data,'Black '+data['name']+emax.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def white(self,ctx,emax=''):
    idd = ctx.author.id
    data = await infoc(idd)
    if data ==False:
      await ctx.send("Select a pokemon")
    elif not getwhite(data['name'],emax):
      await ctx.send("White form is not available for selected pokemon")
    elif await getbal(idd)<2000:
      await ctx.send("You dont have enough balance to buy this form")
    else:
      await ctx.send("You have bought White form for your "+data['name'])
      await statModify(idd,data,'White '+data['name']+emax.upper())
      await setbal(idd,-2000)

  @buy.command()
  async def shard(self,ctx,amount=None):
    idd = ctx.author.id
    price = 300
    try:
      if amount!= None:
        amount = int(amount)
    except:
      await ctx.send("Amount should be in digits")
      return
    data = await getbal(idd) 
    if amount == None:
      await ctx.send('Pls enter amount of shards')
    elif data<(price*amount):
      await ctx.send('You Dont Have enough Balance To Buy Shards')
    else:
      await setbal(idd,-(price*amount))
      await setshard(idd,amount)
      await ctx.send(f'You Have Bought {amount} shard')

  @buy.command()
  async def redeems(self,ctx,rdm=None):
    idd = ctx.author.id
    price = 150
    try:
      if rdm!=None:
        rdm = int(rdm)
    except:
      await ctx.send("Amount should be in digits")
      return
    data = await getshard(idd)
    if rdm == None:
      await ctx.send('Pls enter amount of Redeem') 
    elif data<(price*rdm):
      await ctx.send('You Dont Have enough Shards To Buy Redeem')
    else:
      await setshard(idd,-(price*rdm))
      await setredeem(idd,rdm)
      await ctx.send(f'You Have Bought {rdm} redeem')


  @commands.group(name='shop',invoke_without_command=True)
  async def shop(self,ctx):
    ids = ctx.author.id
    if await checkExist(ids):
      balance = await getbal(ids)
    embed=disnake.Embed(title=f"**Balance: {balance} Zonal Coin's**",description='To see a specific page type `P?shop <Page_No>.`',color=0xFFE900)

    embed.add_field(name='ㅤ',value='` • ` Page 1 • All Page Information''\n''` • ` Page 2 • Nature''\n''` • ` Page 3 • Candy''\n''` • ` Page 4 • Mega''\n''` • ` Page 5 • Forms''\n''` • ` Page 6 • Gigantamax and Eternamax''\n''` • ` Page 7 • Shard')

    await ctx.send(embed=embed)

  @shop.command(name='2',invoke_without_command=True)
  async def two_subcommand(self,ctx):
    page2 = disnake.Embed(
    title="Nature | Cost = 150",description="**Nature Changers** | `It use To change pokemon nature which will increase 10% stat of one type and decrease 10% of other type to buy one type P?buy nature `**`<Nature_Name>`**",
    colour=disnake.Colour.orange())
    page2.add_field(name="Impish",value="+10% Increase In Defence | -10% Decrease In Sp.Atk")
    page2.add_field(name="Bold",value="+10% Increase In Defence | -10% Decrease In Speed")
    page2.add_field(name="Adamant",value="+10% Increase In Attack | -10% Decrease In Sp.Atk")
    page2.add_field(name="Brave",value="+10% Increase In Attack | -10% Decrease In Speed")
    page2.add_field(name="Calm",value="+10% Increase In Sp.Defen | -10% Decrease In Attack")
    page2.add_field(name="Timid",value="+10% Increase In Speed | -10% Decrease In Attack")
    page2.add_field(name="Quiet",value="+10% Increase In Sp.Atk | -10% Decrease In Speed")
    page2.add_field(name="Careful",value="+10% Increase In Sp.Defen | -10% Decrease In Sp.Atk")
    page2.add_field(name="Gentle",value="+10% Increase In Sp.Defen | -10% Decrease In Sp.Atk")
    page2.add_field(name="Hasty",value="+10% Increase In Speed | -10% Decrease In Defen")
    page2.add_field(name="Jolly",value="+10% Increase In Speed | -10% Decrease In Sp.Atk")
    page2.add_field(name="Relaxed",value="+10% Increase In Defen | -10% Decrease In Speed")
    page2.add_field(name="Rash",value="+10% Increase In Sp.Atk | -10% Decrease In Sp.Defen")
    page2.add_field(name="Naughty",value="+10% Increase In Attack | -10% Decrease In Sp.Defen")
    page2.add_field(name="Naive",value="+10% Increase In Speed | -10% Decrease In Sp.Defen")
    page2.add_field(name="Modest",value="+10% Increase In Sp.Atk | -10% Decrease In Attack")
    page2.add_field(name="Mild",value="+10% Increase In Sp.Atk | -10% Decrease In Defen")
    page2.add_field(name="Lonely",value="+10% Increase In Attack | -10% Decrease In Defen")
    page2.add_field(name="Lax",value="+10% Increase In Defen | -10% Decrease In Sp.Defen")
    page2.add_field(name="Sassy",value="+10% Increase In Sp.Def | -10% Decrease In Speed")

    await ctx.send(embed=page2)

  @shop.command(name='3')
  async def three_subcommand(self,ctx):
    page3 = disnake.Embed(title="Candy",
                      description="Cost :-""\n""Candies level up your selected Pokémon by one level for each candy you feed it.\n`P?buy candy <amount>`\n",
                      colour=disnake.Colour.orange())
    await ctx.send(embed=page3)

  @shop.command(name='4')
  async def four_subcommand(self,ctx):
    page4 = disnake.Embed(title="Mega | Cost = 1000",description="**Mega**""\n""`P?buy mega`""\n""**Mega Y**""\n""`P?buy mega y`""\n""**Mega X**""\n""`P?buy mega x`",colour=disnake.Colour.blue())
    await ctx.send(embed=page4)

  @shop.command(name='5')
  async def five_subcommand(self,ctx):
    embed=disnake.Embed(title='Forms | Price = 2000',description="`Some Pokemon Have Different forms.You Can Buy them.To Buy Type P?buy <form_name>` \n```\nNote: Must Select the pokemon Which is  eligible to transform into this Form```",colour=0x00FFFF)
    embed.add_field(name='`•` Primal',value='Primal Kyogre / Groudon: `P?buy primal`')
    embed.add_field(name='`•` Solgaleo',value='Radiant Sun Solgaleo: `P?buy radiant sun`')
    embed.add_field(name='`•`Lunala',value='Full Moon Lunala: `P?buy full moon`')
    embed.add_field(name='`•` Necrozma',value='Ultra: `P?buy ultra`\nDawn: `P?buy dawn`\nDusk: `P?buy dusk`')
    embed.add_field(name='`•` Zygarde',value='Complete: `P?buy complete`\n10%: `P?buy 10%`')
    embed.add_field(name='`•` Crowned',value='Zacian: `P?buy crowned sword`\nZamazenta: `P?buy crowned shield`')
    embed.add_field(name='`•` Greninja',value='Ash: `P?buy ash`')
    embed.add_field(name='`•` Giratina',value='Origin: `P?buy origin`')
    embed.add_field(name='`•` Calyrex',value='Ice Rider: `P?buy rider ice`\nShadow Rider: `P?buy rider shadow`')
    embed.add_field(name='`•` Deoxys',value='Attack: `P?buy attack`\nDefence: `P?buy defence`\nSpeed: `P?buy speed`')
    embed.add_field(name='`•` Kyurem',value='Black: `P?buy black`\nWhite: `P?buy white`')
    await ctx.send(embed=embed)

  @shop.command(name='6')
  async def six_subcommand(self,ctx):
    embed=disnake.Embed(title='Gigantamax | Price: 20,000\nEternamax | Price: 40,000',description='`Some Pokemon can be further evolved to Gigantamax and Eternamax.` \n```\nNote: Must Select the pokemon Which is  eligible to Evolve into this Form```',color=0xDC143C)
    embed.add_field(name='Gigantamax',value='`P?buy gigantamax`')
    embed.add_field(name='Eternamax',value='`P?buy eternamax`')
    await ctx.send(embed=embed)

  @shop.command(name='7')
  async def seven_subcommand(self,ctx):
    bal = await getbal(ctx.author.id)
    embed=disnake.Embed(title=f'Your Balance: {bal}',description='To Check Your Shards and other information type `P?shards` and each redeem costs 150 shards',color=0xDC143C)
    embed.add_field(name='Redeem',value='`P?buy redeem <amount>`')
    await ctx.send(embed=embed)
    
  @commands.command()
  async def shards(self,ctx):
    srd = await getshard(ctx.author.id)
    embed=disnake.Embed(title=f'Your Shards: {srd}',description='Each Shard Costs `300 ZC`',color=0xDC143C)
    embed.add_field(name='Shard',value='`P?buy shard <amount>`')
    await ctx.send(embed=embed)

def setup(bot):
  bot.add_cog(Shop(bot))