import unittest

from lxml import etree

from tei_transform.observer import IdAttributeObserver


class FilenameElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = IdAttributeObserver()

    def test_observer_identifies_matching_element_in_tree(self):
        matching_elements = [
            etree.XML("<element id='value'/>"),
            etree.XML("<element id='value'>text</element>"),
            etree.XML("<TEI><element id='value'>text</element></TEI>"),
            etree.XML(
                "<TEI><teiHeader><element id='someval'>text</element></teiHeader></TEI>"
            ),
            etree.XML(
                "<first><second><third id='val1' attr='val2'>text</third></second></first>"
            ),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0' id='file.xml'><someOtherElements/></TEI>"
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<element/>"),
            etree.XML("<TEI><element>id</element></TEI>"),
            etree.XML("<TEI><idno xml:id='filename'>file.txt</idno></TEI>"),
            etree.XML("<first><second><third attr='val'></third></second></first>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<element id='val'/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<TEI><element id='val'/></TEI>")
        result = self.observer.observe(node)
        self.assertFalse(result)

    def test_id_attribute_removed_on_TEI_root(self):
        node = etree.XML("<TEI id='file.xml'></TEI>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_id_attribute_replaced_on_non_TEI_nodes(self):
        node = etree.XML("<publisher id='some id'> some name </publisher>")
        self.observer.transform_node(node)
        self.assertEqual(node.keys(), ["{http://www.w3.org/XML/1998/namespace}id"])

    def test_action_with_namespaced_tei_element(self):
        node = etree.XML("<TEI xmlns='http://www.tei-c.org/ns/1.0' id='file.xml'/>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_xml_prefix_added_on_namespaced_node(self):
        root = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <someNode id='test'>Test</someNode></TEI>"""
        )
        node = root.getchildren()[0]
        self.observer.transform_node(node)
        self.assertEqual(node.keys(), ["{http://www.w3.org/XML/1998/namespace}id"])

    def test_xml_prefix_rendered_correctly_on_string_output(self):
        root = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
    <someNode id='test'>Test</someNode></TEI>"""
        )
        node = root.getchildren()[0]
        self.observer.transform_node(node)
        self.assertEqual(
            etree.tostring(node, encoding="unicode"),
            '<someNode xmlns="http://www.tei-c.org/ns/1.0" xml:id="test">Test</someNode>',
        )
