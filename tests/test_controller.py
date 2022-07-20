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
        self.assertEqual(self.mock_use_case.request.file, file)

    def test_controller_extracts_list_of_observers(self):
        observer = ["obs1", "obs2", "obs3"]
        self.controller.process_arguments(["file", "--transformation"] + observer)
        self.assertEqual(self.mock_use_case.request.observers, observer)

    def test_controller_extracts_list_of_observers_with_keyword_argument(self):
        observer = ["obs1", "obs2", "obs3"]
        self.controller.process_arguments(["file", "-t"] + observer)
        self.assertEqual(self.mock_use_case.request.observers, observer)

    def test_controlelr_sets_default_observer_if_no_observer_was_passed(self):
        self.controller.process_arguments(["file.xml"])
        self.assertEqual(
            self.mock_use_case.request.observers,
            [
                "schemalocation",
                "id-attribute",
                "teiheader",
                "notestmt",
                "filename-element",
            ],
        )
