import unittest
from importlib import metadata

from tei_transform.observer import FilenameElementObserver
from tei_transform.observer_constructor import InvalidObserver, ObserverConstructor


class ObserverConstructorTester(unittest.TestCase):
    def test_observer_construction(self):
        constructor = ObserverConstructor()
        test_observer = constructor.construct_observers(["filename-element"])[0]
        self.assertTrue(isinstance(test_observer, FilenameElementObserver))

    def test_exception_raised_if_observer_is_not_registered_as_plugin(self):
        constructor = ObserverConstructor()
        self.assertRaises(
            InvalidObserver, constructor.construct_observers, ["fake-observer"]
        )

    def test_exception_raised_if_observer_is_invalid(self):
        constructor = ObserverConstructor()
        constructor.plugins_by_name["fake-observer"] = metadata.EntryPoint(
            name="fake-observer",
            group="node-observer",
            value="tests.test_tei_transformer:FakeObserver",
        )
        self.assertRaises(
            InvalidObserver, constructor.construct_observers, ["fake-observer"]
        )
