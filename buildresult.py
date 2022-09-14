from champion import Champion
from itemlist import ItemList


class BuildResult(object):
    def __init__(self, item_list: ItemList = ItemList(), champion: Champion = Champion()):
        self.items = item_list
        self.champion = champion
