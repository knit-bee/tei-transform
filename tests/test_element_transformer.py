import unittest

from lxml import etree

from tei_transform.element_transformer import ElementTransformer


class ElementTransformerTester(unittest.TestCase):
    def setUp(self):
        self.element_transformer = ElementTransformer()

    def test_remove_attribute_from_element(self):
        xml = etree.XML('<TEI schemaLocation="some/url"><test/></TEI>')
        self.element_transformer.remove_attribute_from_node(xml, "schemaLocation")
        self.assertTrue("schemaLocation" not in xml.attrib)

    def test_remove_attribute_with_namespace_from_element(self):
        xml = etree.XML(
            '<TEI xmlns="url1" xmlns:xsi="url2" xsi:schemaLocation="url3"><test/></TEI>'
        )
        xml_xsi_ns = xml.nsmap["xsi"]
        self.element_transformer.remove_attribute_from_node(
            xml, "schemaLocation", "xsi"
        )
        self.assertTrue(f"{{{xml_xsi_ns}}}schemaLocation" not in xml.attrib)

    def test_remove_id_attribute_from_element(self):
        xml = etree.XML('<TEI xmlns="url" id="filename.xml"><test/></TEI>')
        self.element_transformer.remove_attribute_from_node(xml, "id")
        self.assertTrue("id" not in xml.attrib)