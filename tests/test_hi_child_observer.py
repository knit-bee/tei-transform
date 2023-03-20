import unittest

from lxml import etree

from tei_transform.observer import HiChildObserver


class HiChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HiChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><hi>text<p/></hi></p>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<p><hi>text<hi/></hi></p>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p>a<hi>b<p>c</p>d</hi></p>"),
            etree.XML("<div><p><hi>text<p/>text</hi></p></div>"),
            etree.XML("<p><hi rendition='#b'>ab<p>cd</p></hi></p>"),
            etree.XML("<div><p>text<hi>text<p>abc</p></hi></p></div>"),
            etree.XML("<div><p>text</p><p><hi>ab<p>cd</p>ef</hi></p></div>"),
            etree.XML("<div><hi>ab<p/>cd</hi></div>"),
            etree.XML("<TEI xmlns='a'><div><hi><p>text</p></hi></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<hi>text<p>text</p></hi></p></TEI>"),
            etree.XML("<TEI xmlns='a'><p>a</p><p>b<hi>c<p>d</p>e</hi></p></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text<hi>text</hi></p>"),
            etree.XML("<p><hi>ab</hi>text<hi>cd<hi>ef</hi></hi></p>"),
            etree.XML("<div><p>ab<hi>cd</hi></p><hi>text</hi></div>"),
            etree.XML("<div><p><hi>ab<hi>cd</hi></hi></p></div>"),
            etree.XML("<div><p><hi><fw>text</fw></hi></p></div>"),
            etree.XML("<div><p><hi>text<quote/></hi></p></div>"),
            etree.XML("<div><p/><p>ab<hi>cd</hi>ef<hi/></p></div>"),
            etree.XML("<TEI xmlns='a'><div><p>text<hi>ab</hi>text</p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p><hi/></p><hi>text</hi></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p><hi>text</hi><p/></p></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
