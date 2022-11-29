import unittest

from lxml import etree

from tei_transform.observer import BylineSiblingObserver


class PAfterBylineObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = BylineSiblingObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<div><p/><byline/><p/></div>")
        node = root[2]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<div><p/><byline/><dateline/></div>")
        node = root[2]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<div><p>text</p><byline>author</byline><p/></div>"),
            etree.XML("<div><p/><p/><p/><byline/><p>text</p></div>"),
            etree.XML("<text><div><p/><byline/><p/></div></text>"),
            etree.XML(
                "<div><p>text</p><byline><docAuthor>name</docAuthor></byline><p/></div>"
            ),
            etree.XML(
                "<div><div><p>text</p><byline>author</byline></div><div><p/><byline/><p/></div></div>"
            ),
            etree.XML("<text><div><div><head/><p/><byline/><p/></div></div></text>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><head/><p/><byline/><p>text</p></div></TEI>"
            ),
            etree.XML("<div><head/><p/><byline/><p/></div>"),
            etree.XML("<div><p/><byline/><dateline/><p/></div>"),
            etree.XML("<div><table/><byline/><p/></div>"),
            etree.XML("<div><p/><byline/><dateline/><p/></div>"),
            etree.XML("<div><p/><byline/><docAuthor/><p/></div>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<div><p/><byline/></div>"),
            etree.XML("<text><div><byline>author</byline></div></text>"),
            etree.XML("<div><p/><p/><byline/></div>"),
            etree.XML("<list><item/><byline/></list>"),
            etree.XML("<text><div><div><head/><p/><byline/></div><p/></div></text>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><p/><byline/></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><p/><byline/></div><div><p/></div></TEI>"
            ),
            etree.XML("<div><head/><byline/><p/></div>"),
            etree.XML("<div><opener/><byline/><p/></div>"),
            etree.XML("<div><argument/><byline/><p/></div>"),
            etree.XML("<div><dateline/><byline/><p/></div>"),
            etree.XML("<div><docAuthor/><byline/><p/></div>"),
            etree.XML("<div><docDate/><byline/><p/></div>"),
            etree.XML("<div><epigraph/><byline/><p/></div>"),
            etree.XML("<div><signed/><byline/><p/></div>"),
            etree.XML("<div><meeting/><byline/><p/></div>"),
            etree.XML("<div><salute/><byline/><p/></div>"),
            etree.XML("<div><byline/><byline/><p/></div>"),
            etree.XML("<div><byline/><argument/><p/></div>"),
            etree.XML("<div><byline/><dateline/><p/></div>"),
            etree.XML("<div><byline/><docDate/><p/></div>"),
            etree.XML("<div><byline/><docAuthor/><p/></div>"),
            etree.XML("<div><byline/><epigraph/><p/></div>"),
            etree.XML("<div><byline/><signed/><p/></div>"),
            etree.XML("<div><byline/><meeting/><p/></div>"),
            etree.XML("<div><byline/><salute/><p/></div>"),
            etree.XML("<div><byline/><head/><p/></div>"),
            etree.XML("<div><byline/><opener/><p/></div>"),
            etree.XML("<div><p/><byline/><argument/></div>"),
            etree.XML("<div><p/><byline/><byline/></div>"),
            etree.XML("<div><p/><byline/><dateline/></div>"),
            etree.XML("<div><p/><byline/><docDate/></div>"),
            etree.XML("<div><p/><byline/><docAuthor/></div>"),
            etree.XML("<div><p/><byline/><epigraph/></div>"),
            etree.XML("<div><p/><byline/><signed/></div>"),
            etree.XML("<div><p/><byline/><meeting/></div>"),
            etree.XML("<div><p/><byline/><salute/></div>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_observer_action_performed_on_simple_byline(self):
        root = etree.XML("<div><p/><byline/><p/></div>")
        node = root[2]
        self.observer.transform_node(node)
        result = [node.tag for node in root.find("div").iter()]
        self.assertEqual(result, ["div", "p", "byline"])

    def test_observer_action_performed_on_simple_byline_wiht_sibling(self):
        root = etree.XML("<div><p>text</p><byline>byline</byline><p>text2</p></div>")
        node = root.find(".//byline").getnext()
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["div", "div", "p", "byline", "p"])

    def test_observer_action_performed_on_byline_with_children(self):
        root = etree.XML(
            "<div><p>text</p><byline><docAuthor/>byline</byline><p>text2</p></div>"
        )
        node = root.find(".//byline").getnext()
        self.observer.transform_node(node)
        result = [node.tag for node in root.find(".//div").iter()]
        self.assertEqual(result, ["div", "p", "byline", "docAuthor"])

    def test_observer_action_performed_on_namespaced_node(self):
        root = etree.XML(
            "<TEI xmlns='ns'><text><div><p/><byline/><p/></div></text></TEI>"
        )
        node = root.find(".//{*}byline").getnext()
        self.observer.transform_node(node)
        result = [
            etree.QName(node).localname for node in root.find(".//{*}div/{*}div").iter()
        ]
        self.assertEqual(result, ["div", "p", "byline"])

    def test_observer_action_performed_on_namespaced_byline_with_children(self):
        root = etree.XML(
            "<TEI xmlns='ns'><div><p/><byline><docAuthor/>byline</byline><p>text</p></div></TEI>"
        )
        node = root.find(".//{*}byline").getnext()
        self.observer.transform_node(node)
        result = [
            etree.QName(node).localname for node in root.find(".//{*}div/{*}div").iter()
        ]
        self.assertEqual(result, ["div", "p", "byline", "docAuthor"])

    def test_observer_action_performed_on_byline_with_multiple_p_siblings(self):
        root = etree.XML("<div><p/><p/><p/><p/><byline/><p/></div>")
        node = root.find(".//byline").getnext()
        self.observer.transform_node(node)
        result = [node.tag for node in root.find("div").iter()]
        self.assertEqual(result, ["div", "p", "p", "p", "p", "byline"])

    def test_observer_action_performed_on_byline_with_mixed_siblings(self):
        root = etree.XML("<div><p/><list/><byline/><p/></div>")
        node = root.find(".//byline").getnext()
        self.observer.transform_node(node)
        result = [node.tag for node in root.find("./div").iter()]
        self.assertEqual(result, ["div", "p", "list", "byline"])

    def test_observer_action_performed_on_byline_with_p_and_div_as_sibling(self):
        root = etree.XML("<div><div/><p/><byline/><p/></div>")
        node = root.find(".//byline").getnext()
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["div", "div", "div", "p", "byline", "p"])

    def test_performed_on_byline_with_p_and_div_as_sibling_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><div/><p/><byline/><p/></div></TEI>")
        node = root.find(".//{*}byline").getnext()
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "div", "div", "div", "p", "byline", "p"])

    def test_action_performed_on_namespaced_byline_with_multiple_p_siblings(self):
        root = etree.XML(
            "<TEI xmlns='ns'><div><p/><p/><p>text</p><byline/><p/></div></TEI>"
        )
        node = root.find(".//{*}byline").getnext()
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "div", "div", "p", "p", "p", "byline", "p"])

    def test_action_performed_on_namespaced_byline_with_mixed_siblings(self):
        root = etree.XML(
            "<TEI xmlns='ns'><div><list/><p/><ab/><byline/><p/></div></TEI>"
        )
        node = root.find(".//{*}byline").getnext()
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(
            result, ["TEI", "div", "div", "list", "p", "ab", "byline", "p"]
        )

    def test_valid_sibling_after_added_to_new_div(self):
        root = etree.XML("<div><p/><byline/><docAuthor/><ab/></div>")
        node = root.find("ab")
        self.observer.transform_node(node)
        result = [node.tag for node in root.find("div").iter()]
        self.assertEqual(result, ["div", "p", "byline", "docAuthor"])

    def test_valid_sibling_before_byline_added_to_new_div(self):
        root = etree.XML("<div><head/><p/><signed/><byline/><ab/></div>")
        node = root.find("ab")
        self.observer.transform_node(node)
        result = [node.tag for node in root.find("div").iter()]
        self.assertEqual(result, ["div", "head", "p", "signed", "byline"])

    def test_valid_sibling_before_added_to_new_div_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><div><head/><p/><signed/><byline/><ab/></div></TEI>"
        )
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        result = [
            etree.QName(node).localname for node in root.find("./{*}div/{*}div").iter()
        ]
        self.assertEqual(result, ["div", "head", "p", "signed", "byline"])

    def test_valid_sibling_after_added_to_new_div_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><div><p/><byline/><meeting/><ab/></div></TEI>"
        )
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        result = [
            etree.QName(node).localname for node in root.find("./{*}div/{*}div").iter()
        ]
        self.assertEqual(result, ["div", "p", "byline", "meeting"])
