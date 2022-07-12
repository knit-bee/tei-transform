import unittest

from lxml import etree

from tei_transform.filename_element_observer import FilenameElementObserver
from tei_transform.observer_constructor import check_if_observer_pattern_is_valid_xpath


class FilenameElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = FilenameElementObserver()

    def test_observer_pattern_is_valid_xpath(self):
        result = check_if_observer_pattern_is_valid_xpath(self.observer.xpattern)
        self.assertTrue(result)

    def test_observer_identifies_matching_element(self):
        matching_elements = [
            etree.XML("<filename/>"),
            etree.XML("<filename></filename>"),
            etree.XML("<TEI><filename>file</filename></TEI>"),
            etree.XML(
                "<TEI><teiHeader><filename attr='someval'>file</filename></teiHeader></TEI>"
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertTrue(any(result))

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<element/>"),
            etree.XML("<TEI><element>filename</element></TEI>"),
            etree.XML("<TEI><idno xml:id='filename'>file.txt</idno></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))
