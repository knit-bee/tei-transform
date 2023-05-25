import unittest

from lxml import etree

from tei_transform.observer import TermContentObserver


class TermContentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TermContentObserver(term_content="Target")

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<keywords><term>Hello</term></keywords>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<keywords><term>Target</term></keywords>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<textClass><keywords><term>,</term></keywords></textClass>"),
            etree.XML("<keywords><term>text</term><term>text2</term></keywords>"),
            etree.XML("<textClass><keywords><term/></keywords></textClass>"),
            etree.XML(
                "<textClass><keywords><term>Target</term><term>,</term></keywords></textClass>"
            ),
            etree.XML(
                "<textClass><keywords><term>text</term><term>Target</term></keywords></textClass>"
            ),
            etree.XML("<textClass><keywords><term>text</term></keywords></textClass>"),
            etree.XML(
                "<TEI xmlns='a'><textClass><keywords><term/></keywords></textClass></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><textClass><keywords><term>,</term></keywords></textClass></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><textClass><keywords><term>text</term><term/></keywords></textClass></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><textClass><keywords><term>text</term><term>Target</term></keywords></textClass></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<keywords><term>Target</term></keywords>"),
            etree.XML("<keywords/>"),
            etree.XML("<keywords><term>Target</term><term>text</term></keywords>"),
            etree.XML("<TEI xmlns='a'><keywords><term>Target</term></keywords></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><keywords><term>Target</term><term>text</term></keywords></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><keywords><term>Target</term><term>text</term><term>text2</term></keywords></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_configure_observer(self):
        observer = TermContentObserver()
        cfg = {"content": "Target"}
        observer.configure(cfg)
        self.assertEqual(observer.term_content, "Target")

    def test_observer_not_configured_if_config_wrong(self):
        observer = TermContentObserver()
        cfg = {"term": "Target"}
        observer.configure(cfg)
        self.assertIsNone(observer.term_content)

    def test_invalid_config_triggers_logger_warning_missing_key(self):
        cfg = {"term": "Target"}
        observer = TermContentObserver()
        with self.assertLogs() as logger:
            observer.configure(cfg)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.term_content_observer:"
                "Invalid configuration for TermContentObserver"
            ],
        )

    def test_invalid_config_triggers_logger_warning_missing_value(self):
        cfg = {"content": ""}
        observer = TermContentObserver()
        with self.assertLogs() as logger:
            observer.configure(cfg)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.term_content_observer:"
                "Invalid configuration for TermContentObserver"
            ],
        )
