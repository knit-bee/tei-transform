import unittest

from lxml import etree

from tei_transform.observer import MisusedBylineObserver


class MisusedBylineObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MisusedBylineObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p/><byline/><p/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><byline/><p/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><p/><byline/><p/><p/></div>"),
            etree.XML("<div><head/><p/><byline>text<lb/></byline><p/></div>"),
            etree.XML("<div><p/><byline/><p/><figure/></div>"),
            etree.XML("<div><head/><p/><byline/><p/><p/><p/></div>"),
            etree.XML("<div><p/><byline>a</byline><p/></div>"),
            etree.XML("<div><p/><byline/><head/></div>"),
            etree.XML("<div><p/><byline/><ab/></div>"),
            etree.XML("<div><ab/><byline/><head/><p/></div>"),
            etree.XML("<TEI xmlns='a'><div><head/><p/><byline/><p/></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><p/><byline>b<lb/></byline><p/></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><head/><byline/><p/><byline/></div>"),
            etree.XML("<div><byline/><p/><head/><byline/></div>"),
            etree.XML("<div><p/><byline/><figure/></div>"),
            etree.XML("<div><head/><p/><p/><byline/><figure/></div>"),
            etree.XML("<div><p/><byline>text<lb/></byline></div>"),
            etree.XML("<div><head/><byline>text</byline><p/></div>"),
            etree.XML("<TEI xmlns='a'><div><head/><byline/><p/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><byline/><p/><byline/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><byline>b<lb/></byline></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><head/><p/><byline/><figure/></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_element_tag_changed(self):
        root = etree.XML("<div><p/><byline/><p/></div>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find("ab") is not None)

    def test_element_tag_changed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><head/><p/><p/><byline>b<lb/></byline><p/></div></TEI>"
        )
        node = root.find(".//{*}byline")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}byline") is None)
        self.assertTrue(root.find(".//{*}ab") is not None)

    def test_old_attributes_not_removed(self):
        root = etree.XML("<div><p/><byline attr='val'/><p/></div>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val"})
