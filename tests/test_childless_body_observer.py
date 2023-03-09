import unittest

from lxml import etree

from tei_transform.observer import ChildlessBodyObserver


class ChildlessBodyObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = ChildlessBodyObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<body/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<body><div/></body>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<text><body></body></text>"),
            etree.XML("<text><front/><body/></text>"),
            etree.XML("<text><body>  </body></text>"),
            etree.XML("<text><body>abc</body></text>"),
            etree.XML("<text><front/><body/>tail<back/></text>"),
            etree.XML("<div><p><floatingText><body/></floatingText></p></div>"),
            etree.XML("<TEI xmlns='a'><text><body/></text></TEI>"),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><body>  </body></text></TEI>"),
            etree.XML("<TEI xmlns='a'><text><front/><body/><back/></text></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><text><floatingText><body/></floatingText></text></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<text><body><p/></body></text>"),
            etree.XML("<text><front/><body><p/></body><back/></text>"),
            etree.XML("<text><body>abc<p/></body></text>"),
            etree.XML("<div><floatingText><body><div/></body></floatingText></div>"),
            etree.XML("<text><front/>tail<body>text<p/>tail</body>tail</text>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body><div/></body></text></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><text><body><list/></body><back/></text></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><text><div><floatingText><body><p/></body></floatingText></div></text></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_empty_p_elment_added(self):
        root = etree.XML("<text><body/></text>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p") is not None)

    def test_empty_p_elment_added_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><teiHeader/><text><body/></text></TEI>")
        node = root.find(".//{*}body")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}p") is not None)

    def test_text_in_body_added_to_p(self):
        root = etree.XML("<div><floatingText><body>text</body></floatingText></div>")
        node = root.find(".//body")
        self.observer.transform_node(node)
        result = root.find(".//p").text
        self.assertEqual(result, "text")

    def test_text_in_body_added_to_p_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><teiHeader/><text><body>text1</body></text></TEI>"
        )
        node = root.find(".//{*}body")
        self.observer.transform_node(node)
        result = root.find(".//{*}p").text
        self.assertEqual(result, "text1")

    def test_text_from_body_removed(self):
        root = etree.XML("<text><front/><body>text1</body></text>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(node.text is None)

    def test_whitespace_text_content_of_body_not_added_to_p(self):
        root = etree.XML("<text><front/><body>   \n\n</body></text>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p").text is None)
