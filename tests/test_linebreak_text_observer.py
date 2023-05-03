import unittest

from lxml import etree

from tei_transform.observer import LinebreakTextObserver


class LinebreakTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LinebreakTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><lb>text</lb></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<p>text<lb/>tail</p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p>text<lb>text2</lb></p>"),
            etree.XML("<div><lb>text</lb>tail</div>"),
            etree.XML("<p>text<hi>a<lb>   b </lb>tail</hi></p>"),
            etree.XML("<TEI xmlns='a'><div><p/><lb>text</lb></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p>text<lb>a</lb>b</p></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text<lb/>tail<lb/></p>"),
            etree.XML("<p>text<hi/>tail<lb/>tail></p>"),
            etree.XML("<div><p>text<lb>  </lb>tail</p></div>"),
            etree.XML("<p>text<lb>  \n\t</lb></p>"),
            etree.XML("<div><p>text</p><lb/>tail<lb/>tail</div>"),
            etree.XML("<TEI xmlns='a'><div><p>text<lb/>tail</p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<lb>  </lb>tail</p></TEI>"),
            etree.XML("<TEI xmlns='a'><body><lb/>tail<p>a<lb/>b</p></body></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
