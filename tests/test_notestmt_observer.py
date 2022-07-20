import unittest

from lxml import etree

from tei_transform.notestmt_observer import NoteStmtObserver
from tei_transform.observer_constructor import check_if_observer_pattern_is_valid_xpath


class NoteStmtObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = NoteStmtObserver()

    def test_observer_pattern_is_valid_xpath(self):
        result = check_if_observer_pattern_is_valid_xpath(self.observer.xpattern)
        self.assertTrue(result)

    def test_observer_identifies_matching_element(self):
        matching_elements = [
            etree.XML("<sourceDesc><noteStmt type='bibl'></noteStmt></sourceDesc>"),
            etree.XML("<noteStmt type='bibl'/>"),
            etree.XML("<noteStmt type='bibl'> <note> text</note> </noteStmt>"),
            etree.XML(
                "<sourceDesc><biblFull><noteStmt type='val'><note/></noteStmt></biblFull></sourceDesc>"
            ),
        ]
        for element in matching_elements:
            res = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(res), 1)

    def test_observer_ignores_non_matching_elements(self):
        non_matching_elements = [
            etree.XML("<noteStmt/>"),
            etree.XML("<sourceDesc><noteStmt xml:id='bibl'></noteStmt></sourceDesc>"),
            etree.XML("<noteStmt> <note type='bibl'> text</note> </noteStmt>"),
            etree.XML(
                "<sourceDesc><biblFull><noteStmt xml:id='val'><note/></noteStmt></biblFull></sourceDesc>"
            ),
        ]
        for element in non_matching_elements:
            res = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(res))

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<noteStmt type='val'/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<TEI><noteStmt type='val'/></TEI>")
        result = self.observer.observe(node)
        self.assertFalse(result)

    def test_remove_type_attribute_on_single_node(self):
        node = etree.XML("<noteStmt type='text'><someSubnode/></noteStmt>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_remove_type_attribute_on_namespaced_node(self):
        root = etree.XML(
            "<TEI xmlns='http://www.tei-c.org/ns/1.0'><noteStmt type='text'>text</noteStmt></TEI>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_remove_type_attribute_on_nested_node(self):
        node = etree.XML(
            "<noteStmt type='a'><note type='a'/><note type='b'/></noteStmt>"
        )
        self.observer.transform_node(node)  #
        children_attrib = [child.attrib for child in node.getchildren()]
        self.assertEqual(node.attrib, {})
        self.assertEqual(children_attrib, [{"type": "a"}, {"type": "b"}])

    def test_remove_type_attribute_on_nested_namespaced_node(self):
        root = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <noteStmt type='text'>
            <note type='a'>text</note>
            <note type='b'>text</note>
            </noteStmt>
            </TEI>"""
        )
        node = root[0]
        self.observer.transform_node(node)
        children_attrib = [child.attrib for child in node.getchildren()]
        self.assertEqual(node.attrib, {})
        self.assertEqual(children_attrib, [{"type": "a"}, {"type": "b"}])

    def test_other_attributes_not_removed(self):
        node = etree.XML("<noteStmt type='a' id='b'>text</noteStmt>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"id": "b"})

    def test_change_not_performed_on_matching_sibling(self):
        root = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <noteStmt type='a'/>
            <noteStmt type='b'/>
            </TEI>"""
        )
        node = root[0]
        sibling = root[1]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})
        self.assertEqual(sibling.attrib, {"type": "b"})
