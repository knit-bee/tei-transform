import unittest

from lxml import etree

from tei_transform.observer import MisusedOpenerObserver


class MisusedOpenerObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MisusedOpenerObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p/><opener/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><opener/><p/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><p/><opener>text</opener></div>"),
            etree.XML("<div><ab/><opener/></div>"),
            etree.XML("<body><p/><opener/></body>"),
            etree.XML("<body><list/><opener>text</opener></body>"),
            etree.XML("<div><p/><opener>abc</opener><dateline/><p/></div>"),
            etree.XML("<div><p/><head/><opener/></div>"),
            etree.XML("<div><head/><p/><opener/></div>"),
            etree.XML("<TEI xmlns='a'><div><p/><opener>text</opener></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/><opener/></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><text><body><ab/><dateline/><opener/></body></text></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><head/><opener/></div>"),
            etree.XML("<div><dateline/><opener/></div>"),
            etree.XML("<div><opener><dateline/></opener></div>"),
            etree.XML("<div><head/><opener><name/></opener></div>"),
            etree.XML("<list><opener/><item/></list>"),
            etree.XML("<div><opener>text</opener><dateline/><p/></div>"),
            etree.XML("<body><opener/><p/></body>"),
            etree.XML("<div><argument/><opener/></div>"),
            etree.XML("<div><byline/><opener/></div>"),
            etree.XML("<div><docDate/><opener/></div>"),
            etree.XML("<div><docAuthor/><opener/></div>"),
            etree.XML("<div><epigraph/><opener/></div>"),
            etree.XML("<div><signed/><opener/></div>"),
            etree.XML("<div><meeting/><opener/></div>"),
            etree.XML("<div><salute/><opener/></div>"),
            etree.XML("<div><opener/><opener/></div>"),
            etree.XML("<div><fw/><opener/></div>"),
            etree.XML("<body><fw/><opener>text</opener><p/></body>"),
            etree.XML("<body><head/><opener/><dateline/></body>"),
            etree.XML("<list><head/><opener/><item/></list>"),
            etree.XML("<div><p/><opener><dateline/></opener></div>"),
            etree.XML("<TEI xmlns='a'><div><p/><opener><daline/></opener></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><opener/><p/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><head/><opener/></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><p/><head/><opener><name/></opener></body></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
