import discord

intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)


counts = {}


@bot.event
async def on_ready():
    channel = bot.get_channel(666328861985865749)
    c = 0
    async for message in channel.history(limit=None):
        c += 1
        print(c)
        user_id = message.author.id
        counts[user_id] = counts.get(user_id, 0) + 1

    with open("count.csv", "w") as f:
        for key in counts:
            f.write(f"{key}, {counts[key]}\n")


bot.run("***REMOVED***")