import asyncio
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
        self.voters = {}
        self.ready = False

    async def on_ready(self):
        print(f"Logged in as {self.user.name} id: {self.user.id}")
        await self.fetch_votes()

    async def fetch_votes(self):
        while True:
            print("Fetching vote messages.")
            await self.wait_until_ready()
            self.ready = False

            channel = self.get_channel(807289103920922684)  # voting channel

            messages = []

            start_dt = datetime.datetime(2021, 2, 5, 16, 40, 47)
            end_dt = datetime.datetime(2021, 2, 5, 17, 55, 27)

            async for message in channel.history(after=start_dt, before=end_dt, limit=1000):
                # print(message.id, message.created_at, message.content)
                messages.append(message)

            self.valid_message_ids = [message.id for message in messages]

            for message in messages:
                # print(message)
                key = str(message.id)  # socketio glitch(?) workaround (last 2 digits go to 0)
                self.votes[key] = {"game": message.content, "yay": 0, "yay_voters": []}

                for reaction in message.reactions:
                    self.votes[key]["yay"] = reaction.count
                    reactors = await reaction.users().flatten()
                    for reactor in reactors:
                        # print(reactor.name, reactor.avatar_url)
                        self.voters[key] = {reactor.id: {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}
            self.votes["partial"] = False
            await sio.emit("votes_discord", data=self.votes, namespace="/gamevotes")
            print("Done fetching votes")
            self.ready = True
            await asyncio.sleep(900)

    async def count_change(self, reaction, count):
        if reaction.message_id in self.valid_message_ids:
            key = str(reaction.message_id)
            if key in self.votes:
                while not self.ready:
                    await asyncio.sleep(1)  # lol workaround
                self.votes[key]["yay"] = self.votes[key].get("yay", 0) + count
                user = self.get_user(reaction.user_id)
                user_data = {
                    "name": user.name,
                    "avatar_url": user.avatar_url._url,
                }
                if count > 0:
                    self.voters[key][user.id] = user_data
                else:
                    self.voters[key][user.id] = user_data
                vote_data = {
                    "message_id": key,
                    "game": self.votes[key]["game"],
                    "yay": self.votes[key]["yay"],
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
