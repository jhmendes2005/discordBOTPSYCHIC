import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from NewFunctionsPYC import CommandPrefix, prefixContext
from discord import slash_command, option

from kiwify_integration.consultas import consultas_kiwify
from ticketBOT.dropdowns.dropdown_verify import TicketsControl
from discord.ui import View


class AdminsCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @commands.has_guild_permissions(administrator = True)
    @slash_command(name="clear", description="Limpa do chat")
    @option(name="qnt", description="Escolha a quantidade de mensagens a serem deletadas")
    @option(name="embed", description="Escolha se é embed ou não", choices=[True, False])
    async def clear_function(self, ctx: prefixContext, qnt: int, embed: bool = False):
        if qnt > 100:
            return await ctx.reply("A quantidade de mensagens não pode ser maior que 100")
        if qnt <= 0:
            return await ctx.reply("A quantidade de mensagens não pode ser menor que 0")
        
        if embed == True:
            msgclear = await ctx.channel.purge(limit=int(qnt))

            e = discord.Embed(
                title="Mensagens deletadas",
                description=f"{len(msgclear)} mensagens foram deletadas deste canal!",
                color=discord.Color.red()
            )
            e.set_footer(text=f"Autor: {ctx.author.name}")

            await ctx.reply(embed=e)
        else:
            msgclear = await ctx.channel.purge(limit=int(qnt))
            await ctx.reply(f"{len(msgclear)} mensagens foram deletadas deste canal por: {ctx.author.name}!")

    @commands.has_guild_permissions(administrator = True)
    @slash_command(name="consultar", description="Consultar dados de aluno")
    @option(name="aluno", description="Mencione o @ do aluno.")
    @option(name="tipo", description="Consulta simplificada ou completa?", choices=[True, False])
    async def consultar(self, ctx: prefixContext, aluno: str, tipo: bool = False):
        consultar = consultas_kiwify.Consulta()
        consult = consultar.order(aluno)
        await ctx.reply(consult)

    @commands.has_guild_permissions(administrator=True)
    @slash_command(name="lock", description="Trava o canal selecionado")
    async def lock(self, interaction: discord.Interaction):
        channel = interaction.channel
        if channel.permissions_for(channel.guild.default_role).send_messages is False:
            await interaction.response.send_message("O canal já está bloqueado.", ephemeral=True)
        else:
            await channel.set_permissions(channel.guild.default_role, send_messages=False)
            await interaction.response.send_message("Canal bloqueado com sucesso!", ephemeral=True)

    @commands.has_guild_permissions(administrator=True)
    @slash_command(name="unlock", description="Destrava o canal selecionado")
    async def unlock(self, interaction: discord.Interaction):
        channel = interaction.channel
        if channel.permissions_for(channel.guild.default_role).send_messages is True:
            await interaction.response.send_message("O canal já está desbloqueado.", ephemeral=True)
        else:
            await channel.set_permissions(channel.guild.default_role, send_messages=True)
            await interaction.response.send_message("Canal destravado com sucesso!", ephemeral=True)
            
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para usar este comando.")

    @commands.has_guild_permissions(administrator=True)
    @slash_command(name="closeticket", description="Fechar ticket aberto")
    async def closeticket(self, interaction: discord.Interaction):
        channel_id = interaction.channel.id
        close = TicketsControl()
        try:
            # Supondo que close_ticket() retorna True se o ticket foi fechado com sucesso
            if close.close_ticket(channel_id):
                channel = self.bot.get_channel(channel_id)  # Correção aqui
                if channel:
                    await channel.delete()
                    await interaction.response.send_message("Ticket encerrado e canal excluído com sucesso!", ephemeral=True)
                else:
                    await interaction.response.send_message("Não foi possível encontrar o canal associado ao ticket.", ephemeral=True)
            else:
                await interaction.response.send_message("O ticket já está fechado ou não existe.", ephemeral=True)
        except Exception as e:
            print(f"Erro ao fechar o ticket: {e}")
            await interaction.response.send_message("Não foi possível encerrar este ticket...", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(AdminsCommands(bot))