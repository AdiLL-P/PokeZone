import disnake
import asyncio
from datetime import datetime
from disnake.ext import commands
from User import leader,allPokes,getlatest,setlatest,setorder,getsh,checkExist,setsh,getbal,getredeem,infoc,lates,selector,getshard,getrel,getcat,getshiny,getstart,getvote
from poke import redeem
class Extension(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
  @commands.group(aliases=["lb","Lb","lB","LB"],invoke_without_command = True)
  async def leaderboard(self,ctx,arg = 'bal'):
    if arg == 'redeem' or arg == 'redeems':
      arg = 'redeem'
      bo = ' redeems'
    elif arg == 'caught' or arg == 'catches':
      arg = 'catches'
      bo = ' catches'
    elif arg == 'shards' or arg == 'shard':
      arg = 'shard'
      bo = ' shards'
    elif arg == 'released' or arg == 'free' or arg =='release':
      arg = 'released'
      bo = ' releases'
    elif arg == 'shinies' or arg == 'shiny':
      arg = 'shinies'
      bo = ' shinies'
    else:
      arg = 'bal'
      bo = 'zc'
    async for data in leader(arg):
      data = sorted(data.items(),key = lambda x:x[1],reverse = True)
      count = 0
      embed = disnake.Embed(title = "LeaderBoard",description = '\n',color=disnake.Colour.blue())
      for i in data:
        try:
          mem = self.bot.get_user(int(i[0])).name
        except:
          continue
        bal = str(i[1])
        embed.add_field(name = mem,value =bal+bo,inline = False)
        count+=1
        if count == 10:
          break
      if arg == 'bal':
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/852097339878801410/852413381851611156/Untitled.png")
      await ctx.send(embed = embed)
      
  
  @leaderboard.command()
  async def redeems(self,ctx):
    async for data in leader('redeem'):
      data = sorted(data.items(),key = lambda x:x[1],reverse = True)
      count = 0
      embed = disnake.Embed(title = "LeaderBoard",description = '\n',            color=disnake.Colour.from_rgb(255,0,0))
      for i in data:
        try:
          mem = self.bot.get_user(int(i[0])).name
        except:
          continue
        bal = str(i[1])
        embed.add_field(name = mem,value =bal+" redeems",inline = False)
        count+=1
        if count == 10:
          break
      await ctx.send(embed = embed)
  @commands.command(aliases=["pk","Pk","pK","PK","pokemon","Pokemon"])
  async def pokemons(self,ctx):
        if not await checkExist(ctx.author.id):
          await ctx.send("You are not a member of bot . Please try p?start")
          return
        current = 0
        broke = True
        channel = ctx.channel
        auth = ctx.author
        a =await allPokes(auth.id)
        if a ==False:
            await ctx.send("```No pokemons were found in your profile!```")
            return
        des = ''
        for i in a :
            name = i['name']
            if '🌟' in name:
              name = name.replace('🌟','`🌟`')
            des+= '`'+str(i['ids'])+'` '+name+' • Level-'+str(i['lvl'])+' • IV: '+str(i['totiv'])+'%'
            des+='\n'
            current+=1
            if current ==20:
                break
        embed = disnake.Embed(title = auth.name+" Pokemons",description = des,color=disnake.Colour.blue())
        embed.set_footer(text="Type `next` To view next page or Type `back` To view Previous Page")
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
                            name = i['name']
                            if '🌟' in name:
                              name = name.replace('🌟','`🌟`')
                            des+= '`'+str(i['ids'])+'` '+name+' • Level-'+str(i['lvl'])+' • IV: '+str(i['totiv'])+'%'
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
                            name = i['name']
                            if '🌟' in name:
                              name = name.replace('🌟','`🌟`')
                            des+= '`'+name+' '+'` ID: '+str(i['ids'])+' | Level-'+str(i['lvl'])+' | IV: '+str(i['totiv'])+'%'
                            des+='\n'
                        if hehe ==20:
                            break
                        count+=1
                    current-=hehe
                embed2 = disnake.Embed(title = auth.name+ " Pokemons",description = des,color=disnake.Colour.blue())
                embed2.set_footer(text="Type `next` To View Next Page or Type `back` To View Previous Page")
                editable = channel.get_partial_message(await getlatest(auth.id))
                await editable.edit(embed =embed2)


  @commands.command()
  async def order(self,ctx,arg):
    if await setorder(ctx.author.id,arg):
      await ctx.send("Your pokemons will be viewed by "+arg.title())
    else:
      await ctx.send("That is an invalid order . Please try again")
   
  @commands.command(aliases = ['sh'])
  async def shinyhunt(self,ctx,*arg):
    if not await checkExist(ctx.author.id):
      await ctx.send(ctx.author.mention+" You still need to start")
      return
    if arg ==():
      hunt= await getsh(ctx.author.id)
      if hunt ==None:
        emb = disnake.Embed(title = "Shiny Hunt",description = "<:Pz_redx:873247207124508742> **Currently You are not shiny hunting any pokemon**",color=0xFFDF00).set_thumbnail(url='https://cdn.discordapp.com/emojis/872675013432594432.gif?v=1')
      else:
         data = redeem(hunt[0],by = True)
         shlink = data[0]                
         emb = disnake.Embed(title = "Shiny Hunt",description='_You can select a specific pokemon to shiny hunt and on each catch your chance will increase of catching a shiny pokemon_',color=0xFFDF00)
         emb.add_field(name="__**CURRENTLY HUNTING**__",value=hunt[0],inline=False)
         emb.add_field(name = "__**CURRENT CHAIN**__",value = hunt[1])
         emb.set_thumbnail(url=shlink)
      await ctx.send(embed = emb)
    else:
      arg = ' '.join(arg)
      data = redeem(arg,by = True)
      if data == None:
        await ctx.send("<:Pz_redx:873247207124508742> **You cannot shinyhunt an invalid pokemon**")
        return
      pkname = data[1]
      if await setsh(ctx.author.id,pkname):
        
        await ctx.send("<:Pz_Green_tick:873247568870662184> **Your shinyhunt has been succesfully set to "+pkname+'**')

  @commands.command(aliases=["pf","PF","Pf","pF","Profile"])
  async def profile(self,ctx):
   ids = ctx.author.id
   if await checkExist(ids):
     alls = await asyncio.gather(getbal(ids),getredeem(ids),getshard(ids),getcat(ids),getrel(ids),getshiny(ids),getstart(ids))
     amt = alls[0]
     rdm = alls[1]
     srd = alls[2]
     catc = alls[3]
     rela = alls[4]
     shs = alls[5]
     tim = alls[6]
     data = await infoc(ctx.author.id)
     if data == False or data == None :
       data = {'lvl':'None','name':''}
     else:
       data['lvl'] ='Level '+str(data['lvl'])  
     data2 = await lates(ctx.author.id)
     if data2 == False:
       data2 = {'ids':0}
     embed = disnake.Embed(description=f"<:ZC:876805945718611970>  **Balance**: ` {amt} Zc`""\n "f"<:Pz_redeem:876713271669968976>  **Redeems**: ` {rdm} `""\n"
      f"<:shards:876693844639490058>  **Shards**: ` {srd} `" "\n"
      f"<a:PokeBall:873523507210895382>  **Total Pokemons**: ` {str(data2['ids'])} `" "\n"f"<:poke_ball:873456060327940146>  **Pokemons Caught**: ` {catc} ` ""\n"f"<a:Pz_star:891332082440208487>  **Shinies Caught**: ` {shs} ` ""\n"f"<a:pokeball:877297877414731896>  **Pokemon Released**: ` {rela} ` ""\n"f"<a:pokemon_dance:873522276161683526>  **Selected Pokemon**: ` {str(data['lvl'])} {data['name']} ` ",color=0xFFDF00)
     embed.set_author(name=f"{ctx.author.name}'s Profile")
     embed.set_thumbnail(url=ctx.author.avatar.url)
     embed.set_footer(text='Started on ・ '+tim)
     await ctx.send(embed=embed)    

  @commands.command(aliases=["s","S"])
  async def select(self,ctx,arg):
    if not await checkExist(ctx.author.id):
      return
    if not arg.isdigit():
      await ctx.send("Invalid Input")
    else:
      if not await selector(ctx.author.id,int(arg)):
        await ctx.send("Number out of range")
      else:
        await ctx.send("Selected Pokemon changed successfully")

  


        
def setup(bot):
  bot.add_cog(Extension(bot))