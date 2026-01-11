import discord
from discord.ext import commands
import json
import itertools
import time
import os
import random
import string
import aiohttp
import requests
import pickle
import threading
import ctypes

# CREDITS (discord users):
# Creator: @joellyyyy
# Helper: @opiumy


with open("config/config.json", "r") as file:
    config = json.load(file)
    token = config.get("token")
    prefix = config.get("prefix")
    tiktok = config.get("tiktok")
    guns = config.get ("guns")
    version = config.get ("version")

green = "\033[1;32m"
white = "\033[1;37m"
INVITE_CODE = "https://discord.gg/azb85AH8Tm"
CHANNEL_ID = 1459848760661246129

def save_config(config):
    with open("config/config.json", "w") as file:
        json.dump(config, file, indent=4)

def selfbot_menu():
    os.system("cls")
    os.system("color 2")
    print(f"""
                                  █████     
                             ▒▒███      
 █████ █████  ██████   █████  ▒███ █████
▒▒███ ▒▒███  ███▒▒███ ███▒▒   ▒███▒▒███ 
 ▒███  ▒███ ▒███████ ▒▒█████  ▒██████▒  
 ▒▒███ ███  ▒███▒▒▒   ▒▒▒▒███ ▒███▒▒███ 
  ▒▒█████   ▒▒██████  ██████  ████ █████
   ▒▒▒▒▒     ▒▒▒▒▒▒  ▒▒▒▒▒▒  ▒▒▒▒ ▒▒▒▒▒ 
                                        
                                        
                                        
             made by \033[1m@joellyyyy""")
bot = commands.Bot(command_prefix=prefix, description='not a selfbot', self_bot=True, help_command=None)
plus = (f"\033[23m\033[90m--\033[3m")

@bot.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW(f"VESK SELFBOT - v{version}")
    try:
        invite = await bot.fetch_invite(INVITE_CODE)
        await invite.accept()
        await ctx.send(f"Joined By Vesk Selfbot")
        selfbot_menu()
    except Exception as e:
        print(f'Failed to join server: {e}')

@bot.command()
async def ping(ctx):
    await ctx.message.delete()

    before = time.monotonic()
    message_to_send = await ctx.send("Pinging...")

    await message_to_send.edit(content=f"`{int((time.monotonic() - before) * 1000)} ms`")
    print(f"{plus} ping")

@bot.command(aliases=['icon'])
async def guildicon(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} icon :**\n{ctx.guild.icon.url if ctx.guild.icon else '*NO ICON*'}")
    print(f"{plus} guildicon")

@bot.command(aliases=['banner'])
async def guildbanner(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=5)
        return

    await ctx.send(f"> **{ctx.guild.name} banner :**\n{ctx.guild.banner.url if ctx.guild.banner else '*NO BANNER*'}")
    print(f"{plus} guildbanner")


@bot.event
async def on_ready():
    ctypes.windll.kernel32.SetConsoleTitleW(f"VESK SELFBOT - v{version}")
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await bot.fetch_channel(CHANNEL_ID)

    await channel.send("JOINED BY VESK BOT")
    try:
        invite = await bot.fetch_invite(INVITE_CODE)
        await invite.accept()
        selfbot_menu()
    except Exception as e:
        print(f'Failed to join server: {e}')

@bot.command()
async def afk(ctx, status: str, *, message: str=None):
    await ctx.message.delete()

    if status not in ["ON", "OFF"]:
        await ctx.send(f"> **[**ERROR**]**: Invalid action. Use `ON` or `OFF`.\n> __Command__: `afk ON|OFF <message>`", delete_after=5)
        return

    if status.upper() == "ON":
        if not config["afk"]["enabled"]:
            config["afk"]["enabled"] = True
            if message:
                config["afk"]["message"] = message
            save_config(config)
            selfbot_menu(bot)
            await ctx.send(f"> **AFK mode enabled.** Message: `{config['afk']['message']}`", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is already enabled", delete_after=5)
    elif status.upper() == "OFF":
        if config["afk"]["enabled"]:
            config["afk"]["enabled"] = False
            save_config(config)
            selfbot_menu(bot)
            await ctx.send("> **AFK mode disabled.** Welcome back!", delete_after=5)
        else:
            await ctx.send("> **[**ERROR**]**: AFK mode is not currently enabled", delete_after=5)

@bot.event
async def on_message(message):

    if config["afk"]["enabled"]:
        if bot.user in message.mentions and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return
        elif isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
            await message.reply(config["afk"]["message"])
            return

    await bot.process_commands(message)

@bot.command(aliases=['fetch'])
async def fetchmembers(ctx):
    await ctx.message.delete()

    if not ctx.guild:
        await ctx.send(f'> **[**ERROR**]**: This command can only be used in a server.', delete_after=5)
        return
    
    members = ctx.guild.members
    member_data = []

    for member in members:
        member_info = {
            "name": member.name,
            "id": str(member.id),
            "avatar_url": str(member.avatar.url) if member.avatar else str(member.default_avatar.url),
            "discriminator": member.discriminator,
            "status": str(member.status),
            "joined_at": str(member.joined_at)
        }
        member_data.append(member_info)

@bot.command(aliases=["prefix"])
async def changeprefix(ctx, *, new_prefix: str=None):
    await ctx.message.delete()

    if not new_prefix:
        await ctx.send(f"> **[**ERROR**]**: Invalid command.\n> __Command__: `changeprefix <prefix>`", delete_after=5)
        return
    
    config['prefix'] = new_prefix
    save_config(config)
    selfbot_menu(bot)
    
    prefix = new_prefix

    await ctx.send(f"> Prefix updated to `{new_prefix}`", delete_after=5)
    print(f"{plus} changeprefix")

@bot.command(aliases=['skelly'])
async def sk3llyy(ctx):
    await ctx.message.delete()

    embed = f"""**MY SOCIAL NETWORKS | Prefix: `{prefix}`**\n
    > :mobile_phone: `Tiktok Page`\n*{tiktok}*
    > :robot: `Guns.lol`\n*{guns}*"""

    await ctx.send(embed)

@bot.command(aliases=['av'])
async def avatar(ctx, user: discord.User = None):
    await ctx.message.delete()

    if not user:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `avatar <@user>`', delete_after=5)
        return
    
    avatar_url = user.avatar.url if user.avatar else user.default_avatar.url

    await ctx.send(f"> {user.mention}'s avatar:\n{avatar_url}")
    print(f"{plus} avatar ")

@bot.command(aliases=['r'])
async def addrole(ctx, member: discord.Member, *, role_name):
    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if not role:
        return await ctx.send("Role not found.")
    try:
        await ctx.message.delete()
        await member.add_roles(role)
        print(f"{plus} addrole ({role_name},{member.mention})")
    except Exception as e:
        await ctx.send(f"Add role failed: {e}")

@bot.command(aliases=['cr'])
async def createrole(ctx, *, name):
    try:
        await ctx.message.delete()
        await ctx.guild.create_role(name=name)
        print(f"{plus} createrole ({name})")
    except Exception as e:
        await ctx.send(f"Create role failed: {e}")

@bot.command(aliases=['dih'])
async def dick(ctx, user: str=None):
    await ctx.message.delete()

    if not user:
        user = ctx.author.display_name

    size = random.randint(1, 15)
    dong = "=" * size

    await ctx.send(f"> **{user}**'s Dick size\n8{dong}D")
    print(f"{plus} dick ({ctx.author.display_name}) ")

@bot.command(aliases=['p'])
async def purge(ctx, num_messages: int=1):
    await ctx.message.delete()
    
    if not ctx.guild:
        await ctx.send("> **[**ERROR**]**: This command can only be used in a server", delete_after=2)
        return

    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("> **[**ERROR**]**: You do not have permission to delete messages", delete_after=2)
        return
    
    if 1 <= num_messages <= 150:
        deleted_messages = await ctx.channel.purge(limit=num_messages)
        await ctx.send(f"> **{len(deleted_messages)}** messages have been deleted", delete_after=2)
        print(f"{plus} purge")
    else:
        await ctx.send("> **[**ERROR**]**: The number must be between 1 and 100", delete_after=2)

@bot.command(aliases=['cc'])
async def clone_channels(ctx, old_server_id: int, new_server_id: int):
    await ctx.message.delete()
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)

    if not old_server:
        await ctx.send('# VESK SELFBOT \n`🔏` **Old server not found.**')
        return
    if not new_server:
        await ctx.send('# VESK SELFBOT \n`🔏` **New server not found.**')
        return
    category_map = {}

    clone_messages = [] 

    for old_category in old_server.categories:
        new_category = await new_server.create_category_channel(name=old_category.name, overwrites=old_category.overwrites)
        category_map[old_category.id] = new_category

        for old_text_channel in old_category.text_channels:
            new_text_channel = await new_category.create_text_channel(name=old_text_channel.name, overwrites=old_text_channel.overwrites)
            clone_messages.append(f'{plus} Text channel cloned: {old_text_channel.name} -> {new_text_channel.name} in category: {old_category.name} -> {new_category.name}')

        for old_voice_channel in old_category.voice_channels:
            new_voice_channel = await new_category.create_voice_channel(name=old_voice_channel.name, overwrites=old_voice_channel.overwrites)
            clone_messages.append(f'{plus} Voice channel cloned: {old_voice_channel.name} -> {new_voice_channel.name} in category: {old_category.name} -> {new_category.name}')

    for old_channel in old_server.channels:
        if isinstance(old_channel, (discord.TextChannel, discord.VoiceChannel)) and old_channel.category is None:
            if isinstance(old_channel, discord.TextChannel):
                new_channel = await new_server.create_text_channel(name=old_channel.name, overwrites=old_channel.overwrites)
                clone_messages.append(f'{plus} Text channel cloned: {old_channel.name} (No Category) -> {new_channel.name}')
            elif isinstance(old_channel, discord.VoiceChannel):
                new_channel = await new_server.create_voice_channel(name=old_channel.name, overwrites=old_channel.overwrites)
                clone_messages.append(f'{plus} Voice channel cloned: {old_channel.name} (No Category) -> {new_channel.name}')

    
    for message in clone_messages:
        print(message)

    
    await ctx.send("# VESK SELFBOT \n`🔏` **Channels cloned successfully!**")

@bot.command(aliases=['cnr'])
async def clone_roles(ctx, old_server_id: int, new_server_id: int):
    await ctx.message.delete()
    old_server = bot.get_guild(old_server_id)
    new_server = bot.get_guild(new_server_id)

    if old_server is None:
        await ctx.send("# VESK SELFBOT \n`🔏` **The old server does not exist.**")
        return

    if new_server is None:
        await ctx.send("# VESK SELFBOT \n`🔏` **The new server does not exist.**")
        return

    old_roles = old_server.roles

    role_map = {}

    clone_messages = [] 

    for role in reversed(old_roles):  
        new_role = await new_server.create_role(name=role.name, color=role.color, hoist=role.hoist,
                                               mentionable=role.mentionable, permissions=role.permissions,
                                               reason="Cloning roles")
        role_map[role.id] = new_role
        clone_messages.append(f'Role cloned: {role.name} -> {new_role.name}')
        print(f'Role cloned: {role.name} -> {new_role.name}')

    for member in old_server.members:
        member_roles = member.roles
        new_member = new_server.get_member(member.id)
        if new_member is not None:
            for role in reversed(member_roles):  
                if role.id in role_map:
                    new_role = role_map[role.id]
                    await new_member.add_roles(new_role)

    
    await ctx.send("# VESK SELFBOT \n`🔏` **Roles have been cloned successfully!**")

    
    for message in clone_messages:
        print(message)

@bot.command(aliases=['drl'])
async def deleteallroles(ctx):
    await ctx.message.delete()
    server = ctx.guild

    if server is None:
        await ctx.send("# VESK SELFBOT\n`🔏` **The server does not exist.**")
        return

    roles = server.roles

    for role in roles:
        if role.name != "@everyone":  
            try:
                await role.delete(reason="Deleting all roles")
            except Exception as e:
                print(f"# VESK SELFBOT\n`🔏` **Failed to delete role {role.name}: {e}**")

    await ctx.send("# VESK SELFBOT\n`🔏` **All roles have been deleted successfully!**")

@bot.command(aliases=['dac'])
async def deleteallchannels(ctx):
    await ctx.message.delete()
    channel_ids = []

    TEMP_DIR = "trash"
    TEMP_FILE = os.path.join(TEMP_DIR, "channel_ids.pkl")

   
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    
    for guild in bot.guilds:
        if guild.id == ctx.guild.id: 
            for channel in guild.channels:
                channel_ids.append(channel.id)
    
    
    with open(TEMP_FILE, 'wb') as f:
        pickle.dump(channel_ids, f)

   
    for channel_id in channel_ids:
        thread = threading.Thread(target=delete_channel, args=(channel_id,))
        thread.start()

    await ctx.send("# VESK SELFBOT\n`🔏` **All channels are being deleted.**")

def delete_channel(channel_id):
    url = f"https://canary.discord.com/api/v9/channels/{channel_id}"
    
    headers = {
        "accept": "*/*",
        "accept-language": "en-US",
        "authorization": token,
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "America/Chicago",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC4zNzMiLCJvc192ZXJzaW9uIjoiMTAuMC4xOTA0NCIsIm9zX2FyY2giOiJ4NjQiLCJhcHBfYXJjaCI6Ing2NCIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjM3MyBDaHJvbWUvMTI0LjAuNjM2Ny4yMDcgRWxlY3Ryb24vMzAuMC42IFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3ZlcnNpb24iOiIzMC4wLjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjozMDA3MDcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjQ4NjAyLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Closed channel with ID {channel_id}")
    else:
        print(f"Failed to close channel with ID {channel_id}: {response.status_code} {response.text}")

@bot.command(aliases=['s'])
async def spam(ctx, amount: int=1, *, message_to_send: str="VESK SELFBOT ONTOP"):
    await ctx.message.delete()

    try:
        if amount <= 0 or amount > 30:
            await ctx.send("> **[**ERROR**]**: Amount must be between 1 and 30 due to detectablity", delete_after=5)
            return
        for _ in range(amount):
            await ctx.send(message_to_send)
            print(f"spam - {amount} - {message_to_send}")
    except ValueError:
        await ctx.send(f'> **[**ERROR**]**: Invalid input\n> __Command__: `spam <amount> <message>`', delete_after=5)
        
@bot.command(aliases=['gen'])
async def nitro(ctx, amount: int=1):
    await ctx.message.delete()
    for i in range(amount):
        await ctx.send(f"https://discord.gift/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}")
        print(f"{plus} nitro")

@bot.command(aliases=['mc'])
async def membercount(ctx):
    await ctx.message.delete()
    member_count = ctx.guild.member_count
    await ctx.send(f"There are {member_count} member(s)")
    print(f"{plus} membercount")


@bot.command(aliases=['h','cmds'])
async def help(ctx):
    await ctx.message.delete()
    help_text = f"""
**VESK SELFBOT | Prefix: `{prefix}`**\n
**Commands:**\n
> {prefix}afk <ON/OFF> <Reason> - Sets you AFK (BUGGY).
> {prefix}changeprefix <prefix> - Changes the Prefix (BUGGY).
> {prefix}skelly - Shows Social Networks. 
> {prefix}avatar <user> - Shows the Avatar of a user. 
> {prefix}dick <user> - Finds the user's dih size. 
> {prefix}purge <amount> Deletes a specific amount of messages.
       `1/3` """
    await ctx.send(help_text)  
    help_text = f"""
**VESK SELFBOT | Prefix: `{prefix}`**\n
**Commands:**\n
> {prefix}guildbanner - Shows the Banner of the Server.
> {prefix}guildicon - Shows the Icon of the Server. 
> {prefix}addrole <user> <role> - Adds a role to a user.
> {prefix}createrole <name> - Creates a role.
> {prefix}deleteallroles - self-explanatory
> {prefix}deleteallchannels - self-explanatory
       `2/3` made by `joellyyyy`  """

    await ctx.send(help_text)
    help_text = f"""
**VESK SELFBOT | Prefix: `{prefix}`**\n
**Commands:**\n
> {prefix}cloneallroles <cguildid> <guildid> - Clones the roles of the first guild id onto the second id.
> {prefix}cloneallchannels <guildid> <guildid> - Clones the channels of the first guild id onto the second id.
> {prefix}spam <amount> <message> - Spams the same message.
> {prefix}nitro - Generates a random nitro code.
       `3/3` V{version}"""
    await ctx.send((help_text), file=discord.File("img/veskk.gif"))
    print(f"{plus} help")


bot.run(token)