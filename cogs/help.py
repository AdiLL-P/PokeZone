import disnake
from disnake.ext import commands
from User import getredeem

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx):
        embed = disnake.Embed(
            title='__HELP COMMAND__',
            description=
            'Type `P?help <page>` To get help about specific  command',
            color=0xFFDF00)
        embed.add_field(name='Page  1',
                        value='```Getting Started```\n',
                        inline=False)
        embed.add_field(name='Page  2',
                        value='```Information about Economy Commands```\n',
                        inline=False)
        embed.add_field(name='Page  3',
                        value='```Information about Gamble Commands```\n',
                        inline=False)
        embed.add_field(name='Page  4',
                        value='```Information about Trade Commands```\n',
                        inline=False)
        embed.add_field(name='Page  5',
                        value='```Information about Pokémon Commands```\n',
                        inline=False)
        embed.add_field(name='Page  6',
                        value='```Information about Shop Commands```\n',
                        inline=False)
        embed.add_field(name='Page  7', 
                        value='```Information about Configuration Commands```\n',
                        inline=False)
        embed.add_field(name='Page  8',
                        value='```Information about redeem commands```',inline=False)
        embed.add_field(name='Page  9',
                        value='```Bot Information```\n',
                        inline=False)
        embed.set_footer(text='Page (0/9)') 
        await ctx.send(embed=embed)

    @help.command(name='1')
    async def pg_one(self, ctx):
        embed = disnake.Embed(title='__GETTING STARTED__', color=0xFFDF00)
        embed.add_field(name='P?start',
                        value='_`Shows start menu`_',
                        inline=False)
        embed.add_field(name='P?pick',
                        value='_`Picks starter`_',
                        inline=False)
        embed.set_thumbnail(
            url=
            'https://th.bing.com/th/id/R.6a314da6fa865c54f3c9e3da79680ec4?rik=eoDW4FsDeLaecg&riu=http%3a%2f%2fimg09.deviantart.net%2f2bb9%2fi%2f2016%2f150%2fa%2f5%2fpokemon_starters_by_quas_quas-da3q6fg.png&ehk=hEjmoSLiX3pPVbQTi9qxaGCDbGkLSH2XxsSrGYUKh2A%3d&risl=&pid=ImgRaw&r=0'
        )
        embed.set_footer(text='Page (1/8)') 
        await ctx.send(embed=embed)

    @help.command(name='2')
    async def pg_two(self, ctx):
        embed = disnake.Embed(title='__ECONOMY COMMANDS__', color=0xFFDF00)
        embed.add_field(name='P?balance',
                        value='_`Use this command to check Your Balance`_',
                        inline=False)
        embed.add_field(name='P?redeems',
                        value='_`Use this command to check Your Redeems`_',
                        inline=False)
        embed.add_field(name='P?shards',
                        value='_`Use this command to check Your Shards`_',
                        inline=False)
        embed.set_thumbnail(
            url=
            'https://cdn.dribbble.com/users/1055192/screenshots/3989257/gold_mbe_animation_fix.gif'
        )
        embed.set_footer(text='Page (2/8)') 
        await ctx.send(embed=embed)

    @help.command(name='3')
    async def pg_3(self, ctx):
        embed = disnake.Embed(title='__GAMBLE COMMANDS__', color=0xFFDF00)
        embed.add_field(
            name='P?bet',
            value=
            '_`This Command Bets a user amount of coin you mentioned.`_ \nFor eg. `P?bet <user> <amount>`',
            inline=False)
        embed.add_field(
            name='P?join',
            value=
            '_`This command joins you to a gamble which you have been invited.`_ \nFor eg. `P?join <gamble_id>`',
            inline=False)
        embed.add_field(
            name='P?coinflip',
            value=
            '_`Flips a coin and if you are lucky you can win amount of u have mentioned`_ \nFor eg. `P?coinflip <amount>`',
            inline=False)
        embed.set_footer(text='Page (3/8)') 
        await ctx.send(embed=embed)

    @help.command(name='4',aliases = ['trade'])
    async def pg_4(self, ctx):
        embed = disnake.Embed(
            title='__TRADE COMMANDS__', color=0xFFDF00
        ).add_field(
            name='P?trade',
            value=
            '_`Starts a Trade with the user you have mentioned`_\nFor eg. `P?t <user>`',
            inline=False
        ).add_field(
            name='P?add pokemon',
            value=
            "_`Add's a Pokémon to  trade.`_ \nFor eg. `P?add pokemon <pokemon number>`",
            inline=False
        ).add_field(
            name='P?add coin',
            value="_`Add's coins to trade`._ \nFor eg. `P?add coin <amount>`",
            inline=False
        ).add_field(
            name='P?add redeem',
            value="_`Add's redeem to trade`_. \nFor eg. `P?add redeem <amount>`",
            inline=False
        ).add_field(
            name='P?trade view',
            value=
            "_`Show's stats of the pokemon added in trade`_ \nFor eg. `P?trade view <id>`",
            inline=False
        ).add_field(
            name='P?trade cancel',
            value="_`Cancel's the trade`_. \nFor eg. `P?trade cancel`",
            inline=False
        ).add_field(
            name='P?trade confirm',
            value="_`Confirm's the trade`_ \nFor eg. `P?trade confirm`"
        ).set_thumbnail(
            url=
            'https://cdn.disnakeapp.com/attachments/853907239257899030/877087147113463858/ff68e32f-pilotgold.png'
        )
        embed.set_footer(text='Page (4/8)') 
        await ctx.send(embed=embed)

    @help.command(name='5')
    async def pg_five(self,ctx):
      embed=disnake.Embed(title='__POKEMON COMMANDS__',color=0xFFDF00)
      embed.add_field(name='P?catch',value='_`Catches a pokemon`_',inline=False)
      embed.add_field(name='P?pokedex',value='_`Gives Pokemon information from pokedex`_',inline=False)
      embed.add_field(name='P?hint',value='_`Gives some letter of spawned Pokemon name`_',inline=False)     
      embed.add_field(name='P?info',value="_`Gives information about selected pokemon and it's statistic`_",inline=False)
      embed.add_field(name='P?info latest',value='_`Gives information and statistic of latest caught pokemon`_',inline=False)
      embed.add_field(name='P?select',value='_`Selects a Pokemon from your caught pokemons`_',inline=False)
      embed.add_field(name='P?shinyhunt',value="_`Start's shiny hunt of Pokémon of your choice`_",inline = False)
      embed.add_field(name ='P?leaderboard',value = "_`Shows top 10 users with highest things`_ \n For eg `P?lb <lbtype>`")
      embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/853907239257899030/877127930789126154/POKEZONE_1.png')
      embed.set_footer(text='Page (5/8)') 
      await ctx.send(embed=embed)
      
    @help.command(name='6')
    async def pg_six(self,ctx):
      embed=disnake.Embed(title='__SHOP COMMANDS__',color=0xFFDF00)
      embed.add_field(name='P?shop',value="_`Show's shop's all category`_",inline=False)
      embed.add_field(name='P?buy',value='_`You can buy things from shop with this command`_')
      embed.set_footer(text='Page (6/8)') 
      await ctx.send(embed=embed)

    @help.command(name='7')
    async def pg_seven(self,ctx):
      embed=disnake.Embed(title=f'__POKEZONE CONFIGURATION__',color=0xFFDF00)
      embed.add_field(name='P?disable spawn',value='_`Disables the spawn in  that specific channel`_',inline=False)
      embed.add_field(name='P?enable spawn',value='_`Enables the spawn in disabled spawn channel`_',inline = False)
      embed.add_field(name = 'P?setprefix',value = '_`Sets the bot prefix for you server`_\nFor eg. `P?setprefix <prefix_1> <prefix_2>`')
      embed.set_footer(text='Page (7/8)')
      await ctx.send(embed=embed)
    #  

    @help.command(name='9')
    async def pg_eight(self,ctx):
      embed = disnake.Embed(title='__BOT INFORMATION__',color=0xFFDF00)
      embed.add_field(name='DEFAULT PREFIX',value='`P?`',inline=False)
      embed.add_field(name='SUPPORT SERVER',value='_[CLICK HERE]() To Join Support server_',inline=False)
      
      embed.add_field(name='INVITE POKEZONE',value='*[CLICK HERE]() To invite me*',inline=False)
      embed.add_field(name='P?stats',value="_`Show's bot statistic`_",inline=False)
      embed.add_field(name= 'Report Bugs',value= "_`p?reportbug (information)`_")
      embed.set_footer(text='Page (9/9)')
      await ctx.send(embed=embed)
    
    @help.command(name='8',aliases = ['redeem'])
    async def redeem(self,ctx):
      rdm = await getredeem(ctx.author.id)
      embed = disnake.Embed(title=f'Your Redeems: {rdm}', color=0xFFDF00)
      embed.add_field(name='P?redeem <pokemon>',
                    value='_`Uses Your Redeem To Get Pokemon Of Your Choice`_',inline = False)
      embed.add_field(
        name='P?redeem spawn <Pokemon>',
        value='_`Uses Your Redeem To Spawn a Pokemon of your choice`_',inline = False)
      embed.add_field(
        name='P?redeem spawn coin',
        value=
        '_`Uses your redeem and spawn coin which will give you coins between 1-100,000 ZC`_'
      )
      embed.set_footer(text='Page (8/9)')
      await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot)) 
