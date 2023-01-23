import random
import unittest
from importlib import metadata

from tei_transform.observer import (
    DivParentObserver,
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

    def test_div_parent_observer_always_at_front(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure div-parent is in plugin list
            if "div-parent" not in plugins_to_use:
                plugins_to_use.append("div-parent")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0], DivParentObserver))
