import os
import json
import discord
from discord.ext.commands import Bot
import NewFunctionsPYC

with open("config.json") as f:
      configdata = json.load(f)

client = NewFunctionsPYC.Client(token=configdata["token"], Intents= discord.Intents.all() ,command_prefix=configdata["prefix"] ,poweredby=False)
client.load_cogs("misclaneousBOT")
client.load_cogs("moderatorBOT")
client.load_cogs("messagesBOT")
client.load_cogs("verificationBOT")
client.__run__()