import os
import discord
import random
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GROUPS = os.getenv('GROUPS')
NUM_GROUPS = 4

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            await get_description(guild)

@client.event
async def on_message(message): 
    text = message.content.lower()
    if "hey tiny chef" in text: 
        if ("dinner" in text and "seat" in text): 
            await assign_seating(message.guild, message.channel)
        
async def assign_seating(guild, channel): 
    all_mems = []
    all_assigned = []
    print(GROUPS)
    for role in guild.roles: 
        print(role.name)
        print(role.name in GROUPS)
        if (role.name in GROUPS):
            print(role.members)
            random.shuffle(role.members)
            print(role.members)
            all_mems += role.members
    i = 1
    for member in all_mems: 
        all_assigned.append("table " + str(i) + ", " + member.display_name)
        i = i + 1 if (i + 1 <= NUM_GROUPS) else 1
    all_assigned.sort()
    current_table = ''
    result = "\n"
    for member in all_assigned: 
        split_str = member.split(",")
        if split_str[0] != current_table: 
            current_table = split_str[0]
            result += f'**{current_table}**\n'
        result += f'{split_str[1]}\n'
    await channel.send(result)

async def get_description(guild):
    print(
        '\nServer description:\n'
        f'{client.user} is connected to the guild {guild.name} (id: {guild.id})\n\n'
        f'{guild.name} members:'
    )
    async for member in guild.fetch_members(limit=150):
        print(member.name)


client.run(TOKEN)