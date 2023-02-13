import unittest

from lxml import etree

from tei_transform.observer import FwChildObserver


class FwChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = FwChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<fw><p/></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<fw>text<hi>text</hi></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<fw><list/></fw>"),
            etree.XML("<fw>text<p>text</p>text</fw>"),
            etree.XML("<div><fw>text<list><item/></list></fw></div>"),
            etree.XML("<div><fw>text<p><hi>text</hi></p></fw></div>"),
            etree.XML("<div><p>text<fw><p>text</p></fw>tail</p></div>"),
            etree.XML("<div>text<fw>text<list/></fw><p/><p/></div>"),
            etree.XML("<div><p>txt</p><fw><p><table/></p></fw></div>"),
            etree.XML("<TEI xmlns='a'><div><fw><list/></fw></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><fw>text<p>text</p>text</fw></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><fw>text<p>text<table/>tail</p>a</fw><p/></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><fw>a</fw><div><fw><list/>tail</fw></div></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<fw>text</fw>"),
            etree.XML("<fw>a<hi>b</hi>c</fw>"),
            etree.XML("<div><p>a</p><fw>b</fw>c<p/>d</div>"),
            etree.XML("<div><fw>text<fw>text</fw>tail</fw><p/></div>"),
            etree.XML("<div><fw/><p><fw>text</fw></p></div>"),
            etree.XML("<div><list><item><fw>a</fw></item></list></div>"),
            etree.XML("<div><fw/><p><list/><fw/></p>tail</div>"),
            etree.XML("<div><fw><quote><list/></quote></fw></div>"),
            etree.XML("<TEI xmlns='a'><div><fw>text</fw><p><list/></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><list><fw>text</fw></list>tail</TEI>"),
            etree.XML("<TEI xmlns='a'><p>b<fw>a<hi>c</hi>d</fw>e</p></TEI>"),
            etree.XML("<TEI xmlns='a'><div><list/><p/><fw>text</fw></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_p_element_merged_with_parent(self):
        root = etree.XML("<div><fw>text<p>inner</p>tail</fw></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p") is None)

    def test_p_element_merged_with_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><fw>a<p>b</p>c</fw></div></TEI>")
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}p") is None)

    def test_nested_p_elements_not_removed_after_merge(self):
        root = etree.XML("<fw><p><quote>a<p>text</p></quote></p></fw>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//p").text
        self.assertEqual(result, "text")

    def test_text_of_p_not_deleted(self):
        root = etree.XML("<div><fw>one<p>two</p>three></fw></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue("two" in root[0].text and "three" in root[0].text)

    def test_fw_converted_to_ab_if_list_child(self):
        root = etree.XML("<div><fw>text<list/></fw></div>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        self.assertEqual(root[0].tag, "ab")

    def test_fw_converted_to_ab_if_list_child_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><fw>text<list/></fw></div></TEI>")
        node = root.find(".//{*}list")
        self.observer.transform_node(node)
        self.assertEqual(node.getparent().tag, "{a}ab")

    def test_text_parts_separated_by_whitespace_after_merge(self):
        root = etree.XML("<div><fw>first<p>second</p>third</fw></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertEqual(root[0].text, "first second third")

    def test_text_of_following_sibling_of_p_in_fw_not_changed(self):
        root = etree.XML("<div><fw>one<p>two</p>three<p>four</p>five</fw></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        result = root.find(".//p").text, root.find(".//p").tail
        self.assertEqual(result, ("four", "five"))

    def test_merging_p_into_fw_with_previous_sibling(self):
        root = etree.XML("<div><fw><hi>text</hi>tail<p>text2</p>tail2</fw></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        result = root.find(".//hi").tail
        self.assertEqual(result, ("tail text2 tail2"))

    def test_children_of_p_not_deleted(self):
        root = etree.XML("<div><fw><p>text1<hi>text2</hi>tail</p></fw></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        result = root.find(".//fw/hi")
        self.assertEqual((result.text, result.tail), ("text2", "tail"))

    def test_removal_of_multiple_inner_elements(self):
        root = etree.XML(
            """
            <div>
              <p>text</p>
              <fw>text1
                <p>text2</p>
                <p>text3
                  <hi>text4</hi>tail1
                </p>tail2
                <quote>
                <list>
                  <item>text5</item>
                </list>tail3
                </quote>tail4
                <p>text7</p>tail5
                <quote>text8</quote>
              </fw>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [
            (node.tag, node.text.strip(), node.tail.strip()) for node in root[1].iter()
        ]
        self.assertEqual(
            result,
            [
                ("fw", "text1 text2 text3", ""),
                ("hi", "text4", "tail1 tail2"),
                ("quote", "", "tail4 text7 tail5"),
                ("list", "", "tail3"),
                ("item", "text5", ""),
                ("quote", "text8", ""),
            ],
        )

    def test_check_node_without_parent(self):
        node = etree.XML("<p/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)
