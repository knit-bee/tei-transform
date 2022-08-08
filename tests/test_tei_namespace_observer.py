import unittest

from lxml import etree

from tei_transform.tei_namespace_observer import TeiNamespaceObserver


class TeiNamespaceObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TeiNamespaceObserver()

    def test_observer_returns_true_for_matching_node(self):
        node = etree.XML("<TEI/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_not_matching_nodes(self):
        node = etree.XML("<TEI xmlns='http://www.tei-c.org/ns/1.0'/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_finds_matching_nodes(self):
        matching_elements = [
            etree.XML("<TEI></TEI>"),
            etree.XML("<TEI><teiHeader/><text/></TEI>"),
            etree.XML(
                "<TEI><teiHeader><fileDesc>text</fileDesc></teiHeader><text>some text</text></TEI>"
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<TEI xmlns='http://www.tei-c.org/ns/1.0'></TEI>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><teiHeader/><text/></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><teiHeader><fileDesc>text</fileDesc></teiHeader><text>some text</text></TEI>"
            ),
            etree.XML("<teiHeader/>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))
