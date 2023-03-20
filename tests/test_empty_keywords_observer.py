import unittest

from lxml import etree

from tei_transform.observer import EmptyKeywordsObserver


class EmptyKeywordsObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyKeywordsObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<textClass><keywords/></textClass>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML(
            "<textClass><keywords><term>Term</term></keywords></textClass>"
        )
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<textclass><keywords/></textclass>"),
            etree.XML("<textClass><classCode/><keywords></keywords></textClass>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><textClass><keywords/></textClass></teiHeader></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><textclass><keywords/></textclass></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML(
                "<textClass><keywords><term>a</term><term>b</term></keywords></textClass>"
            ),
            etree.XML("<textclass><keywords><list/></keywords></textclass>"),
            etree.XML(
                "<textClass><classCode/><keywords><term>A</term></keywords></textClass>"
            ),
            etree.XML(
                "<TEI xmlns='a'><textClass><keywords><term>Term</term></keywords></textClass></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><textclass><classcode/><keywords><term/></keywords></textclass></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><textClass><keywords><list/></keywords></textClass></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
