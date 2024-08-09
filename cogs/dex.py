from disnake.ext import commands
from User import mydex
from poke import byId
import disnake
import copy

class Page(disnake.ui.View):
    def __init__(self,content,count:int,author):
        super().__init__(timeout=60)
        self.count = count
        self.author = author
        self.msg = None
        self.content = content
        self.colour = None

    @disnake.ui.button(style=disnake.ButtonStyle.primary,emoji='<a:Pz_left_arrow:891006674461155328>')
    async def left(self,button,interaction):
        if interaction.user.id !=self.author:
          await interaction.response.send_message("This is not your dex!",ephemeral = True)
        if self.count<=20:
            return
        rem = self.count%20
        rem = rem if rem!=0 else 20
        lc = self.content[self.count-rem-20:self.count-rem]
        c = self.count-19-rem
        self.count-=rem
        em = self.msg.embeds[0]
        em.clear_fields()
        for i in lc:
            em.add_field(name=f'#{i[0]} {i[1][0]}',value = '<:Pz_redx:873247207124508742> Not yet caught !' if i[1][1]==0 else '<:Pz_Green_tick:873247568870662184> '+str(i[1][1])+' caught !')
        await self.msg.edit(embed= em,view = self)

    @disnake.ui.button(style=disnake.ButtonStyle.primary,emoji='<a:Pz_right_arrow:891006842732429323>')
    async def right(self,button,interaction:disnake.Interaction):
        if interaction.user.id != self.author:
          await interaction.response.send_message("This is not your dex!",ephemeral = True)
        c = self.count+1
        lc = self.content[c-1:c+19]
        if lc == []:
            await interaction.response.send_message("Dex Over !Khatam Tata bye-bye !",ephemeral=True)
            return
        self.count+=len(lc)
        em = self.msg.embeds[0]
        em.clear_fields()
        for i in lc:
            em.add_field(name=f'#{i[0]} {i[1][0]}',value = '<:Pz_redx:873247207124508742> Not yet caught !' if i[1][1]==0 else '<:Pz_Green_tick:873247568870662184> '+str(i[1][1])+' caught !')
        await self.msg.edit(embed= em,view = self)

    async def on_timeout(self):
        for i in self.children:
            i.disabled = True
        await self.msg.edit(view = self)


class Dex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      cache = {}
      for i in range(1,899):
        i = str(i) 
        cache[str(i)] = [byId(i,by=True),0]
      self.cache = cache
   
    async def ok(self,author,channel):
      data = await mydex(author.id)
      myd= copy.deepcopy(self.cache)
      c = 0
      for i in data.keys():
        if int(i)>898:
          c+=1
        else:
          myd[i][1] = data[i]
      myd = list(myd.items())
      lol = myd[0:20]
      vi = Page(myd,20,author.id)
      embed  = disnake.Embed(title = 'Your Pokédex',
                     description = f'you have caught {len(data.keys())-c} out of 898 pokemons',color=0xffdf00)
      for i in lol:
        embed.add_field(name=f'#{i[0]} {i[1][0]}',value = '<:Pz_redx:873247207124508742> Not yet caught !' if i[1][1]==0 else '<:Pz_Green_tick:873247568870662184> '+str(i[1][1])+' caught !')
        
      msg = await channel.send(embed = embed)
      await msg.edit(view = vi)
      vi.msg = msg 



def setup(bot):
    bot.add_cog(Dex(bot)) 