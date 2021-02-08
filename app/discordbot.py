import asyncio
import datetime
import json
import os

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
        self.downvoters = {}
        self.last_random = None
        self.channel = None
        self.load_data()

    async def on_ready(self):
        print(f"Logged in as {self.user.name} id: {self.user.id}")
        self.channel = self.get_channel(807289103920922684)  # voting channel
        await self.fetch_votes()

    def load_data(self):
        base_dir = "./data/votes"
        files = [f"{base_dir}/{file}" for file in os.listdir(base_dir) if file.endswith(".json")]
        if files:
            latest = max(files, key=os.path.getctime)
            try:
                with open(latest, "r") as f:
                    data = json.load(f)
                self.votes = data["votes"]
                self.voters = data["voters"]
            except IOError:
                print("Error loading votes")

    def save_data(self):
        base_filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base_dir = "./data/votes"
        os.makedirs(base_dir, exist_ok=True)

        filename = f"{base_dir}/{base_filename}.json"
        try:
            with open(filename, "w") as f:
                data = {"votes": self.votes, "voters": self.voters}
                json.dump(data, f)
        except IOError:
            print("Error saving votes")

    async def parse_message(self, message):
        # print(message)
        key = str(message.id)  # socketio glitch(?) workaround (last 2 digits go to 0)

        if len(message.reactions) > 0:
            if type(message.reactions[0].emoji) is str:
                emote_unicode = True
                emote = message.reactions[0].emoji
            else:
                emote_unicode = False
                emote = str(message.reactions[0].emoji.id)

            self.votes[key] = {
                "game": message.content,
                "yay": 0,
                "nay": 0,
                "emote_unicode": emote_unicode,
                "emote": emote,
                "emote2_unicode": True,
                "emote2": "",
                "extra_emotes": [],
            }

            reaction = message.reactions[0]
            self.votes[key]["yay"] = reaction.count
            reactors = await reaction.users().flatten()
            for reactor in reactors:
                # print(reactor.name, reactor.avatar_url)
                self.voters[key] = {reactor.id: {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}

            if len(message.reactions) > 1:
                if type(message.reactions[1].emoji) is str:
                    emote2_unicode = True
                    emote2 = message.reactions[1].emoji
                else:
                    emote2_unicode = False
                    emote2 = str(message.reactions[1].emoji.id)
                reaction = message.reactions[1]
                self.votes[key]["nay"] = reaction.count
                self.votes[key]["emote2_unicode"] = emote2_unicode
                self.votes[key]["emote2"] = emote2
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    # print(reactor.name, reactor.avatar_url)
                    self.downvoters[key] = {reactor.id: {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}

            for reaction in message.reactions[2:]:
                if type(reaction.emoji) is str:
                    emote_unicode = True
                    emote = reaction.emoji
                else:
                    emote_unicode = False
                    emote = str(reaction.emoji.id)
                self.votes[key]["extra_emotes"].append({"emote_unicode": emote_unicode, "emote": emote})

    async def fetch_votes(self):
        while True:
            print("Fetching vote messages.")
            await self.wait_until_ready()

            messages = []

            start_dt = datetime.datetime(2021, 2, 5, 16, 40, 47)
            end_dt = datetime.datetime(2021, 2, 5, 17, 55, 27)

            async for message in self.channel.history(after=start_dt, before=end_dt, limit=1000):
                # print(f"{message.id}\t{message.created_at}\t{message.content}")
                messages.append(message)

            self.valid_message_ids = [message.id for message in messages]

            for message in messages:
                await self.parse_message(message)

            if "partial" in self.votes:
                del self.votes["partial"]

            for key in list(self.votes):
                if int(key) not in self.valid_message_ids:
                    del self.votes[key]

            self.votes["partial"] = False

            print("Done fetching votes")
            self.save_data()
            await sio.emit("votes_discord", data=self.votes, namespace="/gamevotes")

            await asyncio.sleep(900)

    async def count_change(self, reaction, add=True):
        if reaction.message_id in self.valid_message_ids:
            key = str(reaction.message_id)
            if key in self.votes:
                message = await self.channel.fetch_message(id=reaction.message_id)
                await self.parse_message(message)

                user = self.get_user(reaction.user_id)
                user_data = {
                    "name": user.name,
                    "avatar_url": user.avatar_url._url,
                }
                if add:
                    self.voters[key][user.id] = user_data
                else:
                    if user.id in self.voters[key]:
                        del self.voters[key][user.id]

                vote_data = {
                    "message_id": key,
                    "game": self.votes[key]["game"],
                    "yay": self.votes[key]["yay"],
                    "nay": self.votes[key]["yay"],
                    "partial": True,
                }

                await sio.emit("votes_discord", data=vote_data, namespace="/gamevotes")

    async def on_raw_reaction_add(self, reaction):
        await self.count_change(reaction, add=True)

    async def on_raw_reaction_remove(self, reaction):
        await self.count_change(reaction, add=False)

    async def on_raw_message_delete(self, message):
        if str(message.message_id) in self.votes:
            del self.votes[str(message.message_id)]


bot = DiscordBot(intents=intents)


async def can_vote(user_id):
    guild = bot.get_guild(308515582817468420)
    user = guild.get_member(user_id)
    if not user:
        return
    else:
        return any(role.id in allowed_roles for role in user.roles)
