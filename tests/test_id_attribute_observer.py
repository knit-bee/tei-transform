import unittest

from lxml import etree

from tei_transform.id_attribute_observer import IdAttributeObserver
from tei_transform.observer_constructor import check_if_observer_pattern_is_valid_xpath


class FilenameElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = IdAttributeObserver()

    def test_observer_pattern_is_valid_xpath(self):
        result = check_if_observer_pattern_is_valid_xpath(self.observer.xpattern)
        self.assertTrue(result)

    def test_observer_identifies_matching_element_in_tree(self):
        matching_elements = [
            etree.XML("<element id='value'/>"),
            etree.XML("<element id='value'>text</element>"),
            etree.XML("<TEI><element id='value'>text</element></TEI>"),
            etree.XML(
                "<TEI><teiHeader><element id='someval'>text</element></teiHeader></TEI>"
            ),
            etree.XML(
                "<first><second><third id='val1' attr='val2'>text</third></second></first>"
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<element/>"),
            etree.XML("<TEI><element>id</element></TEI>"),
            etree.XML("<TEI><idno xml:id='filename'>file.txt</idno></TEI>"),
            etree.XML("<first><second><third attr='val'></third></second></first>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<element id='val'/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<TEI><element id='val'/></TEI>")
        result = self.observer.observe(node)
        self.assertFalse(result)
