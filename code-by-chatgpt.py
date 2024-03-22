import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    await channel.send(f'{member.mention} has joined the server.')

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    await channel.send(f'{member.display_name} has left the server.')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Anti-phishing link filter
    suspicious_links = ['example.com', 'phishing_site.com']
    for link in suspicious_links:
        if link in message.content:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, please do not post suspicious links.')
            break

    await bot.process_commands(message)

@bot.command()
async def membercount(ctx):
    total_members = ctx.guild.member_count
    bot_members = sum(1 for member in ctx.guild.members if member.bot)
    await ctx.send(f'Total members: {total_members}, Bots: {bot_members}')

bot.run('YOUR_BOT_TOKEN')