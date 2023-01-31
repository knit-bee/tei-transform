import unittest

from lxml import etree

from tei_transform.observer import LonelyCellObserver


class LonelyCellObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelyCellObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><cell/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><row><cell/></row></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><cell></cell></div>"),
            etree.XML("<div><cell>text</cell></div>"),
            etree.XML("<p><cell><p/></cell></p>"),
            etree.XML("<p><cell><p>text</p></cell></p>"),
            etree.XML("<div><table><cell/></table></div>"),
            etree.XML("<div><cell><cell>text</cell></cell></div>"),
            etree.XML("<table><row><cell><p><cell/></p></cell></row></table>"),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                       <p>text<cell>text</cell></p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                       <cell>text</cell>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                       <p>text<hi>text<cell>text</cell></hi></p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                        <p>text
                          <table>
                            <row>
                              <cell>
                                <p>
                                  <cell>text</cell>
                                </p>
                              </cell>
                            </row>
                          </table>tail
                        </p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <text>
                      <div>
                        <p>text
                          <table>
                            <row>
                              <cell>
                                <p>
                                  <cell>text</cell>
                                </p>
                              </cell>
                            </row>
                          </table>tail
                        </p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <text>
                      <div>
                        <p>
                          <list>
                            <item>
                              <cell>text</cell>
                            </item>
                          </list>
                        </p>
                      </div>
                    </text>
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
            etree.XML("<row><cell/></row>"),
            etree.XML("<row><cell>text</cell></row>"),
            etree.XML("<row><cell><list/></cell></row>"),
            etree.XML("<table><row><cell>text</cell></row></table>"),
            etree.XML("<div><row><cell/></row></div>"),
            etree.XML(
                "<div><table><row><cell><cell>text</cell></cell></row></table></div>"
            ),
            etree.XML(
                "<table><row><cell><table><row><cell/></row></table></cell></row></table>"
            ),
            etree.XML("<p>text<hi>text<row><cell/></row>tail</hi>text</p>"),
            etree.XML(
                """
                <TEI>
                  <text>
                    <div>
                      <p>text</p>
                      <table>
                        <row>
                          <cell>text</cell>
                          <cell/>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <text>
                    <div>
                      <p>text
                          <table>
                            <row>
                              <cell>text</cell>
                              <cell/>
                            </row>
                          </table>tail
                      </p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <text>
                    <div>
                      <p>text</p>
                      <table>
                        <row>
                          <cell>text</cell>
                          <cell>
                            <table>
                              <row>
                               <cell>data</cell>
                              </row>
                            </table>
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

    def test_row_element_added_as_parent(self):
        root = etree.XML("<div><table><cell>text</cell></table></div>")
        node = root.find(".//cell")
        self.observer.transform_node(node)
        result = [node.tag for node in root.find(".//table").iter()]
        self.assertEqual(result, ["table", "row", "cell"])

    def test_row_element_added_as_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><table><cell/></table></div></TEI>")
        node = root.find(".//{*}cell")
        self.observer.transform_node(node)
        result = [
            etree.QName(node).localname for node in root.find(".//{*}table").iter()
        ]
        self.assertEqual(result, ["table", "row", "cell"])

    def test_table_also_added_as_parent_if_missing(self):
        root = etree.XML("<div><cell>text</cell></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = [el.tag for el in root.iter()]
        self.assertEqual(result, ["div", "table", "row", "cell"])

    def test_table_also_added_as_parent_if_missing_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><cell>text</cell></div></TEI>")
        node = root.find(".//{*}cell")
        self.observer.transform_node(node)
        result = [etree.QName(el).localname for el in root.iter()]
        self.assertEqual(result, ["TEI", "div", "table", "row", "cell"])

    def test_attributes_of_cell_preserved_after_transformation(self):
        root = etree.XML("<div><table><cell attr='val'>text</cell></table></div>")
        node = root.find(".//cell")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//row/cell").attrib, {"attr": "val"})

    def test_attributes_of_cell_preserved_after_transformation_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><cell attr='val'/></div></TEI>")
        node = root.find(".//{*}cell")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}row/{*}cell").attrib, {"attr": "val"})

    def test_children_preserved_after_transformation(self):
        root = etree.XML("<div><cell><p>text</p><p/><p/></cell></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//cell")), 3)

    def test_multiple_adjacent_cells_added_to_same_row_element(self):
        root = etree.XML("<div><cell/><cell/><cell/><cell/><cell>text</cell></div>")
        for element in root.iter():
            if self.observer.observe(element):
                self.observer.transform_node(element)
        result = [node.tag for node in root.iter()]
        self.assertEqual(len(root.findall(".//row")), 1)
        self.assertEqual(
            result,
            [
                "div",
                "table",
                "row",
                "cell",
                "cell",
                "cell",
                "cell",
                "cell",
            ],
        )

    def test_multiple_adjacent_cells_added_to_same_row_element_with_namesapce(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <text>
                <div>
                  <p>
                    <table>
                      <cell/>
                      <cell/>
                      <cell/>
                      <cell/>
                    </table>
                  </p>
                </div>
              </text>
            </TEI>
        """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = len(root.find(".//{*}table/{*}row"))
        self.assertEqual(result, 4)

    def test_observer_action_performed_on_nested_cell(self):
        root = etree.XML(
            "<div><table><row><cell><table><cell/></table></cell></row></table></div>"
        )
        node = root.find(".//table/cell")
        self.observer.transform_node(node)
        result = len(root.findall(".//table/row"))
        self.assertEqual(result, 2)

    def test_observer_action_performed_on_nested_cell_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <text>
                <div>
                  <table>
                    <row>
                      <cell>
                        <table>
                          <cell>text</cell>
                        </table>
                      </cell>
                    </row>
                  </table>
                </div>
              </text>
            </TEI>
        """
        )
        node = root.find(".//{*}table/{*}cell")
        self.observer.transform_node(node)
        result = len(root.findall(".//{*}table/{*}row"))
        self.assertEqual(result, 2)

    def test_tail_added_to_text_content(self):
        root = etree.XML("<div><p><cell>text</cell>tail</p></div>")
        node = root.find(".//cell")
        self.observer.transform_node(node)
        result = node.text
        self.assertEqual(result, "text tail")

    def test_tail_from_cell_removed(self):
        root = etree.XML("<p><cell>text</cell>tail</p>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//cell").tail
        self.assertEqual(result, None)

    def test_transformation_only_applied_to_outer_cell_if_nested_in_cell(self):
        root = etree.XML("<p><table><cell><cell>text1</cell></cell></table></p>")
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = len(root.findall(".//row"))
        self.assertEqual(result, 1)

    def test_multiple_non_adjacent_cells_added_to_different_rows_and_tables(self):
        root = etree.XML(
            """
            <div>
                <p>text<cell>a</cell>
                <cell>b</cell>
                <cell>c</cell>
                tail</p>
                <p><cell>1</cell>
                <cell>2</cell>
                <hi>text</hi>
                <cell>new</cell>
                <cell/>
                </p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [
            (
                node.tag,
                etree.tostring(node, method="text", encoding="unicode")
                .replace("\n", "")
                .replace(" ", ""),
            )
            for node in root.findall(".//table/row")
        ]
        self.assertEqual(result, [("row", "abctail"), ("row", "12"), ("row", "new")])

    def test_observer_action_performed_on_cell_with_siblings(self):
        root = etree.XML("<div><p/><cell/><p/></div>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//table/row/cell") is not None)
