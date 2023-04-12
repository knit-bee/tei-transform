import unittest

from lxml import etree

from tei_transform.observer import AvailabilityTextObserver


class AvailabilityTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = AvailabilityTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML(
            "<publicationStmt><availability>text</availability></publicationStmt>"
        )
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML(
            "<publicationStmt><availability><p>text</p></availability></publicationStmt>"
        )
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<availability>text</availability>"),
            etree.XML("<availability status='free'>text<p/></availability>"),
            etree.XML("<availability>text<ab/></availability>"),
            etree.XML("<availability><license/>text</availability>"),
            etree.XML(
                "<publicationStmt><publisher/><availability>text</availability></publicationStmt>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><editor/><availability>text</availability></publicationStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><availability status='free'>text</availability></publicationStmt></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<availability><p>text</p></availability>"),
            etree.XML("<availability status='free'><ab>text</ab></availability>"),
            etree.XML(
                "<publicationStmt><publisher/><availability><license>text</license></availability></publicationStmt>"
            ),
            etree.XML("<availability>    </availability>"),
            etree.XML(
                "<publicationStmt><availability><p/> \n\n</availability></publicationStmt>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <publicationStmt>
                        <editor/>
                        <date/>
                        <availability><p>text</p></availability>
                    </publicationStmt>
                </TEI>"""
            ),
            etree.XML(
                "<TEI xmlns='a'><availability status='restricted'><license>text</license></availability></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_text_added_to_new_p(self):
        root = etree.XML(
            "<publicationStmt><availability>text</availability></publicationStmt>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").text, "text")

    def test_text_added_to_new_p_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><availability>text</availability></TEI>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}p").text, "text")

    def test_text_removed_from_availability(self):
        node = etree.XML("<availability>text</availability>")
        self.observer.transform_node(node)
        self.assertIsNone(node.text)

    def test_tail_text_added_to_new_p(self):
        root = etree.XML(
            "<publicationStmt><availability><ab/>tail</availability></publicationStmt>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").text, "tail")

    def test_tail_of_child_removed(self):
        root = etree.XML(
            "<publicationStmt><availability><ab/>tail</availability></publicationStmt>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//ab").tail)

    def test_new_p_added_after_node_with_tail(self):
        root = etree.XML(
            "<publicationStmt><availability><ab/>tail</availability></publicationStmt>"
        )
        node = root[0]
        self.observer.transform_node(node)
        target = root.find(".//ab").getnext()
        result = target.tag, target.text
        self.assertEqual(result, ("p", "tail"))

    def test_remove_multiple_tails(self):
        root = etree.XML(
            """
            <publicationStmt>
                <availability>
                    text
                    <p/>tail1
                    <ab/>tail2
                    <p/>tail3
                </availability>
            </publicationStmt>
            """
        )
        node = root[0]
        self.observer.transform_node(node)
        result = [(child.tag, child.text) for child in node.iter()]
        expected = [
            ("availability", None),
            ("p", "text"),
            ("p", None),
            ("p", "tail1"),
            ("ab", None),
            ("p", "tail2"),
            ("p", None),
            ("p", "tail3"),
        ]
        self.assertEqual(expected, result)
