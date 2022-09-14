from champion import Champion


class BaseChampionCatalog(object):
    champs = [Champion()]


class BaseChampionSelectStrategy(object):
    def __init__(self, champion_catalog: BaseChampionCatalog = BaseChampionCatalog()):
        self.champion_catalog = champion_catalog

    def select(self):
        return self.champion_catalog.champs[0]


class ChampSelector(object):
    def __init__(
            self,
            selection_strategy: BaseChampionSelectStrategy = BaseChampionSelectStrategy(),
            champion_catalog: BaseChampionCatalog = BaseChampionCatalog()
    ):
        self.select = selection_strategy
        self.available_champs = champion_catalog

    def select(self):
        champion = self.select(self.available_champs)