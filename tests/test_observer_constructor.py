import random
import unittest
from importlib import metadata

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.observer import (
    DivParentObserver,
    DivSiblingObserver,
    DoublePlikeObserver,
    FilenameElementObserver,
    PAsDivSiblingObserver,
)
from tei_transform.observer_constructor import InvalidObserver, ObserverConstructor


class ObserverConstructorTester(unittest.TestCase):
    def setUp(self):
        self.constructor = ObserverConstructor()

    def test_observer_construction(self):
        test_observer = self.constructor.construct_observers(["filename-element"])[0][0]
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

    def test_double_p_like_observer_added_last(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            if "double-plike" not in plugins_to_use:
                plugins_to_use.append("double-plike")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0][-1], DoublePlikeObserver))

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
                self.assertTrue(isinstance(observer_list[0][0], DivParentObserver))

    def test_observers_sorted_in_two_lists(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        first_pass, second_pass = self.constructor.construct_observers(plugins)
        self.assertTrue(isinstance(first_pass, list) and isinstance(second_pass, list))
        self.assertTrue(
            all(
                isinstance(observer, AbstractNodeObserver)
                for observer in first_pass + second_pass
            )
        )

    def test_div_sibling_observers_in_second_list(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure div-sibling pluings are in list
            if "div-sibling" not in plugins_to_use:
                plugins_to_use.append("div-sibling")
            if "p-div-sibling" not in plugins_to_use:
                plugins_to_use.append("p-div-sibling")
            random.shuffle(plugins_to_use)
            _, second_pass = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertEqual(
                    set(
                        isinstance(observer, PAsDivSiblingObserver)
                        or isinstance(observer, DivSiblingObserver)
                        for observer in second_pass
                    ),
                    {True},
                )

    def test_div_sibling_observers_in_not_in_first_list(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure div-sibling pluings are in list
            if "div-sibling" not in plugins_to_use:
                plugins_to_use.append("div-sibling")
            if "p-div-sibling" not in plugins_to_use:
                plugins_to_use.append("p-div-sibling")
            random.shuffle(plugins_to_use)
            first_pass, _ = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertEqual(
                    set(
                        isinstance(observer, PAsDivSiblingObserver)
                        or isinstance(observer, DivSiblingObserver)
                        for observer in first_pass
                    ),
                    {False},
                )

    def test_second_observer_list_empty_if_div_sibling_plugins_not_used(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # remove div-sibling plugins from list
            plugins_to_use = [
                plugin
                for plugin in plugins_to_use
                if plugin not in {"p-div-sibling", "div-sibling"}
            ]
            if "double-plike" not in plugins_to_use:
                plugins_to_use.append("double-plike")
            random.shuffle(plugins_to_use)
            _, second_pass = self.constructor.construct_observers(plugins_to_use)
            with self.subTest():
                self.assertEqual([], second_pass)
