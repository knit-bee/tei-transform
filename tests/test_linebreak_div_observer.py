import unittest

from lxml import etree

from tei_transform.observer import LinebreakDivObserver


class LinebreakDivObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LinebreakDivObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><lb/>text</div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><lb/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><p>text</p><lb/>tail</div>"),
            etree.XML("<div><lb/>a<list/></div>"),
            etree.XML(
                "<body><div><div><head/><lb/>a<p>text<lb/>tail</p></div></div></body>"
            ),
            etree.XML("<div><p>text<lb/>tail</p>tail<lb/>tail</div>"),
            etree.XML("<div><p/><div><p/><lb/>tail</div></div>"),
            etree.XML("<TEI xmlns='a'><body><div><lb/>tail</div></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><div><p>text<lb/>tail</p><lb/>tl</div></body></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p><lb/>tail</p><lb/>tail<list/></div></TEI>"
            ),
        ]

        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p>text<lb/>tail</p></div>"),
            etree.XML("<p><lb/>tail</p>"),
            etree.XML("<div><lb/><p/></div>"),
            etree.XML("<div><lb/><p>text</p><lb/></div>"),
            etree.XML("<body><div><lb/><p>text</p></div></body>"),
            etree.XML("<p>text<lb/>tail<div/></p>"),
            etree.XML("<div><p><hi>text<lb/>ab</hi></p><p/>tail</div>"),
            etree.XML("<TEI xmlns='a'><text><div><p>text</p><lb/></div></text></TEI>"),
            etree.XML("<TEI xmlns='a'><body><lb/>tail<div><lb/></div></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><lb/><p>tex</p><p><lb/>tail</p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
