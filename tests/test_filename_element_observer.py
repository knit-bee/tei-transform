import unittest

from lxml import etree

from tei_transform.filename_element_observer import FilenameElementObserver


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

    def test_observer_action_performed_correctly(self):
        node = etree.Element("oldTag")
        self.observer.transform_node(node)
        self.assertEqual(node.tag, "idno")

    def test_observer_action_on_nested_nodes(self):
        xml = etree.XML("<TEI><someNode><filename>file.xml</filename></someNode></TEI>")
        for node in xml.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in xml.iter()]
        self.assertEqual(result, ["TEI", "someNode", "idno"])

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
            ["TEI", "teiHeader", "fileDesc", "titleStmt", "author", "idno", "text"],
        )

    def test_namespace_prefix_preserved_after_change(self):
        xml = etree.XML(
            """
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <filename>some_file.xml</filename>
        </TEI>
        """
        )
        for node in xml.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in xml.iter()]
        self.assertEqual(
            result,
            ["{http://www.tei-c.org/ns/1.0}TEI", "{http://www.tei-c.org/ns/1.0}idno"],
        )
