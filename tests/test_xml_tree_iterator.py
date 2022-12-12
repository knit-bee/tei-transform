import io
import unittest

from tei_transform.xml_tree_iterator import XMLTreeIterator


class XMLTreeIteratorTester(unittest.TestCase):
    def setUp(self):
        self.tree_iterator = XMLTreeIterator()

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
        nodes = self.tree_iterator.iterate_xml(xml)
        result = [node.tag for node in nodes]
        self.assertEqual(result, ["TEI", "teiHeader", "text"])

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
        nodes = self.tree_iterator.iterate_xml(xml)
        result = [node.tag for node in nodes]
        self.assertEqual(
            result,
            [
                "{http://www.tei-c.org/ns/1.0}TEI",
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
        nodes = self.tree_iterator.iterate_xml(xml)
        result = [node.tag for node in nodes]
        self.assertEqual(result, ["TEI", "teiHeader", "text"])

    def test_no_root_constructed_if_tei_node_missing_in_input(self):
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
        self.assertEqual([node.tag for node in result], ["teiHeader", "text"])

    def test_children_yielded_on_end_event(self):
        xml = io.BytesIO(
            b"""
        <start>
        <teiHeader><text>first</text></teiHeader>
        <text>second</text>
        </start>
        """
        )
        nodes = self.tree_iterator.iterate_xml(xml)
        result = [(node.tag, node.text) for node in nodes]
        self.assertEqual(
            result, [("text", "first"), ("teiHeader", None), ("text", "second")]
        )
