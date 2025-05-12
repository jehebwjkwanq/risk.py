import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import os
import random
import discord
from colorama import init, Fore
import aiohttp
from aiohttp import ClientSession
from aiohttp.helpers import proxies_from_env


init(autoreset=True)

# WARNING: Use environment variables for tokens in production
TOKEN = "MTMyMDIwOTk0MTY1MDIxMDg3Nw.GqfSsL.IJY1-3GgI_WvnYlSNgyMkOhMnNlmaeVHxhLTuI"
PREFIX = "x"
INTENTS = discord.Intents.default()
INTENTS.guilds = True
INTENTS.message_content = True

KIA = """
           /$$    /$$    /$$      
          |__/  /$$$$$$ | $$      
  /$$$$$$  /$$ /$$__  $$| $$   /$$
 /$$__  $$| $$| $$  \__/| $$  /$$/
| $$  \__/| $$|  $$$$$$ | $$$$$$/ 
| $$      | $$ \____  $$| $$_  $$ 
| $$      | $$ /$$  \ $$| $$ \  $$
|__/      |__/|  $$$$$$/|__/  \__/
               \_  $$_/           
                 \__/              
> Developer: ri$k#1337
"""

messagex = [
    "**OH TALAGA, GOD KA? ANONG PAKE KO! HAHAHAHA**\n\n**alliance**\n- https://discord.gg/4GASdn9N | us\n- https://discord.gg/7asPQyJM | ally\n\n**socials**\n- https://www.youtube.com/@ransomx1337\n- https://www.youtube.com/@hazexyz\n- https://www.youtube.com/@mlwrx\n\n@here @everyone"
]

PROXIES = [
]

bot = commands.Bot(command_prefix=PREFIX, intents=INTENTS)
bot.remove_command("help")

# Utils
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def center_text(text):
    try:
        term_width, _ = os.get_terminal_size()
    except:
        term_width = 80
    return "\n".join(line.center(term_width) for line in text.split("\n"))

# Custom HTTP connector with proxy support
async def create_proxy_session():
    proxy = random.choice(PROXIES) if PROXIES else None
    if not proxy:
        env_proxies = proxies_from_env()
        proxy = env_proxies.get("http") or env_proxies.get("https")
    connector = aiohttp.TCPConnector(limit=0)  # Unlimited connections
    return ClientSession(connector=connector, trust_env=True), proxy

# Message button handler
class MessageButtonView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BangButton())

class BangButton(Button):
    def __init__(self):
        super().__init__(label="bang", style=discord.ButtonStyle.primary, custom_id="send")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print("[!] Sent Message")
        session, proxy = await create_proxy_session()
        try:
            for _ in range(1000000):  # Reduced from 100000 to prevent abuse
                try:
                    await interaction.followup.send(random.choice(messagex))
                    await asyncio.sleep(0.01)
                except discord.HTTPException as e:
                    if e.status == 429:
                        print("Rate-limited! Retrying...")
                        await asyncio.sleep(e.retry_after)
                    else:
                        print(f"HTTP error: {e}")
        finally:
            await session.close()

@bot.event
async def on_ready():
    clear_console()
    print(Fore.RED + center_text(KIA))
    print(f"{Fore.GREEN}G NA SAH")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name="nag-mamahal, jai"),
        status=discord.Status.do_not_disturb
    )
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Command to send message to all permissible channels
@bot.tree.command(name="nyoker", description="sabog")
async def nyok(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    tasks = []
    session, proxy = await create_proxy_session()

    async def send_to_channel(channel):
        if channel.permissions_for(guild.me).send_messages:
            try:
                await channel.send(random.choice(messagex))
                return True
            except discord.HTTPException as e:
                if e.status == 429:
                    print(f"Rate-limited in {channel.name}! Retrying...")
                    await asyncio.sleep(e.retry_after)
                    return False
                print(f"Failed to send to {channel.name}: {e}")
                return False
            except Exception as e:
                print(f"Error in {channel.name}: {e}")
                return False
        return False

    try:
        for channel in guild.text_channels:
            tasks.append(send_to_channel(channel))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        sent_count = sum(1 for result in results if result is True)
        await interaction.followup.send(f"Messages sent to {sent_count} channel(s).", ephemeral=True)
    finally:
        await session.close()

# Existing risk command
@bot.tree.command(name="risk", description="wag kupal hahahha, mas masakit ung iniwan ka.")
async def risk(interaction: discord.Interaction):
    try:
        if interaction.channel.permissions_for(interaction.guild.me).send_messages:
            await interaction.response.send_message("pre, miss ko na sya", view=MessageButtonView(), ephemeral=True)
        else:
            await interaction.response.send_message("hindi ako maka send tanga", ephemeral=True)
    except Exception as e:
        print(f"Error: {e}")

bot.run(TOKEN)

# Commands
@bot.command()
async def joinvc(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"[+] Joined VC: **{channel.name}**")
    else:
        await ctx.send("[-] You must be in a voice channel first.")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = member or ctx.author
    await ctx.send(f"{member.name}'s avatar: {member.avatar.url}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    confirm = await ctx.send(f"🧹 Deleted {amount} messages.")
    await confirm.delete(delay=3)

@bot.command()
async def ipinfo(ctx, ip: str):
    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json")
        data = res.json()

        if 'bogon' in data:
            await ctx.send("The desired IP is Private.")
            return

        await ctx.send(
            f"**IP:** {data.get('ip')}\n"
            f"**City:** {data.get('city')}\n"
            f"**Region:** {data.get('region')}\n"
            f"**Country:** {data.get('country')}\n"
            f"**Org:** {data.get('org')}\n"
            f"**Location:** {data.get('loc')}"
        )

        if 'loc' in data:
            lat, lon = data['loc'].split(',')
            maps_url = f"https://www.google.com/maps?q={lat},{lon}"
            await ctx.send(f"[+] URL : ({maps_url})")
    except Exception as e:
        await ctx.send(f"[-] Error: {e}")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, role: discord.Role, action: str):
    if action.lower() == "assign":
        await member.add_roles(role)
        await ctx.send(f"[+] Role `{role.name}` assigned to {member.mention}")
    elif action.lower() == "remove":
        await member.remove_roles(role)
        await ctx.send(f"[-] Role `{role.name}` removed from {member.mention}")
    else:
        await ctx.send("[-] Invalid action. Use `assign` or `remove`.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"[x] {member.mention} has been banned. Reason: {reason or 'No reason provided'}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"[-] {member.mention} has been kicked. Reason: {reason or 'No reason provided'}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: str, *, reason=None):
    match = re.match(r"(\d+)([smhd])", duration)
    if not match:
        await ctx.send("[-] Invalid duration format. Use `10m`, `1h`, etc.")
        return

    value, unit = int(match.group(1)), match.group(2)
    seconds = value * {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}[unit]
    until = datetime.utcnow() + timedelta(seconds=seconds)
    await member.timeout(until, reason=reason)
    await ctx.send(f"[+] {member.mention} has been timed out for {duration}. Reason: {reason or 'No reason provided'}")

@bot.command(name="user_profile_search")
async def user_profile_search(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"{member.name}'s Profile",
        color=discord.Color.dark_teal()
    )
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="blaze <3 u",
        description="Prefix 'x'",
        color=0x000000
    )
    embed.add_field(name="xrole <user> <role> <assign|remove>", value="Assign or remove a role.", inline=False)
    embed.add_field(name="xban <user> [reason]", value="Ban a user.", inline=False)
    embed.add_field(name="xkick <user> [reason]", value="Kick a user.", inline=False)
    embed.add_field(name="xtimeout <user> <duration> [reason]", value="Timeout a user.", inline=False)
    embed.add_field(name="xuser_profile_search <user>", value="User profile info.", inline=False)
    embed.add_field(name="xvc", value="Join your VC.", inline=False)
    embed.add_field(name="xhelp", value="Show help message.", inline=False)
    embed.set_image(url="https://cdn.discordapp.com/banners/1320209941650210877/256f6d897116708465c4295839f02a7d.png?size=4096&ignore=true")

    try:
        await ctx.send(embed=embed)
    except discord.HTTPException as e:
        await ctx.send("Failed to send help message.")

# Start
def main():
    authenticated, username = authenticate()
    if not authenticated:
        print(f"{Fore.RED}[-] Authentication failed")
        return
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"{Fore.RED}[-] Error running bot: {e}")

if __name__ == "__main__":
    main()
