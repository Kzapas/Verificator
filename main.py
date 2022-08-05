from keep_alive import startbot
import discord
from discord.ext import commands
import os
import firebase_admin
from firebase_admin import db
from discord.utils import get
import json
import platform
from datetime import datetime
import urllib.parse

intents = discord.Intents().all()
bot=commands.Bot(command_prefix="!", intents=intents)

cred_obj = firebase_admin.credentials.Certificate(
    'ecgverification-firebase-adminsdk-25eoi-c0db023814.json')
default_app = firebase_admin.initialize_app(
    cred_obj,
    {'databaseURL': "https://ecgverification-default-rtdb.firebaseio.com/"})

#client = discord.Client()

with open("settings.json", 'r', encoding='utf-8') as _settings_data:
    settings = json.load(_settings_data)

server_name = f"{settings['server_name']}"
master_role = f"{settings['master_role']}"

@bot.event
async def on_ready():
    print(f'Discord.py API version: {discord.__version__}')
    print(f'Python version: {platform.python_version()}')
    print(f'Logged in as {bot.user} | {bot.user.id}')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{settings['presence']}"
        )
    )
    print("Bot is ready to be used!")

@bot.command(name="selfrole")
@commands.has_role(master_role)
async def self_role(ctx):
    await ctx.channel.purge(limit=2)
    emojis = []
    roles = []
    for role in settings['roles']:
        roles.append(role['role'])
        emojis.append(role['emoji'])
    channel = bot.get_channel(int(settings['channel_id']))

    bot_msg = await channel.send(settings['message'])

    with open("reactions.json", "r") as f:
        self_roles = json.load(f)

    self_roles[str(bot_msg.id)] = {}
    self_roles[str(bot_msg.id)]["emojis"] = emojis
    self_roles[str(bot_msg.id)]["roles"] = roles

    with open("reactions.json", "w") as f:
        json.dump(self_roles, f)

    for emoji in emojis:
        await bot_msg.add_reaction(emoji)


@bot.event
async def on_raw_reaction_add(payload):
    msg_id = payload.message_id

    with open("reactions.json", "r") as f:
        self_roles = json.load(f)

    if payload.member.bot:
        return

    users = db.reference("/users").get()
    for x in users:
      if x == urllib.parse.quote(str(payload.member)) and str(msg_id) in self_roles:
          emojis = []
          roles = []
  
          for emoji in self_roles[str(msg_id)]['emojis']:
              emojis.append(emoji)
  
          for role in self_roles[str(msg_id)]['roles']:
              roles.append(role)
  
          guild = bot.get_guild(payload.guild_id)
          log_channel = bot.get_channel(int(settings['log_channel_id']))
  
          for i in range(len(emojis)):
              choosed_emoji = str(payload.emoji)
              if choosed_emoji == emojis[i]:
                  selected_role = roles[i]
  
                  role = discord.utils.get(guild.roles, name=selected_role)
  
                  try:
                    await payload.member.add_roles(role)
                    await payload.member.send(f"Added **{selected_role}** Role!")
                    await log_channel.send(f'`{datetime.now()}` - Added {selected_role} role to <@{payload.member.id}>')
                  except:
                    await payload.member.send("Sorry! I don't have permissions to give you that role!")
      else:
        await payload.member.send("Sorry! You aren't verified yet! Please verify yourself before trying to give yourself a role!")
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = bot.get_user(payload.user_id)
        emoji = payload.emoji
        await message.remove_reaction(emoji, user)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = await(guild.fetch_member(payload.user_id))
    msg_id = payload.message_id

    with open("reactions.json", "r") as f:
        self_roles = json.load(f)
      
    users = db.reference("/users").get()
    for x in users:
      if x == urllib.parse.quote(str(member)) and str(msg_id) in self_roles:
          emojis = []
          roles = []
  
          for emoji in self_roles[str(msg_id)]['emojis']:
              emojis.append(
                  emoji)
  
          for role in self_roles[str(msg_id)]['roles']:
              roles.append(role)
  
          log_channel = bot.get_channel(int(settings['log_channel_id']))
  
          for i in range(len(emojis)):
              choosed_emoji = str(payload.emoji)
              if choosed_emoji == emojis[i]:
                  selected_role = roles[i]
                  role = discord.utils.get(guild.roles, name=selected_role)
                  if member is not None:
                      await member.remove_roles(role)
                      await member.send(f"Removed **{selected_role}** Role!")
                      await log_channel.send(f'`{datetime.now()}` - Removed {selected_role} role from <@{payload.user_id}>')

@bot.event
async def on_message(message):
  await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    mbed=discord.Embed(title="Verify Yourself >>", url="https://Verificator.kzap.repl.co", description="In order to properly verify yourself and access the full Discord server, please fill out the form linked above./n", color=0x4dff00)
    mbed.set_author(name="Welcome to the "+server_name+" Discord community!")
    mbed.set_thumbnail(url="https://kzapas.github.io/ECG-Verification/assets/images/ecg-circle-logo-800-800-px-transparent-432x432.png")
    mbed.set_footer(text="*No personal information is shared or sold. All information is used to organize group events, giveaways, etc.")
    await member.send(embed=mbed)

startbot()
bot.run(os.environ['token'])
