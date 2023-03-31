import unittest

from lxml import etree

from tei_transform.observer import AvailabilityTextObserver


class AvailabilityTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = AvailabilityTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML(
            "<publicationStmt><availability>text</availability></publicationStmt>"
        )
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML(
            "<publicationStmt><availability><p>text</p></availability></publicationStmt>"
        )
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<availability>text</availability>"),
            etree.XML("<availability status='free'>text<p/></availability>"),
            etree.XML("<availability>text<ab/></availability>"),
            etree.XML("<availability><license/>text</availability>"),
            etree.XML(
                "<publicationStmt><publisher/><availability>text</availability></publicationStmt>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><editor/><availability>text</availability></publicationStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><availability status='free'>text</availability></publicationStmt></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<availability><p>text</p></availability>"),
            etree.XML("<availability status='free'><ab>text</ab></availability>"),
            etree.XML(
                "<publicationStmt><publisher/><availability><license>text</license></availability></publicationStmt>"
            ),
            etree.XML("<availability>    </availability>"),
            etree.XML(
                "<publicationStmt><availability><p/> \n\n</availability></publicationStmt>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <publicationStmt>
                        <editor/>
                        <date/>
                        <availability><p>text</p></availability>
                    </publicationStmt>
                </TEI>"""
            ),
            etree.XML(
                "<TEI xmlns='a'><availability status='restricted'><license>text</license></availability></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
