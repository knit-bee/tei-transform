import unittest
from importlib import metadata

from tei_transform.observer import FilenameElementObserver
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
