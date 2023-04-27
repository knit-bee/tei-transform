import unittest

from lxml import etree

from tei_transform.observer import DelChildObserver


class DelChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DelChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<del><p/></del>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><del/><p/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<p>text<del>b<p>c</p>d</del></p>"),
            etree.XML("<div><p><del>text<p/>text</del><list/></p></div>"),
            etree.XML("<p>text<del rend='overstrike'>ab<p>cd</p></del></p>"),
            etree.XML("<div><p>text<del>text<p/></del></p></div>"),
            etree.XML("<div><p>text</p><p><del>ab<p>cd</p>ef</del>text</p></div>"),
            etree.XML("<div><p/><del>ab<p/>cd</del><p/><p/></div>"),
            etree.XML("<TEI xmlns='a'><div><del><p>text</p></del></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<del>text<p>text</p></del></p></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><p>a</p><p>b<del>c<p>d</p>e</del>text<list/></p></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text<del>text<quote/></del></p>"),
            etree.XML("<p>text<del>ab</del>text<del>cd<hi>ef</hi></del></p>"),
            etree.XML("<div><p>ab<del>cd</del></p><del>text</del></div>"),
            etree.XML("<div><p>text<del>ab<hi>cd</hi></del></p></div>"),
            etree.XML("<div><p>text<del>text<fw>text</fw></del></p></div>"),
            etree.XML("<div><p><del>text<quote/></del>tail</p></div>"),
            etree.XML("<div><p/><p>ab<del>cd</del>ef<del/></p></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<del>ab<quote/></del>text</p></div></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><p>txt<del/></p><del>text</del></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p><del>text</del>tail<p/></p></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
