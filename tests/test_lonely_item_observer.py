import unittest

from lxml import etree

from tei_transform.observer import LonelyItemObserver


class LonelyItemObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelyItemObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><item/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<list><item/></list>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p><item>text</item></p>"),
            etree.XML("<ab><item/>tail</ab>"),
            etree.XML("<div><item><list><item/></list></item></div>"),
            etree.XML("<p>text<item/>tail</p>"),
            etree.XML("<div><p>text<item>text</item></p></div>"),
            etree.XML("<p><item><item/></item></p>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <p>text
                      <hi>text</hi>
                      <item>text</item>
                    </p>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <item>
                      <list>
                        <item>text</item>
                        <item>text</item>
                      </list>
                    </item>
                    <p/>
                    <ab/>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <p/>
                    <table>
                      <row>
                        <cell>
                          <item>text</item>
                        </cell>
                      </row>
                    </table>
                    <ab/>
                    <list>
                      <item>text</item>
                    </list>
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
            etree.XML("<list><item>text</item></list>"),
            etree.XML("<list><item>text</item><item/><item/></list>"),
            etree.XML("<div><list><item/></list></div>"),
            etree.XML("<p><list><item>text<list/></item></list></p>"),
            etree.XML(
                "<p><list><item>text<list><item>text</item><item/></list></item></list></p>"
            ),
            etree.XML("<p><list>text<item/>tail</list></p>"),
            etree.XML("<div><p/><list><item rend='ol'>text</item></list></div>"),
            etree.XML("<div><list attr='val'><item>text<table/></item></list></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <head>text</head>
                      <list attr='val'>
                        <item>text</item>
                        <item>text</item>
                        <item>text</item>
                      </list>
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
                      <list attr='val'>
                        <item>text</item>
                        <item>text</item>
                        <item>
                          <list>
                            <item/>
                            <item/>
                          </list>
                        </item>
                      </list>
                      <p>text</p>
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

    def test_list_added_as_parent(self):
        root = etree.XML("<p><item>text</item></p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/item") is not None)

    def test_list_added_as_parent_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><p><item>text</item></p></div></TEI>")
        node = root.find(".//{*}item")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}list/{*}item") is not None)

    def test_empty_item_removed(self):
        root = etree.XML("<p>text<item/></p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_empty_item_with_tail_not_removed(self):
        root = etree.XML("<p><item/>tail</p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/item") is not None)

    def test_empty_item_with_text_not_removed(self):
        root = etree.XML("<p><item>text</item></p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/item") is not None)

    def test_empty_item_with_only_whitespace_text_removed(self):
        root = etree.XML("<div><item>   \n\n</item></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//item") is None)

    def test_empty_item_with_only_whitespace_tail_removed(self):
        root = etree.XML("<ab><item/>\n   \n </ab>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//item") is None)

    def test_attributes_of_item_preserved_after_transformation(self):
        root = etree.XML("<div><item rend='val'>text</item><p/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list/item").attrib, {"rend": "val"})

    def test_attributes_of_item_preserved_after_transformation_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><item rend='val'>text</item><p/></div></TEI>"
        )
        node = root.find(".//{*}item")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}list/{*}item").attrib, {"rend": "val"})

    def test_children_preserved_after_transformation(self):
        root = etree.XML(
            """
            <div>
              <p>text</p>
              <item>
                <head>text</head>
                <list>
                  <item>text</item>
                  <item><p>ab</p></item>
                  <item><hi>cd</hi></item>
                </list>
              </item>
            </div>
            """
        )
        node = root.find(".//item")
        self.observer.transform_node(node)
        result = [node.tag for node in root.find(".//list/item").iter()]
        self.assertEqual(
            result, ["item", "head", "list", "item", "item", "p", "item", "hi"]
        )

    def test_multiple_adjacent_items_added_to_same_list_element(self):
        root = etree.XML(
            """
            <div>
              <item>ab</item>
              <item>cd</item>
              <item>ef</item>
              <item>gh</item>
              <item>ij</item>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [len(root), len(root[0])]
        self.assertEqual(result, [1, 5])

    def test_multiple_adjacent_items_added_to_same_list_element_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <teiHeader/>
              <text>
                <body>
                  <div>
                  <p>text</p>
                  <item>text</item>
                  <item>ab</item>
                  <item>cd</item>
                  </div>
                </body>
              </text>
            </TEI>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [len(root.find(".//{*}div")), len(root.find(".//{*}list"))]
        self.assertEqual(result, [2, 3])

    def test_transformation_only_applied_to_outer_item_if_nested(self):
        root = etree.XML(
            """
            <div>
              <item>
                <item>text</item>
              </item>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertTrue(root.find(".//list/item/item") is not None)

    def test_non_item_siblings_not_added_to_list_parent(self):
        root = etree.XML(
            """
            <div>
              <p>text</p>
              <item>ab</item>
              <item>cd</item>
              <p>text</p>
              <item>ef</item>
              <item/>
              <p>text</p>
              <item>gh</item>
              <item>ij</item>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        list_elements = root.findall(".//list")
        result = [len(list_elements), [len(elem) for elem in list_elements]]
        self.assertEqual(result, [3, [2, 1, 2]])

    def test_tail_from_item_removed(self):
        root = etree.XML("<div><item/>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list/item").tail, None)

    def test_tail_from_item_added_to_text_context(self):
        root = etree.XML("<div><item>text</item>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list/item").text, "text tail")

    def test_tail_added_as_text_if_item_empty(self):
        root = etree.XML("<div><item/>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list/item").text, "tail")

    def test_tail_added_to_tail_of_last_child_of_item(self):
        root = etree.XML("<p><item><table/>old tail</item>tail</p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//table").tail, "old tail tail")

    def test_tail_of_item_added_as_tail_of_last_child_if_none(self):
        root = etree.XML("<div><item><p>text</p></item>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p").tail, "tail")

    def test_tail_of_item_only_added_to_last_child(self):
        root = etree.XML("<div><item><p>text</p>text<p>text</p></item>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        result = [node.tail for node in root.find(".//list/item")]
        self.assertEqual(result, ["text", "tail"])
