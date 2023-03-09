import unittest
from typing import Optional

from tei_transform.cli.controller import TeiTransformController
from tei_transform.cli.use_case import CliRequest


class MockUseCase:
    def __init__(self) -> None:
        self.request: Optional[CliRequest] = None

    def process(self, request: CliRequest) -> None:
        assert not self.request
        self.request = request


class TeiTransformControllerTester(unittest.TestCase):
    def setUp(self):
        self.mock_use_case = MockUseCase()
        self.controller = TeiTransformController(self.mock_use_case)

    def test_controller_extracts_input_file_name(self):
        file = "testfile.xml"
        self.controller.process_arguments([file])
        self.assertEqual(self.mock_use_case.request.file_or_dir, file)

    def test_controller_extracts_list_of_observers(self):
        observer = ["obs1", "obs2", "obs3"]
        self.controller.process_arguments(["file", "--transformation"] + observer)
        self.assertEqual(self.mock_use_case.request.observers, observer)

    def test_controller_extracts_list_of_observers_with_keyword_argument(self):
        observer = ["obs1", "obs2", "obs3"]
        self.controller.process_arguments(["file", "-t"] + observer)
        self.assertEqual(self.mock_use_case.request.observers, observer)

    def test_controller_sets_default_observer_if_no_observer_was_passed(self):
        self.controller.process_arguments(["file.xml"])
        self.assertEqual(
            self.mock_use_case.request.observers,
            [
                "schemalocation",
                "id-attribute",
                "teiheader-type",
                "notesstmt",
                "filename-element",
            ],
        )

    def test_controller_extracts_config_file_name(self):
        self.controller.process_arguments(["file.xml", "--config-file", "config"])
        self.assertEqual(self.mock_use_case.request.config, "config")

    def test_controller_extracts_config_file_name_with_kw(self):
        self.controller.process_arguments(["file", "-c", "conf-file"])
        self.assertEqual(self.mock_use_case.request.config, "conf-file")

    def test_controller_returns_none_if_no_config_file_passed(self):
        self.controller.process_arguments(["file"])
        self.assertIsNone(self.mock_use_case.request.config)

    def test_extracts_output_directory_name(self):
        self.controller.process_arguments(["file.xml", "-o", "transformed_output"])
        self.assertEqual(self.mock_use_case.request.output, "transformed_output")

    def test_output_default(self):
        self.controller.process_arguments(["file"])
        self.assertEqual(self.mock_use_case.request.output, "output")

    def test_plugin_only_extracted_once_if_string_passed_multiple_times(self):
        observer = ["obs1", "obs2", "obs2", "obs2", "obs3", "obs1"]
        self.controller.process_arguments(["file", "-t"] + observer)
        self.assertEqual(self.mock_use_case.request.observers, ["obs1", "obs2", "obs3"])

    def test_default_for_validation_is_false(self):
        self.controller.process_arguments(["file"])
        self.assertEqual(self.mock_use_case.request.validation, False)

    def test_controller_extracts_no_validaiton_option(self):
        self.controller.process_arguments(["file", "--no-validation", "-o", "dir"])
        self.assertEqual(self.mock_use_case.request.validation, False)

    def test_controller_extracts_copy_valid_file_option(self):
        self.controller.process_arguments(["file", "--copy-valid"])
        self.assertEqual(self.mock_use_case.request.copy_valid, True)
        self.assertEqual(self.mock_use_case.request.validation, True)

    def test_controller_extracts_ignore_valid_file_option(self):
        self.controller.process_arguments(["file", "--ignore-valid"])
        self.assertEqual(self.mock_use_case.request.copy_valid, False)
        self.assertEqual(self.mock_use_case.request.validation, True)

    def test_controller_throws_error_if_input_is_missing(self):
        with self.assertRaises(SystemExit):
            self.controller.process_arguments(["-t", "classcode", "--copy-valid"])

    def test_default_value_for_valid_file_handling_options_set_to_false(self):
        self.controller.process_arguments(["file"])
        self.assertEqual(self.mock_use_case.request.copy_valid, False)

    def test_valid_file_handling_options_mutually_exclusive(self):
        valid_file_options = ["--no-validation", "--ignore-valid", "--copy-valid"]
        for opt1, opt2 in zip(
            valid_file_options, valid_file_options[1:] + valid_file_options[:1]
        ):
            with self.assertRaises(SystemExit):
                self.controller.process_arguments(["file", opt1, opt2])

    def test_revision_argument_requires_config_file(self):
        with self.assertRaises(SystemExit):
            self.controller.process_arguments(["file", "--revision"])

    def test_revision_argument_requires_config_file_with_flag(self):
        with self.assertRaises(SystemExit):
            self.controller.process_arguments(["file", "-r"])

    def test_controller_extracts_revision_default_false(self):
        self.controller.process_arguments(["file", "-c", "conf-file"])
        self.assertEqual(self.mock_use_case.request.add_revision, False)

    def test_controller_extracts_revision(self):
        self.controller.process_arguments(["file", "-r", "-c", "conf_file"])
        self.assertEqual(self.mock_use_case.request.add_revision, True)
