import disnake
import os
import re
from datetime import date
today = date.today()
from PIL import Image
from User import id_creator, getbal, checkExist, getredeem, leader,getinv,setinv,setpref,getpref,setredeem,setbal#,info
from disnake.ext import commands
from poke import addPoke, redeem
import requests
import asyncio
import random
import datetime
from webserver import keep_alive
intents = disnake.Intents.default()
intents.members = True
from dotenv.main import load_dotenv
load_dotenv()


prefixes = {}
async def get_pre(bot,message):
  return prefixes.get(message.guild.id,['p?',':','P?']) 
  
bot = commands.AutoShardedBot(command_prefix=get_pre,
                   help_command=None,
                   intents=intents,test_guilds = [])

bot.owner_ids = []

prefix=bot.command_prefix
@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name=f"| {len(bot.users)} User's"))
    global prefixes
    prefixes = await getpref()
    print("=======================================\n"+str(bot.user) + " is Online\n===========================================")
    async for i in leader('bal'):
        pass
    async for i in leader('redeem'):
        pass
    async for i in leader('catches'):
        pass
    async for i in leader('shard'):
        pass
    async for i in leader('released'):
        pass
    async for i in leader('shinies'):
        pass

@bot.command()
async def uptime(ctx):
 delta_uptime = datetime.utcnow() - bot.launch_time
 hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
 minutes, seconds = divmod(remainder, 60)
 days, hours = divmod(hours, 24)
 await ctx.send(f"** I have been online for  `{days}` Days, `{hours}` Hours, `{minutes}` Minutes, `{seconds}` Seconds.**")



@bot.command()
async def ping(ctx):
    await ctx.send(
        f"**Pong!!** {ctx.author.mention}  **Current API Latency of Pokézone is {round(bot.latency * 1000)}ms  <a:Pz_Hq_latency:877440554529615872>**"
    )


@bot.command()
async def start(ctx):
    prefix = await get_pre(bot,ctx.message)
    if type(prefix)  == list:
      prefix = prefix[0]
    embed = disnake.Embed(
        title="• WELCOME TO POKÉZONE •",
        description=
        f"**Welcome to the world of pokémon***\n***Hey we think you are a new player wanna start your journey?***\n***Type `{prefix}`pick (Pokemon name) to start your Pokézone journey!!**",
        color=0xFFDF00
    ).set_author(
        name='Professor Cerice',
        url="https://discord.gg/SUMUNTCehH",
        icon_url=
        'https://cdn.discordapp.com/attachments/512275320645353502/867373806539898890/Professor_Cerise_JN.png'
    )
    embed.add_field(name="GEN I  (Kanto)",
                    value="•Bulbasaur  •Squirtle  •Charmander",
                    inline=False)
    embed.add_field(name="GEN II (JHOTO)",
                    value="•Chikorita   •Totodile   •Cyndaquil",
                    inline=False)
    embed.add_field(name="GEN III (HOENN)",
                    value="•Treecko   •Torchic   •Mudkip",
                    inline=False)
    embed.add_field(name="GEN IV (SINHO)",
                    value="•Turtwig   •Chimchar   •Piplup",
                    inline=False)
    embed.add_field(name="GEN V (UNOVA)", value="•Snivy   •Tepig   •Oshawott")
    embed.add_field(name="GEN VI (KALOS)",
                    value="•Froakie   •Fennikin   •Chespin",
                    inline=False)
    embed.add_field(name="GEN VII (ALOLA)",
                    value="•Rowlet   •Popplio   •Litten",
                    inline=False)
    embed.add_field(name="GEN VIII (GALAR)",
                    value="•Grookey   •Sobble   •Scorbunny",
                    inline=False)
    embed.set_image(url="attachment://start.png")
    embed.set_footer(
        text=
        "NOTE: IF FOUND USING AUTO CATCHER YOUR ACCOUNT WILL BE BLACKLISTED FROM THE BOT"
    )
    await ctx.send(file=disnake.File('images/start.png'), embed=embed)


starters = [
    'Bulbasaur', 'Squirtle', 'Charmander', 'Chikorita', 'Totodile',
    'Cyndaquil', 'Treecko', 'Torchic', 'Mudkip', 'Turtwig', 'Chimchar',
    'Piplup', 'Snivy', 'Tepig', 'Oshawott', 'Froakie', 'Fennekin', 'Chespin',
    'Rowlet', 'Popplio', 'Litten', 'Grookey', 'Sobble', 'Scorbunny'
]
strlow = []
for i in starters:
    strlow.append(i.lower())

@commands.max_concurrency(1,per = commands.BucketType.user,wait = False)
@bot.command()
async def pick(ctx, *arg):
    prefix = await get_pre(bot,ctx.message)
    if type(prefix)  == list:
      prefix = prefix[0]
    ids = ctx.author.id
    chan = ctx.channel
    if await checkExist(ids):
        await ctx.send(
            "<:Pz_redx:873247207124508742> **You Have Already Picked Your Starter**"
        )
        return
    arg = ' '.join(arg)
    if arg.lower() in strlow:
        name = starters[strlow.index(arg.lower())]
        mess = await ctx.send(f"{ctx.author.mention} **are you invited by someone to play the bot.**\n_`Pls reply with his or her Id / mention him or her. If you were not reply with No \nConfused ?? Try `_**`{prefix}event`**")
        def check(m):
             return m.channel == chan and m.author.id == ids
        while True:
          try:
            msg = await bot.wait_for('message',timeout = 60.0, check = check)
            content = msg.content
            if content.lower() == f'{prefix}event' or content.lower() == ':event':
              pass
            elif not (content.lower() == 'no' or content.lower() == f'{prefix}no'):
              idd = [i for i in content if i.isdigit()]
              idd = ''.join(idd)
              if not await checkExist(idd):
                await mess.reply("That person is not a member of bot , are you sure !\nPlease reply again")
              else:
                if await getinv(idd)>2:
                  await ctx.send("Please ping someone else")
                else:
                  await setinv(idd)
                  await ctx.send(f"<@{idd}> Your invite perks have been enabled from {ctx.author.name}")
                  break
            else:
              idd = None 
              break
          except asyncio.TimeoutError:
            await ctx.send("Timeout! please pick again")
            return
        message = await ctx.send('<a:Pz_loading:891004070456868864> **ADDING YOUR ID IN DB**')
        tim = today.strftime("%m/%d/%y")
        await id_creator(ids,idd,tim)
        async for i in addPoke(ids, name, lvl=random.randint(1, 40)):
            iv = i
        await message.edit(
            content=
            f'<:Pz_Green_tick:873247568870662184> **Your Profile Has been succesfully created <a:Pz_loading:891004070456868864>  Adding your Starter**')
        data = redeem(name,by = True)
        await asyncio.sleep(1)
        embed = disnake.Embed(
            title='STARTER',
            description=
            f"<:Pz_Green_tick:873247568870662184> **{ctx.author.name} you have succesfully picked "
            + name + f" as your starter **\n`IV: {str(iv)}%`",color=0xFFDF00)
        embed.set_thumbnail(url=data[0])
        await message.edit(content=None, embed=embed)
    else:
        await ctx.send(
            f"<:Pz_redx:873247207124508742> ** {ctx.author.name} You Can't Pick This Pokemon as Your Starter**"
        )

@bot.command()
async def event(ctx): 
    embed = disnake.Embed(title = "Event",description = '**Invite your friends and at their** `10th` / `100th` / `1000th` **catch you will get redeems,Also new Users will get 5k coins**',colour = 0xFFDF00)
    embed.add_field(name = "Usage",value = '**1 : **`When your friend will pick a pokemon,he will be asked to tell the inviter id/ping and if he tells your id,then on his 10th/100th/1000th catch`,**`You will get a Redeem.`**\n**2 : **`User will get 5k coins on their own 10th and 1000th catch`')
    embed.set_footer(text="Note: This event is for our earliest Users and might get modified a little later..")
    await ctx.send(embed = embed)


@bot.command()
async def stats(ctx):
    embed = disnake.Embed(title="Pokézone Bot Stats", color=0xFFCDA2)
    embed.add_field(name="<:Pz_prefix:889221463876444191> ・ DEFAULT PREFIX",
                    value="p?",
                    inline=False)
    embed.add_field(name="<a:Pz_latency:889216596806107166> ・ PING",
                    value=f"`{round(bot.latency * 1000)}ms`",
                    inline=False)
    embed.add_field(
        name="<:Pz_robo:889220120017260544> ・ BOT INFO",
        value=f"Servers: {len(bot.guilds)}\nUsers: {len(bot.users)}")
    embed.add_field(name="<:Pz_zc:889222302607212555> ・ CURRENCY",
                    value="`Zonal Coin's`",
                    inline=False)
    embed.add_field(name="<:Pz_library:889219939246948405> ・ LIBRARY",
                    value="<:Pz_Py:889217125481324584> disnake.py v1.7.3",
                    inline=False)
    embed.set_footer(text="Requested by  " + ctx.author.name)
    embed.set_thumbnail(url=(
        "https://cdn.discordapp.com/attachments/852764649023209502/877403877610242068/servers.gif"
    ))
    await ctx.send(embed=embed)



page1 = disnake.Embed(title="All Page info",
                      description="` • ` **Page 1**  •  All Pages Info"
                      "\n"
                      "` • ` **Page 2**  •  All COMMANDS"
                      "\n"
                      "` • ` **Page 3**  •  Trade, Market & Auction",
                      color=disnake.Colour.orange())

page2 = disnake.Embed(
    title="ALL COMMANDS",
    description=" • `P?Catch`   -   To Catch a Spawned Pokémon"
    "\n"
    "\n"
    " • `Info`   -   To Info a Selected Pokémon"
    "\n"
    "\n"
    " • `nfo Latest`   -   To Info the Latest Pokémon you have Caught"
    "\n"
    "\n"
    " • `Dex`   -   o get Information about a Pokemon"
    "\n"
    "\n"
    " • `Support`   -   To Join Pokézone HQ "
    "\n"
    "\n"
    " • `Invite`   -   To Invite Pokézone To your server",
    colour=disnake.Colour.orange())

page3 = disnake.Embed(title="TRADE / AUCTION / MARKET",
                      description="COMING SOON!",
                      colour=disnake.Colour.orange())



@bot.command(aliases=["Bal", "balance", "Balance"])
async def bal(ctx):
    ids = ctx.author.id
    if await checkExist(ids):
        amt = await getbal(ids)
        embed = disnake.Embed(title=f"{ctx.author.name}'s Balance",
                              description=f"**Balance**: {amt} Zonal Coin's",
                              color=0xFFDF00)
        embed.set_thumbnail(
            url=
            "https://cdn.discordapp.com/attachments/853907239257899030/876805654046736444/ZC.png"
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(ctx.author.mention + "You still need to start")


@bot.command()
async def redeems(ctx):
    ids = ctx.author.id
    if await checkExist(ids):
        rdm = await getredeem(ids)
        embed = disnake.Embed(title=f"{ctx.author.name}'s Redeem",
                              description=f"Redeem: {rdm}",
                              color=0xFFDF00)
        await ctx.send(embed=embed)
    else:
        await ctx.send(ctx.author.mention + "You still need to start")

@bot.command()
async def setprefix(ctx,*prf):
  if ctx.author.guild_permissions.administrator:
    if len(prf)==0:
      await ctx.send("You cannot have an empty prefix for your server !")
    elif len(prf)>4:
      await ctx.send(" <:Pz_redx:873247207124508742> You cannot have more than 4 prefixes for your server !")
    else:
      if len(prf) ==1:
        prf = ''.join(prf)
      await setpref(ctx.guild.id,prf)
      await ctx.send(f" <:Pz_Green_tick:873247568870662184> Sucessfully changed the prefix for this server to `{prf}`")
      global prefixes
      prefixes = await getpref()
  else:
    await ctx.send(" <:Pz_redx:873247207124508742> You dont have Administrator permissions for changing Bot's Prefix !")

@bot.command()
async def invite(ctx):
  embed=disnake.Embed(title=f'Invite! {str(bot.user)}',color=0xffdf00)
  embed.add_field(name='**BOT**',value='**[Click Here]()**')
  embed.add_field(name='SERVER',value='**[CLICK HERE]() TO JOIN SUPPORT SERVER**')
  embed.set_thumbnail(url=bot.user.avatar.url)
  await ctx.send(embed=embed)


for i in ('daily','dexsp','dex','gamble','main2','shop','trade','dev','help'):
  bot.load_extension('cogs.'+i)

bot.load_extension('User')
Token = os.environ['Token']
keep_alive()
bot.run(Token)