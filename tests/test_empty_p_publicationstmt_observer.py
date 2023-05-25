import unittest

from lxml import etree

from tei_transform.observer import EmptyPPublicationstmtObserver
from tei_transform.observer.observer_errors import ManualCurationNeeded


class EmptyPPublicationstmtObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyPPublicationstmtObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<publicationStmt><p/><idno/></publicationStmt>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<publicationStmt><p/><ab/></publicationStmt>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<publicationStmt><publisher/><p/><idno/></publicationStmt>"),
            etree.XML(
                "<fileDesc><publicationStmt><publisher/><date/><ab>text</ab></publicationStmt></fileDesc>"
            ),
            etree.XML("<publicationStmt><publisher/><ab/><address/></publicationStmt>"),
            etree.XML("<publicationStmt><authority/><ptr/><p/></publicationStmt>"),
            etree.XML("<publicationStmt><distributor/><ab/><idno/></publicationStmt>"),
            etree.XML(
                "<publicationStmt><publisher/><p><hi>text</hi></p><date/></publicationStmt>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><publisher/><idno/><ab/></publicationStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><authority/><p/><date/></publicationStmt></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<publicationStmt><ab/><p/><p/></publicationStmt>"),
            etree.XML("<publicationStmt><publisher/><date/></publicationStmt>"),
            etree.XML("<publicationStmt><p>text</p></publicationStmt>"),
            etree.XML("<publicationStmt><p/><p/></publicationStmt>"),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><publisher/><date/></publicationStmt></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><publicationStmt><p/></publicationStmt></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><ab>text</ab><ab/><p/></publicationStmt></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_empty_element_removed(self):
        root = etree.XML("<publicationStmt><publisher/><p/><date/></publicationStmt>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p") is None)

    def test_empty_element_removed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><publicationStmt><ab/><authority/><address/></publicationStmt></TEI>"
        )
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}ab") is None)

    def test_multiple_elements_removed(self):
        root = etree.XML(
            """
            <fileDesc>
                <publicationStmt>
                    <publisher>name</publisher>
                    <distributor/>
                    <p/>
                    <p/>
                    <idno>123</idno>
                    <ab/>
                    <date>2008</date>
                </publicationStmt>
            </fileDesc>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)

        self.assertEqual(len(root[0]), 4)

    def test_element_with_only_whitespace_text_removed(self):
        root = etree.XML(
            "<publicationStmt><ab>    \n\t  </ab><idno/></publicationStmt>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)

    def test_element_with_only_whitespace_tail_removed(self):
        root = etree.XML("<publicationStmt><p/>    \n\t  <idno/></publicationStmt>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)

    def test_exception_raised_if_element_not_empty(self):
        target_elements = ["<p>text</p>", "<p/>tail", "<p><hi>text</hi></p>"]
        for element in target_elements:
            root = etree.XML(
                f"<publicationStmt><publisher/>{element}<idno/></publicationStmt>"
            )
            node = root[1]
            with self.subTest():
                with self.assertRaises(ManualCurationNeeded):
                    self.observer.transform_node(node)
