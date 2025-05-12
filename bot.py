import discord
import os # default module
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True

load_dotenv() # load all the variables from the env file
bot = discord.Bot(intents=intents)

def parse_message_link(url: str) -> tuple[int]:
    URL_PREFIX = 'https://discord.com/channels/'
    assert url.startswith(URL_PREFIX)
    ids = url.strip(URL_PREFIX).split("/")
    assert len(ids) == 3

    server_id, channel_id, message_id  = list(map(int, ids))

    return server_id, channel_id, message_id


def create_message_link(server_id: int, channel_id: int, message_id: int) -> str:
    URL_PREFIX = 'https://discord.com/channels/'
    return URL_PREFIX + '/'.join(map(str, [server_id, channel_id, message_id]))

# cursed
GUILD_IDS = eval(os.getenv("GUILD_IDS"))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(guild_ids=GUILD_IDS, name="hello", description="Say hello to the bot")
@discord.option(name="message_link")
async def test(ctx: discord.ApplicationContext, message_link):
    server_id, channel_id, message_id = parse_message_link(message_link)
    print(server_id, channel_id, message_id)
    discord.guild
    await ctx.respond(f"Message Link: {create_message_link(server_id, channel_id, message_id)}")


@bot.slash_command(guild_ids=GUILD_IDS, name="test", description="Say hello to the bot")
@discord.option(name="message_link")
async def findmsg(ctx, message_id: str):
    message_id = int(message_id)
    guild: discord.Guild = ctx.guild
    all_users = set(guild.members)
    print(list(all_users))
    for channel in guild.text_channels:
        try:
            message = await channel.fetch_message(message_id)
            reactions = message.reactions
            reacted_users = set()
            reacted_users.add(bot.user)
            for reaction in reactions:
                reacted_users = reacted_users.union(set(await reaction.users().flatten()))
            
            unreacted_users  = all_users.difference(reacted_users)

            mentions = ''
            for user in unreacted_users:
                mentions += f"<@{user.id}> "

            await ctx.respond(f"Please react to this message: {create_message_link(ctx.guild.id, channel.id, message.id)}, mentions: {mentions}")

            return

        except discord.NotFound:
            continue
        except discord.Forbidden:
            continue
        except discord.HTTPException:
            continue





bot.run(os.getenv('TOKEN')) # run the bot with the token