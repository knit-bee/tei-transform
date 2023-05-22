import os
import random
import unittest
from importlib import metadata

from tei_transform.abstract_node_observer import AbstractNodeObserver
from tei_transform.observer import (
    DivParentObserver,
    DivSiblingObserver,
    DoublePlikeObserver,
    FilenameElementObserver,
    LinebreakTextObserver,
    PParentObserver,
    UnfinishedElementObserver,
)
from tei_transform.observer_constructor import (
    InvalidObserver,
    MissingConfiguration,
    ObserverConstructor,
)
from tei_transform.parse_config import parse_config_file
from tests.mock_observer import MockConfigurableObserver, add_mock_plugin_entry_point


class ObserverConstructorTester(unittest.TestCase):
    def setUp(self):
        self.constructor = ObserverConstructor()
        self.cfg_dir = os.path.join("tests", "testdata", "conf_files")
        self.default_cfg = parse_config_file(os.path.join(self.cfg_dir, "default.cfg"))

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
            observer_list = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
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
            observer_list = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0][0], DivParentObserver))

    def test_observers_sorted_in_two_lists(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        first_pass, second_pass = self.constructor.construct_observers(
            plugins, self.default_cfg
        )
        self.assertTrue(isinstance(first_pass, list) and isinstance(second_pass, list))
        self.assertTrue(
            all(
                isinstance(observer, AbstractNodeObserver)
                for observer in first_pass + second_pass
            )
        )

    def test_only_allowed_observers_in_second_list(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # make sure div-sibling pluings are in list
            if "div-sibling" not in plugins_to_use:
                plugins_to_use.append("div-sibling")
            random.shuffle(plugins_to_use)
            _, second_pass = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertEqual(
                    set(
                        type(observer)
                        in {
                            DivSiblingObserver,
                            UnfinishedElementObserver,
                        }
                        for observer in second_pass
                    ),
                    {True},
                )

    def test_div_sibling_observers_in_not_in_first_list(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(3, len(plugins)))
            # make sure div-sibling pluings are in list
            if "div-sibling" not in plugins_to_use:
                plugins_to_use.append("div-sibling")
            random.shuffle(plugins_to_use)
            first_pass, _ = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertEqual(
                    set(
                        isinstance(observer, DivSiblingObserver)
                        for observer in first_pass
                    ),
                    {False},
                )

    def test_second_observer_list_empty_if_second_pass_observers_not_used(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            # remove div-sibling plugins from list
            plugins_to_use = [
                plugin
                for plugin in plugins_to_use
                if plugin not in {"div-sibling", "unfinished-elem"}
            ]
            random.shuffle(plugins_to_use)
            _, second_pass = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertEqual([], second_pass)

    def test_observer_initialized_with_configuration(self):
        constructor = ObserverConstructor()
        config = parse_config_file(os.path.join(self.cfg_dir, "config"))
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockConfigurableObserver",
        )
        test_observer = constructor.construct_observers(["mock"], config)[0][0]
        self.assertEqual(test_observer.attribute, "some value")

    def test_error_raised_if_observer_requires_config_but_missing(self):
        config = parse_config_file(os.path.join(self.cfg_dir, "filename.cfg"))
        constructor = ObserverConstructor()
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockObserverConfigRequired",
        )
        with self.assertRaises(MissingConfiguration):
            constructor.construct_observers(["mock"], config)

    def test_error_raised_if_observer_requires_config_but_no_config_passed(self):
        constructor = ObserverConstructor()
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockObserverConfigRequired",
        )
        with self.assertRaises(MissingConfiguration):
            constructor.construct_observers(["mock"])

    def test_construction_of_observer_with_optional_config_if_no_config_passed(self):
        constructor = ObserverConstructor()
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockConfigurableObserver",
        )
        test_observer = constructor.construct_observers(["mock"])[0][0]
        self.assertIsNone(test_observer.attribute)

    def test_config_only_added_to_matching_observer(self):
        constructor = ObserverConstructor()
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockConfigurableObserver",
        )
        config = parse_config_file(os.path.join(self.cfg_dir, "mock.cfg"))
        observers = constructor.construct_observers(
            ["mock", "filename-element"], config
        )
        self.assertEqual(hasattr(observers[0][1], "attribute"), False)
        self.assertEqual(observers[0][0].attribute, "value")

    def test_unnecessary_config_ignored(self):
        constructor = ObserverConstructor()
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockConfigurableObserver",
        )
        config = parse_config_file(os.path.join(self.cfg_dir, "mock.cfg"))
        observers = constructor.construct_observers(["mock"], config)
        mock_observer = observers[0][0]
        self.assertEqual(mock_observer.attribute, "value")

    def test_config_for_non_configurable_observer_ignored(self):
        config = parse_config_file(os.path.join(self.cfg_dir, "filename.cfg"))
        test_observer = self.constructor.construct_observers(
            ["filename-element"], config
        )[0][0]
        self.assertTrue(isinstance(test_observer, FilenameElementObserver))

    def test_configuration_of_observer_skipped_if_not_in_config_file(self):
        config = parse_config_file(os.path.join(self.cfg_dir, "filename.cfg"))
        constructor = ObserverConstructor()
        add_mock_plugin_entry_point(
            constructor,
            "mock",
            "tests.mock_observer:MockConfigurableObserver",
        )
        test_observer = constructor.construct_observers(["mock"], config)[0][0]
        self.assertTrue(isinstance(test_observer, MockConfigurableObserver))

    def test_p_parent_added_last(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            if "p-parent" not in plugins_to_use:
                plugins_to_use.append("p-parent")
            plugins_to_use = [
                plugin for plugin in plugins_to_use if plugin != "double-plike"
            ]
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0][-1], PParentObserver))

    def test_p_parent_added_second_to_last_if_double_p_like_present(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            if "double-plike" not in plugins_to_use:
                plugins_to_use.append("double-plike")
            if "p-parent" not in plugins_to_use:
                plugins_to_use.append("p-parent")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0][-2], PParentObserver))

    def test_lb_text_moved_to_front(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            if "lb-text" not in plugins_to_use:
                plugins_to_use.append("lb-text")
            plugins_to_use = [
                plugin for plugin in plugins_to_use if plugin != "div-parent"
            ]
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0][0], LinebreakTextObserver))

    def test_lb_text_in_second_place_if_div_parent_present(self):
        plugins = list(self.constructor.plugins_by_name.keys())
        for _ in range(10):
            plugins_to_use = random.sample(plugins, random.randint(1, len(plugins)))
            if "lb-text" not in plugins_to_use:
                plugins_to_use.append("lb-text")
            if "div-parent" not in plugins_to_use:
                plugins_to_use.append("div-parent")
            random.shuffle(plugins_to_use)
            observer_list = self.constructor.construct_observers(
                plugins_to_use, self.default_cfg
            )
            with self.subTest():
                self.assertTrue(isinstance(observer_list[0][1], LinebreakTextObserver))
