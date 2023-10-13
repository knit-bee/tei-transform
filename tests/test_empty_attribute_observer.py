import unittest

from lxml import etree

from tei_transform.observer import EmptyAttributeObserver


class EmptyAttributeObserverTester(unittest.TestCase):
    def test_configure_observer(self):
        observer = EmptyAttributeObserver()
        cfg = {"target": ["first", "second", "third"]}
        observer.configure(cfg)
        self.assertEqual(observer.target_attributes, ["first", "second", "third"])

    def test_observer_not_configured_if_config_wrong(self):
        observer = EmptyAttributeObserver()
        cfg = {}
        observer.configure(cfg)
        self.assertEqual(observer.target_attributes, [])

    def test_invalid_config_triggers_logger_warning(self):
        observer = EmptyAttributeObserver()
        cfg = {}
        with self.assertLogs() as logger:
            observer.configure(cfg)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.empty_attribute_observer:"
                "Invalid configuration for EmptyAttributeObserver."
            ],
        )
