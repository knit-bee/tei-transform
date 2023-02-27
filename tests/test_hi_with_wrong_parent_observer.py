import unittest

from lxml import etree

from tei_transform.observer import HiWithWrongParentObserver


class HiOutsidePObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HiWithWrongParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<body><hi/></body>")
        result = self.observer.observe(root[0])
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<body><p><hi/></p></body>")
        result = self.observer.observe(root[0])
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><hi>text</hi></div>"),
            etree.XML("<body><hi/></body>"),
            etree.XML("<body><p/><hi/></body>"),
            etree.XML("<div1><hi/></div1>"),
            etree.XML("<div2><hi/></div2>"),
            etree.XML("<div3><hi/></div3>"),
            etree.XML("<div4><hi/></div4>"),
            etree.XML("<div5><hi/></div5>"),
            etree.XML("<div6><hi/></div6>"),
            etree.XML("<div7><hi/></div7>"),
            etree.XML("<body><div><hi>text</hi><p/></div></body>"),
            etree.XML("<TEI><teiHeader/><text><body><hi/><p/></body></text></TEI>"),
            etree.XML(
                "<TEI xmlns='namespace'><teiHeader/><text><body><hi/><p/></body></text></TEI>"
            ),
            etree.XML(
                "<TEI><teiHeader/><text><body><div><hi/><p/></div></body></text></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p><hi/></p>"),
            etree.XML("<fw><hi/></fw>"),
            etree.XML("<div><p>text text <hi rend='#i'>text</hi></p></div>"),
            etree.XML("<div><p><hi/></p></div>"),
            etree.XML("<classCode><hi/></classCode>"),
            etree.XML("<ab><hi/></ab>"),
            etree.XML("<TEI><teiHeader/><text><body><p><hi/></p></body></text></TEI>"),
            etree.XML(
                "<TEI xmlns='namespace'><teiHeader/><text><body><p><hi/></p></body></text></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_hi_element_removed_if_empty(self):
        root = etree.XML("<div><hi></hi></div>")
        self.observer.transform_node(root[0])
        self.assertEqual(root.getchildren(), [])

    def test_hi_element_removed_if_empty_with_namespace(self):
        root = etree.XML("<TEI xmlns='namespace'><div><hi></hi></div></TEI>")
        self.observer.transform_node(root[0][0])
        self.assertEqual(root[0].getchildren(), [])

    def test_hi_element_removed_if_it_only_contains_whitespace(self):
        root = etree.XML("<TEI xmlns='namespace'><div><hi>  </hi></div></TEI>")
        self.observer.transform_node(root[0][0])
        self.assertEqual(root[0].getchildren(), [])

    def test_hi_element_removed_if_only_tail_contains_whitespace(self):
        root = etree.XML("<TEI xmlns='namespace'><div><hi></hi>\n</div></TEI>")
        self.observer.transform_node(root[0][0])
        self.assertEqual(root[0].getchildren(), [])

    def test_element_wrapped_in_p_if_no_div_siblings(self):
        root = etree.XML("<body><hi>text</hi><p/></body>")
        self.observer.transform_node(root[0])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "p", "hi", "p"])

    def test_element_wrapped_in_p_if_no_div_siblings_with_namespace(self):
        root = etree.XML("<TEI xmlns='namespace'><body><hi>text</hi><p/></body></TEI>")
        self.observer.transform_node(root[0][0])
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "body", "p", "hi", "p"])

    def test_element_wrapped_in_p_and_div_if_div_sibling(self):
        root = etree.XML("<body><div/><hi>text</hi></body>")
        self.observer.transform_node(root[1])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div", "div", "p", "hi"])

    def test_element_wrapped_in_p_and_div_if_div_sibling_after_hi(self):
        root = etree.XML("<body><hi>text</hi><div/></body>")
        self.observer.transform_node(root[0])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div", "p", "hi", "div"])

    def test_no_change_applied_if_conflicting_levels_of_div_siblings(self):
        root = etree.XML("<body><div/><div1/><hi>text</hi></body>")
        self.observer.transform_node(root[2])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div", "div1", "hi"])

    def test_hi_wrapped_in_p_and_div_if_div_sibling_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><body><hi>text</hi><div/></body></TEI>"
        )
        self.observer.transform_node(root[0][0])
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "body", "div", "p", "hi", "div"])

    def test_correct_div_level_chosen_if_div_sibling_is_numbered(self):
        for i in range(8):
            if i == 0:
                i = ""
            root = etree.XML(f"<body><hi>text</hi><div{i}/></body>")
            self.observer.transform_node(root[0])
            result = [node.tag for node in root.iter()]
            with self.subTest():
                self.assertEqual(result, ["body", f"div{i}", "p", "hi", f"div{i}"])

    def test_correct_div_level_chosen_if_div_sibling_is_numbered_with_namespace(self):
        for i in range(8):
            if i == 0:
                i = ""
            root = etree.XML(
                f"<TEI xmlns='namespace'><body><hi>text</hi><div{i}/></body></TEI>"
            )
            self.observer.transform_node(root[0][0])
            result = [etree.QName(node).localname for node in root.iter()]
            with self.subTest():
                self.assertEqual(
                    result, ["TEI", "body", f"div{i}", "p", "hi", f"div{i}"]
                )

    def test_element_with_child_not_removed(self):
        root = etree.XML("<div><hi><quote/></hi></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p/hi") is not None)
