from disnake.ext import commands
from datetime import datetime
import disnake
import asyncio
from User import checkExist, getbal, setbal, getredeem, setredeem, infonum, pkremove, pokeadder, gapfiller


class trinfo():
    def __init__(self, channel, embmsg, id1, id2):
        self.id1 = id1
        self.id2 = id2
        self.channel = channel
        self.embmsg = embmsg
        self.ids = {
            str(id1): {
                'cr': 0,
                'rd': 0,
                'pk': {},
                'confirmed': False
            },
            str(id2): {
                'cr': 0,
                'rd': 0,
                'pk': {},
                'confirmed': False
            }
        }


class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trades = {}

    def start_trade(self, chanid, embmsg, id1, id2):
        lctrade = trinfo(chanid, embmsg, id1, id2)
        self.trades[id1] = lctrade
        self.trades[id2] = lctrade

    async def sub(self, data1, id1, data2, id2):
        def other(i):
            if i == id1:
                return id2
            else:
                return id1

        def his(i):
            if i == id1:
                return data1
            if i == id2:
                return data2

        for i in (id1, id2):
            dt = his(i)
            if dt['cr'] > 0:
                await setbal(i, -dt['cr'])
                await setbal(other(i), dt['cr'])
            if dt['rd'] > 0:
                await setredeem(i, -dt['rd'])
                await setredeem(other(i), dt['rd'])
            pksin = False
            for j in dt['pk'].values():
                pksin = True
                await pkremove(i, j['ids'])
                j['ids'] = -1
                await pokeadder(other(i), j)
            if pksin:
                await gapfiller(i)

    @commands.group(aliases=['t'], invoke_without_command=True)
    async def trade(self, ctx, arg):
        id1 = str(ctx.author.id)
        if not await checkExist(id1):
            await ctx.send("You should be a member of the bot . Try p?start")
            return
        id2 = ''.join([i for i in arg if i.isdigit()])
        if not await checkExist(id2):
            await ctx.send("Mentioned person is not a member of bot")
            return
        if id1 in list(self.trades) or id2 in list(self.trades):
            await ctx.send("You are already in a trade")
            return
        if id1 == id2:
            await ctx.send("You cannot trade with yourself")
            return
        mem = ctx.guild.get_member(int(id2))
        if mem == None:
            await ctx.send(
                'Mentioned Person not found in the respective channel')
            return
        if not ctx.channel.permissions_for(mem).send_messages:
            await ctx.send(
                'Mentioned Person has no permissions to send messages in this channel '
            )
            return
        mess = await ctx.send(
            f'<@{id2}> **you have been invited to trade by {ctx.author.name}**\n _you have 60 seconds to accept the trade_ <a:1min:875423768078606406>'
        )
        await mess.add_reaction('<:Pz_Green_tick:873247568870662184>')
        await mess.add_reaction('<:redx:873247207124508742>')

        def check(reaction, user):
            emoji = str(reaction.emoji)
            return user.id == int(id2) and (
                emoji == '<:Pz_Green_tick:873247568870662184>'
                or emoji == '<:Pz_redx:873247207124508742>')

        try:
            reaction, user = await self.bot.wait_for('reaction_add',
                                                     timeout=60.0,
                                                     check=check)
            if str(reaction.emoji) == '<:Pz_Green_tick:873247568870662184>':
                if user.id in list(self.trades):
                    await ctx.send("You are already in a trade")
                    return
                embed = disnake.Embed(
                    title=f'Trade between {ctx.author.name} and {mem.name}!',
                    description=
                    'If you want help regarding Trade Commands `TYPE P?help 4`',
                    color=0xFFDF00)
                embed.add_field(name=f'{ctx.author.name} is offering',
                                value='```\n ```',
                                inline=False)
                embed.add_field(name=f'{mem.name} is offering',
                                value='```\n ```')
                embmsg = await ctx.send(embed=embed)
                self.start_trade(ctx.channel.id, embmsg, id1, id2)
            elif str(reaction.emoji) == '<:Pz_redx:873247207124508742>':
                await ctx.send("Trade request has been rejected by " +
                               mem.name)
                await mess.delete()
        except asyncio.TimeoutError:
            await ctx.send("Trade request Timed out")
            await mess.delete()

    @commands.command(aliases=['a', 'addy', 'A', 'Add'])
    async def add(self, ctx, what, arg):
        id = str(ctx.author.id)
        if not id in self.trades:
            await ctx.send("You are not in a trade")
            return
        if not arg.isdigit():
            await ctx.send("Amount muse be in integers")
            return
        if ctx.channel.id != self.trades[id].channel:
            await ctx.send(
                "You must be in the same channel to add pokes in the trade")
            return
        if int(arg) <= 0:
            await ctx.send("Amount cannot be less than 0")
        if what == 'coin' or what == 'zc':
            amt = int(arg) + self.trades[id].ids[id]['cr']
            if await getbal(id) < amt:
                await ctx.send("You dont have that many coins ")
                return
            self.trades[id].ids[id]['cr'] += int(arg)
        elif what == 'redeem' or what == 'r':
            amt = int(arg) + self.trades[id].ids[id]['rd']
            if await getredeem(id) < amt:
                await ctx.send("You dont have that many redeems ")
                return
            self.trades[id].ids[id]['rd'] += int(arg)
        elif what == 'pokemon' or what == 'pk':
            pk = await infonum(id, arg)
            if pk == False:
                await ctx.send("You dont have any pokemon at that number")
                return
            if self.trades[id].ids[id]['pk'] == {}:
                self.trades[id].ids[id]['pk']['1'] = pk
            else:
                for i in self.trades[id].ids[id]['pk'].items():
                    if i[1]['ids'] == pk['ids']:
                        await ctx.send(
                            "You have already added that pokemon to the trade")
                        return
                val = list(self.trades[id].ids[id]['pk'])[-1]
                val = int(val) + 1
                self.trades[id].ids[id]['pk'][str(val)] = pk
        else:
            return
        await ctx.message.delete()
        id1 = self.trades[id].id1
        id2 = self.trades[id].id2
        self.trades[id].ids[id1]['confirmed'] = False
        self.trades[id].ids[id2]['confirmed'] = False
        name1 = ctx.guild.get_member(int(id1)).name
        name2 = ctx.guild.get_member(int(id2)).name
        embed = disnake.Embed(
            title=f'Trade between {name1} and {name2}!',
            description=
            'If you want help regarding Trade Commands `TYPE P?help 4`',
            color=0xFFDF00)
        values1 = ''
        values2 = ''
        for i in list(self.trades[id].ids[id1].items()):
            if i[0] == 'cr':
                if i[1] != 0:
                    values1 += "Coins: " + str(i[1])
                    values1 += '\n'
            if i[0] == 'rd':
                if i[1] != 0:
                    values1 += 'Redeems: ' + str(i[1])
                    values1 += '\n'
            if i[0] == 'pk':
                if i[1] != {}:
                    for j in i[1].items():
                        values1 += j[0] + ' | ' + j[1]['name']
                        values1 += '\n'
        for i in list(self.trades[id].ids[id2].items()):
            if i[0] == 'cr':
                if i[1] != 0:
                    values2 += "Coins: " + str(i[1])
                    values2 += '\n'
            if i[0] == 'rd':
                if i[1] != 0:
                    values2 += 'Redeems: ' + str(i[1])
                    values2 += '\n'
            if i[0] == 'pk':
                if i[1] != {}:
                    for j in i[1].items():
                        values2 += j[0] + ' | ' + j[1]['name']
                        values2 += '\n'
        embed.add_field(name=f'{name1} is offering',
                        value=f'```\n{values1} ```',
                        inline=False)

        embed.add_field(name=f'{name2} is offering',
                        value=f'```\n{values2} ```')
        embmsg = self.trades[id].embmsg
        await embmsg.edit(embed=embed)

    @commands.command()
    async def remove(self, ctx, what, arg):
        id = str(ctx.author.id)
        if not id in self.trades:
            await ctx.send("You are not in a trade")
            return
        if not arg.isdigit():
            await ctx.send("Amount muse be in integers")
            return
        if ctx.channel.id != self.trades[id].channel:
            await ctx.send(
                "You must be in the same channel to add items in the trade")
            return
        if int(arg) <= 0:
            await ctx.send("Amount cannot be less than 0")
        if what == 'coin' or what == 'zc':
            if self.trades[id].ids[id]['cr'] < int(arg):
                await ctx.send("You cannot remove more coins ")
                return
            self.trades[id].ids[id]['cr'] -= int(arg)
        elif what == 'redeem' or what == 'r':
            if self.trades[id].ids[id]['rd'] < int(arg):
                await ctx.send("You cannot remove more redeems")
                return
            self.trades[id].ids[id]['rd'] -= int(arg)
        elif what == 'pokemon' or what == 'pk':
            numbers = list(self.trades[id].ids[id]['pk'])
            if not arg in numbers:
                return
            self.trades[id].ids[id]['pk'].pop(arg)
            change = 1
            prev = 0
            for i in sorted(list(self.trades[id].ids[id]['pk'])):
                change = int(i) - prev
                if change == 1:
                    prev = int(i)
                else:
                    prev = int(i) - change + 1
                    pkinfo = self.trades[id].ids[id]['pk'].get(i)
                    self.trades[id].ids[id]['pk'].pop(i)
                    lf = int(i) - change + 1
                    self.trades[id].ids[id]['pk'][str(lf)] = pkinfo
        else:
            return
        await ctx.message.delete()
        id1 = self.trades[id].id1
        id2 = self.trades[id].id2
        self.trades[id].ids[id1]['confirmed'] = False
        self.trades[id].ids[id2]['confirmed'] = False
        name1 = ctx.guild.get_member(int(id1)).name
        name2 = ctx.guild.get_member(int(id2)).name
        embed = disnake.Embed(
            title=f'Trade between {name1} and {name2}!',
            description=
            'If you want help regarding Trade Commands type `P?help 4`',
            color=0xFFDF00)
        values1 = ''
        values2 = ''
        for i in list(self.trades[id].ids[id1].items()):
            if i[0] == 'cr':
                if i[1] != 0:
                    values1 += "Coins: " + str(i[1])
                    values1 += '\n'
            if i[0] == 'rd':
                if i[1] != 0:
                    values1 += 'Redeems: ' + str(i[1])
                    values1 += '\n'
            if i[0] == 'pk':
                if i[1] != {}:
                    for j in i[1].items():
                        values1 += j[0] + ' | ' + j[1]['name']
                        values1 += '\n'
        for i in list(self.trades[id].ids[id2].items()):
            if i[0] == 'cr':
                if i[1] != 0:
                    values2 += "Coins: " + str(i[1])
                    values2 += '\n'
            if i[0] == 'rd':
                if i[1] != 0:
                    values2 += 'Redeems: ' + str(i[1])
                    values2 += '\n'
            if i[0] == 'pk':
                if i[1] != {}:
                    for j in i[1].items():
                        values2 += j[0] + ' | ' + j[1]['name']
                        values2 += '\n'
        embed.add_field(name=f'{name1} is offering',
                        value=f'```\n{values1} ```',
                        inline=False)

        embed.add_field(name=f'{name2} is offering',
                        value=f'```\n{values2} ```')
        embmsg = self.trades[id].embmsg
        await embmsg.edit(embed=embed)

    @trade.command(aliases=['decline'])
    async def cancel(self, ctx):
        if str(ctx.author.id) in list(self.trades):
            trade = self.trades.get(str(ctx.author.id))
            if trade.channel != ctx.channel.id:
                await ctx.send(
                    "You should be in the same channel to cancel the trade")
                return
            self.trades.pop(trade.id1)
            self.trades.pop(trade.id2)
            await trade.embmsg.edit(
                content="This trade has been cancelled by " + ctx.author.name,
                embed=None)
            await ctx.send(f"{ctx.author.mention} cancelled the trade! ")
        else:
            await ctx.send("You are already not in a trade !")

    @trade.command(aliases=['v'])
    async def view(self, ctx, arg):
        id = str(ctx.author.id)
        if id in list(self.trades):
            trade = self.trades.get(id)
            if trade.channel != ctx.channel.id:
                await ctx.send(
                    "You should be in the same channel to view items")
                return
            if not arg.isdigit():
                await ctx.send("Arguments must be in numbers")
            id1 = self.trades[id].id1
            id2 = self.trades[id].id2
            if id == id1:
                data = self.trades[id].ids[id2]['pk'].get(arg)
            elif id == id2:
                data = self.trades[id].ids[id1]['pk'].get(arg)
            if data == None:
                await ctx.send(
                    "No pokemons were found in the trade at that number")
                return
            else:
                embed = disnake.Embed(
                    title="Level " + str(data['lvl']) + " " + data['name'],
                    color=disnake.Colour.green())  #str(data['ids'])
                stats = '**Types**: ' + data['typ'] + '\n**HP**:' + str(
                    data['hp']) + '    **IV:**' + str(
                        data['hpiv']) + '/31\n' + '**Attack**:' + str(
                            data['atk']) + '    **IV**:' + str(
                                data['atkiv']
                            ) + '/31\n' + '**Defense**:' + str(
                                data['defen']) + '    **IV**:' + str(
                                    data['defiv']
                                ) + '/31\n' + '**Sp.Atk**:' + str(
                                    data['spatk']) + '    **IV**:' + str(
                                        data['spatkiv']
                                    ) + '/31\n' + '**Sp.Def**:' + str(
                                        data['spdef']) + '    **IV**:' + str(
                                            data['spdefiv']
                                        ) + '/31\n' + '**Speed**:' + str(
                                            data['speed']
                                        ) + '    **IV**:' + str(
                                            data['speediv']
                                        ) + '/31' '\n**Total IV**: ' + str(
                                            data['totiv']) + "%"
                embed.add_field(name="Nature", value=data['nature'])
                embed.add_field(name="Stats", value=stats, inline=False)
                embed.set_image(url=data['link'])
                await ctx.send(embed=embed)
        else:
            await ctx.send("You are not in a trade !")

    @trade.command(aliases=['c'])
    async def confirm(self, ctx):
        id = str(ctx.author.id)
        if id in list(self.trades):
            trade = self.trades.get(id)
            if trade.channel != ctx.channel.id:
                await ctx.send(
                    "You should be in the same channel to confirm the trade")
                return
            c1con = False
            trade = self.trades[id]
            id1 = trade.id1
            id2 = trade.id2
            for i in list(trade.ids[trade.id1].items()):
                if i[0] == 'cr':
                    if i[1] != 0:
                        c1con = True
                if i[0] == 'rd':
                    if i[1] != 0:
                        c1con = True
                if i[0] == 'pk':
                    if i[1] != {}:
                        c1con = True
            for i in list(trade.ids[trade.id2].items()):
                if i[0] == 'cr':
                    if i[1] != 0:
                        c1con = True
                if i[0] == 'rd':
                    if i[1] != 0:
                        c1con = True
                if i[0] == 'pk':
                    if i[1] != {}:
                        c1con = True
            if not c1con:
                await ctx.send("You cannot confirm an empty trade")
                return
            elif not trade.ids[id]['confirmed']:
                trade.ids[id]['confirmed'] = True
                embmsg = trade.embmsg
                embed = embmsg.embeds
                embed = embed[0]
                if id == trade.id1:
                    index = 0
                elif id == trade.id2:
                    index = 1
                fields = embed.fields
                field = fields[index]
                name = field.name + ' ✅'
                value = field.value
                embed.remove_field(index)
                embed.insert_field_at(index,
                                      name=name,
                                      value=value,
                                      inline=False)
                await embmsg.edit(embed=embed)
                await ctx.send("Trade has been confirmed by " +
                               ctx.author.name + '!')
            if trade.ids[id1]['confirmed'] and trade.ids[id2]['confirmed']:
                data1 = trade.ids[id1]
                data2 = trade.ids[id2]
                embmsg = trade.embmsg
                embed = embmsg.embeds
                embed = embed[0]
                now = datetime.now()
                dtinfo = now.strftime("%d/%m/%Y ・ %H:%M:%S ・ ")
                dtinfo += f"{ctx.guild.name}"
                embed.set_footer(text=dtinfo)
                chan = self.bot.get_channel(877472150410375198)
                self.trades.pop(id1)
                self.trades.pop(id2)
                mess = await ctx.send(
                    "Processing your trade <a:Pz_loading:891004070456868864> ")
                await self.sub(data1, id1, data2, id2)
                await mess.edit(
                    content=
                    "<a:Animated_CheckMark:864742879801114624> Trade has been confirmed !"
                )
                await chan.send(embed=embed)
        else:
            await ctx.send("You are not in trade")


def setup(bot):
    bot.add_cog(Trading(bot))
