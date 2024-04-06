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

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
client.remove_command('help')    
    
@client.event
async def on_ready():
    os.system('cls')
    print(f'Bot: {client.user.name} ({client.user.id})\nGuild Count: {len(client.guilds)}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="clientstudios.net"))

@client.event
async def on_message(message):
    if '!verify' in message.content.lower():
        await client.process_commands(message)
        time.sleep(0.2)
        await message.delete()
    else:
        await client.process_commands(message)

@client.command()
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
client.run(token.read())

# Made by unknusr