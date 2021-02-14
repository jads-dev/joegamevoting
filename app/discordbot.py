import asyncio
import datetime
import json
import os

import discord

from discord.ext import tasks

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
        self.weeb_games = None
        self.extra_messages = [
            809130993507237919,  # votos
            809131104320618546,
            809131123099041832,
            809131141776015472,
            809131166321213471,
            809131185569005598,
            809410955880562701,  # kill purple chan
            809535003406893082,  # hug purple chan
            810207947661508608,  # Davina Cage
            807308502921904158,  # fire emblem
        ]
        self.pending_votes = []

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

        self.vote_sweep.start()
        self.vote_sweep_changed.start()
        self.save.start()
        self.send_changes.start()

    @tasks.loop(seconds=900)
    async def vote_sweep(self):
        await self.fetch_all()

    @tasks.loop(seconds=10)
    async def vote_sweep_changed(self):
        await self.fetch_changed()

    @tasks.loop(seconds=60)
    async def save(self):
        self.save_data()

    @tasks.loop(seconds=0.2)
    async def send_changes(self):
        if self.pending_votes:
            await sio.emit("votes_discord_partial", data=self.pending_votes, namespace="/gamevotes")
            self.pending_votes = []

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
                if not self.votos_time:
                    _votos_time = None
                else:
                    _votos_time = self.votos_time.isoformat()

                data = {"votes": self.votes, "voters": self.voters, "votos_time": _votos_time}
                json.dump(data, f)
        except IOError:
            print("Error saving votes")

    async def get_weeb(self):
        weeb_games_data = get_weeb_games()
        _weeb_games = {}
        for game in weeb_games_data:
            _weeb_games[str(game["message_id"])] = game["weeb_status"]
        self.weeb_games = _weeb_games

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

    def parse_emoji(self, emoji, emoji_unicode=None):
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

    def is_same_emoji(self, emoji_a, emoji_b, a_is_parsed=False):
        if emoji_a is None or emoji_b is None:
            return False
        if a_is_parsed:
            _emoji_a = emoji_a
        else:
            _emoji_a, _emoji_a_unicode = self.parse_emoji(emoji_a)

        _emoji_b, _emoji_b_unicode = self.parse_emoji(emoji_b)

        return _emoji_a == _emoji_b

    async def check_votos(self):
        if "809130993507237919" in self.votes:
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
            _vote = {
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

            if key in self.weeb_games:
                _vote["weeb_status"] = self.weeb_games[key]

            if type(message.reactions[0].emoji) is str:
                _vote["emote"] = message.reactions[0].emoji
                _vote["emote_unicode"] = True
                _vote["upvote_emoji"] = str(message.reactions[0].emoji)
            else:
                _vote["emote"] = str(message.reactions[0].emoji.id)
                _vote["emote_unicode"] = False
                _vote["upvote_emoji"] = message.reactions[0].emoji.id

            reaction = message.reactions[0]
            _vote["yay"] = reaction.count

            if len(message.reactions) > 1:
                _vote["downvote_emoji"] = str(message.reactions[1].emoji)
                if type(message.reactions[1].emoji) is str:
                    _vote["emote2"] = message.reactions[1].emoji
                    _vote["emote2_unicode"] = True
                    _vote["downvote_emoji"] = str(message.reactions[1].emoji)
                else:
                    _vote["emote2"] = str(message.reactions[1].emoji.id)
                    _vote["emote2_unicode"] = False
                    _vote["downvote_emoji"] = message.reactions[1].emoji.id

                reaction = message.reactions[1]
                _vote["nay"] = reaction.count

            for reaction in message.reactions[2:]:
                if type(reaction.emoji) is str:
                    emote_unicode = True
                    emote = reaction.emoji
                else:
                    emote_unicode = False
                    emote = str(reaction.emoji.id)
                _vote["nay"] += reaction.count
                _vote["extra_emotes"].append({"emote_unicode": emote_unicode, "emote": emote, "count": reaction.count})

            # check votos
            await self.check_votos()
            self.votes[key] = _vote

    async def parse_message_voters(self, message):
        key = str(message.id)
        if len(message.reactions) > 0:
            reaction = message.reactions[0]
            reactors = await reaction.users().flatten()
            for reactor in reactors:
                # print(reactor.name, reactor.avatar_url)
                # await self.check_valid(reactor)
                self.voters[key] = {str(reactor.id): {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}

        # if len(message.reactions) > 1:
        #     reaction = message.reactions[1]
        #     reactors = await reaction.users().flatten()
        #     for reactor in reactors:
        #         # print(reactor.name, reactor.avatar_url)
        #         # await self.check_valid(reactor)
        #         self.downvoters[key] = {reactor.id: {"name": reactor.name, "avatar_url": reactor.avatar_url._url} for reactor in reactors}

    async def fetch_changed(self):
        self.ready = False
        _changed = set(self.changed)
        await self.get_weeb()
        for message_id in _changed:
            key = str(message_id)
            try:
                message = await self.channel.fetch_message(id=message_id)
            except discord.errors.NotFound:
                print(f"Failed to fetch {message_id}")
                if message_id in self.extra_messages:
                    self.extra_messages.remove(message_id)
                continue

            vote_data = {
                "message_id": key,
            }

            vote_data.update(self.votes[key])

            self.pending_votes.append(vote_data)

        for message_id in _changed:
            key = str(message_id)
            try:
                message = await self.channel.fetch_message(id=message_id)
            except discord.errors.NotFound:
                print(f"Failed to fetch {message_id}")
                if message_id in self.extra_messages:
                    self.extra_messages.remove(message_id)
                continue
            await self.parse_message_voters(message)

        self.changed = []
        self.ready = True

    async def fetch_all(self):
        print("Fetching vote messages.")
        await self.wait_until_ready()
        await self.get_weeb()
        self.ready = False

        messages = []

        start_dt = datetime.datetime(2021, 2, 5, 16, 40, 47)
        end_dt = datetime.datetime(2021, 2, 5, 17, 55, 27)

        _failed = []
        for message_id in self.extra_messages:
            try:
                message = await self.channel.fetch_message(message_id)
            except discord.errors.NotFound:
                print(f"Failed to fetch {message_id}")
                _failed.append(message_id)
                continue
            messages.append(message)

        for message_id in _failed:
            self.extra_messages.remove(message_id)

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

        self.ready = True
        print("Done fetching votes")
        await sio.emit("votes_discord", data=self.votes, namespace="/gamevotes")

        print("Fetching voter data.")
        for message in messages:
            await self.parse_message_voters(message)
        print("Done fetching voter data.")
        self.save_data()

    async def count_change(self, reaction):
        if reaction.message_id in self.valid_message_ids:
            key = str(reaction.message_id)
            if key in self.votes:
                change = 0
                if reaction.event_type == "REACTION_ADD":
                    change = 1
                elif reaction.event_type == "REACTION_REMOVE":
                    change = -1

                upvote = self.is_same_emoji(self.votes[key]["upvote_emoji"], reaction.emoji)
                downvote = self.is_same_emoji(self.votes[key]["downvote_emoji"], reaction.emoji)

                for extra_emoji in self.votes[key]["extra_emotes"]:
                    if self.is_same_emoji(extra_emoji["emote"], reaction.emoji, a_is_parsed=True):
                        extra_emoji["count"] += change
                        downvote = True

                if upvote:
                    self.votes[key]["yay"] += change
                if downvote:
                    self.votes[key]["nay"] += change

                vote_data = {
                    "message_id": key,
                }

                vote_data.update(self.votes[key])

                self.pending_votes.append(vote_data)

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

    async def on_raw_message_edit(self, message):
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
