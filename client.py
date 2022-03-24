import discord
import random
import io
import urllib3
import json
from utils import display_recommendation, zipf_algo, random_build, historical_build
from config import *


class Client(discord.Client):

    def __init__(self):
        super().__init__()
        self.send_png = True
        self.cmd = 'kms'
        self.latest = "11.17.1"  # TODO set automatically

        self.http2 = urllib3.PoolManager(num_pools=NUM_POOLS)
        self.load_data()

    def load_data(self):
        # print("getting data")
        # update ddragon versions (should kinda always do this i think?)

        with open("versions.json", "w") as f:
            r = self.http2.request('GET', URL_VERSIONS)
            data = r.data.decode('utf-8')
            self.latest = json.loads(data)[0]

            f.write(data)

        # get champions.json
        # TODO save this file instead of getting every single time
        url_champions = f"http://ddragon.leagueoflegends.com/cdn/{self.latest}/data/en_US/champion.json"
        r = self.http2.request("GET", url_champions)
        self.champions_data = json.loads(r.data.decode('utf-8'))["data"]

    def get_champion_by_id(self, id):
        for c, v in self.champions_data.items():
            if v["key"] == str(id):
                return v["id"]

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(self.cmd):
            summ = message.content[len(self.cmd):]
            if not summ:  # empty 2nd arg
                champ = self.generate_recommendation()
            else:
                if summ[0] != ' ':
                    return
                summ = summ[1:]
                rec = self.generate_recommendation(summ)
                champ = rec["champion"]
                build = rec["build"]  #generate_build_recommendation(summ, champ)
                flavor_index = random.randrange(0, len(flavor_verbs))
            str_msg = f"{rec['name']} will {flavor_verbs[flavor_index]} while playing {champ}"
            if self.send_png:
                with io.BytesIO() as output:
                    output = display_recommendation(champ, build, output)
                    f = discord.File(output, filename='Capture.PNG')
                    embed = discord.Embed()
                    embed.set_image(url="attachment://Capture.PNG")
                await message.channel.send(str_msg, file=f)
            else:
                await message.channel.send(str_msg)

    async def on_ready(self):
        print("Logged in as", self.user)

    # TODO: add docstring
    def generate_recommendation(self, name="", region="na1", champ_algo="zipf", build_algo="hist"):
        rec = {}

        champ_algo_switch = {
            "zipf": zipf_algo,
        }

        build_algo_switch = {
            "rng": random_build,
            "hist": historical_build,
        }

        # get summoner
        if name:
            url = URL_SUMM + name + KEY
            r = self.http2.request('GET', url)
            if not r.status == 200:
                print("ERROR:", r.status)
                if r.status == 403:
                    print("Is your API key valid?")
                return
                # TODO raise exception
            summ_data = json.loads(r.data.decode('utf-8'))
            summ_id = summ_data['id']
            rec["name"] = summ_data['name']
            print(name, summ_data)

        champ_id = champ_algo_switch[champ_algo](self.http2, summ_id)
        build = build_algo_switch[build_algo](self.http2, summ_data['puuid'])
        rec["champion"] = self.get_champion_by_id(champ_id)
        # print(champ_id)
        # print(build)
        rec["build"] = build
        return rec


client = Client()
client.run(TOKEN)
