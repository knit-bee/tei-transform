import unittest

from lxml import etree

from tei_transform.observer import NestedFwWithInvalidDescendantObserver


class NestedFwWithInvalidDescendantObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = NestedFwWithInvalidDescendantObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<fw><fw><list/></fw></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<fw><fw>text</fw><list/></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<fw>text<fw>text<list/>tail</fw>tail</fw>"),
            etree.XML("<div><fw><fw>text<list><item/></list></fw></fw></div>"),
            etree.XML("<fw><fw><list/></fw><p/>tail</fw>"),
            etree.XML("<fw>text<fw/><fw><list/><fw/></fw></fw>"),
            etree.XML("<div><fw>text<fw/><fw><fw/><list/></fw></fw></div>"),
            etree.XML("<div><fw>text<fw><fw><p>text<list/></p></fw></fw></fw></div>"),
            etree.XML("<div><fw><fw><quote>text</quote><list/><fw/></fw></fw></div>"),
            etree.XML("<fw>text<fw>text<list/><fw/></fw></fw>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <fw>text</fw>
                    <fw>
                      <fw></fw>
                      <fw>text
                        <list>
                          <item>text</item>
                        </list>tail
                      </fw>
                    </fw>
                    <p>text</p>
                  </div>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <fw>
                      <fw></fw>
                      <fw>text
                        <list>
                          <item>text</item>
                        </list>tail
                      </fw>
                      <fw>
                        <p>text</p>
                      </fw>
                    </fw>
                    <p>text</p>
                  </div>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text</fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <fw>text
                              <p>text
                                 <list/>
                              </p>
                            </fw>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text</fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <fw>text
                              <hi>text</hi>
                              <list/>
                            </fw>
                            <fw/>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML("<fw>text<fw>text<table/>tail</fw>tail</fw>"),
            etree.XML("<div><fw><fw>text<table><row/></table></fw></fw></div>"),
            etree.XML("<fw><fw><table/></fw><p/>tail</fw>"),
            etree.XML("<fw><fw><hi><list/></hi>text<table/></fw><p/>tail</fw>"),
            etree.XML("<fw><fw><table/><list/></fw><p/>tail</fw>"),
            etree.XML("<fw>text<fw/><fw><table/><fw/></fw></fw>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <fw>text</fw>
                    <fw>
                      <fw></fw>
                      <fw>text
                        <table>
                          <row>
                            <cell>text</cell>
                          </row>
                        </table>tail
                      </fw>
                    </fw>
                    <p>text</p>
                  </div>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <fw>
                      <fw></fw>
                      <fw>text
                        <quote>text<p/>text<list/></quote>
                        <table>
                          <row>
                            <cell>text</cell>
                          </row>
                        </table>tail
                      </fw>
                      <fw>
                        <p>text</p>
                      </fw>
                    </fw>
                    <p>text</p>
                  </div>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(min(1, sum(result)), 1)

    def test_invalid_descendants_in_branch_found(self):
        elements = [
            etree.XML("<fw><fw>text<p><list/></p></fw>tail</fw>"),
            etree.XML("<fw><fw>text<fw><list/></fw></fw>tail</fw>"),
            etree.XML("<fw><fw>text<fw><fw><list/></fw></fw></fw>tail</fw>"),
            etree.XML("<fw><fw>text<fw><list><item/></list></fw></fw>tail</fw>"),
            etree.XML("<fw>b<fw>a<fw>c<list/>d</fw>e</fw>f</fw>"),
            etree.XML("<fw><fw><p><fw><p><list/></p></fw></p></fw></fw>"),
            etree.XML(
                "<fw><fw>text<fw><list><item>a</item></list><list/></fw></fw>tail</fw>"
            ),
            etree.XML(
                "<fw><fw>text<fw>text</fw><p>text</p><fw><list/></fw></fw>tail</fw>"
            ),
            etree.XML(
                """
                <fw>
                  <fw>
                    <fw>
                      <fw/>
                    </fw>
                    <fw>
                      <fw>
                        <list/>
                      </fw>
                      <quote/>
                    </fw>
                    <p/>
                  </fw>tail
                </fw>"""
            ),
            etree.XML("<fw><fw>text<fw><fw><table/></fw></fw></fw>tail</fw>"),
            etree.XML("<fw><fw>text<fw><table><row/></table></fw></fw>tail</fw>"),
            etree.XML("<fw>b<fw>a<fw>c<table/>d</fw>e</fw>f</fw>"),
            etree.XML("<fw><fw><p><fw><p><table/></p></fw></p></fw></fw>"),
            etree.XML(
                "<fw><fw><p><fw><quote><list/></quote><p><table/></p></fw></p></fw></fw>"
            ),
        ]
        for element in elements:
            node = element[0]
            with self.subTest():
                self.assertTrue(self.observer.observe(node))

    def test_invalid_descendants_in_branch_found_with_namespace(self):
        elements = [
            etree.XML("<TEI xmlns='a'><fw><fw>text<p><list/></p></fw>tail</fw></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><fw><list/></fw></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><list/></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><list><item/></list></fw></fw>tail</fw></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><fw>b<fw>a<fw>c<list/>d</fw>e</fw>f</fw></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><list><item>a</item></list><list/></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw>text</fw><p>text</p><fw><list/></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                <fw>
                  <fw>
                    <fw>
                      <fw/>
                    </fw>
                    <fw>
                      <fw>
                        <list/>
                      </fw>
                      <quote/>
                    </fw>
                    <p/>
                  </fw>tail
                </fw>
                </TEI>"""
            ),
            etree.XML(
                "<TEI xmlns='a'><fw><fw><p><fw><p><list/></p></fw></p></fw></fw></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><fw><fw>text<p><table/></p></fw>tail</fw></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><fw><table/></fw></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><table/></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fw><fw>text<fw><table><row/></table></fw></fw>tail</fw></TEI>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                <fw>
                  <fw>
                    <fw>
                      <fw/>
                    </fw>
                    <fw>
                      <fw>
                        <table/>
                      </fw>
                      <quote/>
                    </fw>
                    <p/>
                  </fw>tail
                </fw>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                <fw>
                  <fw>
                    <fw>
                      <fw/>
                    </fw>
                    <fw>
                      <fw>
                        <table/>
                      </fw>
                      <quote/>
                    </fw>
                    <p>
                      <list/>
                    </p>
                  </fw>tail
                </fw>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                <fw>
                  <fw>
                    <fw>
                      <fw/>
                    </fw>
                    <fw>
                      <fw>
                        <table>
                          <row>
                            <cell>
                              <list/>
                            </cell>
                          </row>
                        </table>
                      </fw>
                      <quote/>
                    </fw>
                    <p/>text
                  </fw>tail
                </fw>
                </TEI>"""
            ),
        ]

        for element in elements:
            node = element[0][0]
            with self.subTest():
                self.assertTrue(self.observer.observe(node))

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<fw><fw>text</fw></fw>"),
            etree.XML("<fw><list/></fw>"),
            etree.XML("<fw>text<p>text</p></fw>"),
            etree.XML("<fw>a<fw>b</fw>c<list/>d</fw>"),
            etree.XML("<fw><fw><hi>text</hi></fw></fw>"),
            etree.XML("<fw><fw><quote>a</quote></fw></fw>"),
            etree.XML("<div><fw>text<list/></fw><fw>text<fw>text</fw></fw></div>"),
            etree.XML("<div><fw><list/><p/></fw><fw><fw/></fw></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text</fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <p>text</p>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text<fw/>tail</fw>
                        <fw>
                          <p>text</p>
                          <fw>text
                            <hi>text</hi>
                            <p>text</p>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text
                          <fw>a</fw>
                          <fw>b</fw>
                        </fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <quote>text</quote>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML("<fw>a<fw>b</fw>c<table/>d</fw>"),
            etree.XML("<fw><table/></fw>"),
            etree.XML("<div><fw>text<table/></fw><fw>text<fw>text</fw></fw></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text
                          <fw>a</fw>
                          <fw>b</fw>
                        </fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <quote><table/>text</quote>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text
                          <fw>a</fw>
                          <fw>b</fw>
                        </fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <quote><list/>text</quote>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML("<div><fw><fw><hi><list/></hi></fw></fw></div>"),
            etree.XML("<div><fw><fw><quote><table/></quote></fw></fw></div>"),
            etree.XML("<div><fw><fw><fw><p/><hi><list/></hi><p/></fw></fw></fw></div>"),
            etree.XML("<div><fw><fw><fw><p><hi><list/></hi></p></fw></fw></fw></div>"),
            etree.XML(
                "<div><fw><fw><quote><list><item><table/></item></list></quote></fw></fw></div>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_element_added_as_sibling(self):
        root = etree.XML("<div><fw>text<fw><list/></fw></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root), 2)

    def test_attributes_preserved_after_transformation(self):
        root = etree.XML(
            "<div><fw type='header' rend='h2'>text<fw type='header' rend='h3'><list/></fw></fw></div>"
        )
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"type": "header", "rend": "h3"})

    def test_element_added_as_sibling_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><fw>text<fw><list/></fw></fw></div></TEI>"
        )
        node = root.find(".//{*}fw/{*}fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root[0]), 2)

    def test_attributes_preserved_after_transformation_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><fw type='header' rend='h2'>text<fw type='header' rend='h3'><list/></fw></fw></div></TEI>"
        )
        node = root.find(".//{*}fw/{*}fw")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"type": "header", "rend": "h3"})

    def test_transformation_on_target_with_older_siblings(self):
        root = etree.XML("<div><fw><sib/><fw><list/></fw></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root.iter()]
        self.assertEqual(
            result,
            [
                ("div", ["fw", "fw"]),
                ("fw", ["sib"]),
                ("sib", []),
                ("fw", ["list"]),
                ("list", []),
            ],
        )

    def test_transformation_on_target_with_following_siblings(self):
        root = etree.XML("<div><fw>text<fw><list/></fw><sib/></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root.iter()]
        self.assertEqual(
            result,
            [
                ("div", ["fw", "fw", "fw"]),
                ("fw", []),
                ("fw", ["list"]),
                ("list", []),
                ("fw", ["sib"]),
                ("sib", []),
            ],
        )

    def test_parent_removed_if_empty_after_transformation(self):
        root = etree.XML("<div><fw><fw><list/></fw></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 1)

    def test_parent_with_older_sibling_not_removed(self):
        root = etree.XML("<div><fw><sib/><fw><list/></fw></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 2)

    def test_parent_with_tail_not_removed(self):
        root = etree.XML("<div><fw><fw><list/></fw></fw>tail</div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 2)

    def test_parent_with_text_not_removed(self):
        root = etree.XML("<div><fw>text<fw><list/></fw></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 2)

    def test_parent_with_only_whitespace_text_removed(self):
        root = etree.XML("<div><fw>   <fw><list/></fw></fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 1)

    def test_parent_with_only_whitespace_tail_removed(self):
        root = etree.XML("<div><fw><fw><list/></fw></fw>    </div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 1)

    def test_type_and_rendition_attributes_of_parent_transfered_to_new_fw(self):
        root = etree.XML(
            "<div><fw type='header' rend='h2'><fw type='header' rend='h3'><list/></fw><sib/></fw></div>"
        )
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(root[-1].attrib, {"type": "header", "rend": "h2"})

    def test_other_attributes_of_parent_not_transfered_to_new_fw(self):
        root = etree.XML(
            "<div><fw xml:id='id' n='1'><fw type='header' rend='h3'><list/></fw><sib/></fw></div>"
        )
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(root[-1].attrib, {})

    def test_children_of_target_not_changed_after_transformation(self):
        root = etree.XML(
            "<div><fw><fw><p>text</p><list><item>a</item></list></fw></fw></div>"
        )
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        result = [node.tag for node in root[-1].iter()]
        self.assertEqual(result, ["fw", "p", "list", "item"])

    def test_resolve_multiple_nested_fw(self):
        root = etree.XML(
            """
            <div>
              <fw>a
                <fw rend='h2'>b
                  <fw>c
                    <fw>d
                      <list/>
                    </fw>
                  </fw>
                  <fw>e
                    <fw>f</fw>
                  </fw>
                </fw>
              </fw>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [
            (
                node.tag,
                node.text.strip() if node.text is not None else None,
                [child.tag for child in node],
            )
            for node in root.iter()
        ]
        self.assertEqual(
            result,
            [
                ("div", "", ["fw", "fw", "fw", "fw", "fw"]),
                ("fw", "a", []),
                ("fw", "b", []),
                ("fw", "c", []),
                ("fw", "d", ["list"]),
                ("list", None, []),
                ("fw", None, ["fw"]),
                ("fw", "e", ["fw"]),
                ("fw", "f", []),
            ],
        )

    def test_tail_of_target_removed(self):
        root = etree.XML("<div><fw>text<fw><list/></fw>tail</fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(root[-1].tail, None)

    def test_tail_of_target_node_added_as_tail_of_last_child_if_none(self):
        root = etree.XML("<div><fw><fw><list/></fw>tail</fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(node[-1].tail, "tail")

    def test_tail_of_target_concatenated_with_tail_of_last_child(self):
        root = etree.XML("<div><fw><fw><list/>tail1</fw>tail2</fw></div>")
        node = root.find(".//fw/fw")
        self.observer.transform_node(node)
        self.assertEqual(node[-1].tail, "tail1 tail2")

    def test_branch_with_table_and_list(self):
        root = etree.XML(
            """
            <div>
              <fw>a
                <fw rend='h2'>b
                  <fw>c
                    <fw>d
                      <table>
                        <row>
                          <cell>
                            <list/>
                          </cell>
                        </row>
                      </table>
                    </fw>
                  </fw>
                  <fw>e
                    <fw>f
                      <p>
                        <table/>
                      </p>
                      <quote>
                        <list/>
                      </quote>
                    </fw>
                  </fw>
                </fw>
              </fw>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertTrue(root.find(".//table//list") is not None)
        self.assertEqual(len(root), 6)
