import unittest

from lxml import etree

from tei_transform.div_text_observer import DivTextObserver


class DivTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<div>text</div>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_nonmatching_element(self):
        node = etree.XML("<div/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div>some text<p>more text</p></div>"),
            etree.XML("<div><div>text</div></div>"),
            etree.XML(
                "<text><body><div><div><p/></div><div>text</div></div></body></text>"
            ),
            etree.XML(
                """<TEI><teiHeader/>
            <text><body><div>text<p>more text</p></div></body></text>
            </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                     <text><body><div>text<p>more text</p></div></body></text>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p>text</p></div>"),
            etree.XML("<div><p/></div>"),
            etree.XML("<div><div><p>text</p></div></div>"),
            etree.XML("<div><fw>header</fw>tail<p/></div>"),
            etree.XML("<div><p>text</p>text<p>more text</p></div>"),
            etree.XML(
                """<TEI><teiHeader/><text>
            <body><div><p>text></p></div></body>
            </text></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='namespace'>
            <teiHeader/>
            <text>
            <body><div><div><p>text</p>text2</div></div></body>
            </text>
            </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_text_from_div_added_to_next_p_if_only_one_char(self):
        node = etree.XML("<div>T<p>est</p></div>")
        self.observer.transform_node(node)
        self.assertEqual((node.text, node[0].text), (None, "Test"))

    def test_new_p_added_for_long_text_in_div(self):
        node = etree.XML("<div>text<p/></div>")
        self.observer.transform_node(node)
        result = [(el.tag, el.text) for el in node.iter()]
        self.assertEqual(result, [("div", None), ("p", "text"), ("p", None)])

    def test_text_from__namespaced_div_added_to_next_p_if_only_one_char(self):
        root = etree.XML(
            """<TEI xmlns='namespace'><teiHeader/>
        <text><body><div>T<p>est</p></div></body></text></TEI>"""
        )
        target_node = root.find(".//{*}div")
        self.observer.transform_node(target_node)
        self.assertIsNone(target_node.text)
        self.assertEqual(target_node[0].text, "Test")

    def test_new_p_added_for_long_text_in_namespaced_div(self):
        root = etree.XML(
            """<TEI xmlns='namespace'><teiHeader/>
        <text><body><div>Text<p>more text</p></div></body></text></TEI>"""
        )
        target_node = root.find(".//{*}div")
        self.observer.transform_node(target_node)
        self.assertIsNone(target_node.text)
        self.assertEqual(len(target_node.getchildren()), 2)

    def test_new_p_added_if_div_doesnt_contain_p_for_one_char(self):
        node = etree.XML("<div>T</div>")
        self.observer.transform_node(node)
        result = [(el.tag, el.text) for el in node.iter()]
        self.assertEqual(result, [("div", None), ("p", "T")])

    def test_new_p_added_if_div_doesnt_contain_p(self):
        node = etree.XML("<div>Text</div>")
        self.observer.transform_node(node)
        result = [(el.tag, el.text) for el in node.iter()]
        self.assertEqual(result, [("div", None), ("p", "Text")])
