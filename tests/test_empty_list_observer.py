import unittest

from lxml import etree

from tei_transform.observer import EmptyListObserver


class EmptyListObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyListObserver()

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
            etree.XML("<div><p>text<table/>more text</p></div>"),
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
