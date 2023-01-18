import random
import unittest
from importlib import metadata

from tei_transform.observer import (
    DoublePlikeObserver,
    FilenameElementObserver,
    PAsDivSiblingObserver,
)
from tei_transform.observer_constructor import InvalidObserver, ObserverConstructor


class ObserverConstructorTester(unittest.TestCase):
    def setUp(self):
        self.constructor = ObserverConstructor()

    def test_observer_construction(self):
        test_observer = self.constructor.construct_observers(["filename-element"])[0]
        self.assertTrue(isinstance(test_observer, FilenameElementObserver))

    def test_exception_raised_if_observer_is_not_registered_as_plugin(self):
        self.assertRaises(
            InvalidObserver, self.constructor.construct_observers, ["fake-observer"]
        )

    def test_exception_raised_if_observer_is_invalid(self):
        self.constructor.plugins_by_name["fake-observer"] = metadata.EntryPoint(
            name="fake-observer",
            group="node-observer",
            value="tests.test_tei_transformer:FakeObserver",
        )
        self.assertRaises(
            InvalidObserver, self.constructor.construct_observers, ["fake-observer"]
        )

    def test_p_as_div_sibling_observer_always_added_last(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure p-div-sibling is in plugin list
            if "p-div-sibling" not in plugins_to_use:
                plugins_to_use.append("p-div-sibling")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertTrue(isinstance(observer_list[-1], PAsDivSiblingObserver))

    def test_double_p_like_observer_added_last_if_p_div_sibling_not_present(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure double-plike is in plugin list
            plugins_to_use = [
                plugin for plugin in plugins_to_use if plugin != "p-div-sibling"
            ]
            if "double-plike" not in plugins_to_use:
                plugins_to_use.append("double-plike")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertTrue(isinstance(observer_list[-1], DoublePlikeObserver))

    def test_double_p_like_observer_added_second_to_last_if_p_div_sibling_present(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure double-plike and p-div-sibling are in plugin list
            if "double-plike" not in plugins_to_use:
                plugins_to_use.append("double-plike")
            if "p-div-sibling" not in plugins_to_use:
                plugins_to_use.append("p-div-sibling")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertTrue(isinstance(observer_list[-2], DoublePlikeObserver))
