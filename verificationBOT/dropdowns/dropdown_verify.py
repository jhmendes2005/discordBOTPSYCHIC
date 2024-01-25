from discord.ui import Select
import discord
from verificationBOT.modals.modal_verify import ModalVerify

class Drop_down_verify(Select):
    def __init__(self):
        super().__init__(
            placeholder="Selecione uma opção",
            options=[
                discord.SelectOption(label="Selecione uma opção", value="opcaonenhuma"),
                discord.SelectOption(label="INICIAR VERIFICAÇÃO", value="verificar")
            ]
        )


    async def callback(self, interaction: discord.Interaction):
        selected_value = interaction.data["values"][0]
        if selected_value == "verificar":
            modal = ModalVerify()
            await interaction.response.send_modal(modal=modal)