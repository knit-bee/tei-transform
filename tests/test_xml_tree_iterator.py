import io
import unittest

from lxml import etree

from tei_transform.xml_tree_iterator import XMLTreeIterator


class XMLTreeIteratorTester(unittest.TestCase):
    def setUp(self):
        self.tree_iterator = XMLTreeIterator([])

    def test_root_node_constructed_with_correct_attributes(self):
        old_node = etree.Element("element", attrib={"a": "b"})
        new_node = self.tree_iterator.construct_new_tei_root(old_node)
        self.assertEqual(new_node.attrib, {"a": "b"})

    def test_root_node_tag_set_correctly(self):
        old_node = etree.Element("element", attrib={"a": "b"})
        new_node = self.tree_iterator.construct_new_tei_root(old_node)
        self.assertEqual(new_node.tag, "TEI")

    def test_root_node_tag_with_namespace_set_correctly(self):
        old_node = etree.Element(
            "element", attrib={"a": "b"}, nsmap={None: "some/link"}
        )
        new_node = self.tree_iterator.construct_new_tei_root(old_node)
        self.assertEqual(new_node.tag, "{some/link}TEI")

    def test_namespace_for_new_root_node_set_correctly(self):
        old_node = etree.Element(
            "element", attrib={"a": "b"}, nsmap={None: "some/link"}
        )
        new_node = self.tree_iterator.construct_new_tei_root(old_node)
        self.assertEqual(new_node.nsmap, {None: "some/link"})

    def test_children_of_old_node_not_transfered_to_new_root(self):
        old_node = etree.Element("first")
        old_node.append(etree.Element("second"))
        old_node.append(etree.Element("third"))
        new_node = self.tree_iterator.construct_new_tei_root(old_node)
        self.assertEqual(new_node.getchildren(), [])
