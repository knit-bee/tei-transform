import unittest

from lxml import etree

from tei_transform.observer import DivTailObserver


class DivTailObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivTailObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<body><div/>tail</body>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<body><div><p/>tail</div></body>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><div/>tail</div>"),
            etree.XML("<div><div><p/></div>tail</div>"),
            etree.XML("<div><p/><div/>tail</div>"),
            etree.XML("<div><div/>tail<list/></div>"),
            etree.XML("<body><div><p>text</p></div>tail</body>"),
            etree.XML("<div><div><list/>tail<p/></div>tail</div>"),
            etree.XML("<TEI xmlns='a'><body><div/>tail</body></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><table/></div>tail</TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><div><p/><div/>tail</div></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p/>tail</div>"),
            etree.XML("<div>text<div/></div>"),
            etree.XML("<div><p>text</p>tail</div>"),
            etree.XML("<body><div><list/>tail<p/>tail</div></body>"),
            etree.XML("<body><div><div>text<p/>tail</div><div/></div></body>"),
            etree.XML(
                "<body><div>text<p/>tail<div>text<table/>tail</div><p/></div></body>"
            ),
            etree.XML("<body><div>text<div/></div><div>a<p/>tail<p/>tail</div></body>"),
            etree.XML("<div>text<p/>tail<div/><div/><table/>tail</div>"),
            etree.XML(
                "<TEI xmlns='a'><body><div>text<p/>tail<div/></div></body></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><div><p>text<hi/>tail</p><div/></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><div>text<p/>tail<div>a<table/>b</div></div></body></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_tail_of_div_removed(self):
        root = etree.XML("<div><div/>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(node.tail is None)

    def test_tail_of_div_removed_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><p>text</p></div>tail</TEI>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(node.tail is None)

    def test_tail_of_div_added_to_new_p(self):
        root = etree.XML("<body><div/>tail</body>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").text, "tail")

    def test_new_p_added_as_last_child_of_div(self):
        root = etree.XML("<body><div><list/><ab/></div>tail</body>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.index(node.find("p")), 2)

    def test_tail_of_div_added_to_new_p_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><body><div><ab/></div>tail</body></TEI>")
        node = root.find(".//{*}div")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}p").text, "tail")

    def test_tail_on_div_with_previous_sibling_removed(self):
        root = etree.XML("<body><list/><div/>tail</body>")
        node = root.find(".//div")
        self.observer.transform_node(node)
        self.assertTrue(node.tail is None)

    def test_tail_on_div_with_following_sibling_removed(self):
        root = etree.XML("<body><div/>tail<list/><table/><div/></body>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(node.tail is None)

    def test_tail_on_div_with_text_and_children_removed(self):
        root = etree.XML("<body><div>text<div/><table/><p>text</p></div>tail</body>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(node.tail is None)

    def test_tail_of_last_child_of_div_not_changed(self):
        root = etree.XML("<body><div><list/><p/>old</div>tail</body>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").tail, "old")
