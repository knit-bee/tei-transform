import unittest

from lxml import etree

from tei_transform.observer import TeiHeaderObserver


class TeiHeaderObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TeiHeaderObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<teiHeader type='text'></teiHeader>")
        self.assertTrue(self.observer.observe(node))

    def test_observer_returns_true_for_matching_namespaced_element(self):
        root = etree.XML(
            "<TEI xmlns='http://www.tei-c.org/ns/1.0'><teiHeader type='text'>text</teiHeader></TEI>"
        )
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<teiHeader/>")
        self.assertFalse(self.observer.observe(node))

    def test_observer_identifies_matching_element_in_tree(self):
        matching_elements = [
            etree.XML("<teiHeader type='val'/>"),
            etree.XML("<TEI><teiHeader type='val'><titleStmt/></teiHeader></TEI>"),
            etree.XML(
                "<TEI><teiHeader type='val'><titleStmt><title/></titleStmt></teiHeader></TEI>"
            ),
            etree.XML(
                '<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader type="val">text</teiHeader></TEI>'
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<teiHeader></teiHeader>"),
            etree.XML("<TEI><teiHeader><titleStmt/></teiHeader></TEI>"),
            etree.XML(
                "<TEI><teiHeader id='val'><titleStmt><title/></titleStmt></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI><tei type='val'><titleStmt><title/></titleStmt></tei></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))

    def test_type_attribute_removed_from_teiheader(self):
        node = etree.XML("<teiHeader type='text'/>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed_after_type_attr_removal(self):
        node = etree.XML("<teiHeader type='a' id='b'><someNode/> </teiHeader>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"id": "b"})

    def test_type_attribute_removed_from_teiheader_with_namespace(self):
        root = etree.XML("""<TEI xmlns='val'><teiHeader type='a'></teiHeader></TEI>""")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_type_attribute_not_removed_from_children_of_teiheader(self):
        node = etree.XML(
            """<teiHeader type='parent'>
            <node1/>
            <node2 type='child'>text</node2>
            </teiHeader>"""
        )
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_type_attribute_not_removed_from_children_of_namespaced_teiheader(self):
        root = etree.XML(
            """<TEI xmlns='val'>
              <teiHeader type='parent'>
                <child1 type='child'/>
              </teiHeader>
            </TEI>"""
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})
