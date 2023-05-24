import unittest

from lxml import etree

from tei_transform.observer import EmptyPPublicationstmtObserver


class EmptyPPublicationstmtObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyPPublicationstmtObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<publicationStmt><p/><idno/></publicationStmt>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<publicationStmt><p/><ab/></publicationStmt>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<publicationStmt><publisher/><p/><idno/></publicationStmt>"),
            etree.XML(
                "<fileDesc><publicationStmt><publisher/><date/><ab>text</ab></publicationStmt></fileDesc>"
            ),
            etree.XML("<publicationStmt><publisher/><ab/><address/></publicationStmt>"),
            etree.XML("<publicationStmt><authority/><ptr/><p/></publicationStmt>"),
            etree.XML("<publicationStmt><distributor/><ab/><idno/></publicationStmt>"),
            etree.XML(
                "<publicationStmt><publisher/><p><hi>text</hi></p><date/></publicationStmt>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><publisher/><idno/><ab/></publicationStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><authority/><p/><date/></publicationStmt></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<publicationStmt><ab/><p/><p/></publicationStmt>"),
            etree.XML("<publicationStmt><publisher/><date/></publicationStmt>"),
            etree.XML("<publicationStmt><p>text</p></publicationStmt>"),
            etree.XML("<publicationStmt><p/><p/></publicationStmt>"),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><publisher/><date/></publicationStmt></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><publicationStmt><p/></publicationStmt></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><ab>text</ab><ab/><p/></publicationStmt></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
