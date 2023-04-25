import os
import unittest
from itertools import permutations
from typing import Dict, Set

from lxml import etree

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCaseImpl
from tei_transform.observer_constructor import MissingConfiguration, ObserverConstructor
from tei_transform.tei_transformer import TeiTransformer
from tei_transform.xml_tree_iterator import XMLTreeIterator
from tests.mock_observer import add_mock_plugin_entry_point


def create_validator():
    scheme_path = os.path.join("tei_transform", "tei_all.rng")
    return etree.RelaxNG(etree.parse(scheme_path))


class MockXmlWriter:
    def __init__(self, testcase: unittest.TestCase):
        self.written_data: Dict[str, etree._Element] = dict()
        self.created_dirs: Set[str] = set()
        self.copied_files: Dict[str, str] = dict()
        self.testcase = testcase

    def write_xml(self, path: str, xml: etree._Element) -> None:
        self.written_data[path] = xml

    def create_output_directories(self, output_dir: str) -> None:
        self.created_dirs.add(output_dir)

    def copy_valid_files(self, file: str, output_dir: str) -> None:
        self.copied_files[file] = output_dir

    def assertSingleDocumentWritten(self):
        self.testcase.assertEqual(len(self.written_data), 1)
        return self.written_data.popitem()


class UseCaseTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tei_validator = create_validator()

    def setUp(self):
        self.data = os.path.join("tests", "testdata")
        self.xml_writer = MockXmlWriter(testcase=self)
        self.xml_iterator = XMLTreeIterator()
        self.tei_transformer = TeiTransformer(xml_iterator=self.xml_iterator)
        self.observer_constructor = ObserverConstructor()
        self.use_case = TeiTransformationUseCaseImpl(
            xml_writer=self.xml_writer,
            tei_transformer=self.tei_transformer,
            observer_constructor=self.observer_constructor,
            tei_validator=self.tei_validator,
        )

    def test_transformer_returns_none_on_empty_file(self):
        file = os.path.join(self.data, "empty_file.xml")
        request = CliRequest(file, ["teiheader-type"])
        self.use_case.process(request)
        _, result = self.xml_writer.assertSingleDocumentWritten()
        self.assertIsNone(result)

    def test_schemalocation_removed_from_tei_element(self):
        file = os.path.join(self.data, "file_with_schemalocation.xml")
        assert self.file_invalid_because_of_schemalocation(file)
        request = CliRequest(file, ["schemalocation"])
        self.use_case.process(request)
        _, result = self.xml_writer.assertSingleDocumentWritten()
        self.assertEqual(
            (result.tag, result.attrib), ("{http://www.tei-c.org/ns/1.0}TEI", {})
        )

    def test_id_attribute_removed_from_tei_element(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        assert self.file_invalid_because_of_id_in_tei_element(file)
        request = CliRequest(file, ["id-attribute"])
        self.use_case.process(request)
        _, result = self.xml_writer.assertSingleDocumentWritten()
        self.assertEqual(
            (result.tag, result.attrib), ("{http://www.tei-c.org/ns/1.0}TEI", {})
        )

    def test_type_attribute_removed_from_teiheader(self):
        file = os.path.join(self.data, "file_with_type_in_teiheader.xml")
        assert self.file_invalid_because_type_in_element(file, "teiHeader")
        request = CliRequest(file, ["teiheader-type"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        teiheader_element = output[0]
        self.assertEqual(teiheader_element.attrib, {})

    def test_type_attribute_removed_from_notesstmt(self):
        file = os.path.join(self.data, "file_with_type_in_notesstmt.xml")
        assert self.file_invalid_because_type_in_element(file, "notesStmt")
        request = CliRequest(file, ["notesstmt"])
        self.use_case.process(request)
        _, result_tree = self.xml_writer.assertSingleDocumentWritten()
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
        self.use_case.process(request)
        _, result_tree = self.xml_writer.assertSingleDocumentWritten()
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
        self.use_case.process(request)
        _, result_tree = self.xml_writer.assertSingleDocumentWritten()
        filename_nodes = [node.tag for node in result_tree.iterfind(".//{*}filename")]
        self.assertEqual(filename_nodes, [])

    def test_file_is_valid_tei_when_multiple_transformations_are_applied(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_id_in_tei.xml",
            [
                "teiheader-type",
                "id-attribute",
                "filename-element",
                "notesstmt",
                "schemalocation",
            ],
        )
        self.assertTrue(result)

    def test_file_is_valid_when_multiple_transformations_and_revision_change_applied(
        self,
    ):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        conf_file = os.path.join(self.data, "revision.config")
        request = CliRequest(
            file,
            [
                "teiheader-type",
                "id-attribute",
                "filename-element",
                "notesstmt",
                "schemalocation",
            ],
            config=conf_file,
            add_revision=True,
        )
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = self.tei_validator.validate(output)
        self.assertEqual(len(output.find(".//{*}revisionDesc")), 3)
        self.assertTrue(result)

    def test_revision_change_added(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        conf_file = os.path.join(self.data, "revision.config")
        request = CliRequest(
            file, ["teiheader-type"], config=conf_file, add_revision=True
        )
        self.use_case.process(request)
        _, result_tree = self.xml_writer.assertSingleDocumentWritten()
        revision_node = result_tree.find(".//{*}revisionDesc")
        last_change = revision_node[-1]
        expected = etree.Element("{http://www.tei-c.org/ns/1.0}change")
        expected_name = etree.Element("{http://www.tei-c.org/ns/1.0}name")
        expected_name.tail = "The reason why the file was changed"
        expected_name.text = "Some Name"
        expected.set("when", "2022-05-23")
        expected.append(expected_name)
        self.assertEqual(
            (
                last_change.tag,
                last_change.attrib,
                [
                    (child.tag, child.text, child.tail)
                    for child in last_change.getchildren()
                ],
            ),
            (
                expected.tag,
                expected.attrib,
                [
                    (child.tag, child.text, child.tail)
                    for child in expected.getchildren()
                ],
            ),
        )

    def test_output_created_for_file_as_input(self):
        file = os.path.join(self.data, "dir_with_files", "file1.xml")
        request = CliRequest(file, [])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        self.assertTrue(isinstance(output, etree._Element))

    def test_output_created_for_directory_as_input(self):
        input_dir = os.path.join(self.data, "dir_with_files")
        request = CliRequest(input_dir, [])
        self.use_case.process(request)
        result = [
            isinstance(root, etree._Element)
            for filename, root in self.xml_writer.written_data.items()
        ]
        self.assertEqual(len(result), 3)

    def test_output_created_for_directory_with_subdirs_as_input(self):
        input_dir = os.path.join(self.data, "dir_with_subdirs")
        request = CliRequest(input_dir, [])
        self.use_case.process(request)
        result = [
            isinstance(root, etree._Element)
            for file, root in self.xml_writer.written_data.items()
        ]
        self.assertEqual(len(result), 6)

    def test_output_is_valid_tei_when_multiple_transformations_applied(self):
        file = os.path.join(self.data, "file_with_id_in_tei.xml")
        conf_file = os.path.join(self.data, "revision.config")
        request = CliRequest(
            file,
            [
                "teiheader-type",
                "id-attribute",
                "filename-element",
                "notesstmt",
                "schemalocation",
            ],
            config=conf_file,
            add_revision=True,
        )
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = self.tei_validator.validate(output)
        self.assertTrue(result)

    def test_tei_namespace_added_to_root(self):
        file = os.path.join(self.data, "file_without_tei_namespace.xml")
        request = CliRequest(file, ["tei-ns"])
        self.use_case.process(request)
        _, result = self.xml_writer.assertSingleDocumentWritten()
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
        self.use_case.process(request)
        _, transformed = self.xml_writer.assertSingleDocumentWritten()
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

    def test_head_element_for_subheading_renamed(self):
        file = os.path.join(self.data, "file_with_head_after_p.xml")
        assert self.file_invalid_because_head_after_p(file)
        request = CliRequest(file, ["p-head"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = output.find(".//{*}ab")
        self.assertEqual(
            (result.getprevious().tag, result.text),
            ("{http://www.tei-c.org/ns/1.0}p", "Subheading"),
        )

    def test_type_attribute_removed_from_head_node(self):
        file = os.path.join(self.data, "file_with_head_with_type_attr.xml")
        assert etree.parse(file).getroot().find(".//{*}head[@type]") is not None
        request = CliRequest(file, ["head-type"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = output.find(".//{*}head[@type]")
        self.assertIsNone(result)

    def test_textclass_element_renamed(self):
        file = os.path.join(self.data, "file_with_misspelled_textclass.xml")
        assert self.file_invalid_because_textclass_misspelled(file)
        request = CliRequest(file, ["textclass"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = output.find(".//{*}textclass")
        self.assertIsNone(result)

    def test_classcode_element_renamed(self):
        file = os.path.join(self.data, "file_with_misspelled_classcode.xml")
        assert self.file_invalid_because_classcode_misspelled(file)
        request = CliRequest(file, ["classcode"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = output.find(".//{*}classcode")
        self.assertIsNone(result)

    def test_tail_text_removed_and_added_under_new_p_element(self):
        file = os.path.join(self.data, "file_with_tail_text.xml")
        request = CliRequest(file, ["tail-text"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = [
            (node.tag, node.text.strip(), node.tail)
            for node in output.find(".//{*}text").iter("{*}p")
        ]
        self.assertEqual(
            result,
            [
                ("{http://www.tei-c.org/ns/1.0}p", "text", None),
                ("{http://www.tei-c.org/ns/1.0}p", "tail", None),
            ],
        )

    def test_new_div_added_for_p_as_sibling_of_div(self):
        file = os.path.join(self.data, "file_with_p_next_to_div.xml")
        request = CliRequest(file, ["p-div-sibling"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = [
            (
                etree.QName(node).localname,
                [etree.QName(child).localname for child in node.getchildren()],
            )
            for node in output.find(".//{*}text").iter()
        ]
        self.assertEqual(
            result,
            [
                ("text", ["body"]),
                ("body", ["div", "div"]),
                ("div", []),
                ("div", ["p"]),
                ("p", []),
            ],
        )

    def test_text_from_div_element_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_text_in_div.xml", ["div-text"]
        )
        self.assertTrue(result)

    def test_double_item_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_double_item.xml", ["double-item"]
        )
        self.assertTrue(result)

    def test_new_div_added_for_list_as_sibling_of_div(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_list_next_to_div.xml", ["div-sibling"]
        )
        self.assertTrue(result)

    def test_double_cell_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_double_cell.xml", ["double-cell"]
        )
        self.assertTrue(result)

    def test_hi_with_wrong_parent_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_hi_with_wrong_parent.xml", ["hi-parent"]
        )
        self.assertTrue(result)

    def test_output_file_for_single_file_constructed_correctly(self):
        file = os.path.join(self.data, "dir_with_files", "file1.xml")
        request = CliRequest(file, [])
        self.use_case.process(request)
        file, _ = self.xml_writer.assertSingleDocumentWritten()
        self.assertEqual(file, os.path.join("output", "file1.xml"))

    def test_output_filenames_resolved_correctly_for_directory_as_input(self):
        directory = os.path.join(self.data, "dir_with_files")
        request = CliRequest(directory, [])
        self.use_case.process(request)
        result = sorted(self.xml_writer.written_data.keys())
        self.assertEqual(
            result,
            [
                os.path.join("output", "dir_with_files", "file1.xml"),
                os.path.join("output", "dir_with_files", "file2.xml"),
                os.path.join("output", "dir_with_files", "file3.xml"),
            ],
        )

    def test_output_filenames_resolved_correctly_for_dir_with_subdirs_as_input(self):
        directory = os.path.join(self.data, "dir_with_subdirs")
        request = CliRequest(directory, [])
        self.use_case.process(request)
        result = sorted(self.xml_writer.written_data.keys())
        self.assertEqual(
            result,
            [
                os.path.join("output", "dir_with_subdirs", "dir1", "file11.xml"),
                os.path.join("output", "dir_with_subdirs", "dir1", "file12.xml"),
                os.path.join(
                    "output", "dir_with_subdirs", "dir2", "subdir1", "file211.xml"
                ),
                os.path.join(
                    "output", "dir_with_subdirs", "dir2", "subdir1", "file212.xml"
                ),
                os.path.join(
                    "output", "dir_with_subdirs", "dir2", "subdir2", "file221.xml"
                ),
                os.path.join(
                    "output", "dir_with_subdirs", "dir2", "subdir2", "file222.xml"
                ),
            ],
        )

    def test_no_output_created_on_empty_input_dir(self):
        directory = os.path.join(self.data, "empty")
        request = CliRequest(directory, [])
        self.use_case.process(request)
        self.assertFalse(self.xml_writer.written_data)

    def test_only_files_with_xml_ending_processed_from_directory(self):
        directory = os.path.join(self.data, "mixed_dir")
        request = CliRequest(directory, [])
        self.use_case.process(request)
        result = sorted(self.xml_writer.written_data.keys())
        self.assertEqual(
            result,
            [
                os.path.join("output", "mixed_dir", "file1.xml"),
                os.path.join("output", "mixed_dir", "file2.xml"),
                os.path.join("output", "mixed_dir", "file3.xml"),
            ],
        )

    def test_no_output_created_for_single_file_that_is_not_xml(self):
        file = os.path.join(self.data, "mixed_dir", "other_file.txt")
        request = CliRequest(file, [])
        self.use_case.process(request)
        self.assertFalse(self.xml_writer.written_data)

    def test_path_with_trailing_backslash_resolved_to_correct_file_path(self):
        directory = os.path.join(self.data, "mixed_dir", "")
        request = CliRequest(directory, [])
        self.use_case.process(request)
        result = sorted(self.xml_writer.written_data.keys())
        self.assertEqual(
            result,
            [
                os.path.join("output", "mixed_dir", "file1.xml"),
                os.path.join("output", "mixed_dir", "file2.xml"),
                os.path.join("output", "mixed_dir", "file3.xml"),
            ],
        )

    def test_byline_with_following_p_resolved(self):
        file = os.path.join(self.data, "file_with_p_after_byline.xml")
        request = CliRequest(file, ["byline-sibling"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        # document still invalid bc <p> follows <div> but <byline> resolved
        byline_element = output.find(".//{*}byline")
        result = self.tei_validator.validate(output)
        self.assertTrue(byline_element.getnext() is None)
        self.assertEqual(result, False)

    def test_multiple_alternating_byline_and_p_resolved(self):
        file = os.path.join(self.data, "file_with_alternating_p_byline.xml")
        request = CliRequest(file, ["byline-sibling"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        byline_elements = output.findall(".//{*}byline")
        result = [elem.getnext() is None for elem in byline_elements]
        self.assertTrue(all(result))

    def test_p_after_byline_file_valid_if_p_div_sibling_also_called(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_p_after_byline.xml",
            ["byline-sibling", "p-div-sibling"],
        )
        self.assertTrue(result)

    def test_order_of_plugins_not_important_for_byline_p_and_p_div_sibling(self):
        file = "file_with_alternating_p_byline.xml"
        plugins_to_use = [
            ["byline-sibling", "p-div-sibling"],
            ["p-div-sibling", "byline-sibling"],
        ]
        for plugins in plugins_to_use:
            with self.subTest():
                result = self._validate_file_processed_with_plugins(file, plugins)
                self.assertTrue(result)

    def test_byline_with_following_div_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_div_after_byline.xml", ["byline-sibling"]
        )
        self.assertTrue(result)

    def test_empty_publisher_inserted(self):
        file = os.path.join(self.data, "file_with_missing_publisher.xml")
        request = CliRequest(file, ["missing-publisher"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = self.tei_validator.validate(output)
        first_publ_stmt = output.find(".//{*}publicationStmt")
        self.assertEqual(etree.QName(first_publ_stmt[0]).localname, "publisher")
        self.assertTrue(result)

    def test_no_interference_for_multiple_plugins_targeting_consecutive_or_same_nodes(
        self,
    ):
        file = os.path.join(self.data, "file_with_broken_publicationstmt.xml")
        request = CliRequest(file, ["missing-publisher", "id-attribute", "head-type"])
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        publ_stmt_elements = output.findall(".//{*}publicationStmt")
        publisher_added_to_first_publ_stmt = all(
            [
                etree.QName(publ_stmt[0]).localname == "publisher"
                for publ_stmt in publ_stmt_elements[:2]
            ]
        )
        xml_ns_added = "id" not in publ_stmt_elements[0][2].attrib
        type_attr_removed = "type" not in output.find(".//{*}teiHeader//{*}head").attrib
        publisher_not_added_to_last_publ_stmt = (
            publ_stmt_elements[2].find("{*}publisher") is None
        )
        self.assertTrue(
            all(
                [
                    publisher_added_to_first_publ_stmt,
                    xml_ns_added,
                    type_attr_removed,
                    publisher_not_added_to_last_publ_stmt,
                ]
            )
        )

    def test_related_item_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_text_in_related_item.xml", ["rel-item"]
        )
        self.assertTrue(result)

    def test_output_file_and_dirs_created(self):
        input_dir = os.path.join(self.data, "dir_with_subdirs")
        request = CliRequest(input_dir, [])
        self.use_case.process(request)
        output_dir = os.path.join("output", "dir_with_subdirs")
        expected = {
            os.path.join(output_dir, "dir1"),
            os.path.join(output_dir, "dir2", "subdir1"),
            os.path.join(output_dir, "dir2", "subdir2"),
        }
        self.assertEqual(expected, self.xml_writer.created_dirs)
        self.assertEqual(len(self.xml_writer.written_data), 6)

    def test_valid_files_copied_to_output_dir_with_copy_valid_option(self):
        input_dir = os.path.join(self.data, "dir_with_only_valid_files")
        request = CliRequest(
            input_dir, ["byline-sibling"], validation=True, copy_valid=True
        )
        self.use_case.process(request)
        self.assertEqual(len(self.xml_writer.written_data), 0)
        expected = [
            os.path.join(input_dir, "file1.xml"),
            os.path.join(input_dir, "file2.xml"),
        ]
        self.assertEqual(sorted(self.xml_writer.copied_files.keys()), expected)

    def test_valid_files_skipped_with_ignored_valid_option(self):
        input_dir = os.path.join(self.data, "dir_with_some_valid_files")
        request = CliRequest(input_dir, [], validation=True, copy_valid=False)
        self.use_case.process(request)
        self.assertEqual(len(self.xml_writer.written_data), 1)
        self.assertEqual(len(self.xml_writer.copied_files), 0)

    def test_validator_instantiated_if_no_object_passed_as_validator(self):
        request = CliRequest("file", [], validation=True)
        use_case = TeiTransformationUseCaseImpl(
            xml_writer=self.xml_writer,
            tei_transformer=self.tei_transformer,
            observer_constructor=self.observer_constructor,
            tei_scheme=os.path.join("tei_transform", "tei_all.rng"),
        )
        use_case.process(request)
        self.assertTrue(use_case.tei_validator is not None)

    def test_rng_scheme_not_found_raises_system_exit(self):
        request = CliRequest("file", [], validation=True)
        use_case = TeiTransformationUseCaseImpl(
            xml_writer=self.xml_writer,
            tei_transformer=self.tei_transformer,
            observer_constructor=self.observer_constructor,
            tei_scheme=os.path.join("tests", "testdata", "non_existing"),
        )
        with self.assertRaises(SystemExit):
            use_case.process(request)

    def test_invalid_xml_for_rng_scheme_raises_system_exit(self):
        request = CliRequest("file", [], validation=True)
        use_case = TeiTransformationUseCaseImpl(
            xml_writer=self.xml_writer,
            tei_transformer=self.tei_transformer,
            observer_constructor=self.observer_constructor,
            tei_scheme=os.path.join("tests", "testdata", "empty_file.xml"),
        )
        with self.assertRaises(SystemExit):
            use_case.process(request)

    def test_invalid_rng_scheme_raises_system_exit(self):
        request = CliRequest("file", [], validation=True)
        use_case = TeiTransformationUseCaseImpl(
            xml_writer=self.xml_writer,
            tei_transformer=self.tei_transformer,
            observer_constructor=self.observer_constructor,
            tei_scheme=os.path.join("tests", "testdata", "file_with_head_after_p.xml"),
        )
        with self.assertRaises(SystemExit):
            use_case.process(request)

    def test_revision_change_added_only_to_changed_files_if_some_were_valid(self):
        input_dir = os.path.join(self.data, "dir_with_subdir_and_valid_files")
        conf_file = os.path.join(self.data, "revision.config")
        request = CliRequest(
            input_dir,
            ["byline-sibling"],
            validation=False,
            config=conf_file,
            add_revision=True,
        )
        self.use_case.process(request)
        result = sorted(
            [
                (os.path.basename(filename), len(root.findall(".//{*}change")))
                for filename, root in self.xml_writer.written_data.items()
            ]
        )
        expected = [
            ("file1.xml", 2),
            ("file2.xml", 2),
            ("file3.xml", 2),
            ("invalid_file1.xml", 3),
            ("invalid_file2.xml", 3),
        ]
        self.assertEqual(result, expected)

    def test_empty_table_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_tables.xml", ["empty-elem"]
        )
        self.assertTrue(result)

    def test_empty_list_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_lists.xml", ["empty-elem"]
        )
        self.assertTrue(result)

    def test_empty_row_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_rows.xml", ["empty-elem"]
        )
        self.assertTrue(result)

    def test_lonely_row_wrapped_in_table(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_lonely_row.xml", ["lonely-row"]
        )
        self.assertTrue(result)

    def test_lonely_cell_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_lonely_cell.xml", ["lonely-cell"]
        )
        self.assertTrue(result)

    def test_div_sibling_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_div_siblings.xml", ["div-sibling"]
        )
        self.assertTrue(result)

    def test_text_in_list_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_text_in_list.xml", ["list-text"]
        )
        self.assertTrue(result)

    def test_type_attribute_removed_from_author_element(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_author_type_attr.xml", ["author-type"]
        )
        self.assertTrue(result)

    def test_code_element_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_wrong_code_elem.xml", ["code-elem"]
        )
        self.assertTrue(result)

    def test_double_plike_elements_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_nested_p_like.xml", ["double-plike"]
        )
        self.assertTrue(result)

    def test_combination_of_code_elem_and_double_plike_plugin(self):
        file = "file_with_code_with_p_like_child.xml"
        plugins_to_use = ["code-elem", "double-plike"]
        for plugins in [plugins_to_use, plugins_to_use[::-1]]:
            result = self._validate_file_processed_with_plugins(file, plugins)
            with self.subTest():
                self.assertTrue(result)

    def test_wrong_div_parent_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_wrong_div_parent.xml", ["div-parent"]
        )
        self.assertTrue(result)

    def test_combination_of_div_parent_and_other_plugins(self):
        file = "file_with_wrong_div_parent2.xml"
        plugins = [
            "div-parent",
            "div-text",
            "tail-text",
            "p-div-sibling",
            "div-sibling",
            "hi-parent",
        ]
        for plugins_to_use in list(permutations(plugins)):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_lonely_item_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_lonely_item.xml", ["lonely-item"]
        )
        self.assertTrue(result)

    def test_combination_of_p_div_sibling_with_tail_text(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_tail_on_p.xml", ["p-div-sibling", "tail-text"]
        )
        self.assertTrue(result)

    def test_combination_of_div_sibling_and_lonely_element_plugins(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_lonely_elems_next_to_div.xml",
            ["div-sibling", "lonely-row", "lonely-cell", "p-div-sibling"],
        )
        self.assertTrue(result)

    def test_tail_on_list_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_tail_on_list.xml", ["tail-text"]
        )
        self.assertTrue(result)

    def test_tail_on_table_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_tail_on_table.xml", ["tail-text"]
        )
        self.assertTrue(result)

    def test_text_in_table_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_text_in_table.xml", ["table-text"]
        )
        self.assertTrue(result)

    def test_lb_with_div_parent_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_linebreak_in_div.xml", ["lb-div"]
        )
        self.assertTrue(result)

    def test_tail_of_div_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_tail_on_div.xml", ["div-tail"]
        )
        self.assertTrue(result)

    def test_combination_of_div_tail_and_p_div_sibling(self):
        file = "file_with_tail_on_div2.xml"
        plugins = ["div-tail", "p-div-sibling"]
        for plugins_to_use in permutations(plugins):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_fw_with_p_child_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_p_in_fw.xml", ["fw-child"]
        )
        self.assertTrue(result)

    def test_fw_with_list_child_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_list_in_fw.xml", ["fw-child"]
        )
        self.assertTrue(result)

    def test_combination_of_fw_child_double_plike(self):
        file = "file_with_p_and_list_in_fw.xml"
        plugins = ["fw-child", "double-plike"]
        for plugins_to_use in permutations(plugins):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_nested_fw_and_children(self):
        file = "file_with_nested_fw_and_children.xml"
        plugins = ["fw-child", "double-plike", "nested-fw"]
        for plugins_to_use in permutations(plugins):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_multiple_nested_fw_with_list_child_resolved(self):
        file = "file_with_nested_fw.xml"
        plugins = ["fw-child", "nested-fw"]
        for plugins_to_use in permutations(plugins):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_fw_with_tail_resolved(self):
        file = "file_with_nested_fw_and_tail.xml"
        plugins = ["fw-child", "nested-fw"]
        for plugins_to_use in permutations(plugins):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_tail_on_quote_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_tail_on_quote.xml", ["tail-text"]
        )
        self.assertTrue(result)

    def test_nested_table_and_list_in_fw_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_table_in_fw.xml", ["fw-child", "nested-fw"]
        )
        self.assertTrue(result)

    def test_unfinished_table_and_list_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_unfinished_elements.xml", ["unfinished-elem"]
        )
        self.assertTrue(result)

    def test_pass_configuration_from_config_file_to_observer(self):
        add_mock_plugin_entry_point(
            self.observer_constructor,
            "mock",
            "tests.mock_observer:MockConfigurableObserver",
        )
        file = os.path.join(self.data, "file_with_target_to_configure.xml")
        cfg_file = os.path.join(self.data, "conf_files", "config")
        request = CliRequest(file, ["mock"], config=cfg_file)
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = output.find(".//{*}target").attrib
        self.assertEqual(result, {"attribute": "some value"})

    def test_scheme_attribute_resolved(self):
        cfg_file = os.path.join(self.data, "conf_files", "scheme.cfg")
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_scheme.xml", ["empty-scheme"], config=cfg_file
        )
        self.assertTrue(result)

    def test_missing_configuration_for_empty_scheme_raises_error(self):
        with self.assertRaises(MissingConfiguration):
            self._validate_file_processed_with_plugins(
                "file_with_empty_scheme.xml", ["empty-scheme"]
            )

    def test_measure_quantity_attribute_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_measure_quantity_attribute.xml", ["mq-attr"]
        )
        self.assertTrue(result)

    def test_empty_body_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_body.xml", ["empty-body"]
        )
        self.assertTrue(result)

    def test_text_in_body_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_text_in_body.xml", ["body-text"]
        )
        self.assertTrue(result)

    def test_misused_opener_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_misused_opener.xml", ["misused-opener"]
        )
        self.assertTrue(result)

    def test_remove_classcode_with_empty_scheme(self):
        cfg_file = os.path.join(self.data, "conf_files", "remove-scheme.cfg")
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_scheme.xml", ["empty-scheme"], config=cfg_file
        )
        self.assertTrue(result)

    def test_byline_with_figure(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_byline_and_figure.xml", ["byline-sibling", "p-div-sibling"]
        )
        self.assertTrue(result)

    def test_misused_byline_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_misused_byline.xml", ["misused-byline"]
        )
        self.assertTrue(result)

    def test_combination_of_empty_body_and_body_text(self):
        plugins = ["body-text", "empty-body"]
        for plugins_to_use in permutations(plugins):
            with self.subTest():
                self.assertTrue(
                    self._validate_file_processed_with_plugins(
                        "file_with_body_with_text_and_children.xml", plugins_to_use
                    )
                )

    def test_combintation_of_misused_byline_and_opener(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_byline_and_opener.xml", ["misused-byline", "misused-opener"]
        )
        self.assertTrue(result)

    def test_hi_child_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_p_in_hi.xml", ["hi-child"]
        )
        self.assertTrue(result)

    def test_empty_keywords_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_keywords.xml", ["empty-kw"]
        )
        self.assertTrue(result)

    def test_missing_p_parent_resolved(self):
        cfg_file = os.path.join(self.data, "conf_files", "p-parent.cfg")
        result = self._validate_file_processed_with_plugins(
            "file_with_missing_p_parent.xml", ["p-parent"], config=cfg_file
        )
        self.assertTrue(result)

    def test_list_with_wrong_children_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_list_with_wrong_children.xml", ["list-child"]
        )
        self.assertTrue(result)

    def test_combination_of_list_child_and_unfinished_elem_not_empty_item_added(self):
        file = os.path.join(self.data, "file_with_list_with_wrong_children.xml")
        plugins = ["list-child", "unfinished-elem"]
        for plugins_to_use in permutations(plugins):
            request = CliRequest(file, plugins_to_use)
            self.use_case.process(request)
            _, output = self.xml_writer.assertSingleDocumentWritten()
            target_list = output.find(".//{*}list")
            with self.subTest():
                self.assertEqual(len(target_list), 1)
                self.assertTrue(target_list.find("{*}item/{*}p") is not None)

    def test_lang_ident_resolved(self):
        cfg_file = os.path.join(self.data, "conf_files", "lang-ident.cfg")
        result = self._validate_file_processed_with_plugins(
            "file_with_missing_lang_code.xml", ["lang-ident"], config=cfg_file
        )
        self.assertTrue(result)

    def test_invalid_note_in_respStmt_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_invalid_note_in_respstmt.xml", ["resp-note"]
        )
        self.assertTrue(result)

    def test_unicode_whitespace_characters_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_unicode_whitespace.xml", ["tail-text"]
        )
        self.assertTrue(result)

    def test_missing_body_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_missing_body.xml", ["missing-body"]
        )
        self.assertTrue(result)

    def test_combination_of_missing_body_with_other_plugin(self):
        file = "file_missing_body_and_invalid_list.xml"
        plugins = ["missing-body", "empty-elem", "list-text", "tail-text"]
        for plugins_to_use in permutations(plugins):
            result = self._validate_file_processed_with_plugins(file, plugins_to_use)
            with self.subTest():
                self.assertTrue(result)

    def test_text_in_availability_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_text_in_availability.xml", ["avail-text"]
        )
        self.assertTrue(result)

    def test_ul_element_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_ul_elements.xml", ["ul-elem"]
        )
        self.assertTrue(result)

    def test_configured_author_type_plugin(self):
        cfg = os.path.join(self.data, "conf_files", "author.cfg")
        result = self._validate_file_processed_with_plugins(
            "file_with_author_type_attr.xml", ["author-type"], config=cfg
        )
        self.assertTrue(result)

    def test_invalid_attribute_removed(self):
        cfg_file = os.path.join(self.data, "conf_files", "invalid-attr.cfg")
        result = self._validate_file_processed_with_plugins(
            "file_with_invalid_attributes.xml", ["invalid-attr"], config=cfg_file
        )
        self.assertTrue(result)

    def test_misplaced_notesstmt_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_misplaced_notesstmt.xml", ["misp-notesstmt"]
        )
        self.assertTrue(result)

    def test_misused_l_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_l_in_s.xml", ["misused-l"]
        )
        self.assertTrue(result)

    def test_lonely_s_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_lonely_s.xml", ["lonely-s"]
        )
        self.assertTrue(result)

    def test_num_value_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_value_on_num.xml", ["num-value"]
        )
        self.assertTrue(result)

    def test_empty_stmt_in_header_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_stmt.xml", ["empty-stmt"]
        )
        self.assertTrue(result)

    def test_empty_target_attribute_removed(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_empty_target_in_ptr.xml", ["ptr-target"]
        )
        self.assertTrue(result)

    def test_head_with_wrong_parent_resolved(self):
        result = self._validate_file_processed_with_plugins(
            "file_with_head_with_wrong_parent.xml", ["head-parent"]
        )
        self.assertTrue(result)

    def file_invalid_because_classcode_misspelled(self, file):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = "Did not expect element classcode there"
        return expected_error_msg in logs

    def file_invalid_because_textclass_misspelled(self, file):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = "Did not expect element textclass there"
        return expected_error_msg in logs

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

    def file_invalid_because_head_after_p(self, file):
        logs = self._get_validation_error_logs_for_file(file)
        expected_error_msg = "Did not expect element head there"
        return expected_error_msg in logs

    def _get_validation_error_logs_for_file(self, file):
        doc = etree.parse(file)
        self.tei_validator.validate(doc)
        logs = self.tei_validator.error_log
        msg = [entry.message for entry in logs]
        return msg

    def _validate_file_processed_with_plugins(
        self, file_name, plugin_list, config=None
    ):
        file = os.path.join(self.data, file_name)
        request = CliRequest(file, plugin_list, config=config)
        self.use_case.process(request)
        _, output = self.xml_writer.assertSingleDocumentWritten()
        result = self.tei_validator.validate(output)
        return result
