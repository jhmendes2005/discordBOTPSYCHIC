from discord.ui import Select
import discord
import json

class DropDown1(Select):
    def __init__(self):
        super().__init__(
            placeholder="Selecione uma opção",
            options=[
                discord.SelectOption(label="- Suporte geral.", value="suporte_geral"),
                discord.SelectOption(label="- Ajuda com a verificação.", value="ajuda_verificação"),
                discord.SelectOption(label="- Ajuda com meu pedido.", value="ajuda_pedido"),
                discord.SelectOption(label="- Criticas ou sugestões.", value="feedback"),
                discord.SelectOption(label="- Denúncias ou reclamações.", value="denuncia")
            ]
        )


    async def callback(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_name = interaction.user.name

        selected_value = interaction.data["values"][0]
        channel = interaction.channel
        guild = channel.guild

        check_ticket = TicketsControl()
        check_ticket, ticket_name_created = check_ticket.check_existing_ticket(user_id)

        if check_ticket is not True:
            if selected_value == "suporte_geral":
                member = guild.get_member(user_id)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                channel_name = f"suporte-{user_name}"
                channel = await guild.create_text_channel(f"{channel_name}", overwrites=overwrites)
                initial_message = "Olá! Bem-vindo ao seu canal privado."

                ticket = TicketsControl()
                ticket.add_open_ticket(user_id, "suporte_geral", channel.id)  # Adicionando o channel_id ao ticket aberto

                await channel.send(content=initial_message)
                await interaction.response.send_message(f"Você selecionou Suporte Geral! Seu ticket foi criado em: {channel.mention}", ephemeral=True)

            elif selected_value == "ajuda_verificação":
                member = guild.get_member(user_id)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                channel_name = f"verificação-{user_name}"
                channel = await guild.create_text_channel(f"{channel_name}", overwrites=overwrites)
                initial_message = "Olá! Bem-vindo ao seu canal privado."

                ticket = TicketsControl()
                ticket.add_open_ticket(user_id, "ajuda_verificação", channel.id)  # Adicionando o channel_id ao ticket aberto

                await channel.send(content=initial_message)
                await interaction.response.send_message(f"Você selecionou Suporte Geral! Seu ticket foi criado em: {channel.mention}", ephemeral=True)

            elif selected_value == "ajuda_pedido":
                member = guild.get_member(user_id)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                channel_name = f"pedido-{user_name}"
                channel = await guild.create_text_channel(f"{channel_name}", overwrites=overwrites)
                initial_message = "Olá! Bem-vindo ao seu canal privado."

                ticket = TicketsControl()
                ticket.add_open_ticket(user_id, "ajuda_pedido", channel.id)  # Adicionando o channel_id ao ticket aberto

                await channel.send(content=initial_message)
                await interaction.response.send_message(f"Você selecionou Suporte Geral! Seu ticket foi criado em: {channel.mention}", ephemeral=True)

            elif selected_value == "feedback":
                member = guild.get_member(user_id)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                channel_name = f"feedback-{user_name}"
                channel = await guild.create_text_channel(f"{channel_name}", overwrites=overwrites)
                initial_message = "Olá! Bem-vindo ao seu canal privado."

                ticket = TicketsControl()
                ticket.add_open_ticket(user_id, "feedback", channel.id)  # Adicionando o channel_id ao ticket aberto

                await channel.send(content=initial_message)
                await interaction.response.send_message(f"Você selecionou Suporte Geral! Seu ticket foi criado em: {channel.mention}", ephemeral=True)

            elif selected_value == "denuncia":
                member = guild.get_member(user_id)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    member: discord.PermissionOverwrite(read_messages=True)
                }
                channel_name = f"denuncia-{user_name}"
                channel = await guild.create_text_channel(f"{channel_name}", overwrites=overwrites)
                initial_message = "Olá! Bem-vindo ao seu canal privado."

                ticket = TicketsControl()
                ticket.add_open_ticket(user_id, "denuncia", channel.id)  # Adicionando o channel_id ao ticket aberto

                await channel.send(content=initial_message)
                await interaction.response.send_message(f"Você selecionou Suporte Geral! Seu ticket foi criado em: {channel.mention}", ephemeral=True)
        else:
            channel_name_created = guild.get_channel(ticket_name_created)
            channel_mention = f"#{channel_name_created}"
            await interaction.response.send_message(f"Você já tem um ticket aberto! {channel_mention}", ephemeral=True)


class TicketsControl():
    def __init__(self):
        with open("./ticketBOT/temp/tickets_open.json", "r") as file:
            self.opened = json.load(file)
        with open("./ticketBOT/temp/tickets_closed.json", "r") as file:
            self.closed = json.load(file)

    def check_existing_ticket(self, user_id):
        for ticket in self.opened["tickets"]:
            if ticket["user_id"] == user_id:
                return True, ticket["channel_id"]
        return False, None
    
    def save_tickets(self, data, file_path):
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add_open_ticket(self, user_id, ticket_type, channel_id):
        new_ticket = {
            "user_id": user_id,
            "type": ticket_type,
            "channel_id": channel_id
        }

        self.opened["tickets"].append(new_ticket)
        self.save_tickets(self.opened, "./ticketBOT/temp/tickets_open.json")

    def close_ticket(self, channel_id):
        for ticket in self.opened["tickets"]:
            if ticket["channel_id"] == channel_id:
                self.closed["tickets"].append(ticket)
                self.opened["tickets"].remove(ticket)
                self.save_tickets(self.closed, "./ticketBOT/temp/tickets_closed.json")
                self.save_tickets(self.opened, "./ticketBOT/temp/tickets_open.json")
                return True
        return False