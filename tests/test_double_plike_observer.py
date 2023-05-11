import unittest

from lxml import etree

from tei_transform.observer import DoublePlikeObserver


class DoublePlikeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DoublePlikeObserver()
        self.valid_cfg = {"action": "add-lb"}

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p><p>text</p></p></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><quote><p>text</p></quote></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><p><p/></p></div>"),
            etree.XML("<div><ab><p/></ab></div>"),
            etree.XML("<div><p><ab/></p></div>"),
            etree.XML("<div><ab><ab/></ab></div>"),
            etree.XML("<div><p>text<list/><p>text</p></p></div>"),
            etree.XML("<div><p>text<table/><p>text</p><table/></p></div>"),
            etree.XML("<div><p>text<list/><ab>text</ab></p></div>"),
            etree.XML("<div><p>text<list/><ab><hi>text</hi></ab></p></div>"),
            etree.XML("<div><ab>text<quote/><p>text</p></ab></div>"),
            etree.XML("<div><ab>text<list/><p>text</p><quote/></ab></div>"),
            etree.XML(
                "<table><row><cell><p>text</p><p><ab>text</ab></p></cell></row></table>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><p><ab>text</ab>text<list/></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><p><p><hi>text</hi></p>text<list/></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab><ab>text<list/></ab>text</ab></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab>ab<p>text<list/>c</p>text</ab></div></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                  <div>
                    <p>text</p>
                    <ab>text<p>
                      <table>
                        <row>
                          <cell/>
                        </row>
                      </table>
                      </p>
                    </ab>
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
            etree.XML("<p><quote><ab>text</ab></quote></p>"),
            etree.XML("<div><p/><p>text<fw><p>text</p></fw></p></div>"),
            etree.XML(
                "<div><ab>text<table><row><cell><p/></cell></row></table></ab></div>"
            ),
            etree.XML("<div><p/><ab/><p/></div>"),
            etree.XML("<div><ab><list><item><p>text</p></item></list></ab></div>"),
            etree.XML("<div><ab>text<quote>text<ab/>tail</quote></ab></div>"),
            etree.XML("<div><p><hi/></p><ab/></div>"),
            etree.XML(
                "<TEI xmlns='ns'><div><p>text<quote><ab/></quote></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab><list><p>text</p></list></ab></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab>text</ab><p>text<fw/>tail</p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_inner_element_removed(self):
        root = etree.XML("<div><p><p/></p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p/p") is None)

    def test_text_of_inner_node_not_deleted(self):
        root = etree.XML("<div><ab>text1<p>text2</p></ab></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue("text2" in root[0].text)

    def test_text_parts_separated_by_whitespace_after_concatenation(self):
        root = etree.XML("<div><p>text1<ab>text2</ab>text3</p></div>")
        node = root.find(".//ab")
        self.observer.transform_node(node)
        self.assertEqual(root[0].text, "text1 text2 text3")

    def test_formatting_whitespace_removed_after_concatenation(self):
        root = etree.XML(
            """
            <div>
              <p>text1
                <ab>text2</ab>text3
                <p>text4</p>text5
                <p>
                  <ab>
                    <p>text6</p>
                  </ab>
                </p>
              </p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(root[0].text, "text1 text2 text3 text4 text5 text6")

    def test_tail_of_inner_element_not_deleted(self):
        root = etree.XML("<div><p><p>text</p>tail</p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue("tail" in root[0].text)

    def test_children_of_inner_element_not_deleted(self):
        root = etree.XML("<div><p>text<ab>text<list/><table/><fw/></ab></p></div>")
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p/list") is not None)
        self.assertEqual(len(root[0]), 3)

    def test_inner_plike_removed_with_allowed_siblings(self):
        root = etree.XML("<div><p>text<list/>tail<ab>text2</ab>tail2<table/></p></div>")
        node = root.find(".//ab")
        self.observer.transform_node(node)
        result = [(node.tag, node.text, node.tail) for node in root[0].iter()]
        self.assertEqual(
            result,
            [
                ("p", "text", None),
                ("list", None, "tail text2 tail2"),
                ("table", None, None),
            ],
        )

    def test_order_of_text_and_siblings_of_inner_element(self):
        root = etree.XML(
            "<div><p>text1<ab>text2<hi/>tail1<list/><table/></ab>tail2</p></div>"
        )
        node = root[0][0]
        self.observer.transform_node(node)
        result = [(node.tag, node.text, node.tail) for node in root[0].iter()]
        self.assertEqual(
            result,
            [
                ("p", "text1 text2", None),
                ("hi", None, "tail1"),
                ("list", None, None),
                ("table", None, "tail2"),
            ],
        )

    def test_inner_element_removed_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><p>text<ab>text2</ab></p></div></TEI>")
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}ab") is None)

    def test_text_of_inner_node_not_deleted_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><p>text<ab>text2</ab></p></div></TEI>")
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue("text2" in root.find(".//{*}p").text)

    def test_tail_of_inner_element_not_deleted_with_namespace(self):
        root = etree.XML("<TEI xmlns='ns'><div><p>text<ab/>tail</p></div></TEI>")
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue("tail" in root.find(".//{*}p").text)

    def test_children_of_inner_element_not_deleted_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='ns'>
              <div>
                <p>text
                  <ab>
                    <list>
                      <item>item</item>
                    </list>
                  </ab>
                </p>
              </div>
            </TEI>
            """
        )
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}p//{*}list") is not None)

    def test_removal_of_multiple_inner_elements(self):
        root = etree.XML(
            """
            <div>
              <ab>
                <ab>
                  <seg>text</seg>
                </ab>
                <p>
                  <list>
                    <item>text</item>
                  </list>
                </p>tail1
                <p>text</p>tail2
              </ab>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in root[0].iter()]
        self.assertEqual(result, ["ab", "seg", "list", "item"])

    def test_multiple_nested_plike_elements_resolved(self):
        root = etree.XML(
            """
            <div>
              <p>text1
                <ab>text2
                  <p>text3</p>
                  <ab>
                    <p>text4</p>
                  </ab>
                </ab>
                <ab>
                  <p>text5
                    <p>text6
                      <p>text7</p>
                    </p>
                  </p>
                </ab>
              </p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root[0]), 0)

    def test_valid_nested_plike_element_not_removed(self):
        root = etree.XML(
            """
            <div>
              <p>
                <ab>text</ab>
                <list>
                  <item>
                    <p>text1</p>
                    <ab>text2</ab>
                  </item>
                </list>
                <p>text3</p>
              </p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root.find(".//item")), 2)

    def test_text_of_removed_element_added_as_tail_of_previous_sibling(self):
        root = etree.XML("<div><p><list/><ab>text</ab></p></div>")
        node = root[0][1]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list").tail, "text")

    def test_tail_of_removed_element_added_as_tail_of_previous_sibling(self):
        root = etree.XML("<div><p><list/><ab/>tail</p></div>")
        node = root[0][1]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list").tail, "tail")

    def test_tail_of_removed_element_added_as_tail_of_last_child(self):
        root = etree.XML("<div><ab><list/><p><hi>text</hi></p>tail</ab></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//hi").tail, "tail")

    def test_text_of_removed_element_added_as_tail_of_prev_sibling_with_children(self):
        root = etree.XML("<div><ab><list/><p>text<hi>text2</hi></p></ab></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//list").tail, "text")

    def test_configure_observer(self):
        config = {"action": "add-lb"}
        self.observer.configure(config)
        self.assertTrue(self.observer._add_lb)

    def test_observer_not_configured_if_config_wrong(self):
        config = {"do_sth": "add.lb"}
        self.observer.configure(config)
        self.assertEqual(self.observer._add_lb, False)

    def test_invalid_config_triggers_log_warning(self):
        configs = [{"do_sth": "add.lb"}, {"action": "do-sth"}]
        for config in configs:
            with self.subTest():
                with self.assertLogs() as logger:
                    self.observer.configure(config)
                    self.assertEqual(
                        logger.output,
                        [
                            "WARNING:tei_transform.observer.double_plike_observer:"
                            "Invalid configuration, using default."
                        ],
                    )

    def test_lb_added_to_separate_text_parts_if_configured(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML("<div><p>text<ab>text2</ab></p></div>")
        node = root.find(".//ab")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//lb").tail, "text2")

    def test_lb_added_with_namespace(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML("<TEI xmlns='a'><div><p>text<ab/>tail</p></div></TEI>")
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}lb") is not None)

    def test_no_lb_added_if_inner_elem_empty(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML("<div><p>text<ab/></p></div>")
        node = root.find(".//ab")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//lb"))

    def test_no_lb_added_if_parent_contains_no_text(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML("<div><p><ab/>tail</p></div>")
        node = root.find(".//ab")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//lb"))

    def test_no_lb_added_if_inner_elem_contains_children_but_no_text(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML("<div><ab>text<p><hi>text2</hi></p></ab></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//lb"))

    def test_lb_added_if_inner_elem_has_only_tail(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML("<div><ab>text<p/>tail</ab></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//lb").tail, "tail")

    def test_multiple_elements_separated_by_lb(self):
        self.observer.configure(self.valid_cfg)
        root = etree.XML(
            """
            <div>
                <p>text
                    <p>text2</p>
                    <p>text3</p>
                    <ab>text4<hi>text5</hi> </ab>tail
                    <p/>tail2
                    <p/>
                    <ab>text6</ab>
                </p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [(node.tag, node.text, node.tail.strip()) for node in root[0].iter()]
        expected = [
            ("p", "text", ""),
            ("lb", None, "text2"),
            ("lb", None, "text3"),
            ("lb", None, "text4"),
            ("hi", "text5", "tail"),
            ("lb", None, "tail2"),
            ("lb", None, "text6"),
        ]
        self.assertEqual(result, expected)
