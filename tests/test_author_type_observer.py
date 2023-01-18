import unittest

from lxml import etree

from tei_transform.observer import AuthorTypeObserver


class AuthorTypeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = AuthorTypeObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<author type='val'>name</author>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<author>name</author>")
        result = self.observer.observe(node)
        self.assertEqual(result, result)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<author type='val'/>"),
            etree.XML("<author type='val'><name>person</name></author>"),
            etree.XML("<titleStmt><author type='val'/></titleStmt>"),
            etree.XML(
                "<TEI xmlns='ns'><titleStmt><author type='val'>name</author></titleStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><titleStmt><author type='val'><name>person</name></author></titleStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><teiHeader><titleStmt><author type='a'/><title/></titleStmt></teiHeader></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<author/>"),
            etree.XML("<author>name</author>"),
            etree.XML("<author attr='val'><name>person</name></author>"),
            etree.XML("<titleStmt><author attr='val'>name</author></titleStmt>"),
            etree.XML(
                "<TEI xmlns='ns'><titleStmt><author attr='val'>name</author><title/></titleStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><fileDesc type='val'><author><name/></author></fileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><fileDesc><title/><author>name</author></fileDesc></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
