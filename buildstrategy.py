from buildresult import BuildResult
from champ_select import ChampSelector
from shop import Shop


class BuildStrategy:
    def __init__(self):
        self.build = BuildResult

    def generate_build(self, initial_build: BuildResult = None) -> BuildResult:
        """
        Generates a sequence of items, given an optional seed
        :param initial_build:
        :return:
        """
        return self.build


class GenericBuildStrategy(BuildStrategy):
    def __init__(self, champ_selector: ChampSelector = ChampSelector(), item_builder: ItemBuilder = ItemBuilder()):
        self.build = BuildResult()
        self.champ_selector = champ_selector
        self.item_builder = item_builder

    def generate_build(self, initial_build: BuildResult = None) -> BuildResult:
        return self.build
