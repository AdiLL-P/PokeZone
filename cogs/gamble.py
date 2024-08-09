import random
from disnake.ext import commands
from User import getbal,setbal,checkExist
import asyncio
class gam():
    def __init__(self,gid,chid,id1,id2,amount,whose) -> None:
        self.gid = gid
        self.chid = chid
        self.amount = amount
        self.id1 = str(id1)
        self.id2 = str(id2)
        self.id1b = False
        self.id2b = False
        self.id1bo = False
        self.id2bo = False
        print('gid = '+gid)
        print('id1 ='  +self.id1)
        print('id2 ='  +self.id2)
        pre = random.choices([self.id1,self.id2,self.id1,self.id2],weights=[1,1,1,1],k=40)
        while True:
          pre1 = random.choice(pre)
          pre2 = random.randint(1,10)
          if pre1 == self.id1  and pre2>5:
            self.winner = self.id1
            break
          elif pre1 ==self.id2 and pre2<=5:
            self.winner = self.id2 
            break
        print('winner = '+self.winner)
        self.whose = whose
        if self.winner == self.id1:
          self.looser = self.id2
        else:
          self.looser = self.id1
        print('looser = '+self.looser)
    def joined(self,id):
        id = str(id)
        if id == self.id1:
            if self.id1b ==False:
                self.id1bo = True
            self.id1b = True
        elif id == self.id2:
            if self.id2b ==False:
                self.id2bo = True
            self.id2b = True
        if self.id1b and self.id2b :
            return True
        else: return False
    def getOnce(self,id):
        id = str(id)
        if id == self.id1:
           if self.id1bo :
               temp = self.id1bo
               self.id1bo = not self.id1bo
               return temp
           else: return False
        elif id == self.id2:
            if self.id2bo:
                temp = self.id2bo
                self.id2bo = not self.id2bo
                return temp
            else: return False
        else: return False
class Gambling(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.gID = {}
        self.haveID = {}
        self.timers = {}
    async def generate(self): 
        temp = None
        for i in range(1,1000):
            if str(i) not in self.gID:
               temp = i
               break
        return str(temp) 
    async def timeout(self,ctx,val):
        await asyncio.sleep(120)
        if val in self.gID:
           self.gID.pop(val)
           self.haveID[ctx.channel.id]-=1
           await ctx.send("Time Out for gambling id : "+str(val))
    async def release(self,val):
        self.gID.pop(val)

    @commands.command(aliases =['gamble'])
    async def bet(self,ctx,arg1,arg2):
        chid = ctx.channel.id
        id1 = str(ctx.author.id)
        id2 = ''.join([i for i in arg1 if i.isdigit()])
        amount = None
        pas = False
        if not await checkExist(id1):
            await ctx.send("You still need to start your journey")
        elif not await checkExist(id2):
            await ctx.send("Mention User is not a member of <@832266727022395402> bot")
        elif id1 ==id2:
            await ctx.send(ctx.author.mention+" You can't gamble with yourself")
        elif not arg2.isdigit():
            await ctx.send("Amount should be in integer")
        else:
            amount = int(arg2)    
            pas = True
        if not pas:
            return
        elif amount<=0:
            await ctx.send("Amount should be positive")
        elif await getbal(id1)<amount:
            await ctx.send("You dont have enough coins to gamble")
        elif await getbal(id2)<amount:
            await ctx.send("Mentioned Person doesn't have enough coins to gamble")
        else:
            amount = int(arg2)
            temp = await self.generate()
            self.gID[temp] = gam(temp,chid,id1,id2,amount,ctx.author.display_name)
            if self.haveID.get(chid) == None:
                self.haveID[chid] = 1
            else:
                self.haveID[chid]+=1
            await ctx.send("<@"+id2+"> You have been invited to gamble by "+ctx.author.display_name+" Type `P?join "+temp+"`")
            t1 = asyncio.create_task(self.timeout(ctx,temp))
            self.timers[temp] = t1
    @commands.command(aliases = ['Join'])
    async def join(self,ctx,arg):
        if not await checkExist(ctx.author.id):
            return
        if ctx.channel.id not in self.haveID:
            return
        if arg not in self.gID:
            await ctx.send("Invalid gamble id")
            return
        elif self.gID.get(arg).chid != ctx.channel.id:
            await ctx.send("Invalid gamble id")
            return
        elif await getbal(ctx.author.id)<self.gID[arg].amount:
            await self.release(arg)
            self.timers[arg].cancel()
            self.timers.pop(arg)
            self.haveID[ctx.channel.id]+=-1
            if self.haveID[ctx.channel.id] == 0:
                self.haveID.pop(ctx.channel.id)
            await ctx.send(ctx.author.mention+" You dont have enough coins")
        elif self.gID[arg].joined(ctx.author.id):
                if await getbal(self.gID[arg].id1)<self.gID[arg].amount and await getbal(self.gId[arg].id2)<self.gID[arg].amount:
                  await ctx.send("Person you are gambling with has less coins")
                  await self.release(arg)
                  self.timers[arg].cancel()
                  self.timers.pop(arg)
                  self.haveID[ctx.channel.id]+=-1
                  if self.haveID[ctx.channel.id] == 0:
                      self.haveID.pop(ctx.channel.id)
                  return
                t1 = setbal(self.gID[arg].winner,self.gID[arg].amount)
                t2 = setbal(self.gID[arg].looser,-self.gID[arg].amount)
                await asyncio.gather(t1,t2)
                await ctx.send("<@"+self.gID[arg].winner+"> You have won "+str(self.gID[arg].amount) +" coins")
                await self.release(arg)
                self.timers[arg].cancel()
                self.timers.pop(arg)
                self.haveID[ctx.channel.id]+=-1
                if self.haveID[ctx.channel.id] == 0:
                    self.haveID.pop(ctx.channel.id)
        elif self.gID[arg].getOnce(ctx.author.id) :
            await ctx.send("You have joined "+self.gID[arg].whose+" gamble")
        elif self.gID[arg].getOnce(ctx.author.id) :
            await ctx.send("You have joined "+self.gID[arg].whose+' gamble')
    @commands.cooldown(rate = 1,per = 4.0 ,type = commands.BucketType.user)#lets start dex or market 
    @commands.command(aliases=['cf','coinflip'])
    async def CF(self,ctx,arg):
      if arg.isdigit():
       lol =  int(arg)/6000
       lol =int(lol)
      else :
       lol  = 6
      pre = random.choices([True,False],weights=[40,random.randint(40,55+lol)],k= 100)
      wilo = random.choice(pre)
      mess = await ctx.send('Flipping Coin <a:Coinflip3:879628115473760276>')
      lcbal = await getbal(ctx.author.id)
      if arg.isdigit() and lcbal>=int(arg):
        if int(arg) > 30000:
          await mess.delete()
          await ctx.send('Oof ! The amount is too high')
          return
        arg = int(arg)
        if wilo:
          await setbal(ctx.author.id,arg)
          await mess.edit(content = f'** <:Pz_Green_tick:873247568870662184> Congratulations {ctx.author.mention} You have won '+str(arg)+' coins!**')
        else:
          await setbal(ctx.author.id,-arg)
          await mess.edit(content = f'**<:Pz_redx:873247207124508742> {ctx.author.mention}'+ 'You have lost '+str(arg)+' coins!**')
      elif arg.lower() == 'all':
        bal = await getbal(ctx.author.id)
        if bal ==0:
          await mess.delete()
          await ctx.send("You dont have enough bal! ")
          return
        if bal>=50000:
          bal = 50000
        if wilo:
          await setbal(ctx.author.id,bal)
          await mess.edit(content = f'**<:Pz_Green_tick:873247568870662184> Congratulations {ctx.author.mention}' + 'You have won '+str(bal)+' coins!**')
        else:
          await setbal(ctx.author.id,-bal)
          await mess.edit(content = f'**<:Pz_redx:873247207124508742> {ctx.author.mention}'+ 'You have lost '+str(bal)+' coins!**')
      else:
        await mess.delete()
        await ctx.send("You dont have enough bal to coinflip")
    @CF.error
    async def lol(self,ctx,error):
      if isinstance(error,commands.CommandOnCooldown):
        await ctx.send(f"Please wait for {round(error.retry_after,2)} seconds")
def setup(bot):
    bot.add_cog(Gambling(bot))