import unittest

from lxml import etree

from tei_transform.double_item_observer import DoubleItemObserver


class DoubleItemObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DoubleItemObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<item><item/></item>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<item><p/></item>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_nodes(self):
        elements = [
            etree.XML("<item><item>test</item></item>"),
            etree.XML("<list><item><item>some  text</item></item><item/></list>"),
            etree.XML("<item><item>text</item><lb/>more text</item>"),
            etree.XML("<list><item><item>text</item><lb/>more text</item></list>"),
            etree.XML(
                """<TEI><teiHeader/><text>
            <body><div><list><fw/><item><item>test</item></item></list></div></body>
            </text></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/><text>
                        <body><div><p> some text</p><list><fw/><item><item>test</item></item></list></div></body>
                        </text></TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<item>text</item>"),
            etree.XML("<item><p>text</p></item>"),
            etree.XML("<list><item/><item>some  text</item><item/></list>"),
            etree.XML("<item>text<lb/>more text</item>"),
            etree.XML("<list><item/><item><p>text<lb/>more text</p></item></list>"),
            etree.XML(
                """<TEI><teiHeader/><text>
                    <body><div><list><fw/><item/><item>test</item><item/></list></div></body>
                    </text></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/><text>
                    <body><div><p> some text</p>
                    <list><fw/><item>test</item><item/></list></div></body>
                    </text></TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_observer_inner_item_renamed(self):
        root = etree.XML("<list><item><item>text</item></item></list>")
        node = root[0][0]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["list", "item", "ab"])

    def test_inner_item_renamed_on_namespaced_node(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><list><item><item>text</item></item></list></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "list", "item", "ab"])

    def test_namespace_prefix_preserved_after_change_on_target_node(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><list><item><item>text</item></item></list></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = root.find(".//{*}ab").tag
        self.assertEqual(result, "{namespace}ab")

    def test_attributes_preserved_after_transformation(self):
        root = etree.XML(
            "<list><item attr='val'><item attr='val2'>text</item></item></list>"
        )
        node = root[0][0]
        self.observer.transform_node(node)
        result = root.find(".//{*}ab").attrib
        self.assertEqual(result, {"attr": "val2"})

    def test_attributes_preserved_after_transformation_on_namespaced_node(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><list><item><item attr='val'>text</item></item></list></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = root.find(".//{*}ab").attrib
        self.assertEqual(result, {"attr": "val"})

    def test_observer_action_on_node_with_children(self):
        root = etree.XML("<list><item><item><p>text</p></item></item></list>")
        node = root[0][0]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["list", "item", "list", "item", "p"])

    def test_observer_action_on_namespaced_node_with_children(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><list><item><item>text<p/></item></item></list></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "list", "item", "list", "item", "p"])

    def test_attributes_preserved_after_transformation_on_node_with_children(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><list><item><item attr='val'>text<p/></item></item></list></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = node.attrib
        self.assertEqual(result, {"attr": "val"})
