import discord
from discord.ext import commands
import datetime

class BugReport(commands.Cog):
    def __init__(self,Bot):
        self.Bot = Bot

    @commands.command()
    async def reportbug(self,ctx,*,message = None):
        if message==None:
            WARNembed=discord.Embed(title="**Error**",description=f"• **{ctx.message.author.mention}, Make sure you typed the command correctly!**\n• **Usage :** `m!reportbug <bug_message>`\n• **Example : `m!reportbug ping command is not working`**",colour=discord.Color.red())
            await ctx.send(embed=WARNembed)
            return
        else:
            channel = self.Bot.get_channel(852481236026785823)
            embed = discord.Embed(title="New Bug Report",description=f"🚨 {message}",colour=discord.Color.from_rgb(0,255,148),timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Sent by {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
            scembed = discord.Embed(title="Your Report Has Successfully Been Sent!",colour=discord.Color.from_rgb(0,255,148))
            await ctx.send(embed=scembed)
            await channel.send(embed=embed)
            await message.add_reaction("<a:Me_Animated_CheckMark:884316048432713748>")
            await message.add_reaction("<a:cross_animated:852110730409017355>")
            

def setup(Bot):
    Bot.add_cog(BugReport(Bot))