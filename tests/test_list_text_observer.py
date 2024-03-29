import unittest

from lxml import etree

from tei_transform.observer import ListTextObserver


class ListTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = ListTextObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<div><list>text<item/></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<div><list><item>text</item></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<list>text</list>"),
            etree.XML("<list>text<item>text</item></list>"),
            etree.XML("<list><item/>text</list>"),
            etree.XML("<list><item/><item/>text</list>"),
            etree.XML("<div><p/><list><item/>text</list></div>"),
            etree.XML("<div><p/><list>text<item/>text</list><p/></div>"),
            etree.XML("<div><list><item><list>text</list></item></list></div>"),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>text</item>
                        text2
                        <item>text3</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        text
                        <item>text</item>
                        text2
                        <item>text3</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>
                          <list>text
                            <item/>
                            <item/>
                          </list>
                        </item>
                        <item>text3</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <table>
                        <row>
                          <cell>
                            <list>text
                              <item/>
                              <item/>
                            </list>
                          </cell>
                        </row>
                      </table>
                      <p>text</p>
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

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<list/>"),
            etree.XML("<list><item/></list>"),
            etree.XML("<list><item>text</item></list>"),
            etree.XML("<list><item/><item/><item/></list>"),
            etree.XML("<div><p>text<list><item/></list></p></div>"),
            etree.XML("<div><list><item/></list><p>text</p></div>"),
            etree.XML("<div><p/><list><item>text</item></list><p>text</p></div>"),
            etree.XML(
                """
                <list>
                  <item>text</item>
                  <item/>
                </list>
                """
            ),
            etree.XML("<list>   <item/></list>"),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>text</item>
                        <item>text</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>
                          <list>
                            <item>text</item>
                            <item/>
                          </list>
                        </item>
                        <item>text</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text
                      <list>
                        <item>text</item>
                        <item>text2</item>
                      </list>
                      <list>
                        <item>text</item>
                      </list>
                      text</p>
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

    def test_text_in_list_removed(self):
        node = etree.XML("<list>text</list>")
        self.observer.transform_node(node)
        self.assertEqual(node.text, None)

    def test_tail_on_item_removed(self):
        node = etree.XML("<list><item/>tail</list>")
        self.observer.transform_node(node)
        self.assertEqual(node[0].tail, None)

    def test_new_item_child_added_for_text_content(self):
        node = etree.XML("<list>text</list>")
        self.observer.transform_node(node)
        result = node.find(".//item").text
        self.assertEqual(result, "text")

    def test_tail_content_appended_to_item_content(self):
        node = etree.XML("<list><item/>tail</list>")
        self.observer.transform_node(node)
        result = node.find("item").text
        self.assertEqual(result, "tail")

    def test_text_in_nested_list_removed(self):
        root = etree.XML(
            "<div><list><item><list>text<item/></list></item></list></div>"
        )
        node = root.find(".//list//list")
        self.observer.transform_node(node)
        result = root.find(".//list//list").text
        self.assertEqual(result, None)

    def test_tail_on_item_in_nested_list_removed(self):
        root = etree.XML(
            "<div><list><item><list><item/>tail</list></item></list></div>"
        )
        node = root.find(".//list//list")
        self.observer.transform_node(node)
        result = root.find(".//list//list/item")
        self.assertEqual(result.tail, None)
        self.assertEqual(result.text, "tail")

    def test_text_in_list_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <list>text
                  <item>text</item>
                </list>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}list")
        self.observer.transform_node(node)
        self.assertEqual(node.text, None)

    def test_tail_on_item_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <list>
                  <item/>tail
                </list>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}list")
        self.observer.transform_node(node)
        self.assertEqual(node[0].tail, None)
        self.assertEqual(node[0].text, "tail")

    def test_text_in_nested_list_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <list>
                  <item>
                    <list>text
                      <item/>
                    </list>
                  </item>
                </list>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}list//{*}list")
        self.observer.transform_node(node)
        self.assertEqual(node.text, None)
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <list>
                  <item>
                    <list>text
                      <item>text
                      </item>
                      <item/>
                    </list>
                  </item>
                </list>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}list//{*}list")
        self.observer.transform_node(node)
        self.assertEqual(node.text, None)

    def test_tail_on_item_in_nested_list_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <p>text</p>
                <list>
                  <item>
                    <list>
                      <item>text</item>tail
                    </list>
                  </item>
                </list>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}list//{*}list")
        self.observer.transform_node(node)
        self.assertEqual(node[0].tail, None)

    def test_multiple_tails_on_items_removed(self):
        root = etree.XML(
            """
            <div>
              <list>
                <item/>tail1
                <item/>tail2
                <item/>tail3
                <item>text</item>
              </list>
            </div>
             """
        )
        self.observer.transform_node(root[0])
        self.assertEqual(
            any(
                [
                    True if node.tail is not None and node.tail.strip() else False
                    for node in root[0]
                ]
            ),
            False,
        )

    def test_multiple_list_siblings_transformed(self):
        root = etree.XML(
            """
            <div>
              <list>text</list>
              <list>text
                <item/>tail
              </list>
              <list>
                <item/>
              </list>
              <list>
                <item>
                  <list>text
                    <item/>tail
                    <item>text</item>tail
                  </list>
                </item>
              </list>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [
            node.text
            for node in root.findall(".//list")
            if node.text is not None and node.text.strip()
        ]
        result += [
            node.tail
            for node in root.findall(".//item")
            if node.tail is not None and node.tail.strip()
        ]
        self.assertEqual(result, [])

    def test_namespace_for_new_item_set_correctly(self):
        root = etree.XML("<TEI xmlns='test'><list>text</list></TEI>")
        node = root[0]
        self.observer.transform_node(node)
        result = root.find(".//{*}item").tag
        self.assertEqual(result, "{test}item")

    def test_order_of_text_parts_correct_after_transformation(self):
        root = etree.XML(
            """
            <div>
              <list>text1
                <item>text2</item>text3
                <item/>text4
                <item>text5</item>text6
                <item/>text7
                <item>text8</item>
              </list>
            </div>
            """
        )
        node = root[0]
        self.observer.transform_node(node)
        result = [node.text for node in root[0]]
        self.assertEqual(
            result,
            [
                "text1",
                "text2 text3",
                "text4",
                "text5 text6",
                "text7",
                "text8",
            ],
        )

    def test_only_tail_on_item_children_removed(self):
        node = etree.XML("<list><item/>tail<item><p/>tail2</item><item/>tail3</list>")
        self.observer.transform_node(node)
        self.assertEqual(node.find(".//p").tail, "tail2")

    def test_only_tail_on_direct_item_children_removed(self):
        root = etree.XML(
            """
            <div>
              <list>
                <item/>tail1
                <item>
                  <list>
                    <item/>tail2
                  </list>
                </item>
              </list>
            </div>
            """
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue("tail2" in root.find(".//list//list/item").tail)

    def test_tail_of_item_concatenated_with_tail_of_last_subchild(self):
        root = etree.XML("<list><item><p>text</p></item>tail</list>")
        self.observer.transform_node(root)
        self.assertEqual(root.find(".//p").tail, "tail")

    def test_tail_of_item_concatenated_with_text_content(self):
        root = etree.XML("<list><item>text</item>tail</list>")
        self.observer.transform_node(root)
        self.assertEqual(root[0].text, "text tail")

    def test_lb_child_added_to_previous_sibling_with_only_text(self):
        root = etree.XML("<div><list>text<lb/>tail</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//item/lb") is not None)

    def test_lb_child_added_to_previous_sibling_with_previous_sibling(self):
        root = etree.XML("<div><list><item>text</item><lb/>tail</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//item")[0].tag, "lb")

    def test_lb_child_added_to_previous_sibling_with_following_sibling(self):
        root = etree.XML("<div><list>text<lb/>tail<item>text2</item>tail</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//item")), 2)
        self.assertEqual(root.find(".//item")[0].tag, "lb")

    def test_adding_lb_to_sibling_with_child(self):
        root = etree.XML("<div><list><item><p>text</p></item><lb/>tail</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = [child.tag for child in root.find(".//item")]
        self.assertEqual(result, ["p", "lb"])

    def test_adding_lb_to_sibling_with_child_and_tail(self):
        root = etree.XML("<div><list><item>text</item>tail1<lb/>tail2</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        target = root.find(".//item")
        self.assertEqual(target.text, "text tail1")
        self.assertEqual(target[0].tag, "lb")
        self.assertEqual(target[0].tail, "tail2")

    def test_lb_as_first_child_with_only_whitespace_text_before(self):
        root = etree.XML("<div><list>    \n<lb/>tail</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//list/lb"))

    def test_tail_removed_if_lb_converted_to_item(self):
        root = etree.XML("<div><list>    \n<lb/>tail<item/></list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertIsNone(node[0].tail)

    def test_tail_added_as_text_if_lb_converted_to_item(self):
        root = etree.XML("<div><list>    \n<lb/>tail</list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node[0].text, "tail")

    def test_lb_without_tail_not_converted_to_item(self):
        root = etree.XML("<div><list><item/><lb/><item/></list></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/lb") is not None)

    def test_tail_only_on_valid_children_removed(self):
        root = etree.XML(
            """
            <div>
                <list>
                    <head>text</head>tail
                    <item/>tail
                    <p>text1</p>tail1
                    <fw>text2</fw>tail2
                    <item>text3</item>tail3
                </list>
            </div>
            """
        )
        node = root[0]
        self.observer.transform_node(node)
        result = [
            (child.tag, child.tail.strip())
            for child in node
            if child.tail is not None and child.tail.strip()
        ]
        self.assertEqual(result, [("p", "tail1")])
