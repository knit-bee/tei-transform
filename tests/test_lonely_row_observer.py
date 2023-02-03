import unittest

from lxml import etree

from tei_transform.observer import LonelyRowObserver


class LonelyRowObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelyRowObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<div><row/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<div><table><row/></table></div>")
        node = root.find(".//row")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<p><row/></p>"),
            etree.XML("<div><row></row></div>"),
            etree.XML("<div><row><cell/></row></div>"),
            etree.XML("<div><row><cell>text</cell></row></div>"),
            etree.XML("<table><row><cell><row/></cell></row></table>"),
            etree.XML("<div><row>text</row></div>"),
            etree.XML(
                """
                <TEI>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text
                          <hi>text
                            <row>
                              <cell>text</cell>
                            </row>
                          </hi>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                          <head>text
                            <row>
                              <cell>text</cell>
                            </row>tail
                        </head>
                        <p>text
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <row>
                          <cell>text</cell>
                        </row>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <row>
                          <cell>text</cell>
                        </row>
                        <table>
                          <row>
                            <cell>text</cell>
                          </row>
                        </table>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <table>
                          <row>
                            <cell>text
                              <row>
                                <cell>text</cell>tail
                              </row>tail
                            </cell>
                          </row>
                        </table>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                        <row>
                          <cell>text</cell>
                        </row>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                          <list>
                            <item>
                              <row>
                                <cell>text</cell>
                              </row>
                            </item>
                          </list>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<table><row/></table>"),
            etree.XML("<table><row/><row><cell/></row></table>"),
            etree.XML("<div><table><row><cell>text</cell></row></table></div>"),
            etree.XML(
                "<table><row><cell><table><row><cell/></row></table></cell></row></table>"
            ),
            etree.XML("<table><row><cell>text</cell><cell>text</cell></row></table>"),
            etree.XML("<div><head><table><row/></table></head></div>"),
            etree.XML(
                "<div><p>text<table><row><cell>text</cell><cell/></row></table></p></div>"
            ),
            etree.XML(
                "<div><p><table><row><cell/><cell/></row><row><cell>text</cell></row></table></p></div>"
            ),
            etree.XML(
                """
                <TEI>
                <teiHeader/>
                <text>
                  <body>
                    <div>
                      <p>text<table><row><cell>text</cell></row></table>tail</p>
                    </div>
                  </body>
                </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <p>
                          <table>
                            <row>
                              <cell>
                                <table>
                                  <row/>
                                </table>
                              </cell>
                            </row>
                          </table>
                        </p>tail
                        <p>more text</p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_table_element_added_as_parent(self):
        root = etree.XML("<div><row><cell/></row></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root[0].tag, "table")

    def test_table_element_added_as_parent_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <text><div>
                <row>
                  <cell>text</cell>
                </row>
              </div></text>
            </TEI>
            """
        )
        node = root.find(".//{*}row")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}table") is not None)

    def test_lonely_empty_row_removed(self):
        root = etree.XML("<div><row/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_attributes_of_row_preserved_after_transformation(self):
        root = etree.XML("<div><row attr='val'><cell>text</cell></row></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//row").attrib
        self.assertEqual(result, {"attr": "val"})

    def test_children_preserved_after_transformation(self):
        root = etree.XML(
            """
            <div>
              <row>
                <cell>data</cell>
                <cell><floatingText/></cell>
                <cell><list><item>text</item></list></cell>
                <cell><p>text2</p>tail</cell>
                <cell>text3</cell>
              </row>
            </div>
            """
        )
        node = root[0]
        self.observer.transform_node(node)
        result = [elem.tag for elem in root.find(".//table/row").iter()]
        self.assertEqual(
            result,
            [
                "row",
                "cell",
                "cell",
                "floatingText",
                "cell",
                "list",
                "item",
                "cell",
                "p",
                "cell",
            ],
        )

    def test_attributes_of_row_preserved_after_transformation_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><div><row attr='val'><cell/></row></div></TEI>"
        )
        node = root.find(".//{*}row")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}row").attrib, {"attr": "val"})

    def test_multiple_adjacent_rows_added_to_same_table_element(self):
        root = etree.XML(
            """<div>
                <row>
                    <cell/>
                </row>
                <row>
                    <cell/>
                </row>
                <row>
                    <cell/>
                    <cell/>
                </row>
                <row>
                    <cell>text</cell>
                </row>
              </div>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertTrue(len(root.findall(".//table")), 1)

    def test_multiple_adjacent_rows_added_to_same_table_element_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
                <text>
                  <body>
                    <div>
                        <row>
                            <cell/>
                        </row>
                        <row>
                            <cell/>
                        </row>
                        <row>
                            <cell/>
                            <cell/>
                        </row>
                        <row>
                            <cell>text</cell>
                        </row>
                    </div>
                  </body>
                </text>
            </TEI>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertTrue(len(root.findall(".//{*}table")), 1)

    def test_empty_rows_not_added_to_table_with_multiple_adjacent_rows(self):
        root = etree.XML(
            """<div>
                <row/>
                <row>
                    <cell/>
                </row>
                <row/>
                <row>
                    <cell/>
                </row>
                <row>
                    <cell/>
                    <cell/>
                </row>
                <row/>
                <row>
                    <cell>text</cell>
                </row>
              </div>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertTrue(len(root.findall(".//table/row")), 4)

    def test_observer_action_performed_on_nested_row(self):
        root = etree.XML(
            "<div><table><row><cell><row><cell/></row></cell></row></table></div>"
        )
        node = root.findall(".//row")[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//table//table") is not None)

    def test_observer_action_performed_on_nested_row_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <text>
                <div>
                  <p>
                    <table>
                      <row>
                        <cell>
                          <row>
                            <cell>text</cell>
                          </row>
                        </cell>
                      </row>
                    </table>
                  </p>
                </div>
              </text>
            </TEI>
            """
        )
        node = root.findall(".//{*}row")[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}table//{*}table") is not None)

    def test_nested_empty_row_removed(self):
        root = etree.XML("<div><table><row><cell><row/></cell></row></table></div>")
        node = root.find(".//cell/row")
        self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//cell")), 0)

    def test_nested_empty_row_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <table>
                  <row>
                    <cell>
                      <row>
                      </row>
                    </cell>
                  </row>
                </table>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}cell/{*}row")
        self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//{*}cell")), 0)

    def test_tail_on_lonely_row_last_cell_child(self):
        root = etree.XML(
            """
            <div>
              <p>text
                <row>
                  <cell>data</cell>
                </row>tail
              </p>
            </div>
            """
        )
        node = root.find(".//row")
        self.observer.transform_node(node)
        result = root.find(".//cell").text
        self.assertEqual(result, "data tail")

    def test_tail_removed_from_lonely_row_after_transformation(self):
        root = etree.XML(
            """
            <div>
              <p>text
                <row>
                  <cell>data</cell>
                </row>tail
              </p>
            </div>
            """
        )
        node = root.find(".//row")
        self.observer.transform_node(node)
        result = root.find(".//row").tail
        self.assertEqual(result, None)

    def test_row_without_children_but_with_text_not_removed(self):
        root = etree.XML("<div><row>text</row></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root[0].tag, "table")

    def test_row_without_children_but_with_tail_not_removed(self):
        root = etree.XML("<div><p><row/>tail</p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//table") is not None)

    def test_multiple_table_elements_inserted_if_lonely_rows_not_adjacent(self):
        root = etree.XML(
            """
            <div>
              <row><cell>first</cell></row>
              <row><cell>first</cell></row>
              <p>intermediate text</p>
              <row><cell>second</cell></row>
              <p>second intermediate text</p>
              <row><cell>third</cell></row>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//table")), 3)

    def test_tail_on_empty_row_added_to_new_cell(self):
        root = etree.XML("<div><p><row/>tail</p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//cell").text, "tail")

    def test_moving_tail_of_row_to_cell_with_children(self):
        root = etree.XML(
            """
            <div>
              <p>
                <row>
                  <cell>text
                    <p>inner
                    </p>tail
                  </cell>
                </row>target
              </p>
            </div>
            """
        )
        node = root.find(".//row")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//row//p").tail, "tail target")
        self.assertIsNone(node.tail)
