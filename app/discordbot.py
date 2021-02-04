import datetime

import discord

from app.routers.socketio import sio

intents = discord.Intents.default()
intents.members = True
intents.reactions = True


allowed_roles = [
    689248011456610362,  # Twitch Subscriber: Tier 3
    689248011456610347,  # Twitch Subscriber: Tier 2
    689248011452416166,  # Twitch Subscriber: Tier 1
    375428806019776522,  # Twitch Subscriber
    462500164695752705,  # twitch sub color workaround
    309295971790094337,  # Patrons
    379650847149129738,  # Mrs. Anderson (Joe's wife)
    309157040570499077,  # Admin
    309296131072851968,  # Lili and Some Guy
]


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.valid_message_ids = []
        self.votes = {}

    async def on_ready(self):
        print(f"Logged in as {self.user.name} id: {self.user.id}")
        await self.fetch_votes()

    async def fetch_votes(self):
        print("Fetching vote messages.")
        await self.wait_until_ready()

        channel = self.get_channel(375432166659588099)  # voting channel

        messages = []

        start_dt = datetime.datetime(2017, 11, 4, 4, 21, 1)
        end_dt = datetime.datetime(2017, 11, 4, 4, 24, 59)

        async for message in channel.history(after=start_dt, before=end_dt, limit=500):
            # print(message.id, message.created_at, message.content)
            messages.append(message)

        self.valid_message_ids = [message.id for message in messages]

        for message in messages:
            # print(message)
            key = str(message.id)  # socketio glitch(?) workaround (last 2 digits go to 0)
            self.votes[key] = {"game": message.content, "yay": 0, "yay_voters": []}

            for reaction in message.reactions:
                # print(reaction.emoji, reaction.count)
                if type(reaction.emoji) is not str:
                    continue
                # print(ord(reaction.emoji))
                # if reaction.emoji.id == 447984382926520343:
                if reaction.emoji == "👍":
                    self.votes[key]["yay"] = reaction.count
                    reactors = await reaction.users().flatten()
                    for reactor in reactors:
                        # print(reactor.name, reactor.avatar_url)
                        self.votes[key]["yay_voters"] = {reactor.id: {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}
        self.votes["partial"] = False
        await sio.emit("votes_discord", data=self.votes, namespace="/gamevotes")
        print("Done fetching votes")

    async def count_change(self, reaction, count):
        if reaction.message_id in self.valid_message_ids:
            if reaction.emoji.name == "👍":
                key = str(reaction.message_id)
                if key in self.votes:
                    self.votes[key]["yay"] = self.votes[key].get("yay", 0) + count
                    user = self.get_user(reaction.user_id)
                    user_data = {
                        "name": user.name,
                        "avatar_url": user.avatar_url._url,
                    }
                    self.votes[key]["yay_voters"][user.id] = user_data

                    vote_data = {
                        "message_id": key,
                        "game": self.votes[key]["game"],
                        "yay": self.votes[key]["yay"],
                        "yay_voters": self.votes[key]["yay_voters"],
                        "partial": True,
                    }

                    await sio.emit("votes_discord", data=vote_data, namespace="/gamevotes")

    async def on_raw_reaction_add(self, reaction):
        await self.count_change(reaction, 1)

    async def on_raw_reaction_remove(self, reaction):
        await self.count_change(reaction, -1)


bot = DiscordBot(intents=intents)


async def can_vote(user_id):
    guild = bot.get_guild(308515582817468420)
    user = guild.get_member(user_id)
    if not user:
        return
    else:
        return any(role.id in allowed_roles for role in user.roles)
