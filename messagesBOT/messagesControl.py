import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
from ticketBOT.dropdowns.dropdown_verify import DropDown1
from verificationBOT.dropdowns.dropdown_verify import Drop_down_verify
from discord.ui import View
from database.bonifications import BonificationsPoints
from database.insert_clientes_backup import BancoDados
from kiwify_integration.consultas.consultas_kiwify import Orders_extract
from socialMediaBOT.insta import InstagramNotifier
from socialMediaBOT.ytb_vids import YouTubeNotifier

class moderationEvents(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot = bot
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[LOG] - BOT ONLINE {self.bot.user}")
        self.update_status.start()
        self.update_activity.start()
        self.create_ticket.start()
        self.create_validation.start()
        self.top10_bonifications.start()
        self.process_users_30min.start()
        self.process_users_7days.start()
        self.process_newsletter.start()
        return True
    
    @tasks.loop(minutes=0.1)
    async def update_activity(self):
        status_list = [
            discord.Activity(type=discord.ActivityType.playing, name="Suporte online diáriamente.", url="https://psychicdesigner.com.br/"),
            discord.Activity(type=discord.ActivityType.watching, name="Aulas do nosso amigo Psychic.", url="https://psychicdesigner.com.br/"),
            discord.Activity(type=discord.ActivityType.listening, name="Ouvindo uma musiquinha relaxante.", url="https://psychicdesigner.com.br/"),
            discord.Activity(type=discord.ActivityType.streaming, name="Master Creator Sports JÁ DISPONÍVEL!", url="https://psychicdesigner.com.br/"),
        ]
        while True:
            for status in status_list:
                await self.bot.change_presence(activity=status)
                await asyncio.sleep(10)

    @tasks.loop(minutes=30)
    async def process_newsletter(self):
        channel = self.bot.get_channel(1199356523302883350)
        try:
            get_insta_post = InstagramNotifier()
            post_insta = get_insta_post.main_insta()
            if post_insta is not None:
                await channel.send(f"NOVO POST NO INSTAGRAM! @everyone \n\n{post_insta['Link do Post']}")
        except Exception as e:
            print("Erro ao tentar executar instagram Newsletter")
            print(f"Erro: {e}")

        try:
            get_ytb_vid = YouTubeNotifier()
            ytb_vid = get_ytb_vid.main_ytb()
            if ytb_vid is not None:
                await channel.send(f"NOVO VÍDEO NO YOUTUBE! @everyone \n\n{ytb_vid['Link do Vídeo']}")
        except Exception as e:
            print("Erro ao tentar executar Youtube Newsletter")
            print(f"Erro: {e}")

    @tasks.loop(minutes=720)
    async def process_users_7days(self):
        channel = self.bot.get_channel(1198071364465205258)
        e1 = discord.Embed(
            title=f"Operação automática de insersação de dados iniciada!",
            description=f"Inserção: 720min",
            color=discord.Color.dark_purple()
        )
        await channel.send(embed=e1)
        order_extractor = Orders_extract()
        start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        extracted_data = order_extractor.extract_all_data(start_date, end_date, page_size=10)
        order_extractor.save_data_to_json(extracted_data, "./database/configs/extracted_data.json")
        insert = BancoDados()
        insert.inserir_cliente_e_compra
        clientes = insert.quantidade_clientes()
        e2 = discord.Embed(
            title=f"Operação automática de insersação de dados realizada!",
            description=f"Inserção: 720min",
            color=discord.Color.dark_purple()
        )
        e2.add_field(name="Quantidade de clientes atuais:", value=f"{clientes}", inline=False)
        await channel.send(embed=e2)

    @tasks.loop(minutes=30)
    async def process_users_30min(self):
        channel = self.bot.get_channel(1198071364465205258)
        e1 = discord.Embed(
            title=f"Operação automática de insersação de dados iniciada!",
            description=f"Inserção: 30min",
            color=discord.Color.dark_purple()
        )
        await channel.send(embed=e1)
        order_extractor = Orders_extract()
        start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = datetime.now().strftime('%Y-%m-%d')
        extracted_data = order_extractor.extract_all_data(start_date, end_date, page_size=10)
        order_extractor.save_data_to_json(extracted_data, "./database/configs/extracted_data.json")
        insert = BancoDados()
        insert.inserir_cliente_e_compra
        clientes = insert.quantidade_clientes()
        e2 = discord.Embed(
            title=f"Operação automática de insersação de dados realizada!",
            description=f"Inserção: 30min",
            color=discord.Color.dark_purple()
        )
        e2.add_field(name="Quantidade de clientes atuais:", value=f"{clientes}", inline=False)
        await channel.send(embed=e2)

    @tasks.loop(minutes=2)
    async def create_ticket(self):
        channel = self.bot.get_channel(1193673666618208407)
        e = discord.Embed(
                title=f"CRIAR TICKET PARA SUPORTE!",
                description=f"Precisa de ajuda? Conte conosco para os seguintes temas:",
                color=discord.Color.dark_purple()
            )

        e.add_field(name="- Suporte geral.", value=f"", inline=False)
        e.add_field(name="- Ajuda com a verificação.", value=f"", inline=False)
        e.add_field(name="- Ajuda com meu pedido.", value=f"", inline=False)
        e.add_field(name="- Criticas ou sugestões.", value=f"", inline=False)
        e.add_field(name="- Denúncias ou reclamações.", value=f"", inline=False)
        e.set_footer(text=f"Developed by .jotazinn")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/852967954445893641/1194066495504928898/logo-nova-santos-design-branca-png-768x432.png.webp?ex=65af0015&is=659c8b15&hm=76d79115c82a0c282341fc6c9d2970379566ca78fc5beb1bc71c436b7cdf29fe&")
        e.set_image(url="https://cdn.discordapp.com/attachments/852967954445893641/1194065844125315182/Criar_Ticket.png?ex=65aeff79&is=659c8a79&hm=53fd1eaccaedf5a2b84410fb2f778ba05b0071a65fcff2d2c6a1ecf57abecd43&")

        await channel.purge(limit=int(20))
        await channel.send(embed=e, view=View(DropDown1()))

    @tasks.loop(minutes=1)
    async def create_validation(self):
        channel = self.bot.get_channel(1193225703932571648)
        e = discord.Embed(
                title=f"INICIAR VALIDAÇÃO",
                description=f"Esta comunidade é exclusiva para membros que adiquiriram algum produto ou curso da nossa plataforma! Basta inserir o código do pedido clicando o botão abaixo, e sua entrada será liberada AUTOMÁTICAMENTE! Caso não tenha nenhum produto, basta adiquirir em nossa loja de cursos e packs oficiais para você se tornar um designer de sucesso!",
                color=discord.Color.dark_purple()
            )

        e.set_footer(text=f"Developed by .jotazinn")
        e.set_thumbnail(url="https://cdn.discordapp.com/attachments/852967954445893641/1194066495504928898/logo-nova-santos-design-branca-png-768x432.png.webp?ex=65af0015&is=659c8b15&hm=76d79115c82a0c282341fc6c9d2970379566ca78fc5beb1bc71c436b7cdf29fe&")
        e.set_image(url="https://media.discordapp.net/attachments/852967954445893641/1194065843802349628/Criar_Ticket_1.png?ex=65aeff79&is=659c8a79&hm=382daad76d908824c5f77313bc1e6bebb798ceee7575bd9c761b6f77d098f92e&=&format=webp&quality=lossless&width=707&height=471")

        await channel.purge(limit=int(20))
        await channel.send(embed=e, view=View(Drop_down_verify()))

    @tasks.loop(minutes=10)
    async def update_status(self):
        channel = self.bot.get_channel(1193673882687782962)
        if channel:
            e = discord.Embed(
                title="INSTÂNCIA INICIALIZADA COM SUCESSO!",
                color=discord.Color.blue()
            )
            
            e.add_field(name="INFORMAÇÕES SISTEMA:", value=f"- Latência: {self.bot.latency * 1000}.\n- Erros encontrados: {0}.", inline=False)
            e.add_field(name="INFORMAÇÕES API:", value=f"- Kiwify API(main): {'Online'}.\n- Database Status: {'Online'}.", inline=False)
            e.set_footer(text="CI: TA_1 || Developed by .jotazinn")

            try:
                await channel.purge(limit=int(10))
                await channel.send("@Psychic - Programador", embed=e)
            except Exception as e:
                print(f"Erro ao enviar a mensagem embed: {e}")
        else:
            print("Canal não encontrado.")
    
    @tasks.loop(minutes=10)
    async def top10_bonifications(self):
        top_users = BonificationsPoints()
        top_users = top_users.obter_top_usuarios(10)

        channel = self.bot.get_channel(1198038071178952826)

        embed = discord.Embed(
            title="Top 10 Usuários com Mais Pontos",
            color=discord.Color.gold()
        )

        for position, (user_id, points) in enumerate(top_users, start=1):
            user = self.bot.get_user(int(user_id))
            embed.add_field(
                name=f"{position}. {user.display_name}" if user else f"{position}. Usuário Desconhecido",
                value=f"{points} pontos",
                inline=False
            )

        await channel.purge(limit=int(100))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # O resto do seu código aqui
        if message.author.name != self.bot.user.name:
            channel = self.bot.get_channel(1193914236540293241)
            data_atual = datetime.now()
            e = discord.Embed(
                title=f"Mensagem Enviada por {message.author.name}:",
                description=f"Mensagem:\n {message.content}",
                color=discord.Color.blue()
            )
            e.add_field(name="Channel ID:", value=f"- {message.channel.id}", inline=True)
            e.add_field(name="Message ID:", value=f"- {message.id}", inline=True)
            e.add_field(name="Author ID:", value=f"- {message.author.id}", inline=False)
            e.add_field(name="Data:", value=f"- {data_atual}", inline=False)
            e.set_footer(text=f"Developed by .jotazinn")
            await channel.send(embed=e)

            if message.content.startswith("https://discord.gg/") or message.content.startswith("https://discord.com/invite/"):
            # Verificar se o autor não é um administrador
                if not any(role.permissions.administrator for role in message.author.roles):
                    await message.delete()
                    await message.channel.send(f"{message.author.mention}, você não tem permissão para enviar convites de outros servidores.")
                    return
            if message.channel.id == 1198030340497887273:
                # Adicionar pontos ao usuário
                user_id = str(message.author.id)
                points_a_adicionar = 5
                bonifi = BonificationsPoints()
                bonifi.inserir_pontos(user_id, points_a_adicionar)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel_id = 1193225414185848964  # Substitua pelo ID do canal de boas-vindas
        role_id = 1193672352941228042  # Substitua pelo ID do papel que você deseja adicionar

        channel = self.bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(title=f"Bem-vindo(a) {member.name}!", description=f"Seja bem-vindo(a) a nossa comunidade PSYCHIC DESIGNER, {member.mention}! Faça sua validação em: #validação e aproveite tudo o que temos a oferecer!", color=0x00ff00)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Entrou em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await channel.send(embed=embed)

            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """ channel = self.bot.get_channel(555133251757408273)
        ##canal = message.guild.get_channel(555133251757408273) -- GLOBAL
        await channel.send(message.content) """
        pass

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """ channel = before.guild.get_channel(1100401126735609898)

        e = discord.Embed(
            title="Mensagem Editada:",
            description=f"||{before.content} -> {after.content}||",
            color=discord.Color.blue()
        )

        await channel.send(embed=e) """
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para usar esse comando!")

        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send("Você não tem permissão para usar esse comando aqui!")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        # Aqui você pode adicionar o código que será executado sempre que um comando for chamado
        print(f'O comando "{ctx.command.name}" foi chamado.')

def setup(bot: commands.Bot):
    bot.add_cog(moderationEvents(bot))
""" 
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(1193225499426697286)  # Substitua pelo ID do canal de despedida
        if channel:
            embed = discord.Embed(title=f"Até logo {member.name}!", description=f"{member.name} saiu do servidor. Até logo!", color=0xff0000)
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(text=f"Saiu em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await channel.send(embed=embed) """