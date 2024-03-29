import io
import os
import unittest

from lxml import etree

from tei_transform.observer import TeiNamespaceObserver
from tei_transform.parse_config import RevisionDescChange
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator


class TeiTransformerTester(unittest.TestCase):
    def setUp(self):
        self.iterator = XMLTreeIterator()
        self.transformer = TeiTransformer(FakeIterator())

    def test_tree_constructed_correctly(self):
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = io.BytesIO(
            b"""<TEI>
        <first>text</first>
        <second/>
        </TEI>
        """
        )
        tree = self.transformer.perform_transformation(xml)
        result = [node.tag for node in tree.iter()]
        expected = ["TEI", "first", "second"]
        self.assertEqual(result, expected)

    def test_no_tree_constructed_if_tei_node_missing(self):
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(([FakeObserver()], []))
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
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(([FakeObserver()], []))
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
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(([FakeObserver()], []))
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
        self.transformer.set_list_of_observers(
            ([FakeObserver("match", action=change_tag)], [])
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
        tree = self.transformer.perform_transformation(xml)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(result, ["TEI", "first", "someTag", "newTag", "second"])

    def test_attribute_change_on_observer_activation(self):
        self.transformer.set_list_of_observers(
            ([FakeObserver("match", action=remove_id_attrib)], [])
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
        tree = self.transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(
            result, [("TEI", []), ("match", []), ("subnode", ["attribute"])]
        )

    def test_observer_doesnt_perform_change_on_non_matching_node(self):
        self.transformer.set_list_of_observers(
            ([FakeObserver("match", action=remove_id_attrib)], [])
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
        tree = self.transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(result, [("TEI", []), ("match", []), ("subnode", ["id"])])

    def test_transformation_with_multiple_observers_on_sibling_nodes(self):
        tag_observer = FakeObserver("tag-to-change", action=change_tag)
        id_observer = FakeObserver("match", action=remove_id_attrib)
        self.transformer.set_list_of_observers(([tag_observer, id_observer], []))
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
        tree = self.transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(
            result, [("TEI", []), ("newTag", []), ("match", []), ("subnode", [])]
        )

    def test_transformation_with_multiple_observers_on_nested_nodes(self):
        tag_observer = FakeObserver("tag-to-change", action=change_tag)
        id_observer = FakeObserver("match", action=remove_id_attrib)
        self.transformer.set_list_of_observers(([tag_observer, id_observer], []))
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
        tree = self.transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(
            result, [("TEI", []), ("newTag", []), ("match", []), ("subnode", [])]
        )

    def test_two_observers_activate_on_same_node(self):
        id_observer = FakeObserver("match", action=remove_id_attrib)
        tag_observer = FakeObserver("match", action=change_tag)
        self.transformer.set_list_of_observers(([id_observer, tag_observer], []))
        xml = io.BytesIO(
            b"""
        <TEI>
        <match id='matching node'>
        <subnode/>
        </match>
        </TEI>
        """
        )
        tree = self.transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(result, [("TEI", []), ("newTag", []), ("subnode", [])])

    def test_two_observers_activate_on_same_node_with_conflicting_actions(self):
        tag_observer = FakeObserver("match", action=change_tag)
        id_observer = FakeObserver("match", action=remove_id_attrib)
        self.transformer.set_list_of_observers(([tag_observer, id_observer], []))
        xml = io.BytesIO(
            b"""
        <TEI>
        <match id='matching node'>
        <subnode/>
        </match>
        </TEI>
        """
        )
        tree = self.transformer.perform_transformation(xml)
        result = [(node.tag, node.keys()) for node in tree.iter()]
        self.assertEqual(result, [("TEI", []), ("newTag", ["id"]), ("subnode", [])])

    def test_returns_none_when_file_is_empty(self):
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(([FakeObserver()], []))
        xml = io.BytesIO(b"")
        result = transformer.perform_transformation(xml)
        self.assertIsNone(result)

    def test_change_info_recorded_if_tree_changed(self):
        transformer = TeiTransformer(FakeIterator())
        transformer.set_list_of_observers(
            ([FakeObserver("oldTag", action=change_tag)], [])
        )
        xml = io.BytesIO(b"<someTag><oldTag/></someTag>")
        transformer.perform_transformation(xml)
        self.assertTrue(transformer.xml_tree_changed())

    def test_no_change_recorded_if_tree_hasnt_changed(self):
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = io.BytesIO(b"<someTag><oldTag/></someTag>")
        self.transformer.perform_transformation(xml)
        self.assertFalse(self.transformer.xml_tree_changed())

    def test_add_change_to_revision_desc(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
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
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                    <teiHeader>
                    <revisionDesc><change>0</change></revisionDesc>
                    </teiHeader>
                    </TEI>"""
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
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
        self.transformer.set_list_of_observers(([FakeObserver()], []))
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
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.find(".//revisionDesc")]
        self.assertEqual(result, ["listChange", "change"])

    def test_revision_desc_added_if_not_present_before(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(b"<TEI><teiHeader><fileDesc/><profileDesc/></teiHeader></TEI>")
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(
            result,
            [
                "TEI",
                "teiHeader",
                "fileDesc",
                "profileDesc",
                "revisionDesc",
                "change",
                "name",
            ],
        )

    def test_namespace_added_to_new_revision_desc(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"""<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <teiHeader><fileDesc/><profileDesc/></teiHeader></TEI>"""
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        result = tree.find(".//{*}revisionDesc").tag
        self.assertEqual(result, "{http://www.tei-c.org/ns/1.0}revisionDesc")

    def test_person_name_for_change_set_correctly(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        person_name = revision_desc[-1][0].text
        self.assertEqual(person_name, "Vorname Nachname")

    def test_multiple_person_names_set_correctly(self):
        change = RevisionDescChange(
            person=["Erste Person", "Zweite Person"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
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
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1]
        self.assertEqual(last_change.attrib, {"when": "2022-07-25"})

    def test_change_reason_set_correctly(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1][-1]
        self.assertEqual(last_change.tail, "Change reason")

    def test_change_reason_set_as_tail_of_last_person_name(self):
        change = RevisionDescChange(
            person=["Vorname Nachname", "Zweite Person"],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1][-1]
        self.assertEqual(last_change.tail, "Change reason")

    def test_change_reason_set_as_text_of_change_element_if_name_missing(self):
        change = RevisionDescChange(
            person=[],
            date="2022-07-25",
            reason="Change reason",
        )
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        revision_desc = tree.find(".//revisionDesc")
        last_change = revision_desc[-1]
        self.assertEqual(last_change.text, "Change reason")

    def test_no_person_name_inserted_if_missing(self):
        change = RevisionDescChange(person=[], date="2022-02-20", reason="Some reason")
        self.transformer.set_list_of_observers(([FakeObserver()], []))
        xml = etree.parse(
            io.BytesIO(
                b"<teiHeader><revisionDesc><change>0</change></revisionDesc></teiHeader>"
            )
        ).getroot()
        tree = self.transformer.add_change_to_revision_desc(xml, change)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(result, ["teiHeader", "revisionDesc", "change", "change"])

    def test_namespace_to_tei_element_added_if_tei_namespace_observer_is_passed(self):
        self.transformer.set_list_of_observers(([TeiNamespaceObserver()], []))
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
        tree = self.transformer.perform_transformation(xml)
        self.assertTrue("http://www.tei-c.org/ns/1.0" in tree.nsmap.values())

    def test_tei_namespace_added_to_child_nodes(self):
        self.transformer.set_list_of_observers(([TeiNamespaceObserver()], []))
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
        tree = self.transformer.perform_transformation(xml)
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

    def test_xml_changed_flag_reset_after_each_document(self):
        change = RevisionDescChange(
            person=["Vorname Nachname"],
            date="2022-07-25",
            reason="Change reason",
        )
        transformer = TeiTransformer(FakeIterator())
        transformer.set_list_of_observers(
            ([FakeObserver(tag="oldTag", action=change_tag)], [])
        )
        doc1 = io.BytesIO(
            b"""
                <TEI>
                    <teiHeader>
                        <fileDesc/>
                    </teiHeader>
                    <text>
                      <body>
                        <oldTag>text</oldTag>
                      </body>
                    </text>
                </TEI>
                """
        )
        doc2 = io.BytesIO(
            b"""
                <TEI>
                    <teiHeader>
                        <fileDesc/>
                    </teiHeader>
                    <text>
                      <body>
                        <otherTag>text</otherTag>
                      </body>
                    </text>
                </TEI>
                """
        )
        doc4 = io.BytesIO(
            b"""
                <TEI>
                    <teiHeader>
                        <fileDesc/>
                    </teiHeader>
                    <text>
                      <body>
                        <someTag>text</someTag>
                      </body>
                    </text>
                </TEI>
                """
        )
        doc3 = io.BytesIO(
            b"""
                <TEI>
                    <teiHeader>
                        <fileDesc/>
                    </teiHeader>
                    <text>
                      <body>
                        <oldTag/>
                        <oldTag>text</oldTag>
                      </body>
                    </text>
                </TEI>
                """
        )
        docs = [doc1, doc2, doc3, doc4]
        result = []
        for doc in docs:
            tree = transformer.perform_transformation(doc)
            if transformer.xml_tree_changed():
                transformer.add_change_to_revision_desc(tree, change)
            rev_desc_added = tree.find(".//{*}revisionDesc") is not None
            result.append(rev_desc_added)
        self.assertEqual(result, [True, False, True, False])

    def test_both_lists_of_observers_applied(self):
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(
            (
                [FakeObserver("match", action=change_tag)],
                [FakeObserver("newTag", action=remove_id_attrib)],
            )
        )
        xml = io.BytesIO(
            b"""
        <TEI>
          <text>
            <match id='matching node'>
              <subnode attribute="not matching"/>
            </match>
          </text>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = tree.find(".//newTag").attrib
        self.assertEqual(result, {})

    def test_both_lists_of_observers_applied_different_output_for_different_order(self):
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(
            (
                [FakeObserver("newTag", action=remove_id_attrib)],
                [FakeObserver("match", action=change_tag)],
            )
        )
        xml = io.BytesIO(
            b"""
        <TEI>
          <text>
            <match id='matching node'>
              <subnode attribute="not matching"/>
            </match>
          </text>
        </TEI>
        """
        )
        tree = transformer.perform_transformation(xml)
        result = tree.find(".//newTag").attrib
        self.assertEqual(result, {"id": "matching node"})

    def test_filename_logged_if_file_empty(self):
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(([FakeObserver()], []))
        file = os.path.join("tests", "testdata", "empty_file.xml")
        with self.assertLogs() as logger:
            transformer.perform_transformation(file)
        self.assertIn("empty_file.xml", logger.output[0])

    def test_filename_logged_if_file_not_tei(self):
        transformer = TeiTransformer(self.iterator)
        transformer.set_list_of_observers(([FakeObserver()], []))
        file = os.path.join("tests", "testdata", "no_tei_file.xml")
        with self.assertLogs() as logger:
            transformer.perform_transformation(file)
        self.assertIn("no_tei_file.xml", logger.output[0])


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
