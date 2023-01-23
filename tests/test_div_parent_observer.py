import unittest

from lxml import etree

from tei_transform.observer import DivParentObserver


class DivParentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><div/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><div/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<quote><div/></quote>"),
            etree.XML("<code><div/></code>"),
            etree.XML("<p><div><p>text</p></div></p>"),
            etree.XML("<table><row><cell><div/></cell></row></table>"),
            etree.XML("<p>text<div>text</div>text</p>"),
            etree.XML("<p><quote><div><p>text</p></div></quote></p>"),
            etree.XML("<div><table><row><cell>text<div/></cell></row></table></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                       <p>text</p>
                       <quote>
                         <div>
                           <p>text</p>
                         </div>
                        </quote>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <div>
                         <table>
                           <row>
                            <cell>
                              <div>
                                <p>text</p>
                              </div>
                            </cell>
                          </row>
                         </table>
                        </div>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <list>
                          <item>
                            <div/>
                          </item>
                        </list>
                        <p/>
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

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p/><div/></div>"),
            etree.XML("<app><lem><div/></lem></app>"),
            etree.XML("<cell><app><rdg><div><p>text</p></div></rdg></app></cell>"),
            etree.XML("<text><back><div/></back></text>"),
            etree.XML("<text><front><div/></front></text>"),
            etree.XML(
                "<div><p><floatingText><body><div/></body></floatingText></p></div>"
            ),
            etree.XML("<div><quote><p/></quote><div><p>text</p></div></div>"),
            etree.XML(
                """<body>
                    <div>
                        <table>
                            <row>
                                <cell>
                                    <floatingText>
                                        <body><div/></body>
                                    </floatingText>
                                </cell>
                            </row>
                        </table>
                    </div>
                  </body>"""
            ),
            etree.XML("<body><div><p/><div><p>text</p></div></div></body>"),
            etree.XML("<body><div><quote/><p/><div><table/></div></div></body>"),
            etree.XML(
                "<body><p><floatingText><body><div><p/></div></body></floatingText></p></body>"
            ),
            etree.XML("<div><list/><div><p/><div><p/></div></div></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <div>
                          <p/>
                        </div>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                          <floatingText>
                            <body>
                              <div>
                                <p>text</p>
                              </div>
                            </body>
                          </floatingText>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                          <floatingText>
                            <body>
                              <div>
                                <p>text</p>
                              </div>
                            </body>
                          </floatingText>
                        </p>
                        <div>
                          <p>text</p>
                          <table>
                            <row>
                              <cell>
                                <p>text
                                </p>
                              </cell>
                            </row>
                          </table>
                        </div>
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

    def test_div_added_as_sibling_if_parent_plike(self):
        for parent_tag in ["p", "ab"]:
            root = etree.XML(f"<div><{parent_tag}><div><p/></div></{parent_tag}></div>")
            node = root[0][0]
            self.observer.transform_node(node)
            with self.subTest():
                self.assertEqual(len(root), 2)

    def test_div_tags_removed_if_parent_tag_not_plike(self):
        tags = ["quote", "cell", "item", "fw"]
        for parent_tag in tags:
            root = etree.XML(f"<{parent_tag}><div><p/></div></{parent_tag}>")
            node = root[0]
            self.observer.transform_node(node)
            with self.subTest():
                self.assertEqual(root[0].tag, "p")

    def test_div_added_as_sibling_if_parent_plike_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><p><div><list/></div></p></TEI>")
        node = root.find(".//{*}div")
        self.observer.transform_node(node)
        self.assertEqual(len(root), 2)

    def test_div_tags_removed_if_parent_tag_not_plike_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><list><item><div><p>text</p></div></item></list></TEI>"
        )
        node = root.find(".//{*}div")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}item")[0].tag, "{a}p")

    def test_empty_div_removed(self):
        root = etree.XML("<item><div/></item>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_empty_div_removed_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><body><p><div/></p></body></TEI>")
        node = root.find(".//{*}div")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}div") is None)

    def test_text_of_div_without_children_not_removed(self):
        root = etree.XML("<tag><div>text</div></tag>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue("text" in root.text)

    def test_tail_of_div_without_children_not_removed(self):
        root = etree.XML("<tag><div/>tail</tag>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue("tail" in root.text)

    def test_children_preserved_after_transformation(self):
        root = etree.XML("<item><div><div><p>text</p><list/></div></div></item>")
        node = root[0]
        self.observer.transform_node(node)
        result = [node.tag for node in root.find(".//div").iter()]
        self.assertEqual(result, ["div", "p", "list"])

    def test_div_added_as_sibling_with_previous_sibling(self):
        root = etree.XML("<div><p><hi>text</hi><div><p/></div></p></div>")
        node = root.find(".//p/div")
        self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root]
        self.assertEqual(result, [("p", ["hi"]), ("div", ["p"])])

    def test_div_added_as_sibling_with_following_sibling(self):
        root = etree.XML("<div><p><div><list/></div><hi/></p></div>")
        node = root.find(".//p/div")
        self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root]
        self.assertEqual(result, [("p", []), ("div", ["list"]), ("div", ["p"])])

    def test_div_tag_removed_with_previous_sibling(self):
        root = etree.XML("<cell><p/><div><p/></div></cell>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//div") is None)

    def test_div_tag_removed_with_following_sibling(self):
        root = etree.XML("<item><div><p/></div><ab/></item>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//div") is None)

    def test_multiple_div_elements_with_different_parents_transformed(self):
        root = etree.XML(
            """
            <body>
              <div>
                <p>
                  <div>
                    <p>text0</p>
                  </div>
                </p>
                <p>text1
                  <div/>
                </p>
                <p>text2
                  <div/>tail
                </p>
                <list>
                  <item>
                    <div>
                      <p>text3</p>
                      <div>
                        <list/>
                      </div>
                    </div>
                  </item>
                </list>
                <p>text4</p>
                <table>
                  <row>
                    <cell>
                      <div>
                        <p>text5</p>
                      </div>
                    </cell>
                  </row>
                </table>
                <someTag>
                  <div>
                    <p>text6</p>
                  </div>
                </someTag>
                <p>
                  <hi>text7</hi>
                  <div>
                    <p>text8</p>
                  </div>
                  <hi>text9</hi>
                </p>
                <p>
                  <div>
                    <p>
                      <floatingText>
                        <body>
                          <div>
                            <p>text10</p>
                          </div>
                        </body>
                      </floatingText>
                    </p>
                  </div>
                </p>
              </div>
            </body>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [
            (node.tag, [child.tag for child in node.iterdescendants()])
            for node in root[0]
        ]
        expected = [
            ("p", []),
            ("div", ["p"]),
            ("p", []),
            ("p", []),
            ("list", ["item", "p", "list"]),
            ("p", []),
            ("table", ["row", "cell", "p"]),
            ("someTag", ["p"]),
            ("p", ["hi"]),
            ("div", ["p"]),
            ("div", ["p", "hi"]),
            ("p", []),
            ("div", ["p", "floatingText", "body", "div", "p"]),
        ]
        self.assertEqual(result, expected)

    def test_div_with_p_parent_and_older_siblings_that_shouldnt_be_in_div(self):
        root = etree.XML(
            """
            <div>
              <p>text
                <hi>text</hi>tail
                <code>abc</code>
                <div>
                  <p>text</p>
                </div>
              </p>
            </div>
            """
        )
        node = root.find(".//p/div")
        self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root]
        self.assertEqual(
            result,
            [("p", ["hi", "code"]), ("div", ["p"])],
        )

    def test_div_with_p_parent_and_following_siblings_that_shouldnt_be_in_div(self):
        root = etree.XML(
            """
            <div>
              <ab>text
                <div>
                  <p>text</p>
                </div>
                <hi>text</hi>tail
                <code>abc</code>
              </ab>
            </div>
            """
        )
        node = root.find(".//ab/div")
        self.observer.transform_node(node)
        result = [
            (node.tag, [child.tag for child in node.iterdescendants()]) for node in root
        ]
        self.assertEqual(
            result,
            [("ab", []), ("div", ["p"]), ("div", ["ab", "hi", "code"])],
        )

    def test_tail_of_div_added_to_new_p_with_plike_parent_if_div_with_child(self):
        root = etree.XML("<div><p><div><p/></div>tail</p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        result = root.findall(".//p")[2].text
        self.assertTrue(result, "tail")

    def test_tail_of_div_added_to_plike_parent_if_div_without_children(self):
        root = etree.XML("<div><p><div/>tail</p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue("tail" in root[0].text)

    def test_text_of_div_added_to_plike_parent_if_div_without_children(self):
        root = etree.XML("<div><p><div>text</div></p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue("text" in root[0].text)
