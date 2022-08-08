import unittest

from lxml import etree

from tei_transform.tei_namespace_observer import TeiNamespaceObserver


class TeiNamespaceObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TeiNamespaceObserver()

    def test_observer_returns_false_for_any_node(self):
        elements = [
            etree.XML("<TEI xmlns='http://www.tei-c.org/ns/1.0'></TEI>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><teiHeader/><text/></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                <teiHeader><fileDesc>text</fileDesc></teiHeader>
                <text>some text</text>
                </TEI>"""
            ),
            etree.XML("<teiHeader/>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))
