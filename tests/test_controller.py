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
                "teiheader",
                "notesstmt",
                "filename-element",
            ],
        )

    def test_controller_extracts_config_file_name(self):
        self.controller.process_arguments(["file.xml", "--revision_config", "config"])
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
