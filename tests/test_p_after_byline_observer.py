import unittest

from lxml import etree

from tei_transform.observer import PAfterBylineObserver


class PAfterBylineObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = PAfterBylineObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<div><byline/><p/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<div><p/><byline/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<div><p>text</p><byline>author</byline><p/></div>"),
            etree.XML("<div><p/><p/><p/><byline/><p>text</p></div>"),
            etree.XML("<text><div><p/><byline/><p/></div></text>"),
            etree.XML(
                "<div><p>text</p><byline><docAuthor>name</docAuthor></byline><p/></div>"
            ),
            etree.XML(
                "<div><div><p>text</p><byline>author</byline></div><div><p/><byline/><p/></div></div>"
            ),
            etree.XML("<text><div><div><head/><p/><byline/><p/></div></div></text>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><byline/><p>text</p></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<div><p/><byline/></div>"),
            etree.XML("<text><div><byline>author</byline></div></text>"),
            etree.XML("<div><p/><p/><byline/></div>"),
            etree.XML("<list><item/><byline/></list>"),
            etree.XML("<text><div><div><head/><p/><byline/></div><p/></div></text>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><p/><byline/></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><p/><byline/></div><div><p/></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
