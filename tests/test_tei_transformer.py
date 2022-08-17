import io
import unittest

from lxml import etree

from tei_transform.observer import TeiNamespaceObserver
from tei_transform.revision_desc_change import RevisionDescChange
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

    def test_change_info_recorded_if_tree_changed(self):
        transformer = TeiTransformer(
            FakeIterator(), [FakeObserver("oldTag", action=change_tag)]
        )
        xml = io.BytesIO(b"<someTag><oldTag/></someTag>")
        transformer.perform_transformation(xml)
        self.assertTrue(transformer.xml_tree_changed())

    def test_no_change_recorded_if_tree_hasnt_changed(self):
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = io.BytesIO(b"<someTag><oldTag/></someTag>")
        transformer.perform_transformation(xml)
        self.assertFalse(transformer.xml_tree_changed())

    def test_add_change_to_revision_desc(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(
            result, ["teiHeader", "revisionDesc", "change", "change", "name"]
        )

    def test_change_with_namespace_added(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                    <teiHeader>
                    <revisionDesc><change>0</change></revisionDesc>
                    </teiHeader>
                    </TEI>"""
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iterfind(".//{*}change")]
        self.assertEqual(
            result,
            [
                "{http://www.tei-c.org/ns/1.0}change",
                "{http://www.tei-c.org/ns/1.0}change",
            ],
        )

    def test_add_change_to_revision_desc_with_listchange(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"""<teiHeader>
            <revisionDesc>
            <listChange>
            <change>0</change>
            </listChange>
            </revisionDesc>
            </teiHeader>"""
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(
            result,
            ["teiHeader", "revisionDesc", "listChange", "change", "change", "name"],
        )

    def test_revision_desc_added_if_not_present_before(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(b"<teiHeader><fileDesc/><profileDesc/></teiHeader>")
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(
            result,
            ["teiHeader", "fileDesc", "profileDesc", "revisionDesc", "change", "name"],
        )

    def test_namespace_added_to_new_revision_desc(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <teiHeader><fileDesc/><profileDesc/></teiHeader></TEI>"""
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        result = tree.find(".//{*}revisionDesc").tag
        self.assertEqual(result, "{http://www.tei-c.org/ns/1.0}revisionDesc")

    def test_person_name_for_change_set_correctly(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        person_name = revision_desc[-1][0].text
        self.assertEqual(person_name, "Vorname Nachname")

    def test_multiple_person_names_set_correctly(self):
        change = RevisionDescChange(
            person=["Erste Person", "Zweite Person"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1]
        person_names = [(node.tag, node.text) for node in last_change.getchildren()]
        self.assertEqual(
            person_names, [("name", "Erste Person"), ("name", "Zweite Person")]
        )

    def test_change_date_set_as_attribute(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1]
        self.assertEqual(last_change.attrib, {"when": "2022-07-25"})

    def test_change_reason_set_correctly(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1]
        self.assertEqual(last_change.text, "Change reason")

    def test_no_person_name_inserted_if_missing(self):
        change = RevisionDescChange(person=[], date="2022-02-20", reason="Some reason")
        transformer = TeiTransformer(FakeIterator(), [FakeObserver()])
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(result, ["teiHeader", "revisionDesc", "change", "change"])

    def test_namespace_to_tei_element_added_if_tei_namespace_observer_is_passed(self):
        transformer = TeiTransformer(FakeIterator(), [TeiNamespaceObserver()])
        xml = io.BytesIO(
            b"""
        <TEI>
        <tag>
        <tag2>
        <subnode/>
        </tag2>
        </tag>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        self.assertTrue("http://www.tei-c.org/ns/1.0" in tree.nsmap.values())

    def test_tei_namespace_added_to_child_nodes(self):
        transformer = TeiTransformer(FakeIterator(), [TeiNamespaceObserver()])
        xml = io.BytesIO(
            b"""
        <TEI>
        <teiHeader>
        <fileDesc>
        <subnode/>
        </fileDesc>
        </teiHeader>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        new_xml = etree.tostring(tree, encoding="utf-8")
        new_tree = etree.XML(new_xml)
        result = [node.tag for node in new_tree.iter()]
        expected = [
            "{http://www.tei-c.org/ns/1.0}TEI",
            "{http://www.tei-c.org/ns/1.0}teiHeader",
            "{http://www.tei-c.org/ns/1.0}fileDesc",
            "{http://www.tei-c.org/ns/1.0}subnode",
        ]
        self.assertEqual(result, expected)


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
