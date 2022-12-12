import unittest

from lxml import etree

from tei_transform.observer import FilenameElementObserver


class FilenameElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = FilenameElementObserver()

    def test_observer_identifies_matching_element(self):
        matching_elements = [
            etree.XML("<filename/>"),
            etree.XML("<filename></filename>"),
            etree.XML("<TEI><filename>file</filename></TEI>"),
            etree.XML(
                "<TEI><teiHeader><filename attr='someval'>file</filename></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><teiHeader><filename>file</filename></teiHeader></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader><titleStmt><filename/><title>title</title></titleStmt>
            </teiHeader><text><body/></text></TEI>"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<element/>"),
            etree.XML("<TEI><element>filename</element></TEI>"),
            etree.XML("<TEI><idno xml:id='filename'>file.txt</idno></TEI>"),
            etree.XML("<TEI xmlns='ns'><idno>file</idno></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(result))

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<filename/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<TEI><filename/></TEI>")
        result = self.observer.observe(node)
        self.assertFalse(result)

    def test_empty_element_removed(self):
        node = etree.XML("<parent><filename/></parent>")
        self.observer.transform_node(node[0])
        self.assertEqual(len(node), 0)

    def test_element_with_text_removed(self):
        node = etree.XML("<parent><filename>file.xml</filename></parent>")
        self.observer.transform_node(node[0])
        self.assertEqual(len(node), 0)

    def test_observer_action_on_nested_nodes(self):
        xml = etree.XML("<TEI><someNode><filename>file.xml</filename></someNode></TEI>")
        for node in xml.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in xml.iter()]
        self.assertEqual(result, ["TEI", "someNode"])

    def test_observer_action_performed_on_element_with_namespace_prefix(self):
        xml = etree.XML(
            """
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
        <teiHeader type="text">
            <fileDesc>
                <titleStmt>
                    <author>Author Name</author>
                </titleStmt>
                <filename>some_file.xml</filename>
            </fileDesc>
        </teiHeader>
        <text>hello world </text>
        </TEI>
        """
        )
        for node in xml.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in xml.iter()]
        self.assertEqual(
            result,
            [
                "TEI",
                "teiHeader",
                "fileDesc",
                "titleStmt",
                "author",
                "text",
            ],
        )

    def test_empty_element_with_attribute_removed(self):
        root = etree.XML("<teiHeader><filename type='val'/><bibl/></teiHeader>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find("filename") is None)

    def test_element_with_text_and_attribute_removed(self):
        root = etree.XML(
            "<teiHeader><filename type='val'>file</filename><bibl/></teiHeader>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find("filename") is None)

    def test_empty_element_removed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><teiHeader><filename/><bibl/></teiHeader></TEI>"
        )
        node = root.find(".//{*}filename")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}filename") is None)

    def test_element_with_text_removed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><teiHeader><filename>text</filename><bibl/></teiHeader></TEI>"
        )
        node = root.find(".//{*}filename")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}filename") is None)

    def test_empty_element_with_attribute_removed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><teiHeader><filename attr='val'/><bibl/></teiHeader></TEI>"
        )
        node = root.find(".//{*}filename")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}filename") is None)

    def test_element_with_text_and_attribute_removed_with_namespace(self):
        root = etree.XML(
            """<TEI xmlns='ns'><teiHeader>
                <filename attr='val'>text</filename>
                <bibl/>
                </teiHeader></TEI>"""
        )
        node = root.find(".//{*}filename")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}filename") is None)
