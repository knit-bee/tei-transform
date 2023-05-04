import unittest

from lxml import etree

from tei_transform.observer import DelChildObserver


class DelChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DelChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<del><p/></del>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><del/><p/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<p>text<del>b<p>c</p>d</del></p>"),
            etree.XML("<div><p><del>text<p/>text</del><list/></p></div>"),
            etree.XML("<p>text<del rend='overstrike'>ab<p>cd</p></del></p>"),
            etree.XML("<div><p>text<del>text<p/></del></p></div>"),
            etree.XML("<div><p>text</p><p><del>ab<p>cd</p>ef</del>text</p></div>"),
            etree.XML("<div><p/><del>ab<p/>cd</del><p/><p/></div>"),
            etree.XML("<TEI xmlns='a'><div><del><p>text</p></del></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<del>text<p>text</p></del></p></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><p>a</p><p>b<del>c<p>d</p>e</del>text<list/></p></TEI>"
            ),
            etree.XML("<p>a<del>b<ab>c</ab></del></p>"),
            etree.XML("<p>text<del>text<head/></del></p>"),
            etree.XML("<div><del><head>text</head><quote/></del></div>"),
            etree.XML("<div><p>text<del>text<ab>text</ab></del></p></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>a<del><head>b</head>c</del></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><del>text<ab>text</ab>text</del></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text<del>text<quote/></del></p>"),
            etree.XML("<p>text<del>ab</del>text<del>cd<hi>ef</hi></del></p>"),
            etree.XML("<div><p>ab<del>cd</del></p><del>text</del></div>"),
            etree.XML("<div><p>text<del>ab<hi>cd</hi></del></p></div>"),
            etree.XML("<div><p>text<del>text<fw>text</fw></del></p></div>"),
            etree.XML("<div><p><del>text<quote/></del>tail</p></div>"),
            etree.XML("<div><p/><p>ab<del>cd</del>ef<del/></p></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<del>ab<quote/></del>text</p></div></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><p>txt<del/></p><del>text</del></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p><del>text</del>tail<p/></p></div></TEI>"),
            etree.XML("<div><head>text<del>ab</del></head></div>"),
            etree.XML("<div><p/><ab>text<del>b</del></ab></div>"),
            etree.XML("<div><head/><p>text<del>ab</del></p><ab/></div>"),
            etree.XML("<div><head/><ab/><p/><del>text<hi>xy</hi></del></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><head/><p>text<del><quote/></del></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><ab/><p>text<del><quote>text<ab/></quote></del></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_p_child_removed(self):
        root = etree.XML("<div><del>text1<p/></del></div>")
        node = root.find(".//del/p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//del/p") is None)

    def test_p_child_removed_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><p>text<del>text2<p>text3</p></del></p></TEI>")
        node = root.find(".//{*}del/{*}p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}del/{*}p") is None)

    def test_p_with_child_resolved(self):
        root = etree.XML("<div><del>a<p>b<del>c</del></p></del></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//del/del") is not None)

    def test_text_of_p_element_not_removed(self):
        root = etree.XML("<div><del>text1<p>text2</p></del></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue("text2" in root[0].text)

    def test_tail_of_p_element_not_removed(self):
        root = etree.XML("<div><del>text<p/>tail</del></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue("tail" in root[0].text)

    def test_multiple_p_elements_resolved(self):
        root = etree.XML(
            """
            <div>
                <p>
                    <del>text1
                        <p>text2</p>
                        <p>text3</p>
                        <p>text4</p>tail
                    </del>tail2
                </p>
            </div>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//del")), 0)
        self.assertEqual(root.find(".//del").text, "text1 text2 text3 text4 tail")

    def test_del_with_empty_p_child(self):
        root = etree.XML("<div><p><del>text<p/></del></p></div>")
        node = root.find(".//del/p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//del").text, "text")
