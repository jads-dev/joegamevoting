import asyncio
import datetime
import json
import os

import discord

from app.routers.socketio import sio
from app.models.game_discord import get_weeb_games


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
    309517708309954560,  # mods
]

extra_messages = [
    809130993507237919,  # votos
    809131104320618546,
    809131123099041832,
    809131141776015472,
    809131166321213471,
    809131185569005598,
    809410955880562701,  # kill purple chan
    809535003406893082,  # hug purple chan
]


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.valid_message_ids = []
        self.votes = {}
        self.voters = {}
        self.downvoters = {}
        self.last_random = None
        self.guild = None
        self.channel = None
        self.changed = []
        self.last_scan = None
        self.last_save = None
        self.ready = True
        self.load_data()
        self.votos_time = None

        # self.clean_up()

        self.known_invalid = []
        self.recent_members = []

    async def on_ready(self):
        print(f"Logged in as {self.user.name} id: {self.user.id}")
        self.guild = self.get_guild(308515582817468420)  # JADS
        self.channel = self.get_channel(807289103920922684)  # voting channel

        cut_date = datetime.datetime(2021, 2, 9, 19, 0, 0)
        members = await self.guild.fetch_members(limit=None, after=cut_date).flatten()
        self.recent_members = [member.id for member in members]

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
                try:
                    self.votos_time = datetime.datetime.fromisoformat(data.get("votos_time", ""))
                except (ValueError, TypeError):
                    self.votos_time = None
            except IOError:
                print("Error loading votes")

    def clean_up(self):
        self.votes = {}
        self.voters = {}

    def save_data(self):
        base_filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        base_dir = "./data/votes"
        os.makedirs(base_dir, exist_ok=True)

        filename = f"{base_dir}/{base_filename}.json"
        try:
            with open(filename, "w") as f:
                data = {"votes": self.votes, "voters": self.voters, "votos_time": self.votos_time}
                json.dump(data, f)
        except IOError:
            print("Error saving votes")

    async def check_weeb(self):
        weeb_games = get_weeb_games()

        for game in weeb_games:
            key = str(game["message_id"])
            if key in self.votes:
                self.votes[key]["weeb_status"] = game["weeb_status"]

    def get_games_by_user(self, user_id):
        _user_id = str(user_id)
        game_ids = []
        for game in self.voters:
            if _user_id in self.voters[game]:
                game_ids.append(game)
        return sorted(game_ids)

    async def check_valid(self, reactor):
        if reactor.id in self.known_invalid:
            return True

        if reactor.id in self.recent_members:
            self.known_invalid.append(reactor.id)
            games = self.get_games_by_user(reactor.id)
            with open("ripfun.txt", "a") as f:
                f.write(f"{reactor.id};{reactor.name};Member joined after cut-off date;{reactor.created_at};{len(games)};{games}\n")
            return True

        if type(reactor) is discord.User:  # User was returned, most likely no longer in server
            try:
                member = await self.guild.fetch_member(reactor.id)  # asking the server just to make sure
            except discord.errors.NotFound:
                self.known_invalid.append(reactor.id)
                # print(f"{reactor.id};{reactor.name};Member not in guild; ")
                return False
        else:
            member = reactor

        valid = False
        for role in member.roles:
            if role.id in allowed_roles:
                valid = True

        if not valid:
            self.known_invalid.append(reactor.id)
            # print(f"{reactor.id};{reactor.name};No matching server role found; ")
            return False
        return False

    def parse_emoji(self, emoji):
        if type(emoji) is str:
            _emoji = emoji
            _emoji_unicode = True
        elif type(emoji) is int:
            _emoji = str(emoji)
            _emoji_unicode = False
        elif type(emoji) is discord.partial_emoji.PartialEmoji:
            _emoji_unicode = emoji.is_unicode_emoji()
            if _emoji_unicode:
                _emoji = emoji.name
            else:
                _emoji = str(emoji.id)
        else:
            _emoji = str(emoji.id)
            _emoji_unicode = False
        return _emoji, _emoji_unicode

    def is_same_emoji(self, emoji_a, emoji_b):
        if emoji_a is None or emoji_b is None:
            return False

        _emoji_a, _emoji_a_unicode = self.parse_emoji(emoji_a)
        _emoji_b, _emoji_b_unicode = self.parse_emoji(emoji_b)

        return _emoji_a == _emoji_b

    async def check_votos(self):
        if self.votes["809130993507237919"]["yay"] > 400 and self.votos_time is None:
            self.votos_time = datetime.datetime.now()
            await sio.emit("votos_time", data=self.votos_time.isoformat(), namespace="/gamevotes")
        if self.votes["809130993507237919"]["yay"] <= 400 and self.votos_time is not None:
            self.votos_time = None
            await sio.emit("votos_time", data=self.votos_time, namespace="/gamevotes")

    async def parse_message(self, message):
        # print(message)
        key = str(message.id)  # socketio glitch(?) workaround (last 2 digits go to 0)

        if len(message.reactions) > 0:
            self.votes[key] = {
                "game": message.content,
                "yay": 0,
                "nay": 0,
                "emote_unicode": None,
                "emote": None,
                "emote2_unicode": True,
                "emote2": "",
                "extra_emotes": [],
                "upvote_emoji": None,
                "downvote_emoji": None,
            }

            if type(message.reactions[0].emoji) is str:
                self.votes[key]["emote"] = message.reactions[0].emoji
                self.votes[key]["emote_unicode"] = True
                self.votes[key]["upvote_emoji"] = str(message.reactions[0].emoji)
            else:
                self.votes[key]["emote"] = str(message.reactions[0].emoji.id)
                self.votes[key]["emote_unicode"] = False
                self.votes[key]["upvote_emoji"] = message.reactions[0].emoji.id

            reaction = message.reactions[0]
            self.votes[key]["yay"] = reaction.count
            reactors = await reaction.users().flatten()
            for reactor in reactors:
                # print(reactor.name, reactor.avatar_url)
                # await self.check_valid(reactor)
                self.voters[key] = {str(reactor.id): {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}

            # check votos
            if key == "809130993507237919":
                await self.check_votos()

            if len(message.reactions) > 1:
                self.votes[key]["downvote_emoji"] = str(message.reactions[1].emoji)
                if type(message.reactions[1].emoji) is str:
                    self.votes[key]["emote2"] = message.reactions[1].emoji
                    self.votes[key]["emote2_unicode"] = True
                    self.votes[key]["downvote_emoji"] = str(message.reactions[1].emoji)
                else:
                    self.votes[key]["emote2"] = str(message.reactions[1].emoji.id)
                    self.votes[key]["emote2_unicode"] = False
                    self.votes[key]["downvote_emoji"] = message.reactions[1].emoji.id

                reaction = message.reactions[1]
                self.votes[key]["nay"] = reaction.count
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    # print(reactor.name, reactor.avatar_url)
                    # await self.check_valid(reactor)
                    self.downvoters[key] = {reactor.id: {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}

            for reaction in message.reactions[2:]:
                if type(reaction.emoji) is str:
                    emote_unicode = True
                    emote = reaction.emoji
                else:
                    emote_unicode = False
                    emote = str(reaction.emoji.id)
                self.votes[key]["extra_emotes"].append({"emote_unicode": emote_unicode, "emote": emote})

    async def fetch_changed(self):
        self.ready = False
        _changed = set(self.changed)
        await self.check_weeb()
        for message_id in _changed:
            key = str(message_id)
            message = await self.channel.fetch_message(id=message_id)
            await self.parse_message(message)

            vote_data = {
                "message_id": key,
                "partial": True,
            }

            vote_data.update(self.votes[key])

            await sio.emit("votes_discord", data=vote_data, namespace="/gamevotes")
        self.changed = []
        self.ready = True

    async def fetch_all(self):
        print("Fetching vote messages.")
        await self.wait_until_ready()
        self.ready = False

        messages = []

        start_dt = datetime.datetime(2021, 2, 5, 16, 40, 47)
        end_dt = datetime.datetime(2021, 2, 5, 17, 55, 27)

        for message_id in extra_messages:
            message = await self.channel.fetch_message(message_id)
            messages.append(message)

        async for message in self.channel.history(after=start_dt, before=end_dt, limit=1000):
            # print(f"{message.id}\t{message.created_at}\t{message.content}")
            messages.append(message)

        self.valid_message_ids = [message.id for message in messages]

        for message in messages:
            await self.parse_message(message)
            await self.fetch_changed()  # more responsive

        if "partial" in self.votes:
            del self.votes["partial"]

        for key in list(self.votes):
            if int(key) not in self.valid_message_ids:
                del self.votes[key]

        self.votes["partial"] = False
        self.ready = True
        print("Done fetching votes")
        await self.check_weeb()
        self.save_data()

        await sio.emit("votes_discord", data=self.votes, namespace="/gamevotes")

    async def fetch_votes(self):
        while True:
            if self.last_scan is None or self.last_scan < datetime.datetime.now() - datetime.timedelta(seconds=900):
                await self.fetch_all()
                self.last_scan = datetime.datetime.now()
                self.last_save = datetime.datetime.now()
            else:
                await self.fetch_changed()
            if self.last_save is None or self.last_save < datetime.datetime.now() - datetime.timedelta(seconds=60):
                self.save_data()
                self.last_save = datetime.datetime.now()

            await asyncio.sleep(20)

    async def count_change(self, reaction):
        if reaction.message_id in self.valid_message_ids:
            key = str(reaction.message_id)
            if key in self.votes:
                upvote = self.is_same_emoji(self.votes[key]["upvote_emoji"], reaction.emoji)
                downvote = self.is_same_emoji(self.votes[key]["downvote_emoji"], reaction.emoji)
                change = 0
                if reaction.event_type == "REACTION_ADD":
                    change = 1
                elif reaction.event_type == "REACTION_REMOVE":
                    change = -1
                if upvote:
                    self.votes[key]["yay"] += change
                if downvote:
                    self.votes[key]["nay"] += change

                vote_data = {
                    "message_id": key,
                    "partial": True,
                }

                vote_data.update(self.votes[key])

                await sio.emit("votes_discord", data=vote_data, namespace="/gamevotes")
                await self.check_votos()

                while not self.ready:
                    await asyncio.sleep(1)
                self.changed.append(reaction.message_id)

    async def on_raw_reaction_add(self, reaction):
        await self.count_change(reaction)

    async def on_raw_reaction_remove(self, reaction):
        await self.count_change(reaction)

    async def on_raw_message_delete(self, message):
        if str(message.message_id) in self.votes:
            del self.votes[str(message.message_id)]

    async def on_raw_message_delete(self, message):
        if str(message.message_id) in self.votes:
            self.changed.append(message.message_id)


bot = DiscordBot(intents=intents)


async def can_vote(user_id):
    guild = bot.get_guild(308515582817468420)
    user = guild.get_member(user_id)
    if not user:
        return
    else:
        return any(role.id in allowed_roles for role in user.roles)
