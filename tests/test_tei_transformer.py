import io
import unittest

from lxml import etree

from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator


class TeiTransformerTester(unittest.TestCase):
    def setUp(self):
        self.iterator = XMLTreeIterator()

    def test_tree_constructed_correctly(self):
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = io.BytesIO(
            b"""<TEI>
        <first>text</first>
        <second/>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [node.tag for node in tree.iter()]
        expected = ["TEI", "first", "second"]
        self.assertEqual(result, expected)

    def test_no_tree_constructed_if_tei_node_missing(self):
        transformer = TeiTransformer(XMLTreeIterator(), [FakeObserver()])
        xml = io.BytesIO(
            b"""<someTag>
        <first>text</first>
        <second/>
        </someTag>
        """
        )
        result = transformer.perform_transformation(xml)
        self.assertIsNone(result)

    def test_transformer_interaction_with_iterator(self):
        transformer = TeiTransformer(self.iterator, [FakeObserver()])
        xml = io.BytesIO(
            b"""
        <TEI>
        <teiHeader>
        <subNode/>
        </teiHeader>
        <text>
        Some text here
        </text>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [node.tag for node in tree.getchildren()]
        self.assertEqual(result, ["teiHeader", "text"])

    def test_transformer_interaction_with_iterator_with_namespace(self):
        transformer = TeiTransformer(self.iterator, [FakeObserver()])
        xml = io.BytesIO(
            b"""
            <TEI xmlns="http://www.tei-c.org/ns/1.0">
              <teiHeader>
               <someSubNode/>
              </teiHeader>
              <text>Some text here</text>
            </TEI>"""
        )
        tree = transformer.perform_transformation(xml)
        result = [node.tag for node in tree.getchildren()]
        self.assertEqual(
            result,
            [
                "{http://www.tei-c.org/ns/1.0}teiHeader",
                "{http://www.tei-c.org/ns/1.0}text",
            ],
        )

    def test_observer_performs_tag_change_when_matching_node_found(self):
        transformer = TeiTransformer(
            FakeIterator(), [FakeObserver("match", action=change_tag)]
        )
        xml = io.BytesIO(
            b"""<TEI>
            <first>
              <someTag>text</someTag>
              <match>text</match>
            </first>
            <second/>
        </TEI>"""
        )
        tree = transformer.perform_transformation(xml)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(result, ["TEI", "first", "someTag", "newTag", "second"])

    def test_attribute_change_on_observer_activation(self):
        transformer = TeiTransformer(
            FakeIterator(), [FakeObserver("match", action=remove_id_attrib)]
        )
        xml = io.BytesIO(
            b"""
        <TEI>
        <match id='matching node'>
        <subnode attribute="not matching"/>
        </match>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(
            result, [("TEI", []), ("match", []), ("subnode", ["attribute"])]
        )

    def test_observer_doesnt_perform_change_on_non_matching_node(self):
        transformer = TeiTransformer(
            FakeIterator(), [FakeObserver("match", action=remove_id_attrib)]
        )
        xml = io.BytesIO(
            b"""
        <TEI>
        <match id='matching node'>
        <subnode id="not matching"/>
        </match>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(result, [("TEI", []), ("match", []), ("subnode", ["id"])])

    def test_transformation_with_multiple_observers_on_sibling_nodes(self):
        tag_observer = FakeObserver("tag-to-change", action=change_tag)
        id_observer = FakeObserver("match", action=remove_id_attrib)
        transformer = TeiTransformer(FakeIterator(), [tag_observer, id_observer])
        xml = io.BytesIO(
            b"""
        <TEI>
        <tag-to-change>
        some text here
        </tag-to-change>
        <match id='matching node'>
        <subnode/>
        </match>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(
            result, [("TEI", []), ("newTag", []), ("match", []), ("subnode", [])]
        )

    def test_transformation_with_multiple_observers_on_nested_nodes(self):
        tag_observer = FakeObserver("tag-to-change", action=change_tag)
        id_observer = FakeObserver("match", action=remove_id_attrib)
        transformer = TeiTransformer(FakeIterator(), [tag_observer, id_observer])
        xml = io.BytesIO(
            b"""
        <TEI>
        <tag-to-change>
        <match id='matching node'>
        <subnode/>
        </match>
        </tag-to-change>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(
            result, [("TEI", []), ("newTag", []), ("match", []), ("subnode", [])]
        )

    def test_two_observers_activate_on_same_node(self):
        id_observer = FakeObserver("match", action=remove_id_attrib)
        tag_observer = FakeObserver("match", action=change_tag)
        transformer = TeiTransformer(FakeIterator(), [id_observer, tag_observer])
        xml = io.BytesIO(
            b"""
        <TEI>
        <match id='matching node'>
        <subnode/>
        </match>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(result, [("TEI", []), ("newTag", []), ("subnode", [])])

    def test_two_observers_activate_on_same_node_with_conflicting_actions(self):
        tag_observer = FakeObserver("match", action=change_tag)
        id_observer = FakeObserver("match", action=remove_id_attrib)
        transformer = TeiTransformer(FakeIterator(), [tag_observer, id_observer])
        xml = io.BytesIO(
            b"""
        <TEI>
        <match id='matching node'>
        <subnode/>
        </match>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(result, [("TEI", []), ("newTag", ["id"]), ("subnode", [])])

    def test_returns_none_when_file_is_empty(self):
        transformer = TeiTransformer(XMLTreeIterator(), [FakeObserver()])
        xml = io.BytesIO(b"")
        result = transformer.perform_transformation(xml)
        self.assertIsNone(result)


# helper functions for node transformation with FakeObserver
def change_tag(node):
    node.tag = "newTag"


def remove_id_attrib(node):
    node.attrib.pop("id", None)


class FakeObserver:
    def __init__(self, tag=None, action=None):
        self.action = action
        self.tag = tag

    def observe(self, node):
        if node.tag == self.tag:
            return True
        return False

    def transform_node(self, node):
        if self.action is not None:
            self.action(node)


class FakeIterator:
    def iterate_xml(self, filename):
        for node in etree.parse(filename).iter():
            yield node
