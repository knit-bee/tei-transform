import unittest

from lxml import etree

from tei_transform.observer import MisusedLObserver


class MisusedLObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MisusedLObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<s><l>text</l></s>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<p><l>text</l></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p><s><l>text</l></s></p>"),
            etree.XML("<div><s><l>text</l></s><p/></div>"),
            etree.XML("<quote><s><l>text</l></s></quote>"),
            etree.XML("<TEI xmlns='a'><div><p><s><l>text</l></s></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><s><l>text</l><s/></s></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p><s><w/><l/><s/></s></p></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p><s/><l/></p>"),
            etree.XML("<p><l><s>text</s></l></p>"),
            etree.XML("<p><l>text<s>text2</s></l></p>"),
            etree.XML("<p><hi><l>text</l><s/></hi></p>"),
            etree.XML("<TEI xmlns='a'><p><s/><l><s/></l></p></TEI>"),
            etree.XML("<TEI xmlns='a'><p><l>text<s>text</s></l></p></TEI>"),
            etree.XML("<TEI xmlns='a'><p><lg><l/><l/><l><s/></l></lg></p></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_tag_changed_to_w(self):
        root = etree.XML("<s><l>text</l></s>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root[0].tag, "w")

    def test_tag_changed_to_w_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><p><s>text<l>text1</l></s></p></div></TEI>"
        )
        node = root.find(".//{*}l")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}s")[0].tag, "{a}w")

    def test_attributes_of_node_not_removed_after_transformation(self):
        root = etree.XML("<p><s><l attr='val'>text</l></s></p>")
        node = root.find(".//l")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val"})
