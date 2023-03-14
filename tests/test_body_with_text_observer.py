import unittest

from lxml import etree

from tei_transform.observer import BodyWithTextObserver


class BodyWithTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = BodyWithTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<body>text<div/></body>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<body><div/></body>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<body>text<p>text</p>tail</body>"),
            etree.XML("<text><body>abc<div><p/></div></body></text>"),
            etree.XML("<text><body>abc<list/></body></text>"),
            etree.XML("<TEI><text><body>abc<div/><div/><div/></body></text></TEI>"),
            etree.XML("<div><floatingText><body>abc<p/></body></floatingText></div>"),
            etree.XML(
                "<p><floatingText><body>abc<list/>tail</body></floatingText></p>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body>a<p/></body></text></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><text><body>abc<div/></body></text></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><text><p><floatingText><body>abc<div/></body></floatingText></p></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body>abc<list/><table/>tail</body></text></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<body/>"),
            etree.XML("<body>   </body>"),
            etree.XML("<text><body>  \n   \t</body></text>"),
            etree.XML("<body><div/></body>"),
            etree.XML("<text><body><div/>tail</body></text>"),
            etree.XML("<text><body><div><list/></div><div/></body></text>"),
            etree.XML("<text><body><p>abc</p><div/></body></text>"),
            etree.XML("<div><floatingText><body/></floatingText></div>"),
            etree.XML(
                "<div><floatingText><body><p>text</p><div/></body></floatingText></div>"
            ),
            etree.XML(
                "<TEI xmlns='a'><text><body><p/><div>abc</div></body></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body><div/>tail<div/></body></text></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><text><p><floatingText><body><div/></body></floatingText></p></text></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><body/></text>  </TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_text_added_to_new_p(self):
        node = etree.XML("<body>text<div/></body>")
        self.observer.transform_node(node)
        self.assertEqual(node.find("p").text, "text")

    def test_text_added_to_new_p_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><body>abc<div/></body></TEI>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}body/{*}p").text, "abc")

    def test_text_removed_from_body(self):
        node = etree.XML("<body>text<div/></body>")
        self.observer.transform_node(node)
        self.assertTrue(node.text is None)

    def test_p_inserted_as_first_child_if_other_children(self):
        root = etree.XML(
            "<div><floatingText><body>abc<div><p/></div><div/><list/></body></floatingText></div>"
        )
        node = root.find(".//body")
        self.observer.transform_node(node)
        self.assertEqual(node[0].tag, "p")

    def test_text_added_to_first_child_if_it_can_contain_text(self):
        root = etree.XML("<text><body>text1<head>text2</head></body></text>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node[0].text, "text1 text2")

    def test_no_new_p_added_if_first_child_can_contain_text(self):
        root = etree.XML("<text><body>text1<ab>text2</ab></body></text>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p") is None)

    def test_new_p_added_if_no_children(self):
        root = etree.XML("<text><body>text1</body></text>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").text, "text1")
