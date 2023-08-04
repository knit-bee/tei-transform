import unittest

from lxml import etree

from tei_transform.observer import UParentObserver


class UParentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = UParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><u/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><u/><p/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<p><u who='a'>text</u></p>"),
            etree.XML("<div><p><u>text</u></p></div>"),
            etree.XML("<body><p><u/></p><p>text</p></body>"),
            etree.XML("<p>text<u>text</u>tail</p>"),
            etree.XML("<div><p/><p><u>text</u></p></div>"),
            etree.XML("<TEI xmlns='a'><div><p><u>text</u></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p>text<u/>tail</p></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><p><u who='a'>text</u></p><p/></body></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p/><u/></div>"),
            etree.XML("<div><u>text</u></div>"),
            etree.XML("<body><div><p/><u who='a'>text</u></div></body>"),
            etree.XML("<body><u>text</u><u/><u/></body>"),
            etree.XML("<body><div><u>text</u></div></body>"),
            etree.XML("<body><u>text</u>tail</body>"),
            etree.XML("<TEI xmlns='a'><div><p/><u>text</u></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><head/><u who='a'>ab</u><u/><u/></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_parent_tag_converted_to_div(self):
        root = etree.XML("<body><p><u>text</u></p></body>")
        node = root.find(".//u")
        self.observer.transform_node(node)
        self.assertEqual(node.getparent().tag, "div")

    def test_parent_tag_converted_to_div_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><body><p><u>text</u></p></body></TEI>")
        node = root.find(".//{*}u")
        self.observer.transform_node(node)
        self.assertEqual(etree.QName(node.getparent()).localname, "div")

    def test_text_of_parent_added_to_new_p(self):
        root = etree.XML("<body><p>text1<u>text2</u></p></body>")
        node = root.find(".//u")
        self.observer.transform_node(node)
        target = root[0][0]
        self.assertEqual(target.tag, "p")
        self.assertEqual(target.text, "text1")

    def test_text_of_parent_removed(self):
        root = etree.XML("<body><p>text1<u>text2</u></p></body>")
        node = root.find(".//u")
        self.observer.transform_node(node)
        self.assertIsNone(root[0].text)

    def test_tail_of_u_added_to_text_content(self):
        root = etree.XML("<body><p><u>text</u>tail</p></body>")
        node = root.find(".//u")
        self.observer.transform_node(node)
        self.assertEqual(node.text, "text tail")

    def test_tail_of_u_added_to_last_child_tail_if_present(self):
        root = etree.XML("<body><p><u>text<hi/></u>tail</p></body>")
        node = root.find(".//u")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//hi").tail, "tail")

    def test_target_removed_if_empty(self):
        root = etree.XML("<body><p><u></u></p></body>")
        node = root.find(".//u")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//u"))
