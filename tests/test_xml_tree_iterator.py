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

    def test_only_relevant_tags_added_as_child_nodes_of_root(self):
        xml = io.BytesIO(
            b"""
            <TEI>
              <teiHeader>
               <someSubNode/>
              </teiHeader>
              <text>Some text here</text>
            </TEI>"""
        )
        root = self.tree_iterator.iterate_xml(xml)
        result = [node.tag for node in root.getchildren()]
        self.assertEqual(result, ["teiHeader", "text"])

    def test_tag_events_with_namespace_are_identified_correctly(self):
        xml = io.BytesIO(
            b"""
            <TEI xmlns="http://www.tei-c.org/ns/1.0">
              <teiHeader>
               <someSubNode/>
              </teiHeader>
              <text>Some text here</text>
            </TEI>"""
        )
        root = self.tree_iterator.iterate_xml(xml)
        result = [node.tag for node in root.getchildren()]
        self.assertEqual(
            result,
            [
                "{http://www.tei-c.org/ns/1.0}teiHeader",
                "{http://www.tei-c.org/ns/1.0}text",
            ],
        )

    def test_ignore_unwanted_siblings_of_teiheader_and_text(self):
        xml = io.BytesIO(
            b"""
            <TEI>
              <teiHeader>
               <someSubNode/>
              </teiHeader>
              <text>Some text here</text>
              <someOtherNode/>
            </TEI>"""
        )
        root = self.tree_iterator.iterate_xml(xml)
        result = [node.tag for node in root.getchildren()]
        self.assertEqual(result, ["teiHeader", "text"])

    def test_no_tree_constructed_if_tei_node_missing_in_input(self):
        xml = io.BytesIO(
            b"""
            <TEI.2>
              <teiHeader>
               <someSubNode/>
              </teiHeader>
              <text>Some text here</text>
            </TEI.2>"""
        )
        result = self.tree_iterator.iterate_xml(xml)
        self.assertTrue(isinstance(result, list))
        self.assertEqual([node.tag for node in result], ["teiHeader", "text"])

    def test_chilren_added_on_end_event(self):
        xml = io.BytesIO(
            b"""
        <start>
        <teiHeader><text>first</text></teiHeader>
        <text>second</text>
        </start>
        """
        )
        tree = self.tree_iterator.iterate_xml(xml)
        result = [(node.tag, node.text) for node in tree]
        self.assertEqual(
            result, [("text", "first"), ("teiHeader", None), ("text", "second")]
        )
