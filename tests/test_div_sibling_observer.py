import unittest

from lxml import etree

from tei_transform.observer import DivSiblingObserver


class DivSiblingObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivSiblingObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<body><div/><table/></body>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<body><div/><div/></body>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><div/><table></table></div>"),
            etree.XML("<div><div><p/></div><quote/></div>"),
            etree.XML("<div><div/><quote/></div>"),
            etree.XML("<body><p/><div><p/></div><table><row/></table></body>"),
            etree.XML(
                "<div><p>text</p><div><p>text</p></div><quote>text</quote></div>"
            ),
            etree.XML(
                "<text><div><fw/><div><p>a</p></div><quote><p/></quote></div></text>"
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <div>
                            <p>text</p>
                          </div>
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
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <div>
                            <p>text</p>
                          </div>
                          <quote>text<p>text</p></quote>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <p>text</p>
                          <div>
                            <list>
                              <item>text</item>
                            </list>
                          </div>
                          <table>
                            <row>
                              <cell>
                                <table>
                                  <row/>
                                </table>
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
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <div>
                            <p>text</p>
                            <table>
                              <row>
                                <cell>text</cell>
                              </row>
                            </table>
                          </div>
                          <div>
                            <p>text</p>
                          </div>
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
            etree.XML("<div><div/><list/></div>"),
            etree.XML("<body><div/><list></list></body>"),
            etree.XML("<body><list/><div/><list/></body>"),
            etree.XML("<body><div/><list><item/></list></body>"),
            etree.XML("<div><div/><div><div/></div><list/></div>"),
            etree.XML(
                """<div><div><list/></div>
            <p>some text</p>
            <list>
            <item>more text</item>
            </list>
            </div>"""
            ),
            etree.XML(
                """<text>
                <body>
                  <div>
                    <div>
                      <fw rend="h1" type="header">header</fw>
                      <div>
                        <p>Some text</p>
                      </div>
                      <div/>
                      <list/>
                    </div></div></body></text>"""
            ),
            etree.XML(
                """<text>
                    <body>
                      <div type="entry">
                        <fw rend="h1" type="header">heading </fw>
                        <div>
                          <list><item/><item/></list>
                        </div>
                        <list/>
                        </div></body></text>"""
            ),
            etree.XML(
                """
            <TEI>
            <teiHeader/>
            <text>
            <body>
              <div type="entry">
                <fw rend="h1" type="header">heading </fw>
                <div>
                  <p/>
                </div>
                <list/>
                </div>
            </body></text>
            </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='namespace'>
                <teiHeader/>
                <text>
                <body>
                  <div type="entry">
                    <fw rend="h1" type="header">heading </fw>
                    <div>
                      <p>text
                      <lb/>more text
                      </p>
                    </div>
                    <p/>
                    <list/>
                    </div>
                </body></text>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><div><table/></div></div>"),
            etree.XML("<div><quote/></div>"),
            etree.XML("<body><table/><div><p/></div></body>"),
            etree.XML("<div><quote>text</quote><div><p>text</p></div></div>"),
            etree.XML("<div><table><row><cell>text</cell></row></table><div/></div>"),
            etree.XML(
                "<div><div><quote>text</quote></div><div><p>text</p></div></div>"
            ),
            etree.XML("<body><p>text</p><table/><div><p/></div></body>"),
            etree.XML("<div><table><row><cell/></row></table><div/><div/></div>"),
            etree.XML("<body><div><p>text</p></div><div><table/></div></body>"),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <table>
                            <row>
                              <cell>text</cell>
                            </row>
                          </table>
                          <div>
                            <p>text</p>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <div>
                            <table>
                              <row>
                                <cell>text</cell>
                              </row>
                            </table>
                          </div>
                          <div>
                            <p>text</p>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <quote>
                            <p>text</p>
                          </quote>
                          <div>
                            <p>text</p>
                            <quote/>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text
                            <quote>text</quote>
                          </p>
                          <table>
                            <row>
                              <cell>text</cell>
                            </row>
                          </table>
                          <div>
                            <p>text</p>
                          </div>
                          <div>
                            <quote/>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML("<body><div><list/></div></body>"),
            etree.XML("<div><list/></div>"),
            etree.XML("<body><list/><div/></body>"),
            etree.XML("<div><div><list/></div></div>"),
            etree.XML(
                "<div><list><item>some text</item><item>more text</item></list></div>"
            ),
            etree.XML("<body><div><list><item/></list></div><div><list/></div></body>"),
            etree.XML("<text><body><div><list/><p/><list/></div></body></text>"),
            etree.XML(
                """<div>
                        <div><p>text</p></div>
                        <div><list><item/></list></div>
                        <div><div><list/></div></div>
                        </div>"""
            ),
            etree.XML(
                """
                            <TEI>
                            <teiHeader/>
                            <text>
                            <body>
                              <div type="entry">
                                <div>
                                  <list/>
                                </div>
                                </div>
                            </body></text>
                            </TEI>"""
            ),
            etree.XML(
                """
                            <TEI xmlns='namespace'>
                            <teiHeader/>
                            <text>
                            <body>
                              <div>
                                <fw rend="h1" type="header">heading </fw>
                                <div>
                                  <p>text</p>
                                  <list><item/></list>
                                </div>
                                <div>
                                 <list/>
                                </div>
                                </div>
                            </body></text>
                            </TEI>
                            """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_new_div_added_as_parent(self):
        root = etree.XML("<body><div/><table/></body>")
        node = root[1]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div", "div", "table"])
        self.assertTrue(root.find(".//div/table") is not None)

    def test_new_div_added_as_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><body><div/><table/></body></TEI>")
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "body", "div", "div", "table"])

    def test_new_div_added_as_parent_for_complex_element(self):
        root = etree.XML(
            """<body>
                <div><p>text</p></div>
                <table>
                  <row>
                    <cell>text</cell>
                  </row>
                </table>
               </body>"""
        )
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//div/table") is not None)

    def test_new_div_added_as_parent_of_list_with_children(self):
        root = etree.XML(
            """<TEI><teiHeader/>
                <text><body><div>
                <div/><list><item>text</item><item/></list>
                </div></body></text></TEI>"""
        )
        target_node = root.find(".//{*}list")
        self.observer.transform_node(target_node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(
            result,
            [
                "TEI",
                "teiHeader",
                "text",
                "body",
                "div",
                "div",
                "div",
                "list",
                "item",
                "item",
            ],
        )

    def test_new_div_added_as_parent_of_complex_element_with_namepace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <body>
                <div><p>text</p></div>
                <table>
                  <row>
                    <cell>text</cell>
                  </row>
                </table>
               </body>
            </TEI>"""
        )
        node = root.find(".//{*}table")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}div/{*}table") is not None)

    def test_new_div_added_as_parent_of_namespaced_list_with_children(self):
        root = etree.XML(
            """<TEI xmlns='namespace'><teiHeader/>
                <text><body>
                <div>
                <div/>
                <list><item>text</item><item/></list>
                </div></body></text></TEI>"""
        )
        target_node = root.find(".//{*}list")
        self.observer.transform_node(target_node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(
            result,
            [
                "TEI",
                "teiHeader",
                "text",
                "body",
                "div",
                "div",
                "div",
                "list",
                "item",
                "item",
            ],
        )

    def test_order_of_element_correct_when_multiple_divs_added(self):
        root = etree.XML(
            """<body>
                <div><p>text</p></div>
                <table>
                  <row>
                    <cell>text</cell>
                  </row>
                </table>
                <p/>
                <quote>text</quote>
                <div><list/></div>
               </body>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root]
        self.assertEqual(
            result,
            [
                ("div", ["p"]),
                ("div", ["table"]),
                ("p", []),
                ("div", ["quote"]),
                ("div", ["list"]),
            ],
        )

    def test_new_div_added_for_element_that_is_not_direct_sibling_of_div(self):
        root = etree.XML(
            """<body>
                <div><p>text</p></div>
                <fw>text</fw>
                <table>
                  <row>
                    <cell>text</cell>
                  </row>
                </table>
               </body>"""
        )
        node = root.find(".//table")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//div/table") is not None)

    def test_new_div_inserted_at_correct_index(self):
        root = etree.XML(
            """
            <body>
              <div><p>text</p></div>
              <div/>
              <div/>
              <div/>
              <div/>
              <quote>text</quote>
              <div/>
            </body>
            """
        )
        node = root.find(".//quote")
        expected = node.getparent().index(node)
        self.observer.transform_node(node)
        new_div = root.find(".//div/quote").getparent()
        result = root.index(new_div)
        self.assertEqual(result, expected)

    def test_multiple_adjacent_elements_added_to_same_div(self):
        root = etree.XML(
            """
            <body>
              <p>text</p>
              <div>
                <p>text2</p>
              </div>
              <quote>text3</quote>
              <table>
                <row>
                  <cell>text4</cell>
                </row>
              </table>
            </body>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        quote_elem = root.find(".//div/quote")
        table_elem = root.find(".//div/table")
        self.assertEqual(quote_elem.getparent(), table_elem.getparent())

    def test_multiple_adjacent_elements_added_to_same_div_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
            <body>
              <p>text</p>
              <div>
                <p>text2</p>
              </div>
              <quote>text3</quote>
              <table>
                <row>
                  <cell>text4</cell>
                </row>
              </table>
              <div>
                <p>text5</p>
              </div>
              <table/>
            </body>
            </TEI>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        quote_elem = root.find(".//{*}div/{*}quote")
        table_elem = root.find(".//{*}div/{*}table")
        self.assertEqual(quote_elem.getparent(), table_elem.getparent())
        self.assertTrue(len(table_elem.getparent()), 2)

    def test_multiple_div_added_if_target_elements_not_adjacent(self):
        root = etree.XML(
            """
            <body>
              <p>text</p>
              <div>
                <p>text2</p>
              </div>
              <quote>text3</quote>
              <div/>
              <table>
                <row>
                  <cell>text4</cell>
                </row>
              </table>
              <div>
                <p>text5</p>
              </div>
              <div/>
              <table/>
            </body>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root]
        self.assertEqual(
            result,
            [
                ("p", []),
                ("div", ["p"]),
                ("div", ["quote"]),
                ("div", []),
                ("div", ["table"]),
                ("div", ["p"]),
                ("div", []),
                ("div", ["table"]),
            ],
        )

    def test_new_div_added_during_iteration(self):
        root = etree.XML(
            """<TEI xmlns='namespace'><teiHeader/>
                        <text><body>
                        <div>
                        <div/>
                        <list><item>text</item><item/></list>
                        </div></body></text></TEI>"""
        )
        for target_node in root.iter():
            if self.observer.observe(target_node):
                self.observer.transform_node(target_node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(
            result,
            [
                "TEI",
                "teiHeader",
                "text",
                "body",
                "div",
                "div",
                "div",
                "list",
                "item",
                "item",
            ],
        )

    def test_new_div_added_for_list_if_older_sibling_not_only_div(self):
        root = etree.XML(
            """<TEI><teiHeader/>
                <text><body><div>
                <p/>
                <div/>
                <list><item>text</item><item/></list>
                <div/>
                </div></body></text></TEI>"""
        )
        for target_node in root.iter():
            if self.observer.observe(target_node):
                self.observer.transform_node(target_node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(
            result,
            [
                "TEI",
                "teiHeader",
                "text",
                "body",
                "div",
                "p",
                "div",
                "div",
                "list",
                "item",
                "item",
                "div",
            ],
        )
