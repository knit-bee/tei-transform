import unittest

from lxml import etree

from tei_transform.observer import EmptyElementObserver


class EmptyElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><list/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><list><item/></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<list/>"),
            etree.XML("<div><list/><list><item/></list></div>"),
            etree.XML("<div><list><item><list/></item></list></div>"),
            etree.XML("<ab><list></list></ab>"),
            etree.XML("<p><list/>text</p>"),
            etree.XML("<p>text<list/>more text</p>"),
            etree.XML("<div><p>text<list/>more text</p></div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                <text><body>
                <list/>
                </body>
                </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <list></list>
                            </body>
                            </text></TEI>
                                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <div><p>text</p>
                            <list/>
                            </div>
                            </body>
                            </text></TEI>
                                """
            ),
            etree.XML("<table><row><cell><list/></cell></row></table>"),
            etree.XML("<div><list>    </list></div>"),
            etree.XML(
                """<div><p><list>
            </list></p></div>"""
            ),
            etree.XML("<table/>"),
            etree.XML("<div><table>   </table></div>"),
            etree.XML("<div><table></table></div>"),
            etree.XML("<div><p><table/>tail</p></div>"),
            etree.XML("<div><list><item>text<table/></item></list></div>"),
            etree.XML("<div><p>text</p><table/>tail</div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                <text><body>
                <table/>
                </body>
                </text></TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                    <table/>tail
                    </body>
                    </text></TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body><p>text
                    <table/>tail</p>
                    </body>
                    </text></TEI>
                """
            ),
            etree.XML("<row/>"),
            etree.XML("<row></row>"),
            etree.XML("<table><row>   </row></table>"),
            etree.XML("<table><row/></table>"),
            etree.XML("<div><table><row><cell/></row><row/></table></div>"),
            etree.XML("<div><table><row><cell/></row><row/>tail</table></div>"),
            etree.XML("<div><row>text</row><row/></div>"),
            etree.XML("<div><row/>tail</div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                    <div>
                    <table>
                    <row/>
                    </table>
                    </div>
                    </body>
                    </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                        <text><body><p>text
                        <table><row/>tail</table></p>
                        </body>
                        </text></TEI>
                """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<list><item/></list>"),
            etree.XML("<list><item>text</item></list>"),
            etree.XML("<div><list><item/></list></div>"),
            etree.XML(
                "<div><list><item><list><item>text</item></list></item></list></div>"
            ),
            etree.XML("<ab><list><item/></list></ab>"),
            etree.XML("<p><list><item>text</item></list>text</p>"),
            etree.XML("<p>text<list><item>item text</item></list>more text</p>"),
            etree.XML("<div><p>text<table>text</table>more text</p></div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                <text><body>
                <list>
                  <item/>
                </list>
                </body>
                </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <list><item>text</item></list>
                            </body>
                            </text></TEI>
                                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <div><p>text</p>
                            <list>
                            <item>text</item></list>
                            </div>
                            </body>
                            </text></TEI>
                                """
            ),
            etree.XML("<div><list>text</list></div>"),
            etree.XML("<div><list><item>text1<list>text2</list></item></list></div>"),
            etree.XML("<table><row><cell/></row></table>"),
            etree.XML("<table>text</table>"),
            etree.XML("<div><table><row>text</row></table></div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                    <table>
                      <row>
                        <cell/>
                      </row>
                    </table>
                    </body>
                    </text></TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                      <div>
                        <table>
                          text
                        </table>
                      </div>
                    </body>
                    </text></TEI>
                        """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                    <table>
                      <row>
                        <cell/>
                      </row>
                    </table>
                    </body>
                    </text></TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                      <table>
                        <row>
                          text
                        </row>
                      </table>
                    </body>
                    </text></TEI>
                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_empty_list_removed(self):
        root = etree.XML("<div><list/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_nested_empty_list_removed(self):
        root = etree.XML("<div><list><item>text<list/></item><item/></list></div>")
        node = root.findall(".//list")[1]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["div", "list", "item", "item"])

    def test_empty_list_with_namespace_removed(self):
        root = etree.XML("<TEI xmlns='namespace'><text><div><list/></div></text></TEI>")
        node = root.find(".//{*}list")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "text", "div"])

    def test_nested_empty_list_with_namespace_removed(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><div><list><item>text<list/></item><item/></list></div></TEI>"
        )
        node = root.findall(".//{*}list")[1]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "div", "list", "item", "item"])

    def test_empty_list_with_attributes_removed(self):
        root = etree.XML("<div><list type='val'/></div>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_empty_list_with_attributes_and_namespace_removed(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><text><div><list type='val'/></div></text></TEI>"
        )
        node = root.find(".//{*}list")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "text", "div"])

    def test_nested_empty_list_with_attributes_removed(self):
        root = etree.XML(
            "<div><list rend='numbered'><item><list rend='dotted'/></item></list></div>"
        )
        node = root.findall(".//list")[1]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["div", "list", "item"])

    def test_nested_list_with_namespace_and_attribute_removed(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><text><div><list><item><list type='ul'/></item></list></div></text></TEI>"
        )
        node = root.findall(".//{*}list")[1]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "text", "div", "list", "item"])

    def test_tail_text_on_empty_list_retained_within_p(self):
        root = etree.XML("<div><p><list/>tail</p></div>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_tail_text_on_empty_list_retained_within_div(self):
        root = etree.XML("<div><list/>tail</div>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_tail_text_on_nested_empty_list_retained(self):
        root = etree.XML("<div><list><item><list/>tail</item></list></div>")
        node = root.findall(".//list")[1]
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_tail_on_list_with_text_containing_parent_retained(self):
        tags = ["item", "cell", "ab", "fw", "quote", "head"]
        for tag in tags:
            root = etree.XML(f"<div><{tag}>text<list/>tail</{tag}></div>")
            node = root.find(".//list")
            self.observer.transform_node(node)
            with self.subTest():
                self.assertTrue(
                    "tail" in etree.tostring(root, method="text", encoding="unicode")
                )

    def test_order_of_text_parts_retained_if_tail_of_empty_list_is_moved(self):
        root = etree.XML("<div><p>text1<list/>tail</p>text2</div>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        result = etree.tostring(root, method="text", encoding="unicode").replace(
            " ", ""
        )
        self.assertEqual(result, "text1tailtext2")

    def test_tail_text_on_empty_list_retained_within_body(self):
        root = etree.XML("<text><body><p>text</p><list/>tail</body></text>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_new_p_added_if_list_parent_is_div_or_body(self):
        roots = [
            etree.XML("<text><body><list/>tail<p>text</p></body></text>"),
            etree.XML("<div><p>text1</p><list/>tail<p>text2</p></div>"),
        ]
        for root in roots:
            node = root.find(".//list")
            num_of_ps_before_transformation = len(root.findall(".//p"))
            self.observer.transform_node(node)
            with self.subTest():
                self.assertEqual(
                    len(root.findall(".//p")), num_of_ps_before_transformation + 1
                )

    def test_whitespace_inserted_if_tail_is_concatenated_to_parent_text(self):
        root = etree.XML("<div><p>text<list/>tail</p></div>")
        node = root.find(".//list")
        self.observer.transform_node(node)
        self.assertTrue(
            "text tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_empty_table_removed(self):
        root = etree.XML("<div><table/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_nested_empty_table_removed(self):
        root = etree.XML(
            "<div><table><row><cell>text<table/></cell></row></table></div>"
        )
        node = root.findall(".//table")[1]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["div", "table", "row", "cell"])

    def test_empty_table_with_namespace_removed(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><text><div><table/></div></text></TEI>"
        )
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "text", "div"])

    def test_nested_empty_table_with_namespace_removed(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><div><table><row><cell>text<table/></cell></row></table></div></TEI>"
        )
        node = root.findall(".//{*}table")[1]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "div", "table", "row", "cell"])

    def test_empty_table_with_attributes_removed(self):
        root = etree.XML("<div><table type='val'/></div>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_empty_table_with_attributes_and_namespace_removed(self):
        root = etree.XML(
            """<TEI xmlns='namespace'>
                  <text>
                    <div>
                      <table type='val'></table>
                    </div>
                  </text>
                </TEI>"""
        )
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "text", "div"])

    def test_nested_empty_table_with_attributes_removed(self):
        root = etree.XML(
            """<div>
                <table type='val'>
                  <row>
                    <cell>
                      <table type='val2'/>
                    </cell>
                  </row>
                </table>
              </div>"""
        )
        node = root.findall(".//table")[1]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["div", "table", "row", "cell"])

    def test_nested_table_with_namespace_and_attribute_removed(self):
        root = etree.XML(
            """<TEI xmlns='namespace'>
                <text><div>
                  <table>
                    <row>
                      <cell>
                        <table type='val'/>
                      </cell>
                    </row>
                  </table>
                </div></text></TEI>"""
        )
        node = root.findall(".//{*}table")[1]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "text", "div", "table", "row", "cell"])

    def test_tail_text_on_empty_table_retained_within_p(self):
        root = etree.XML("<div><p><table/>tail</p></div>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_tail_text_on_empty_table_retained_within_div(self):
        root = etree.XML("<div><table/>tail</div>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_tail_text_on_nested_empty_table_retained(self):
        root = etree.XML(
            "<div><table><row><cell><table/>tail</cell></row></table></div>"
        )
        node = root.findall(".//table")[1]
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_tail_on_table_with_text_containing_parent_retained(self):
        tags = ["item", "cell", "ab", "fw", "quote", "head"]
        for tag in tags:
            root = etree.XML(f"<div><{tag}>text<table/>tail</{tag}></div>")
            node = root.find(".//table")
            self.observer.transform_node(node)
            with self.subTest():
                self.assertTrue(
                    "tail" in etree.tostring(root, method="text", encoding="unicode")
                )

    def test_order_of_text_parts_retained_if_tail_of_empty_table_is_moved(self):
        root = etree.XML("<div><p>text1<table/>tail</p>text2</div>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        result = etree.tostring(root, method="text", encoding="unicode").replace(
            " ", ""
        )
        self.assertEqual(result, "text1tailtext2")

    def test_tail_text_on_empty_table_retained_within_body(self):
        root = etree.XML("<text><body><p>text</p><table/>tail</body></text>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(
            "tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_new_p_added_if_table_parent_is_div_or_body(self):
        roots = [
            etree.XML("<text><body><table/>tail<p>text</p></body></text>"),
            etree.XML("<div><p>text1</p><table/>tail<p>text2</p></div>"),
        ]
        for root in roots:
            node = root.find(".//table")
            num_of_ps_before_transformation = len(root.findall(".//p"))
            self.observer.transform_node(node)
            with self.subTest():
                self.assertEqual(
                    len(root.findall(".//p")), num_of_ps_before_transformation + 1
                )

    def test_whitespace_inserted_if_tail_is_concatenated_to_parent_text_with_table(
        self,
    ):
        root = etree.XML("<div><p>text<table/>tail</p></div>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(
            "text tail" in etree.tostring(root, method="text", encoding="unicode")
        )

    def test_empty_row_removed(self):
        root = etree.XML("<div><table><row/><row><cell/></row></table></div>")
        node = root.find(".//row")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//row")), 1)

    def test_table_containing_only_empty_row_also_removed(self):
        root = etree.XML("<div><table><row/></table></div>")
        node = root.find(".//row")
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_nested_empty_row_removed(self):
        root = etree.XML("<div><table><row><cell>text<row/></cell></row></table></div>")
        node = root.findall(".//row")[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//row")), 1)

    def test_empty_row_with_namespace_removed(self):
        root = etree.XML(
            """<TEI xmlns='ns'>
                <text>
                  <table>
                    <row><cell/></row>
                    <row/>
                  </table>
                </text>
            </TEI>"""
        )
        node = root.findall(".//{*}row")[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//{*}row")), 1)

    def test_nested_empty_row_with_namespace_removed(self):
        root = etree.XML(
            """<TEI xmlns='ns'>
                        <text>
                          <table>
                            <row><cell/></row>
                            <row>
                              <cell>
                                <table>
                                  <row/>
                                  <row>
                                    <cell>text</cell>
                                  </row>
                                </table>
                              </cell>
                            </row>
                          </table>
                        </text>
                    </TEI>"""
        )
        node = root.findall(".//{*}row")[2]
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//{*}row")), 3)

    def test_empty_row_with_attributes_removed(self):
        root = etree.XML("<div><table><row att='val'/><row><cell/></row></table></div>")
        node = root.find(".//row")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//row")), 1)

    def test_empty_row_with_attribute_and_namespace_removed(self):
        root = etree.XML(
            """<TEI xmlns='ns'>
                        <text>
                          <table>
                            <row><cell/></row>
                            <row att='val'/>
                          </table>
                        </text>
                    </TEI>"""
        )
        node = root.findall(".//{*}row")[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//{*}row")), 1)

    def test_tail_on_empty_row_retained_in_cell(self):
        root = etree.XML("<div><table><row/>tail</table></div>")
        node = root.find(".//row")
        self.observer.transform_node(node)
        result = [(elem.tag, elem.text, elem.tail) for elem in root.iter()]
        expected = [
            ("div", None, None),
            ("table", None, None),
            ("row", None, None),
            ("cell", "tail", None),
        ]
        self.assertEqual(result, expected)

    def test_tail_of_empty_element_not_added_as_tail_of_new_p(self):
        root = etree.XML("<div><table/>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(
            etree.tostring(root, method="text", encoding="unicode"), "tail"
        )
