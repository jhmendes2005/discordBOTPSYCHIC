import discord
from discord.ui import InputText
from database.main import BancoDeDados

class ModalVerify(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="VERIFICAÇÃO ALUNOS")

        self.add_item(
            InputText(
                label="Digite o email utilizado na compra:",
                placeholder="exemplo@email.com",
                value="",
                style=discord.InputTextStyle.short,
                required=True
            )
        ) 
        self.add_item(
            InputText(
                label="Digite seu nome:",
                placeholder="Nome completo",
                value="",
                style=discord.InputTextStyle.short,
                required=True
            )
        )

    async def callback(self, interaction: discord.Interaction):
        banco = BancoDeDados()
        user_id = interaction.user.id
        user_purchase = self.children[0].value
        order_info = banco.consultar_cliente(user_purchase, tipo_consulta='email')
        print(order_info)
        
        if order_info and len(order_info) >= 5:  # Verifica se order_info tem o formato esperado
            compras_cliente = banco.consultar_compras_cliente(order_info[0])  # Substitua 0 pelo índice correto do ID do cliente
            if compras_cliente is not None:
                for compra in compras_cliente:
                    role_id = banco.consultar_produto_por_id(compra[2])
                    await self.set_role(interaction, user_id, role_id)
                
                await self.set_role(interaction, user_id, 1193672121411448942)
                await self.remove_role(interaction, user_id, 1193672352941228042)
                await interaction.response.send_message("Seja bem vindo!", ephemeral=True)
            else:
                await interaction.response.send_message("Não foi possível se registrar...", ephemeral=True)
        else:
            await interaction.response.send_message("Cadastro não localizado ou formato inválido. Acione nossa STAFF.", ephemeral=True)

    def create_order_info_embed(self, order_info):
        embed = discord.Embed(title="Informações do Cliente", color=discord.Color.green())
        embed.add_field(name="ID do Cliente", value=order_info[0], inline=False)
        embed.add_field(name="Nome", value=order_info[1], inline=False)
        embed.add_field(name="Email", value=order_info[2], inline=False)
        embed.add_field(name="CPF", value=order_info[3], inline=False)
        embed.add_field(name="Número de Telefone", value=order_info[4], inline=False)
        return embed

    def create_compras_embed(self, compras_cliente):
        embed = discord.Embed(title="Compras do Cliente", color=discord.Color.blue())
        banco = BancoDeDados()

        if compras_cliente is not None:
            for compra in compras_cliente:
                embed.add_field(name="ID da Compra", value=compra[0], inline=False)
                embed.add_field(name="ID do Produto", value=compra[2], inline=False)
        else:
            embed.add_field(name="Erro", value="Erro ao consultar as compras do cliente.", inline=False)

        return embed

    async def set_role(self, interaction: discord.Interaction, user_id, role_id):
        try:
            guild = interaction.guild
            member = guild.get_member(user_id)
            role = guild.get_role(role_id)
            await member.add_roles(role)
            return f"Role added successfully to {member.display_name}."

        except Exception as e:
            print(f"Error in set_role: {e}")
            return "An error occurred while adding the role."

    async def remove_role(self, interaction: discord.Interaction, user_id, role_id):
        try:
            guild = interaction.guild
            member = guild.get_member(user_id)
            role = guild.get_role(role_id)
            await member.remove_roles(role)
            return f"Role removed successfully from {member.display_name}."

        except Exception as e:
            print(f"Error in remove_role: {e}")
            return "An error occurred while removing the role."