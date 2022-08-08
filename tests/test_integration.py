import os
import unittest

import pytest
from lxml import etree

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCaseImpl


def create_validator():
    scheme_path = os.path.join("tests", "testdata", "tei_all.rng")
    return etree.RelaxNG(etree.parse(scheme_path))


class IntegrationTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tei_validator = create_validator()

    def setUp(self):
        self.use_case = TeiTransformationUseCaseImpl()
        self.data = os.path.join("tests", "testdata")

    def test_returns_none_on_empty_file(self):
        file = os.path.join(self.data, "empty_file.xml")
        request = CliRequest(file, ["teiheader"])
        result = self.use_case.process(request)
        self.assertIsNone(result)

    def test_schemalocation_removed_from_tei_element(self):
        file = os.path.join(self.data, "file_with_schemalocation.xml")
        assert self.file_invalid_because_of_schemalocation(file)
        request = CliRequest(file, ["schemalocation"])
        result = self.use_case.process(request)
        self.assertEqual(
            (result.tag, result.attrib), ("{http://www.tei-c.org/ns/1.0}TEI", {})
        )

    def test_id_attribute_removed_from_tei_element(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        assert self.file_invalid_because_of_id_in_tei_element(file)
        request = CliRequest(file, ["id-attribute"])
        result = self.use_case.process(request)
        self.assertEqual(
            (result.tag, result.attrib), ("{http://www.tei-c.org/ns/1.0}TEI", {})
        )

    def test_type_attribute_removed_from_teiheader(self):
        file = os.path.join(self.data, "file_with_type_in_teiheader.xml")
        assert self.file_invalid_because_type_in_element(file, "teiHeader")
        request = CliRequest(file, ["teiheader"])
        result_tree = self.use_case.process(request)
        teiheader_element = result_tree[0]
        self.assertEqual(teiheader_element.attrib, {})

    def test_type_attribute_removed_from_notesstmt(self):
        file = os.path.join(self.data, "file_with_type_in_notesstmt.xml")
        assert self.file_invalid_because_type_in_element(file, "notesStmt")
        request = CliRequest(file, ["notesstmt"])
        result_tree = self.use_case.process(request)
        notesstmt_elements_attribs = [
            node.attrib for node in result_tree.iterfind(".//{*}notesStmt")
        ]
        self.assertTrue(
            all("type" not in attrib for attrib in notesstmt_elements_attribs)
        )

    def test_xml_namespace_added_to_id_attribute(self):
        file = os.path.join(self.data, "file_with_id_attribute.xml")
        assert self.file_invalid_because_id_attribute_is_missing_xml_namespace(file)
        request = CliRequest(file, ["id-attribute"])
        result_tree = self.use_case.process(request)
        nodes_with_id_attr = [
            node.tag
            for node in result_tree.iterfind(
                ".//*[@{http://www.w3.org/XML/1998/namespace}id]"
            )
        ]
        self.assertEqual(
            nodes_with_id_attr,
            [
                "{http://www.tei-c.org/ns/1.0}publisher",
                "{http://www.tei-c.org/ns/1.0}sourceDesc",
                "{http://www.tei-c.org/ns/1.0}date",
                "{http://www.tei-c.org/ns/1.0}sourceDesc",
                "{http://www.tei-c.org/ns/1.0}publisher",
                "{http://www.tei-c.org/ns/1.0}taxonomy",
            ],
        )

    def test_filename_element_renamed(self):
        file = os.path.join(self.data, "file_with_filename_element.xml")
        assert self.file_invalid_because_of_filename_element(file)
        request = CliRequest(file, ["filename-element"])
        result_tree = self.use_case.process(request)
        filename_nodes = [node.tag for node in result_tree.iterfind(".//{*}filename")]
        self.assertEqual(filename_nodes, [])

    # decorator to be removed later if issue is solved
    @pytest.mark.xfail(
        reason="<idno/> not valid TEI as replacement for <filename/> in <fileDesc/>"
    )
    def test_file_is_valid_tei_when_all_transformations_are_applied(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        request = CliRequest(
            file,
            [
                "teiheader",
                "id-attribute",
                "filename-element",
                "notesstmt",
                "schemalocation",
            ],
        )
        result = self.use_case.process(request)
        result = self.tei_validator.validate(result)
        self.assertTrue(result)

    @pytest.mark.xfail(
        reason="<idno/> not valid TEI as replacement for <filename/> in <fileDesc/>"
    )
    def test_file_is_valid_when_all_transformations_and_revision_change_applied(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        conf_file = os.path.join(self.data, "revision.config")
        request = CliRequest(
            file,
            [
                "teiheader",
                "id-attribute",
                "filename-element",
                "notesstmt",
                "schemalocation",
            ],
            config=conf_file,
        )
        result = self.use_case.process(request)
        result = self.tei_validator.validate(result)
        self.assertTrue(result)

    def test_revision_change_added(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        conf_file = os.path.join(self.data, "revision.config")
        request = CliRequest(file, ["teiheader"], config=conf_file)
        result_tree = self.use_case.process(request)
        revision_node = result_tree.find(".//{*}revisionDesc")
        last_change = revision_node[-1]
        expected = etree.Element("{http://www.tei-c.org/ns/1.0}change")
        expected.text = "The reason why the file was changed"
        expected_name = etree.Element("{http://www.tei-c.org/ns/1.0}name")
        expected_name.text = "Some Name"
        expected.set("when", "2022-05-23")
        expected.append(expected_name)
        self.assertEqual(
            (
                last_change.tag,
                last_change.text,
                last_change.attrib,
                [(child.tag, child.text) for child in last_change.getchildren()],
            ),
            (
                expected.tag,
                expected.text,
                expected.attrib,
                [(child.tag, child.text) for child in expected.getchildren()],
            ),
        )

    def test_tei_namespace_added_to_root(self):
        file = os.path.join(self.data, "file_without_tei_namespace.xml")
        request = CliRequest(file, ["tei-ns"])
        result = self.use_case.process(request)
        result_ns = result.nsmap
        self.assertEqual(
            (result_ns, result.tag),
            (
                {None: "http://www.tei-c.org/ns/1.0"},
                "{http://www.tei-c.org/ns/1.0}TEI",
            ),
        )

    def test_tei_namespace_added_to_children(self):
        file = os.path.join(self.data, "file_without_tei_namespace.xml")
        request = CliRequest(file, ["tei-ns"])
        transformed = self.use_case.process(request)
        new_xml = etree.tostring(transformed, encoding="utf-8")
        new_tree = etree.XML(new_xml)
        result = [node.tag for node in new_tree.getchildren()]
        self.assertEqual(
            result,
            [
                "{http://www.tei-c.org/ns/1.0}teiHeader",
                "{http://www.tei-c.org/ns/1.0}text",
            ],
        )

    def file_invalid_because_id_attribute_is_missing_xml_namespace(self, file):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = "Invalid attribute id for element"
        return any(msg.startswith(expected_error_msg) for msg in logs)

    def file_invalid_because_of_filename_element(self, file):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = "Did not expect element filename there"
        return expected_error_msg in logs

    def file_invalid_because_type_in_element(self, file, element):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = f"Invalid attribute type for element {element}"
        return expected_error_msg in logs

    def file_invalid_because_of_id_in_tei_element(self, file):
        doc = etree.parse(file)
        return "id" in doc.getroot().attrib

    def file_invalid_because_of_schemalocation(self, file):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = "Invalid attribute schemaLocation for element TEI"
        return expected_error_msg in logs

    def _get_validation_error_logs_for_file(self, file):
        doc = etree.parse(file)
        self.tei_validator.validate(doc)
        logs = self.tei_validator.error_log
        msg = [entry.message for entry in logs]
        return msg
