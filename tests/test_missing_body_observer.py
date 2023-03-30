import unittest

from lxml import etree

from tei_transform.observer import MissingBodyObserver


class MissingBodyObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MissingBodyObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<TEI><text><p/></text></TEI>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<TEI><text><body><p/></body></text></TEI>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<text><front/></text>"),
            etree.XML("<text><fw/><front/><back/></text>"),
            etree.XML("<text><group><text/></group></text>"),
            etree.XML("<text><back/></text>"),
            etree.XML("<text><p>text</p></text>"),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><p/></text></TEI>"),
            etree.XML("<TEI xmlns='a'><text><front/><back/></text></TEI>"),
            etree.XML("<TEI xmlns='a'><text><group><text/></group></text></TEI>"),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><front/><note/></text></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<text><body/></text>"),
            etree.XML("<text><front/><body/><back/></text>"),
            etree.XML("<text><group><text><body/></text></group></text>"),
            etree.XML("<text><front/><body><p/></body></text>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><front/><body/><back/></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><text><group><text><body/></text></group></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><front/><body><p/></body></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body/></text><text><body/></text></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_body_added_as_child_of_text(self):
        root = etree.XML("<TEI><text/></TEI>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//body") is not None)

    def test_body_added_as_child_of_text_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><text/></TEI>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}body") is not None)

    def test_body_added_during_iteration(self):
        root = etree.XML(
            """
        <TEI>
          <teiHeader/>
          <text>
            <p>ab</p>
            <p/>
          </text>
        </TEI>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//text")), 1)

    def test_children_of_text_added_to_body(self):
        root = etree.XML("<text><p/><ab/><p/></text>")
        self.observer.transform_node(root)
        result = [child.tag for child in root[0]]
        self.assertEqual(["p", "ab", "p"], result)

    def test_children_of_text_removed_unless_front_or_back(self):
        root = etree.XML("<text><front/><p/><ab/><p/><back/></text>")
        self.observer.transform_node(root)
        result = [child.tag for child in root]
        self.assertEqual(["front", "body", "back"], result)

    def test_back_not_added_to_body(self):
        root = etree.XML("<text><p/><back/></text>")
        self.observer.transform_node(root)
        result = [node.tag for node in root]
        self.assertEqual(["body", "back"], result)

    def test_front_not_added_to_body(self):
        root = etree.XML("<text><front/><p/></text>")
        self.observer.transform_node(root)
        result = [node.tag for node in root]
        self.assertEqual(["front", "body"], result)

    def test_body_added_after_front_sibling(self):
        root = etree.XML("<text><front/><p/><back/></text>")
        self.observer.transform_node(root)
        result = [node.tag for node in root]
        self.assertEqual(["front", "body", "back"], result)

    def test_empty_p_added_to_new_body_if_empty_otherwise(self):
        root = etree.XML("<text><front/><back/></text>")
        self.observer.transform_node(root)
        self.assertTrue(root.find(".//body/p") is not None)
