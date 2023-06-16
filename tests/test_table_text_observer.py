import unittest

from lxml import etree

from tei_transform.observer import TableTextObserver


class TableTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TableTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<table>text</table>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><table><row><cell>text</cell></row></table></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<table><row/>tail</table>"),
            etree.XML("<div><table>text<row><cell/></row>tail</table></div>"),
            etree.XML("<div><table><head>text</head>tail<row/></table></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>text
                      <row>
                        <cell>text</cell>
                      </row>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <row>
                        <cell>text</cell>
                      </row>tail
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <head>text</head>tail
                      <row>
                        <cell>text</cell>
                      </row>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><table/>tail</div>"),
            etree.XML("<table>  <row/></table>"),
            etree.XML("<div><table><row><cell><p/>tail</cell></row></table></div>"),
            etree.XML("<table><row/> <row/>\n  </table>"),
            etree.XML(
                "<div><table><head>text</head><row><cell/>tail</row></table></div>"
            ),
            etree.XML("<table><row/><fw>text</fw><row/></table>"),
            etree.XML("<table><row><cell><table/>tail</cell></row></table>"),
            etree.XML("<table><row><cell>text<p>text</p></cell></row></table>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text</cell>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text
                            <p>text</p>tail
                          </cell>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text</cell>
                        </row>
                      </table>tail
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <head>text</head>
                        <row>
                          <cell>text</cell>
                        </row>
                      </table>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text</cell>
                        </row>
                        <fw>text</fw>
                        <row/>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text
                            <table>
                              <row/>
                            </table>tail
                          </cell>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_text_from_table_removed(self):
        node = etree.XML("<table>text<row/></table>")
        self.observer.transform_node(node)
        self.assertTrue(node.text is None)

    def test_text_in_table_added_to_new_head_elem(self):
        root = etree.XML("<div><table>text<row/></table></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//head").text, "text")

    def test_tail_on_row_child_removed(self):
        node = etree.XML("<table><row><cell/></row>tail</table>")
        self.observer.transform_node(node)
        self.assertTrue(node[0].tail is None)

    def test_tail_on_other_children_resolved(self):
        node = etree.XML("<table><head/>tail<row/></table>")
        self.observer.transform_node(node)
        self.assertTrue(node[0].tail is None)

    def test_text_from_table_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <table>text
                <row><cell/></row>
              </table>
            </TEI>
            """
        )
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        self.assertTrue(node.text is None)

    def test_text_in_table_added_to_new_head_elem_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <div>
                <table>text
                  <row>
                    <cell>data</cell>
                  </row>
                </table>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}head").text, "text")

    def test_tail_on_row_child_resolved_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><table><row/><row><cell/></row>tail</table></TEI>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(all(child.tail is None for child in node))

    def test_tail_on_other_children_resolved_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <table>
                <head/>tail
                <row/>
                <row>
                  <cell>text</cell>
                </row>
              </table>
            </TEI>
            """
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(node[0].tail is None)

    def test_text_in_nested_table_removed(self):
        root = etree.XML(
            """
            <div>
              <table>
                <row>
                  <cell>
                    <table>
                      text
                      <row/>
                    </table>
                  </cell>
                </row>
              </table>
            </div>
            """
        )
        node = root.find(".//cell/table")
        self.observer.transform_node(node)
        result = node.text.strip() if node.text is not None else None
        self.assertFalse(result)

    def test_tail_on_row_child_in_nested_list_removed(self):
        root = etree.XML(
            """
            <div>
              <table>
                <row>
                  <cell>
                    <table>
                      <row>
                        <cell/>
                      </row>tail
                      <row/>
                    </table>
                  </cell>
                </row>
              </table>
            </div>
            """
        )
        node = root.find(".//cell/table")
        self.observer.transform_node(node)
        result = [
            node
            for node in root.findall("row")
            if node.tail is not None or node.tail.strip()
        ]
        self.assertEqual(result, [])

    def test_table_with_multiple_text_tail_components_handled_correctly(self):
        root = etree.XML(
            """
        <div>
          <table>
            <head>text1</head>tail1
            <row>
              <cell>text</cell>
            </row>tail2
            <row/>tail3
            <fw>text2</fw>tail4
            <row>
              <cell/>
            </row>tail5
          </table>
        </div>
        """
        )
        node = root[0]
        self.observer.transform_node(node)
        result = [
            (node.tag, node.text.strip() if node.text is not None else None)
            for node in root[0].iter()
        ]
        self.assertEqual(
            result,
            [
                ("table", ""),
                ("head", "text1 tail1"),
                ("row", ""),
                ("cell", "text tail2"),
                ("row", None),
                ("cell", "tail3"),
                ("fw", "text2 tail4"),
                ("row", ""),
                ("cell", "tail5"),
            ],
        )

    def test_tail_of_row_concatenated_with_last_cell_child(self):
        node = etree.XML("<table><row><cell>text</cell></row>tail</table>")
        self.observer.transform_node(node)
        self.assertEqual(node.find(".//cell").text, "text tail")

    def test_new_cell_added_for_tail_on_empty_row(self):
        root = etree.XML("<div><table><row/><row/>tail</table></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//table/row[2]/cell").text, "tail")

    def test_no_head_element_inserted_for_only_whitespace_text_content_of_table(self):
        root = etree.XML("<div><p><table>    <row/>  <row/>  </table></p></div>")
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//head") is None)

    def test_tail_on_p_with_child_concatenated_to_tail_of_last_child(self):
        root = etree.XML(
            """
            <div>
              <p>
              <table>
                <row>
                  <cell>text</cell>
                </row>
                <p>text1
                  <hi>text2</hi>tail1
                </p>tail2
              </table>
              </p>
            </div>
            """
        )
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//hi").tail, "tail1 tail2")

    def test_tail_on_row_with_grandchild_concatenated_with_grandchild_tail(self):
        root = etree.XML(
            """
            <div>
              <table>
                <row>
                  <cell>text
                    <p>inner</p>tail
                  </cell>
                </row>target
              </table>
            </div>
            """
        )
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").tail, "tail target")
        self.assertIsNone(root.find(".//row").tail)
