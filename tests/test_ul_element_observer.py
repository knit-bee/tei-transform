import unittest

from lxml import etree

from tei_transform.observer import UlElementObserver


class UlElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = UlElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><ul><item/></ul></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><list><item/></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><ul/></div>"),
            etree.XML("<div><ul class='val'><item/><item/></ul></div>"),
            etree.XML("<ul><item>text</item></ul>"),
            etree.XML("<div><div/><ul/></div>"),
            etree.XML("<div><ul><item/></ul><p/>></div>"),
            etree.XML("<TEI xmlns='a'><div><ul/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><ul><item>text</item></ul></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><div/><ul class='a'/><p/></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<element/>"),
            etree.XML("<TEI xmlns='a'><div><list/></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_ul_element_renamed(self):
        root = etree.XML("<div><ul><item/></ul></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find("ul") is None)
        self.assertEqual(node.tag, "list")

    def test_ul_element_renamed_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><ul><item/></ul></div></TEI>")
        node = root.find(".//{*}ul")
        self.observer.transform_node(node)
        self.assertEqual(node.tag, "{a}list")

    def test_attributes_of_node_not_removed_after_transformation(self):
        root = etree.XML("<div><ul attr='val'><item/></ul></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val"})
