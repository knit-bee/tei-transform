import unittest

from lxml import etree

from tei_transform.observer import LonelySObserver


class LonelySObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelySObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<body><s>text</s></body>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<body><p><s>text</s></p></body>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<body><p/><s>text</s></body>"),
            etree.XML("<div><s><l>text</l></s></div>"),
            etree.XML("<body><list/><s>text<w/></s></body>"),
            etree.XML("<div>text<s>text</s><p><s/></p></div>"),
            etree.XML("<TEI xmlns='a'><div><p/><s><w/></s></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/><s>text</s><p/></body></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/><div><p/><s/></div></body></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p><s/></p>"),
            etree.XML("<div><p><s>text<w/></s></p></div>"),
            etree.XML("<body><p>text<s>text</s></p></body>"),
            etree.XML("<div><p>text<s><w>text</w></s></p></div>"),
            etree.XML("<TEI xmlns='a'><body><p><s>text</s></p></body></TEI>"),
            etree.XML("<TEI xmlns='a'><div><quote><s/></quote></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><head><s>text</s></head></body></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
