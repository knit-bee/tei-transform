import unittest

from lxml import etree

from tei_transform.observer import LonelySObserver


class LonelySObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelySObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<body><s>text</s></body>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<body><p><s>text</s></p></body>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<body><p/><s>text</s></body>"),
            etree.XML("<div><s><l>text</l></s></div>"),
            etree.XML("<body><list/><s>text<w/></s></body>"),
            etree.XML("<div>text<s>text</s><p><s/></p></div>"),
            etree.XML("<TEI xmlns='a'><div><p/><s><w/></s></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/><s>text</s><p/></body></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/><div><p/><s/></div></body></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p><s/></p>"),
            etree.XML("<div><p><s>text<w/></s></p></div>"),
            etree.XML("<body><p>text<s>text</s></p></body>"),
            etree.XML("<div><p>text<s><w>text</w></s></p></div>"),
            etree.XML("<TEI xmlns='a'><body><p><s>text</s></p></body></TEI>"),
            etree.XML("<TEI xmlns='a'><div><quote><s/></quote></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><head><s>text</s></head></body></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_p_added_as_parent(self):
        root = etree.XML("<div><s>text</s></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p/s") is not None)

    def test_p_added_as_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><p/><s>text</s></div></TEI>")
        node = root.find(".//{*}s")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}p/{*}s") is not None)

    def test_attributes_of_s_preserved_after_transformation(self):
        root = etree.XML("<div><s attr='val'/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val"})

    def test_children_of_s_preserved_after_transformation(self):
        root = etree.XML("<body><s><w/><w/></s></body>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//p/s")), 2)

    def test_multiple_adjacent_s_added_to_same_p_element(self):
        root = etree.XML("<div><s>text1</s><s>text2</s><s>text3</s></div>")
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [(node.tag, node.text) for node in root.find(".//p")]
        self.assertEqual(result, [("s", "text1"), ("s", "text2"), ("s", "text3")])

    def test_transformation_only_applied_to_outer_s_if_nested(self):
        root = etree.XML("<div><s><s>text</s></s></div>")
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//p")), 1)

    def test_elements_added_to_different_p_if_other_sibling_inbetween(self):
        root = etree.XML(
            """
            <body>
                <s>text1</s>
                <s>text2</s>
                <p/>
                <s>text3</s>
                <s>text4</s>
                <p/>
            </body>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [[(child.tag, child.text) for child in node] for node in root]
        self.assertEqual(
            result,
            [
                [("s", "text1"), ("s", "text2")],
                [],
                [
                    ("s", "text3"),
                    ("s", "text4"),
                ],
                [],
            ],
        )
