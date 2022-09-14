class Champion(object):
    def __init__(self):
        self.champion_name = ""
        self.champion_id = 0

    def __init__(self, champion_name: str = "", champion_id: int = 0):
        self.champion_name = champion_name
        self.champion_id = champion_id

    def __str__(self):
        return self.champion_name
