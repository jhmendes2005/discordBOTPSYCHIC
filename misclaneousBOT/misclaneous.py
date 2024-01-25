import discord
from discord.ext import commands
from NewFunctionsPYC import CommandPrefix, prefixContext
from discord import slash_command, option
import requests

from database.bonifications import BonificationsPoints

class MisclaneousCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    # @commands.has_guild_permissions(administrator = True)
    @slash_command(name="dollar", description="Cotação do Dólar hoje")
    async def dollar_function(self, ctx: prefixContext):
            req = requests.get('https://economia.awesomeapi.com.br/all/USD-BRL')
            cotacao = req.json()
            date = cotacao["USD"]["create_date"]
            value = cotacao["USD"]["bid"]
            e = discord.Embed(
                title=f"DÓLAR ATUALIZADO:",
                description=f"Data: {date}",
                color=discord.Color.red()
            )
            e.add_field(name="Valor:", value=f"R${value}", inline=False)
            e.set_author(name=f"Fonte: economia.awesomeapi.com.br", icon_url="https://indicadoreseconomicos.com.br/wp-content/uploads/2022/06/dolar12.png")
            e.set_thumbnail(url="https://1.bp.blogspot.com/-fEr-digD0X0/VR7ttB5YoEI/AAAAAAAADkg/yOOX3Il8fEQ/w1200-h630-p-k-no-nu/dollars.jpg")
            e.set_image(url="https://www.meusdicionarios.com.br/wp-content/uploads/2016/05/sh_bandeira-dos-eua_1056155741.jpg")
            e.set_footer(text="Developed by .jotazinn")
            await ctx.reply(embed=e)
            await ctx.author.send(embed=e)
    
    @slash_command(name="points", description="Confira seus pontos no servidor!")
    async def points(self, ctx: prefixContext):
            boni = BonificationsPoints()
            boni = boni.consultar_pontos(ctx.user.id)
            e = discord.Embed(
                title=f"PONTOS DE {ctx.user.name}",
                description=f"Confira seus pontos {ctx.user.mention}",
                color=discord.Color.red()
            )
            e.add_field(name="Pontos totais:", value=f"{boni}", inline=False)
            e.set_footer(text="Developed by .jotazinn")
            await ctx.reply(embed=e, ephemeral=True)
            await ctx.author.send(embed=e)

def setup(bot: commands.Bot):
    bot.add_cog(MisclaneousCommands(bot))