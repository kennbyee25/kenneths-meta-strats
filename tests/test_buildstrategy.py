import unittest

from buildstrategy import BuildStrategy, GenericBuildStrategy


class TestBuildStrategy(unittest.TestCase):

    def test_base_build_strategy_generate_build(self):
        builder = BuildStrategy()

        build = builder.generate_build()

        self.assertIsNotNone(build)

    def test_random_build_strategy_generate_build(self):
        builder = GenericBuildStrategy()

        build = builder.generate_build()

        self.assertIsNotNone(build)


if __name__ == "__main__":
    unittest.main()
