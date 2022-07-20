from lxml import etree

import tei_transform.element_transformation as et


def test_remove_attribute_from_element():
    xml = etree.XML('<TEI schemaLocation="some/url"><test/></TEI>')
    et.remove_attribute_from_node(xml, "schemaLocation")
    assert "schemaLocation" not in xml.attrib


def test_remove_attribute_with_namespace_from_element():
    xml = etree.XML(
        '<TEI xmlns="url1" xmlns:xsi="url2" xsi:schemaLocation="url3"><test/></TEI>'
    )
    xml_xsi_ns = xml.nsmap["xsi"]
    et.remove_attribute_from_node(xml, "schemaLocation", namespace="xsi")
    assert f"{{{xml_xsi_ns}}}schemaLocation" not in xml.attrib


def test_remove_id_attribute_from_element():
    xml = etree.XML('<TEI xmlns="url" id="filename.xml"><test/></TEI>')
    et.remove_attribute_from_node(xml, "id")
    assert "id" not in xml.attrib


def test_remove_type_attribute_in_teiheader():
    xml = etree.XML('<teiHeader type="text"/>')
    et.remove_attribute_from_node(xml, "type")
    assert "type" not in xml.attrib


def test_remove_non_existing_attribute():
    xml = etree.XML('<teiHeader type="text"/>')
    et.remove_attribute_from_node(xml, "id")
    assert xml.attrib == {"type": "text"}


def test_remove_non_existing_attribute_with_namespace():
    xml = etree.XML(
        '<TEI xmlns="url1" xmlns:xsi="url2" xsi:schemaLocation="url3"><test/></TEI>'
    )
    et.remove_attribute_from_node(xml, "id", namespace="xsi")
    assert xml.attrib == {"{url2}schemaLocation": "url3"}


def test_remove_attribute_from_node_with_children():
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
    et.remove_attribute_from_node(xml, "type")
    assert "type" not in xml.attrib
    assert [node.tag for node in xml.iter()] == [
        "teiHeader",
        "fileDesc",
        "titleStmt",
        "title",
        "author",
    ]


def test_add_namespace_to_attribute_simple_node():
    node = etree.XML('<someElement attr="value"/>')
    et.add_namespace_prefix_to_attribute(node, "attr", namespace="some/address")
    assert node.attrib == {"{some/address}attr": "value"}


def test_add_namespace_to_attribute_on_node_with_multiple_attributes():
    node = etree.XML('<someElement attr="val1" otherAttr="val2"/>')
    et.add_namespace_prefix_to_attribute(node, "attr", namespace="some/address")
    assert node.attrib == {"{some/address}attr": "val1", "otherAttr": "val2"}


def test_add_namespace_to_attribute():
    node = etree.XML('<TEI><someElement id="attribute"/></TEI>').getchildren()[0]
    et.add_namespace_prefix_to_attribute(node, "id", namespace="some/address")
    assert node.attrib == {"{some/address}id": "attribute"}


def test_add_namespace_to_non_existing_attribute():
    node = etree.XML('<body><someElement attr="value"/></body>').getchildren()[0]
    et.add_namespace_prefix_to_attribute(node, "id", namespace="some/address")
    assert node.attrib == {"attr": "value"}


def test_add_namespace_to_attribute_node_with_children():
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
    et.add_namespace_prefix_to_attribute(xml, "type", namespace="xml")
    assert xml.attrib == {"{xml}type": "text"}
    assert xml.getchildren()[0].attrib == {"type": "other"}


def test_change_tag_of_simple_element():
    node = etree.XML("<someElement/>")
    et.change_element_tag(node, "newElement")
    assert node.tag == "newElement"


def test_change_element_tag():
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
    et.change_element_tag(xml.find(".//filename"), "idno")
    all_tags = [node.tag for node in xml.iter()]
    assert "filename" not in all_tags
    assert "idno" in all_tags


def test_change_tag_of_element_children_not_changed():
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
    et.change_element_tag(xml.find(".//titleStmt"), "newElement")
    assert [child.tag for child in xml.find(".//newElement").iter()] == [
        "newElement",
        "title",
        "author",
    ]


def test_change_filename_element_with_namespace():
    xml = etree.XML(
        """<TEI xmlns="http://www.tei-c.org/ns/1.0">
            <teiHeader>
                <fileDesc>
                    <filename>file.xml</filename>
                </fileDesc>
            </teiHeader>
            </TEI>
            """
    )
    et.change_element_tag(xml.find(".//{*}filename"), "idno")
    all_tags = [node.tag for node in xml.iter()]
    assert all_tags == [
        "{http://www.tei-c.org/ns/1.0}TEI",
        "{http://www.tei-c.org/ns/1.0}teiHeader",
        "{http://www.tei-c.org/ns/1.0}fileDesc",
        "{http://www.tei-c.org/ns/1.0}idno",
    ]
