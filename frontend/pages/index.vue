<template>
  <v-row class="mt-4">
    <template v-if="official">
      <v-col cols="12" class="align-center">
        <v-row>
          <v-col cols="12">
            <p class="text-center ma-0">{{ stats.nr_voters }} voters have voted on {{ stats.nr_games }} games</p>
            <p class="text-center ma-0" v-if="stats.votes_average">Average of all votes: {{ stats.votes_average.toFixed(2) }}</p>
            <p class="text-center ma-0">Median of all votes: {{ stats.votes_median }}</p>
          </v-col>
        </v-row>
        <v-expansion-panels>
          <v-expansion-panel>
            <v-expansion-panel-header> Base rules </v-expansion-panel-header>
            <v-expansion-panel-content>
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/807712044555436052/unknown.png" /><img />
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header> Feb 6 rules </v-expansion-panel-header>
            <v-expansion-panel-content>
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/807711737406160997/unknown.png" /><img />
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header> Feb 7 rules (Updated 2:44PM EST) (2nd update 9:52PM EST) </v-expansion-panel-header>
            <v-expansion-panel-content>
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808011604447854592/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808011756386910223/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808012036189061150/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808061001144336414/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808169342097162322/unknown.png" /><img />
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header> Feb 8 rules (Updated 2:13PM EST)</v-expansion-panel-header>
            <v-expansion-panel-content>
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808371582460362762/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808371734948085770/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808451208024424479/unknown.png" /><img />
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header> Feb 9 changes</v-expansion-panel-header>
            <v-expansion-panel-content>
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808766895476965467/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/808790132437155840/unknown.png" /><img />
            </v-expansion-panel-content>
          </v-expansion-panel>
          <v-expansion-panel>
            <v-expansion-panel-header> Feb 10 changes</v-expansion-panel-header>
            <v-expansion-panel-content>
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/809265332060946462/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/809116104206581790/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/809116751765438504/unknown.png" /><img />
              <img src="https://cdn.discordapp.com/attachments/648620063045189656/809139404462882856/unknown.png" /><img />
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
      <v-col cols="12" md="6">
        <v-card class="mt-2">
          <v-card-title> Latest Pitches </v-card-title>
          <v-card-text>
            <v-card outlined elevation="12" class="mt-3" v-for="pitch in latest_pitches" :key="`pitch-latest-${pitch.user_id}-${pitch.message_id}`">
              <v-card-title
                @click="goto_game(pitch)"
                style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap; cursor: pointer"
                class="ma-0 pa-0 ml-2"
              >
                {{ pitch.game_name }}
              </v-card-title>
              <v-row>
                <v-col class="pr-0" cols="2">
                  <v-img @click="goto_game(pitch)" style="cursor: pointer" class="mt-1 ml-1 mr-1 pa-0" max-width="100%" :src="pitch.cover_url_big"></v-img>
                </v-col>
                <v-col class="pl-0 mt-1 pr-5 pb-5" cols="10">
                  <v-card outlined elevation="12" :style="pitch.pinned ? 'border: 1px solid green;' : ''">
                    <div class="text-center my-n3" v-if="pitch.pinned">
                      <span class="px-1" :style="pitch.pinned ? 'color: green; background: #1E1E1E' : ''"> Pinned </span>
                    </div>
                    <v-card-text style="white-space: pre-wrap">{{ pitch.pitch }}</v-card-text>
                    <v-card-title class="justify-center">
                      <v-avatar left size="35">
                        <v-img :src="pitch.avatar_url" :alt="pitch.username"></v-img>
                      </v-avatar>
                      <span class="ml-1">{{ pitch.username }}</span>
                    </v-card-title>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6" class="px-1">
        <v-card class="mt-2">
          <v-card-title> Random Pitches </v-card-title>
          <v-card-text>
            <v-card outlined elevation="12" class="mt-3" v-for="pitch in random_pitches" :key="`pitch-random-${pitch.user_id}-${pitch.message_id}`">
              <v-card-title
                @click="goto_game(pitch)"
                style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap; cursor: pointer"
                class="ma-0 pa-0 ml-2"
              >
                {{ pitch.game_name }}
              </v-card-title>
              <v-row>
                <v-col class="pr-0" cols="2">
                  <v-img @click="goto_game(pitch)" style="cursor: pointer" class="mt-1 ml-1 mr-1 pa-0" max-width="100%" :src="pitch.cover_url_big"></v-img>
                </v-col>
                <v-col class="pl-0 mt-1 pr-5 pb-5" cols="10">
                  <v-card outlined elevation="12" :style="pitch.pinned ? 'border: 1px solid green;' : ''">
                    <div class="text-center my-n3" v-if="pitch.pinned">
                      <span class="px-1" :style="pitch.pinned ? 'color: green; background: #1E1E1E' : ''"> Pinned </span>
                    </div>
                    <v-card-text style="white-space: pre-wrap">{{ pitch.pitch }}</v-card-text>
                    <v-card-title class="justify-center">
                      <v-avatar left size="35">
                        <v-img :src="pitch.avatar_url" :alt="pitch.username"></v-img>
                      </v-avatar>
                      <span class="ml-1">{{ pitch.username }}</span>
                    </v-card-title>
                  </v-card>
                </v-col>
              </v-row>
            </v-card>
          </v-card-text>
        </v-card>
      </v-col>
    </template>
    <template v-else>
      <v-col cols="12">
        <p class="text-h3 text-center">This is the fan poll, it is unofficial and fanmade and doesn't affect what Joe plays on stream at all!</p>
        <p class="text-h4 text-center">You can see the results of the official discord poll by click the switch on the top left.</p>
      </v-col>
      <v-col cols="12">
        <v-card>
          <p class="text-h4 text-center pt-2">Short Version:</p>
          <v-card-text class="text-center">
            <p class="text-h5 font-weight-bold">
              You need the patron/twitch sub role on discord or have more than 100 posts in #dragons-den before Jan 27 to be able to vote.
            </p>
            <p class="text-h5 font-weight-bold">The voting here is unofficial and just to gauge interest.</p>
            <p class="text-h5 font-weight-bold">You can vote on more than one game.</p>
            <p class="text-h6 font-weight-bold">You can add any game to the list by searching for it and voting on it.</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col>
        <v-card>
          <v-card-title class="headline">What's this? </v-card-title>
          <v-card-text>
            <p>
              This website is for people to vote on which game they would like for Joe to play on stream, the vote is merely symbolical and doesn't affect what
              joe plays on stream. This page is not officially endorsed by Joe (I haven't asked him) and should be treated as a fan page.
            </p>
            <p>
              On the left there should be a descending list of what people have voted on, this should be updated in real time. You can click on the games there
              to visit it's page and cast your own vote or use the search bar above. You can vote on more than one game. Votes are <b>NOT</b> anonymous.
            </p>
            <p>
              The available game list was fetched from igdb.com and does not include every game (like re-releases/remasters/collections/etc.) if there's a big
              one missing, you can ping me on discord
            </p>
            <p>
              Voting is restricted to people that have the twitch or patreon roles on discord. This is done to limit people manipulating votes with bots/etc. If
              you had more that 100 posts on #dragons-den before Jan 27, 2021 you can also vote.
            </p>
            <p>The site is probably a bit rough around the edges, but should be at the very minimum functional :P</p>
          </v-card-text>
        </v-card>
      </v-col>
    </template>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    random_pitches: [],
    stats: {},
    hall_ascension: [
      {
        message_id: "807308420104323103",
        name: "Zero Escape Series (999, Virtue's Last Reward, and Zero Time Dilemma)",
        emote_url: "https://cdn.discordapp.com/emojis/667825926507331604",
        votes: "306",
        extra_emotes: [],
      },
    ],
    headers: [
      { text: "votes", value: "votes", width: "80px" },
      { text: "game", value: "name" },
    ],
  }),
  created: async function () {
    const random_pitches = await this.$axios.$get("/api/game_discord/random_pitches/");
    this.random_pitches = random_pitches;

    if (this.official) {
      const stats = await this.$axios.$get("/api/game_discord/stats/");
      this.stats = stats;
    }
  },
  computed: {
    official: {
      get() {
        return this.$store.state.localStorage.official;
      },
      set(value) {},
    },
    latest_pitches: {
      get() {
        return this.$store.state.latest_pitches;
      },
      set(value) {},
    },
  },
  methods: {
    goto_game: async function (game) {
      this.$router.push({
        path: "/game_discord/" + game.message_id,
      });
    },
    get_bg_style: function (vote) {
      const percent = (vote.votes / this.hall_ascension[0].votes) * 100;
      var color = "#7289da";
      return {
        "background-image": `linear-gradient(to right,${color} ${percent}%,transparent ${percent}%)`,
      };
    },
  },
};
</script>
