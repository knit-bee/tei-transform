import unittest

from lxml import etree

from tei_transform.div_text_observer import DivTextObserver


class DivTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<div>text</div>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_nonmatching_element(self):
        node = etree.XML("<div/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div>some text<p>more text</p></div>"),
            etree.XML("<div><div>text</div></div>"),
            etree.XML(
                "<text><body><div><div><p/></div><div>text</div></div></body></text>"
            ),
            etree.XML(
                """<TEI><teiHeader/>
            <text><body><div>text<p>more text</p></div></body></text>
            </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                     <text><body><div>text<p>more text</p></div></body></text>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p>text</p></div>"),
            etree.XML("<div><p/></div>"),
            etree.XML("<div><div><p>text</p></div></div>"),
            etree.XML("<div><fw>header</fw>tail<p/></div>"),
            etree.XML("<div><p>text</p>text<p>more text</p></div>"),
            etree.XML(
                """<TEI><teiHeader/><text>
            <body><div><p>text></p></div></body>
            </text></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='namespace'>
            <teiHeader/>
            <text>
            <body><div><div><p>text</p>text2</div></div></body>
            </text>
            </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
