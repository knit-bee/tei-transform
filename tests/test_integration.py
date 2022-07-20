import os
import unittest

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCaseImpl


class IntegrationTester(unittest.TestCase):
    def setUp(self):
        self.use_case = TeiTransformationUseCaseImpl()
        self.data = "testdata"

    def test_returns_none_on_empty_file(self):
        file = os.path.join(self.data, "empty_file.xml")
        request = CliRequest(file, ["teiheader"])
        result = self.use_case.process(request)
        self.assertIsNone(result)
