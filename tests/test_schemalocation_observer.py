import unittest

from lxml import etree

from tei_transform.schemalocation_observer import SchemaLocationObserver


class SchemaLocationObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = SchemaLocationObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'
            xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
            xsi:schemaLocation='http://www.tei-c.org/ns/1.0'/>"""
        )
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'
            xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'/>"""
        )
        result = self.observer.observe(node)
        self.assertFalse(result)

    def test_observer_identifies_matching_element_in_tree(self):
        matching_elements = [
            etree.XML("<TEI xmlns='val1' xmlns:xsi='val2' xsi:schemaLocation='val'/>"),
            etree.XML(
                """<TEI xmlns='val1' xmlns:xsi='val2' xsi:schemaLocation='val'>
                <teiHeader><someElement>text</someElement></teiHeader></TEI>"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<TEI xmlns='val1' xmlns:xsi='val2'/>"),
            etree.XML(
                """<TEI xmlns='val1' xmlns:xsi='val2'>
                <teiHeader>
                <someElement>text</someElement>
                </teiHeader>
                </TEI>"""
            ),
            etree.XML(
                "<TEI xmlns='val1'><teiHeader><someElement>text</someElement></teiHeader></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))
