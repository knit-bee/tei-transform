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
            xml, "schemaLocation", namespace="xsi"
        )
        self.assertTrue(f"{{{xml_xsi_ns}}}schemaLocation" not in xml.attrib)

    def test_remove_id_attribute_from_element(self):
        xml = etree.XML('<TEI xmlns="url" id="filename.xml"><test/></TEI>')
        self.element_transformer.remove_attribute_from_node(xml, "id")
        self.assertTrue("id" not in xml.attrib)

    def test_remove_type_attribute_in_teiheader(self):
        xml = etree.XML('<teiHeader type="text"/>')
        self.element_transformer.remove_attribute_from_node(xml, "type")
        self.assertTrue("type" not in xml.attrib)

    def test_remove_non_existing_attribute(self):
        xml = etree.XML('<teiHeader type="text"/>')
        self.element_transformer.remove_attribute_from_node(xml, "id")
        self.assertEqual(xml.attrib, {"type": "text"})

    def test_remove_non_existing_attribute_with_namespace(self):
        xml = etree.XML(
            '<TEI xmlns="url1" xmlns:xsi="url2" xsi:schemaLocation="url3"><test/></TEI>'
        )
        self.element_transformer.remove_attribute_from_node(xml, "id", namespace="xsi")
        self.assertEqual(xml.attrib, {"{url2}schemaLocation": "url3"})

    def test_remove_attribute_from_node_with_children(self):
        xml = etree.XML(
            """
        <teiHeader type="text">
            <fileDesc>
                <titleStmt>
                    <title level="a" type="main">Some great title</title>
                    <author>Author Name</author>
                </titleStmt>
            </fileDesc>
        </teiHeader>
        """
        )
        self.element_transformer.remove_attribute_from_node(xml, "type")
        self.assertTrue("type" not in xml.attrib)
        self.assertEqual(
            [node.tag for node in xml.iter()],
            ["teiHeader", "fileDesc", "titleStmt", "title", "author"],
        )

    def test_add_namespace_to_attribute_simple_node(self):
        node = etree.XML('<someElement attr="value"/>')
        self.element_transformer.add_namespace_prefix_to_attribute(
            node, "attr", namespace="some/address"
        )
        self.assertEqual(node.attrib, {"{some/address}attr": "value"})

    def test_add_namespace_to_attribute_on_node_with_multiple_attributes(self):
        node = etree.XML('<someElement attr="val1" otherAttr="val2"/>')
        self.element_transformer.add_namespace_prefix_to_attribute(
            node, "attr", namespace="some/address"
        )
        self.assertEqual(
            node.attrib, {"{some/address}attr": "val1", "otherAttr": "val2"}
        )

    def test_add_namespace_to_attribute(self):
        node = etree.XML('<TEI><someElement id="attribute"/></TEI>').getchildren()[0]
        self.element_transformer.add_namespace_prefix_to_attribute(
            node, "id", namespace="some/address"
        )
        self.assertEqual(node.attrib, {"{some/address}id": "attribute"})

    def test_add_namespace_to_non_existing_attribute(self):
        node = etree.XML('<body><someElement attr="value"/></body>').getchildren()[0]
        self.element_transformer.add_namespace_prefix_to_attribute(
            node, "id", namespace="some/address"
        )
        self.assertEqual(node.attrib, {"attr": "value"})

    def test_add_namespace_to_attribute_node_with_children(self):
        xml = etree.XML(
            """
    <teiHeader type="text">
        <fileDesc type="other">
            <titleStmt>
                <title level="a" type="main">Some great title</title>
                <author>Author Name</author>
            </titleStmt>
        </fileDesc>
    </teiHeader>
    """
        )
        self.element_transformer.add_namespace_prefix_to_attribute(
            xml, "type", namespace="xml"
        )
        self.assertEqual(xml.attrib, {"{xml}type": "text"})
        self.assertEqual(xml.getchildren()[0].attrib, {"type": "other"})

    def test_change_tag_of_simple_element(self):
        node = etree.XML("<someElement/>")
        self.element_transformer.change_element_tag(node, "newElement")
        self.assertEqual(node.tag, "newElement")

    def test_change_element_tag(self):
        xml = etree.XML(
            """
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title level="a" type="main">Some great title</title>
                        <author>Author Name</author>
                    </titleStmt>
                    <filename>file.xml</filename>
                </fileDesc>
            </teiHeader>
            """
        )
        self.element_transformer.change_element_tag(xml.find(".//filename"), "idno")
        all_tags = [node.tag for node in xml.iter()]
        self.assertTrue("filename" not in all_tags)
        self.assertTrue("idno" in all_tags)

    def test_change_tag_of_element_children_not_changed(self):
        xml = etree.XML(
            """
            <teiHeader>
                <fileDesc>
                    <titleStmt>
                        <title level="a" type="main">Some great title</title>
                        <author>Author Name</author>
                    </titleStmt>
                    <filename>file.xml</filename>
                </fileDesc>
            </teiHeader>
            """
        )
        self.element_transformer.change_element_tag(
            xml.find(".//titleStmt"), "newElement"
        )
        self.assertEqual(
            [child.tag for child in xml.find(".//newElement").iter()],
            ["newElement", "title", "author"],
        )
