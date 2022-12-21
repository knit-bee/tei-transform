import unittest

from lxml import etree

from tei_transform.observer import PAsDivSiblingObserver


class PAsDivSiblingObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = PAsDivSiblingObserver()

    def test_observer_returns_true_for_matching_node(self):
        p_node = etree.XML("<body><div/><p/></body>")[1]
        result = self.observer.observe(p_node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_nodes(self):
        p_node = etree.XML("<body><div><p/></div></body>")[0][0]
        result = self.observer.observe(p_node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        matching_elements = [
            etree.XML("<body><div/><p>text</p></body>"),
            etree.XML("<div><div/><p/></div>"),
            etree.XML("<body><p/><div/></body>"),
            etree.XML("<body><div><p>text></p></div><p>more text></p></body>"),
            etree.XML("<div><div/><div><div/></div><p/></div>"),
            etree.XML(
                """<div><div><p/></div>
                <p>some text</p>
                <p>more text</p>
                <p>more text that shouldn't be here</p>
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
          <p>new paragraph</p>
        </div></div></body></text>"""
            ),
            etree.XML(
                """<text>
    <body>
      <div type="entry">
        <fw rend="h1" type="header">heading </fw>
        <div>
          <p>text
          <lb/>more text
          </p>
        </div>
        <p/>
        </div></body></text>
"""
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
              <p>text
              <lb/>more text
              </p>
            </div>
            <p/>
            </div>
        </body></text>
        </TEI>
"""
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
            </div>
        </body></text>
        </TEI>
"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertTrue(any(result))

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div></div>"),
            etree.XML("<div><div><p/></div></div>"),
            etree.XML("<div><p>some text</p><p>more text</p></div>"),
            etree.XML(
                "<body><div><p>text></p></div><div><p>more text></p></div></body>"
            ),
            etree.XML("<text><body><div><p/><p/><p/></div></body></text>"),
            etree.XML(
                """<div>
                <div><p>text</p></div>
                <div><p>more text</p></div>
                <div><div><p/></div></div>
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
                  <p>text</p>
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
          <p>text
          <lb/>more text
          </p>
        </div>
        <div>
        <p/>
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

    def test_p_removed_if_empty(self):
        root = etree.XML("<body><div/><p/></body>")
        self.observer.transform_node(root[1])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div"])

    def test_p_not_removed_if_tail_not_empty(self):
        root = etree.XML("<body><div/><p></p>tail</body>")
        self.observer.transform_node(root[1])
        tags = [node.tag for node in root.iter()]
        self.assertTrue("p" in tags)

    def test_empty_p_removed_with_div_sibling_after_p(self):
        root = etree.XML("<body><p/><div/></body>")
        self.observer.transform_node(root[0])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div"])

    def test_new_div_added_as_parent_of_p(self):
        root = etree.XML("<body><div/><p>text</p></body>")
        self.observer.transform_node(root[1])
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div", "div", "p"])

    def test_multiple_p_elements_as_sibling_of_div(self):
        root = etree.XML("<body><div/><p>text</p><p>text 2</p><p>text 3 </p></body>")
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["body", "div", "div", "p", "p", "p"])

    def test_div_with_p_and_div_as_sibling_new_div_only_added_once(self):
        root = etree.XML(
            """
        <TEI>
        <teiHeader/>
        <text>
        <body>
        <div/>
        <div/>
        <p>text</p>
        </body>
        </text>
        </TEI>
        """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        expected = ["TEI", "teiHeader", "text", "body", "div", "div", "div", "p"]
        self.assertEqual(result, expected)

    def test_p_removed_if_empty_with_namespace(self):
        root = etree.XML(
            """
        <TEI xmlns='namespace'>
        <teiHeader/>
        <text>
        <body>
        <div/>
        <p></p>
        </body>
        </text>
        </TEI>
        """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "teiHeader", "text", "body", "div"])

    def test_new_div_added_as_parent_of_p_with_namespace(self):
        root = etree.XML("<TEI xmlns='namespace'><body><div/><p>text</p></body></TEI>")
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "body", "div", "div", "p"])

    def test_multiple_p_elements_as_sibling_of_div_with_namespace(self):
        root = etree.XML(
            """<TEI xmlns='namespace'>
            <body><div/><p>text</p><p>text 2</p><p>text 3 </p></body>
            </TEI>"""
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "body", "div", "div", "p", "p", "p"])

    def test_div_with_p_and_div_as_sibling_with_namepace(self):
        root = etree.XML(
            """
        <TEI xmlns='namespace'>
        <teiHeader/>
        <text>
        <body>
        <div/>
        <div/>
        <p>text</p>
        </body>
        </text>
        </TEI>
        """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        expected = ["TEI", "teiHeader", "text", "body", "div", "div", "div", "p"]
        self.assertEqual(result, expected)

    def test_new_div_added_if_p_comes_before_div_sibling(self):
        root = etree.XML(
            """
        <TEI>
        <teiHeader/>
        <text>
        <body>
        <p>text</p>
        <div/>
        </body>
        </text>
        </TEI>
        """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        expected = ["TEI", "teiHeader", "text", "body", "div", "p", "div"]
        self.assertEqual(result, expected)

    def test_new_div_added_if_p_comes_before_div_sibling_with_namespace(self):
        root = etree.XML(
            """
        <TEI xmlns='namespace'>
        <teiHeader/>
        <text>
        <body>
        <p>text</p>
        <div/>
        </body>
        </text>
        </TEI>
        """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        expected = ["TEI", "teiHeader", "text", "body", "div", "p", "div"]
        self.assertEqual(result, expected)

    def test_new_div_added_if_div_after_p_with_other_element_before_p(self):
        root = etree.XML(
            """
        <TEI xmlns='namespace'>
        <teiHeader/>
        <text>
        <body>
        <fw/>
        <p>text</p>
        <div/>
        </body>
        </text>
        </TEI>
        """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        expected = ["TEI", "teiHeader", "text", "body", "fw", "div", "p", "div"]
        self.assertEqual(result, expected)

    def test_multiple_p_elements_added_to_same_div_if_div_sibling_comes_after(self):
        root = etree.XML(
            """
            <TEI>
            <teiHeader/>
            <text>
            <body>
            <p>text</p>
            <p>text</p>
            <p>text</p>
            <div/>
            </body>
            </text>
            </TEI>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(
            result, ["TEI", "teiHeader", "text", "body", "div", "p", "p", "p", "div"]
        )

    def test_p_not_removed_if_child_but_not_text_or_tail(self):
        root = etree.XML(
            """
        <body>
            <div>
            <div/>
            <p><hi>text</hi></p>
            </div>
        </body>
        """
        )
        self.observer.transform_node(root.find(".//p"))
        self.assertTrue(root.find(".//p") is not None)

    def test_p_with_child_but_otherwise_empty_not_removed_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns="ns">
                <teiHeader/>
                <text>
                    <body>
                        <div>
                        <div/>
                        <p><hi>text</hi></p>
                        </div>
                    </body>
                </text>
            </TEI>
            """
        )
        self.observer.transform_node(root.find(".//{*}p"))
        self.assertTrue(root.find(".//{*}p") is not None)
