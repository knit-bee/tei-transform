import unittest

from lxml import etree

from tei_transform.observer import WrongListChildObserver


class WrongListChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = WrongListChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<list><item/><p>text</p></list>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<list><item>text</item></list>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p><list><p>text</p></list></p>"),
            etree.XML("<p><list><p/><item/></list></p>"),
            etree.XML("<div><list><item/><p/><hi/></list></div>"),
            etree.XML("<div><list><p/><hi>text</hi><item/></list></div>"),
            etree.XML("<list><item><p/></item><fw>text</fw><p/></list>"),
            etree.XML("<list><ab>text</ab><item/></list>"),
            etree.XML("<list><item/><item><p>text</p></item><ab/></list>"),
            etree.XML("<TEI xmlns='a'><div><list><p/><item/></list></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><list><head/><item/><fw/><hi/><p/></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><list><p>text<hi>a</hi></p></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p><list><hi>text</hi><item/></list></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(min(sum(result), 1), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p><list><item>text</item></list></p>"),
            etree.XML("<list><item><p>text</p></item></list>"),
            etree.XML("<list><item/><item><ab>text</ab></item></list>"),
            etree.XML("<list><item>text</item><fw>text</fw></list>"),
            etree.XML("<list><head>a</head><item><p/></item></list>"),
            etree.XML("<div><list><item><ab/><p/></item><item/><item/></list></div>"),
            etree.XML(
                "<div><p><list><item/><item/><item><p>text</p></item></list></p></div>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><list><item><p><hi>text</hi></p></item></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p><list><item><ab>x</ab><p>y</p></item></list></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><list><item/><item/><item>text<hi>text</hi></item></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><list><item>ab<p/></item><item><hi/>tail</item></list></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_item_added_as_parent(self):
        root = etree.XML("<div><list><p>text</p></list></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/item/p") is not None)

    def test_item_added_as_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><list><ab>text</ab></list></div></TEI>")
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}list/{*}item/{*}ab") is not None)

    def test_handling_of_target_with_tail(self):
        root = etree.XML("<p><list><item/><p>text</p>tail</list></p>")
        node = root.find(".//list/p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//item/p").tail, "tail")

    def test_handling_of_target_with_children(self):
        root = etree.XML(
            "<p><list><item/><p>text<hi/><table/><list/><hi/>tail</p>tail</list></p>"
        )
        node = root.find(".//list/p")
        self.observer.transform_node(node)
        result = [child.tag for child in root.find(".//item/p")]
        self.assertEqual(result, ["hi", "table", "list", "hi"])

    def test_handle_multiple_targets_during_iteration(self):
        root = etree.XML(
            """
        <div>
            <list>
                <item>text</item>
                <p>text2</p>tail
                <p>text3</p>
                <hi>text4</hi>
                <p/>
                <ab>text5</ab>
                <item>text6</item>
                <p/>tail
            </list>
        </div>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [
            (
                child.tag,
                [
                    (subchild.tag, subchild.text, subchild.tail.strip())
                    for subchild in child
                ],
            )
            for child in root[0]
        ]
        expected = [
            ("item", []),
            ("item", [("p", "text2", "tail")]),
            ("item", [("p", "text3", "")]),
            ("item", [("hi", "text4", "")]),
            ("item", [("ab", "text5", "")]),
            ("item", []),
            ("item", [("p", None, "tail")]),
        ]
        self.assertEqual(result, expected)

    def test_empty_element_removed(self):
        root = etree.XML("<div><list><item/><p/></list></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//p"))

    def test_element_with_tail_not_removed(self):
        root = etree.XML("<div><list><item/><p/>tail</list></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//item/p") is not None)

    def test_element_with_text_but_without_children_not_removed(self):
        root = etree.XML("<div><list><item/><p><hi/></p></list></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//item/p") is not None)

    def test_element_with_text_not_removed(self):
        root = etree.XML("<div><list><item/><p>text</p></list></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//item/p") is not None)
