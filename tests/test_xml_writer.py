import os
import unittest

from lxml import etree

from tei_transform.xml_writer import XmlWriterImpl


class XmlWriterTester(unittest.TestCase):
    def setUp(self):
        self.data = os.path.join("tests", "testdata")
        self.output_dir = os.path.join(self.data, "output")
        self.xml_writer = XmlWriterImpl()

    def tearDown(self):
        if os.path.isdir(self.output_dir):
            for root, dirs, files in os.walk(self.output_dir, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                else:
                    os.rmdir(root)

    def test_output_file_created(self):
        file_path = os.path.join(self.output_dir, "test.xml")
        os.makedirs(self.output_dir)
        data = etree.XML("<element/>")
        self.xml_writer.write_xml(file_path, data)
        self.assertTrue(os.path.exists(file_path))

    def test_data_written_to_file(self):
        file_path = os.path.join(self.output_dir, "test.xml")
        os.makedirs(self.output_dir)
        data = etree.XML("<element/>")
        self.xml_writer.write_xml(file_path, data)
        with open(file_path, "r", encoding="utf-8") as ptr:
            file_data = ptr.read()
        xml_declaration = "<?xml version='1.0' encoding='UTF-8'?>"
        expected = f"{xml_declaration}\n{etree.tostring(data, encoding='unicode')}"
        self.assertEqual(expected, file_data)

    def test_file_created_in_nested_dir(self):
        file_path = os.path.join(self.output_dir, "subdir", "text.xml")
        os.makedirs(os.path.join(self.output_dir, "subdir"))
        data = etree.XML("<element/>")
        self.xml_writer.write_xml(file_path, data)
        self.assertTrue(os.path.exists(file_path))
