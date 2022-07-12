import unittest

from lxml import etree

from tei_transform.observer_constructor import check_if_observer_pattern_is_valid_xpath
from tei_transform.teiheader_observer import TeiHeaderObserver


class TeiHeaderObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TeiHeaderObserver()

    def test_observer_pattern_is_valid_xpath(self):
        result = check_if_observer_pattern_is_valid_xpath(self.observer.xpattern)
        self.assertTrue(result)

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<teiHeader type='text'></teiHeader>")
        self.assertTrue(self.observer.observe(node))

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<teiHeader/>")
        self.assertFalse(self.observer.observe(node))

    def test_observer_identifies_matching_element_in_tree(self):
        matching_elements = [
            etree.XML("<teiHeader type='val'/>"),
            etree.XML("<TEI><teiHeader type='val'><titleStmt/></teiHeader></TEI>"),
            etree.XML(
                "<TEI><teiHeader type='val'><titleStmt><title/></titleStmt></teiHeader></TEI>"
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<teiHeader></teiHeader>"),
            etree.XML("<TEI><teiHeader><titleStmt/></teiHeader></TEI>"),
            etree.XML(
                "<TEI><teiHeader id='val'><titleStmt><title/></titleStmt></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI><tei type='val'><titleStmt><title/></titleStmt></tei></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))
