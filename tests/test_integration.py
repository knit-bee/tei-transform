import os
import unittest

from lxml import etree

from tei_transform.cli.use_case import CliRequest, TeiTransformationUseCaseImpl


def create_validator():
    scheme_path = os.path.join("testdata", "tei_all.rng")
    return etree.RelaxNG(etree.parse(scheme_path))


class IntegrationTester(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tei_validator = create_validator()

    def setUp(self):
        self.use_case = TeiTransformationUseCaseImpl()
        self.data = "testdata"

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
