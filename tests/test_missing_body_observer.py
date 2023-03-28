import unittest

from lxml import etree

from tei_transform.observer import MissingBodyObserver


class MissingBodyObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MissingBodyObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<TEI><text><p/></text></TEI>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<TEI><text><body><p/></body></text></TEI>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<text><front/></text>"),
            etree.XML("<text><fw/><front/><back/></text>"),
            etree.XML("<text><group><text/></group></text>"),
            etree.XML("<text><back/></text>"),
            etree.XML("<text><p>text</p></text>"),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><p/></text></TEI>"),
            etree.XML("<TEI xmlns='a'><text><front/><back/></text></TEI>"),
            etree.XML("<TEI xmlns='a'><text><group><text/></group></text></TEI>"),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><front/><note/></text></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<text><body/></text>"),
            etree.XML("<text><front/><body/><back/></text>"),
            etree.XML("<text><group><text><body/></text></group></text>"),
            etree.XML("<text><front/><body><p/></body></text>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><front/><body/><back/></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><text><group><text><body/></text></group></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><front/><body><p/></body></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body/></text><text><body/></text></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
