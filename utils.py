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
def random_build():
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