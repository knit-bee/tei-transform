import unittest

from lxml import etree

from tei_transform.observer import RespStmtNoteObserver


class RespStmtNoteObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = RespStmtNoteObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<respStmt><note>text</note></respStmt>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<respStmt><resp><note>text</note></resp></respStmt>")
        node = root.find(".//note")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<respStmt><name/><note/></respStmt>"),
            etree.XML("<respStmt><orgName>org</orgName><note/></respStmt>"),
            etree.XML(
                "<respStmt><persName>name</persName><note>text</note></respStmt>"
            ),
            etree.XML("<respStmt><orgName/><note/><resp/></respStmt>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><respStmt><note/><name/></respStmt></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><respStmt><name>N</name><note>text</note></respStmt></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<respStmt><resp/><orgName/><note/><resp/></respStmt>"),
            etree.XML("<respStmt><resp/><name/></respStmt>"),
            etree.XML(
                "<respStmt><resp>a</resp><name>n</name><note>text</note></respStmt>"
            ),
            etree.XML("<respStmt><resp/><note/><orgName/></respStmt>"),
            etree.XML(
                "<respStmt><resp><note>text</note></resp><orgName>org</orgName></respStmt>"
            ),
            etree.XML("<respStmt><resp/><name/><resp/><note/></respStmt>"),
            etree.XML("<respStmt><resp/><persName/><note/><note/></respStmt>"),
            etree.XML(
                "<TEI xmlns='a'><respStmt><name/><resp/><note/></respStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><respStmt><resp/><name/><resp/><note/></respStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><respStmt><resp/><resp><note/></resp><note/></respStmt></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><respStmt><name/><resp/><note/><note/></respStmt></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_resp_added_as_parent_if_missing(self):
        root = etree.XML("<respStmt><name/><note/></respStmt>")
        node = root.find("note")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//resp/note") is not None)

    def test_resp_added_as_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><respStmt><name/><note/></respStmt></TEI>")
        node = root.find(".//{*}note")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}resp/{*}note") is not None)

    def test_first_note_wrapped_in_resp_if_resp_missing(self):
        root = etree.XML(
            """
            <teiHeader>
                <respStmt>
                    <persName/>
                    <note>text1</note>
                    <note>text2</note>
                    <note>text3</note>
                </respStmt>
            </teiHeader>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertTrue(root.find(".//resp/note") is not None)
        self.assertEqual(len(root.findall(".//respStmt/note")), 2)
