import unittest

from lxml import etree

from tei_transform.observer import HiChildObserver


class HiChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HiChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><hi>text<p/></hi></p>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<p><hi>text<hi/></hi></p>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p>a<hi>b<p>c</p>d</hi></p>"),
            etree.XML("<div><p><hi>text<p/>text</hi></p></div>"),
            etree.XML("<p><hi rendition='#b'>ab<p>cd</p></hi></p>"),
            etree.XML("<div><p>text<hi>text<p>abc</p></hi></p></div>"),
            etree.XML("<div><p>text</p><p><hi>ab<p>cd</p>ef</hi></p></div>"),
            etree.XML("<div><hi>ab<p/>cd</hi></div>"),
            etree.XML("<TEI xmlns='a'><div><hi><p>text</p></hi></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<hi>text<p>text</p></hi></p></TEI>"),
            etree.XML("<TEI xmlns='a'><p>a</p><p>b<hi>c<p>d</p>e</hi></p></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text<hi>text</hi></p>"),
            etree.XML("<p><hi>ab</hi>text<hi>cd<hi>ef</hi></hi></p>"),
            etree.XML("<div><p>ab<hi>cd</hi></p><hi>text</hi></div>"),
            etree.XML("<div><p><hi>ab<hi>cd</hi></hi></p></div>"),
            etree.XML("<div><p><hi><fw>text</fw></hi></p></div>"),
            etree.XML("<div><p><hi>text<quote/></hi></p></div>"),
            etree.XML("<div><p/><p>ab<hi>cd</hi>ef<hi/></p></div>"),
            etree.XML("<TEI xmlns='a'><div><p>text<hi>ab</hi>text</p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p><hi/></p><hi>text</hi></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p><hi>text</hi><p/></p></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_p_child_removed(self):
        root = etree.XML("<p><hi>text1<p>text2</p></hi></p>")
        node = root.find(".//hi/p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//hi/p") is None)

    def test_p_child_removed_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><p>text<hi>text2<p>text3</p></hi></p></TEI>")
        node = root.find(".//{*}hi/{*}p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}hi/{*}p") is None)

    def test_p_with_child_resolved(self):
        root = etree.XML("<p><hi>a<p>b<hi>c</hi></p></hi></p>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//hi/hi") is not None)

    def test_text_of_p_element_not_removed(self):
        root = etree.XML("<div><hi><p>text2</p></hi></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue("text2" in root[0].text)

    def test_lb_added_to_separate_text_parts(self):
        root = etree.XML("<div><hi>text1<p>text2</p></hi></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue("text2" in root.find(".//lb").tail)

    def test_lb_added_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><hi>text1<p>text2</p></hi></div></TEI>")
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}lb").tail, "text2")

    def test_tail_of_p_element_not_removed(self):
        root = etree.XML("<div><hi><p/>tail</hi></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue("tail" in root[0].text)

    def test_multiple_p_elements_resolved(self):
        root = etree.XML(
            """
            <div>
                <p>
                    <hi>text1
                        <p>text2</p>
                        <p>text3</p>
                        <p>text4</p>tail
                    </hi>tail2
                </p>
            </div>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        hi_elem = root.find(".//hi")
        result = [(node.tag, node.text, node.tail.strip()) for node in hi_elem.iter()]
        self.assertEqual(len(hi_elem.findall("p")), 0)
        self.assertEqual(
            result,
            [
                ("hi", "text1", "tail2"),
                ("lb", None, "text2"),
                ("lb", None, "text3"),
                ("lb", None, "text4 tail"),
            ],
        )

    def test_hi_with_empty_p_child(self):
        root = etree.XML("<div><p><hi>text<p/></hi></p></div>")
        node = root.find(".//hi/p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//hi").text, "text")

    def test_no_lb_added_if_p_empty(self):
        root = etree.XML("<div><p><hi>text<p/></hi></p></div>")
        node = root.find(".//hi/p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//lb") is None)

    def test_no_lb_added_if_p_contains_no_text_but_children(self):
        root = etree.XML("<p><hi>text<p><hi>inner</hi></p></hi></p>")
        node = root.find(".//hi/p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//lb") is None)

    def test_lb_added_if_p_has_only_tail(self):
        root = etree.XML("<p><hi>text<p/>tail</hi></p>")
        node = root.find(".//hi/p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//lb").tail, "tail")
