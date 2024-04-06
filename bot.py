# Made by unknusr

import discord
import os
import time
from discord.ext import commands
import mysql.connector

db_name = 'NAME'

mydb = mysql.connector.connect(
  host='127.0.0.1',
  user='root',
  password='',
  database=db_name,
)
mycursor = mydb.cursor()

krma = commands.Bot(command_prefix='!', intents=discord.Intents.all())
krma.remove_command('help')    
    
@krma.event
async def on_ready():
    os.system('cls')
    print(f'Bot: {krma.user.name} ({krma.user.id})\nGuild Count: {len(krma.guilds)}')
    await krma.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="krmastudios.net"))

@krma.event
async def on_message(message):
    if '!verify' in message.content.lower():
        await krma.process_commands(message)
        time.sleep(0.2)
        await message.delete()
    else:
        await krma.process_commands(message)

@krma.command()
async def verify(ctx, args):
    role = 1225863775169544253
    user = ctx.author
    discord_id = ctx.author.id
    mycursor.execute(f'SELECT * FROM {db_name}_verification')
    tables = mycursor.fetchone()
    if args == tables[1]:
        if tables[3] == 0:
            mycursor.execute(f'UPDATE {db_name}_verification SET discord_id = {discord_id} WHERE discord_id IS NULL')
            mycursor.execute(f'UPDATE {db_name}_verification SET verified = 1 WHERE verified = 0')
            await user.add_roles(user.guild.get_role(role))
        else:
            await ctx.send('Code already verified.', delete_after = 0.5)
    else:
        await ctx.send('Invalid Code.', delete_after = 0.5)
    mydb.commit()

# Made by unknusr

token = open('sub/token.txt')
krma.run(token.read())

# Made by unknusr