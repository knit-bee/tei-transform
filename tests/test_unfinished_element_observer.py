import unittest

from lxml import etree

from tei_transform.observer import UnfinishedElementObserver


class UnfinishedElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = UnfinishedElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><table><head/></table></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><table><row/></table></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><list><head/></list></div>"),
            etree.XML("<div><table><head>text</head></table></div>"),
            etree.XML("<div><list><byline/></list></div>"),
            etree.XML("<div><list><note/></list></div>"),
            etree.XML("<div><list><fw/></list></div>"),
            etree.XML("<div><table><index/></table></div>"),
            etree.XML("<div><table><byline/></table></div>"),
            etree.XML("<div><table><index/></table></div>"),
            etree.XML("<TEI xmlns='a'><table><head/></table></TEI>"),
            etree.XML("<TEI xmlns='a'><list><head/></list></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><table><head/></table></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<table><byline/></table></p></TEI>"),
            etree.XML("<TEI xmlns='a'><div><list><head/></list></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<table><head/></table></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<list><byline/></list></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><table><head/><row/></table></div>"),
            etree.XML("<div><table><row/></table></div>"),
            etree.XML("<div><table></table></div>"),
            etree.XML("<div><list><head/><item/></list></div>"),
            etree.XML("<div><table><head/><fw/><row/><row/></table></div>"),
            etree.XML("<div><table><row><cell/></row><byline/></table></div>"),
            etree.XML("<div><p><list><head/><item>text</item></list></p></div>"),
            etree.XML("<TEI xmlns='a'><div><table><head/><row/></table></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><list><head/><item/></list></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<table><head/><row/></table></p></div></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><div><p>text<list/></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p>text<table/></p></div></TEI>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <p>text
                      <table>
                        <row>
                          <cell>
                            <list/>
                          </cell>
                        </row>
                      </table>
                    </p>
                  </div>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_handle_unfinished_list(self):
        root = etree.XML("<div><list><fw/></list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/item") is not None)

    def test_handle_unfinished_table(self):
        root = etree.XML("<div><table><fw/></table></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//table/row/cell") is not None)

    def test_handle_unfinished_list_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><list><byline/></list></div></TEI>")
        node = root.find(".//{*}list")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}list/{*}item") is not None)

    def test_handle_unfinished_table_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><table><pb/></table></div></TEI>")
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}table/{*}row/{*}cell") is not None)

    def test_item_added_as_second_element_for_list_with_head(self):
        root = etree.XML("<div><list><head/></list></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//list/item").getprevious().tag
        self.assertEqual(result, "head")

    def test_new_row_added_as_second_child_for_table_with_head(self):
        root = etree.XML("<div><table><head/></table></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//table/row").getprevious().tag
        self.assertEqual(result, "head")

    def test_item_added_as_second_element_for_list_with_desc(self):
        root = etree.XML("<div><list><desc/></list></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//list/item").getprevious().tag
        self.assertEqual(result, "desc")

    def test_item_added_after_last_head_or_desc(self):
        elements = [
            (etree.XML("<div><list><desc/><byline/></list></div>"), 1),
            (etree.XML("<div><list><head/><desc/></list></div>"), 0),
            (etree.XML("<div><list><head/><fw/><desc/></list></div>"), 0),
            (
                etree.XML(
                    "<div><list><head/><desc/><head/><byline/><fw/></list></div>"
                ),
                2,
            ),
            (
                etree.XML(
                    "<div><list><head/><desc/><head/><head/><byline/><fw/></list></div>"
                ),
                2,
            ),
            (
                etree.XML(
                    "<div><list><head/><desc/><fw/><head/><fw/><byline/></list></div>"
                ),
                2,
            ),
            (
                etree.XML(
                    "<TEI xmlns='a'><list><desc/><head/><fw/><head/><fw/><byline/></list></TEI>"
                ),
                2,
            ),
        ]
        for root, expected_siblings in elements:
            node = root[0]
            self.observer.transform_node(node)
            with self.subTest():
                item_child = root.find(".//{*}item")
                result = [sib.tag for sib in item_child.itersiblings()]
                self.assertEqual(len(result), expected_siblings)
                self.assertTrue("head" not in result and "desc" not in result)

    def test_row_added_after_last_head(self):
        elements = [
            (etree.XML("<div><table><head/><fw/></table></div>"), 1),
            (etree.XML("<div><table><head/><head/><fw/></table></div>"), 1),
            (etree.XML("<div><table><head/><fw/><fw/><dateline/></table></div>"), 3),
            (etree.XML("<div><table><fw/><head/><fw/><trailer/></table></div>"), 2),
            (
                etree.XML(
                    "<TEI xmlns='a'><table><head/><head/><fw/><head/></table></TEI>"
                ),
                0,
            ),
        ]
        for root, expected_siblings in elements:
            node = root[0]
            self.observer.transform_node(node)
            with self.subTest():
                row_child = root.find(".//{*}row")
                result = [sib.tag for sib in row_child.itersiblings()]
                self.assertEqual(len(result), expected_siblings)
                self.assertTrue("head" not in result)

    def test_resolve_multiple_unfinished_elements_during_iteration(self):
        root = etree.XML(
            """
            <div>
              <table>
                <head>text1</head>
              </table>
              <p>
                <list>
                  <item>
                    <list>
                      <head>text2</head>
                      <fw>text3</fw>
                    </list>
                  </item>
                </list>
              <table>
                <head>text4</head>
                <byline>text5</byline>
                <fw>text6</fw>
              </table>
            </p>
            <list>
              <desc>text7</desc>
              <fw/>
              <byline/>
            </list>
            <p>text8</p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)

        result = [
            (node.tag, [child.tag for child in node])
            for node in root.iterdescendants(["list", "table"])
        ]
        expected = [
            ("table", ["head", "row"]),
            ("list", ["item"]),
            ("list", ["head", "item", "fw"]),
            ("table", ["head", "row", "byline", "fw"]),
            ("list", ["desc", "item", "fw", "byline"]),
        ]
        self.assertEqual(result, expected)

    def test_new_item_added_as_first_child_if_other_priority_child_present(self):
        root = etree.XML("<div><list><fw/><byline/><fw/></list></div>")
        node = root[0]
        self.observer.transform_node(node)
        target = root.find(".//item")
        self.assertEqual(node.index(target), 0)

    def test_new_row_added_as_first_child_if_no_head_child_present(self):
        root = etree.XML("<div><table><fw/><byline/></table></div>")
        node = root[0]
        self.observer.transform_node(node)
        target = root.find(".//row")
        self.assertEqual(node.index(target), 0)
