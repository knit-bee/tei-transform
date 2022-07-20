import unittest
from importlib import metadata

import pytest

import tei_transform.observer_constructor as oc
from tei_transform.filename_element_observer import FilenameElementObserver

valid_patterns = [
    ".//element",
    "first/second",
    "element[@attr='something']",
    "element[@attr]",
    "first//subelement",
    ".//someelement[@attr]",
    "node/text()",
    "//*",
    "//*[contains(., sth)]",
    "../node",
    "//node/subelement[2]" "/node[@attr='val']/sub1[3]/sub2",
    "//element[not(@attr='value')]",
]
invalid_patterns = [
    r"\element",
    "/node/text text",
    "//*contains",
    "//*[contains()]",
    "element'",
    "//",
]


@pytest.mark.parametrize("pattern", valid_patterns)
def test_valid_pattern_returns_true(pattern):
    result = oc.check_if_observer_pattern_is_valid_xpath(pattern)
    assert result


@pytest.mark.parametrize("pattern", invalid_patterns)
def test_invalid_pattern_returns_false(pattern):
    result = oc.check_if_observer_pattern_is_valid_xpath(pattern)
    assert result is False


class ObserverConstructorTester(unittest.TestCase):
    def test_observer_construction(self):
        constructor = oc.ObserverConstructor()
        test_observer = constructor.construct_observers(["filename-element"])[0]
        self.assertTrue(isinstance(test_observer, FilenameElementObserver))

    def test_exception_raised_if_observer_is_not_registered_as_plugin(self):
        constructor = oc.ObserverConstructor()
        self.assertRaises(
            oc.InvalidObserver, constructor.construct_observers, ["fake-observer"]
        )

    def test_exception_raised_if_observer_is_invalid(self):
        constructor = oc.ObserverConstructor()
        constructor.plugins_by_name["fake-observer"] = metadata.EntryPoint(
            name="fake-observer",
            group="node-observer",
            value="tests.test_tei_transformer:FakeObserver",
        )
        self.assertRaises(
            oc.InvalidObserver, constructor.construct_observers, ["fake-observer"]
        )
