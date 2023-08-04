import unittest

from lxml import etree

from tei_transform.observer import UParentObserver


class UParentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = UParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><u/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><u/><p/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<p><u who='a'>text</u></p>"),
            etree.XML("<div><p><u>text</u></p></div>"),
            etree.XML("<body><p><u/></p><p>text</p></body>"),
            etree.XML("<p>text<u>text</u>tail</p>"),
            etree.XML("<div><p/><p><u>text</u></p></div>"),
            etree.XML("<TEI xmlns='a'><div><p><u>text</u></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p>text<u/>tail</p></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><p><u who='a'>text</u></p><p/></body></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p/><u/></div>"),
            etree.XML("<div><u>text</u></div>"),
            etree.XML("<body><div><p/><u who='a'>text</u></div></body>"),
            etree.XML("<body><u>text</u><u/><u/></body>"),
            etree.XML("<body><div><u>text</u></div></body>"),
            etree.XML("<body><u>text</u>tail</body>"),
            etree.XML("<TEI xmlns='a'><div><p/><u>text</u></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><head/><u who='a'>ab</u><u/><u/></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
