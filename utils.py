from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from config import *
import numpy as np
import json
import random

def display_recommendation(champ, build, buf):
    VERSION = "11.13.1"
    # TODO this is where an image is generated, should also add to the image here
    # print(champ)
    fn = f'{champ}_0.jpg'
    fp = Path(r"img\champion\splash").joinpath(fn)
    img = Image.open(fp)

    # add to the image (package in a function TODO)
    # background for items
    w, h = img.size
    shape = [(40, 40), (w // 3, h - 40)]
    img1 = ImageDraw.Draw(img)
    img1.rectangle(shape, fill="#000000", outline="white")

    # add items
    for i, (item_id, text) in enumerate(build):
        if item_id and int(item_id) > 0:
            fn = f'{item_id}.png'
            fp = Path(rf"{VERSION}\img\item").joinpath(fn)

            item = Image.open(fp)
            font = ImageFont.truetype(r".\resources\Friz-Quadrata-Font\Friz Quadrata Bold.otf", 20)
            offset = 72 * i
            img1.text((122, 50 + offset), text, font=font)

            img.paste(item, (50, 50 + offset))

    img.save(buf, "png")
    buf.seek(0)
    return buf


# TODO this should be a class method
def zipf_algo(http, id):
    # get mastery data

    url = URL_MAST + id + KEY
    r = http.request('GET', url)
    if r.status == 200:  # success
        mast_data = json.loads(r.data.decode('utf-8'))
        n = len(mast_data)
        mast_recent_idx = np.flip(np.argsort([x["lastPlayTime"] for x in mast_data]))
        mast_recent = np.array(mast_data)[mast_recent_idx]
    else:
        print(r.status)

    # suggest a champion by weight - zipf on mastery or on most recent
    zipf_idx = int(np.exp(random.random() * np.log(n)))
    if random.random() > RECENT_WEIGHT:
        champ = mast_recent[zipf_idx]
    else:
        champ = mast_data[zipf_idx]
    champ_id = champ["championId"]
    return champ_id

# TODO this should be a class method
def random_build(http, puuid):
    latest = "11.13.1"  # TODO this should be a class variable

    # TODO this should be stored in a class
    with open(rf"{latest}\data\en_US\item.json", "r") as f:
        js = json.load(f)
    items = js["data"]
    item_ids = list(items.keys())

    n = len(items)
    rng = np.random.randint(0, n, 6)
    build_ids = [item_ids[i] for i in rng]
    return [(i, items[i]["name"]) for i in build_ids]

def historical_build(http, puuid):
    latest = "11.13.1"
    URL_MATCHES_BY_PUUID = API_BASEURL + f'/lol/match/v5/matches/by-puuid/{puuid}/ids' + KEY
    r = http.request('GET', URL_MATCHES_BY_PUUID)
    if r.status == 200:  # success
        match_ids = json.loads(r.data.decode('utf-8'))
        n = len(match_ids)
        if n > 0:
            matchId = match_ids[np.random.randint(0, len(match_ids))]  # most recent
            URL_MATCH_BY_MATCHID = API_BASEURL + f'/lol/match/v5/matches/{matchId}' + KEY
            # TODO: request is a bottleneck
            r = http.request('GET', URL_MATCH_BY_MATCHID)
            if r.status == 200:  # success
                match = json.loads(r.data.decode('utf-8'))
                build = [str(match['info']['participants'][np.random.randint(0, 10)][f'item{n}']) for n in range(6)]
                # TODO this should be stored in a class
                with open(rf"{latest}\data\en_US\item.json", "r") as f:
                    js = json.load(f)
                items = js["data"]

                with open("complete_items.txt", "r") as f:
                    fstring = f.read()
                if fstring:
                    complete_items = fstring.split(',')
                else:
                    complete_items = []

                # replace incomplete items with complete
                ok_list = []
                for i, item_id in enumerate(build):
                    with open("no_conflict.json", "r") as f:
                        no_conflict = json.load(f)

                    if item_id and item_id in complete_items:  # item OK
                        ok_list.append(item_id)
                    elif len(items.get(item_id, {}).get("from", [])) > 0\
                            and len(items.get(item_id, {"into": [None]}).get("into", [])) == 0:
                        # is a mythic or legendary that is not kept track of
                        complete_items.append(item_id)  # add to list
                        with open("complete_items.txt", "a") as f:
                            f.write(f",{item_id}")  # update list
                    else:
                        # change item to a complete item
                        # grab random item from complete_items list
                        # valid_count_dict: {item_id: count}
                        valid_count_dict = {}
                        for j in range(i):  # iterate through existing items
                            candidate_items = no_conflict.get(build[i], [])  # list of items that have no conflict
                            for candidate_item in candidate_items:
                                # add to count of non-conflicts
                                valid_count_dict[candidate_item] = valid_count_dict.get(candidate_item, 0) + 1
                        valid_ids = []
                        valid_counts = []
                        for id, count in valid_count_dict.items():
                            valid_ids.append(id)
                            valid_counts.append(count)

                        sort_idxs = np.argsort(valid_counts)
                        if len(sort_idxs) > 0:
                            new_item = valid_ids[sort_idxs[0]]
                        elif complete_items:
                            new_item = complete_items[random.randint(0, len(complete_items))]
                        else:
                            new_item = ''
                        build[i] = new_item

                rewrite = False
                if len(ok_list) > 1:
                    for i, item1 in enumerate(ok_list[:-1]):
                        for item2 in ok_list[i+1:]:
                            if item2 not in no_conflict.get(item1, []):
                                no_conflict[item1] = no_conflict.get(item1, []) + [item2]
                                if not item1 == item2:
                                    no_conflict[item2] = no_conflict.get(item2, []) + [item1]
                                rewrite = True
                if rewrite:
                    with open("no_conflict.json", "w") as f:
                        json.dump(no_conflict, f)


                return [(i, items.get(i, {}).get("name", "")) for i in build]
            else:
                print(f"ERROR {r.status} FOR REQUEST: {URL_MATCH_BY_MATCHID}")
        else:
            return random_build(http, puuid)
    else:
        print(f"ERROR {r.status} FOR REQUEST: {URL_MATCHES_BY_PUUID}")