import unittest

from lxml import etree

from tei_transform.observer import HeadAfterPElementObserver


class HeadAfterPElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HeadAfterPElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        tree = etree.XML("<body><p/><head></head></body>")
        node = tree[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        tree = etree.XML("<div><head/><p/></div>")
        node = tree[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        matching_elements = [
            etree.XML("<div><p>text</p><head/></div>"),
            etree.XML("<div><p/><head></head><p/></div>"),
            etree.XML("<TEI><text><body><p/><head/></body></text></TEI>"),
            etree.XML("<div><p/><head rendition='#b'></head></div>"),
            etree.XML(
                "<TEI><text><body><div><head/><p/><head/><p/></div></body></text></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
             <text>
             <body><p/><head>text</head><p/></body>
             </text>
             </TEI>"""
            ),
            etree.XML("<div><p/><fw>some other element</fw><head/></div>"),
            etree.XML("<div><list/><head/></div>"),
            etree.XML("<div><p/><figure/><head/></div>"),
            etree.XML("<div><table/><head/></div>"),
            etree.XML("<div><p/><docAuthor/><head/></div>"),
            etree.XML(
                """
                <TEI xmlns='http://www.tei-c.org/ns/1.0'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p/>
                        <byline/>
                        <head/>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        non_matching_elements = [
            etree.XML("<div><head/></div>"),
            etree.XML("<div1><head>text</head></div1>"),
            etree.XML("<div><head/></div>"),
            etree.XML("<div1><div2><head/></div2></div1>"),
            etree.XML("<div><head/><p/></div>"),
            etree.XML("<text><body><div><head/><p/></div></body></text>"),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <text>
            <body><div><head>text</head></div><p/></body>
            </text>
            </TEI>"""
            ),
            etree.XML("<div><fw/><head/></div>"),
            etree.XML("<div><byline/><head/></div>"),
            etree.XML("<div><dateline/><head>text</head><p/></div>"),
            etree.XML("<div><opener/><head/></div>"),
            etree.XML("<div><docAuthor/><head/></div>"),
            etree.XML("<div><docDate/><head/></div>"),
            etree.XML("<div><epigraph/><head/></div>"),
            etree.XML("<div><signed/><head/></div>"),
            etree.XML("<div><meeting/><head/></div>"),
            etree.XML("<div><salute/><head/></div>"),
            etree.XML(
                """
                <TEI xmlns='http://www.tei-c.org/ns/1.0'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <byline/>
                        <head/>
                        <p/>
                      </div>
                    </body>
                  </text>
                </TEI>"""
            ),
        ]
        for element in non_matching_elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual((result), {False})

    def test_observer_action_performed_correctly(self):
        node = etree.Element("head")
        node.text = "heading"
        self.observer.transform_node(node)
        self.assertEqual((node.tag, node.attrib), ("ab", {"type": "head"}))

    def test_old_attributes_preserved_after_transformation(self):
        node = etree.Element("head")
        node.text = "some text"
        node.set("rendition", "value")
        self.observer.transform_node(node)
        self.assertTrue(("rendition", "value") in node.attrib.items())

    def test_observer_action_on_nested_nodes(self):
        tree = etree.XML(
            """<TEI><text><body><div><p/><head>text</head></div></body></text></TEI>"""
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in tree.iter()]
        self.assertEqual(result, ["TEI", "text", "body", "div", "p", "ab"])

    def test_observer_action_performed_on_elements_with_namespace(self):
        tree = etree.XML(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0">
            <text><body><div><p/><head>text</head></div></body></text>
            </TEI>"""
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [etree.QName(node.tag).localname for node in tree.iter()]
        self.assertEqual(result, ["TEI", "text", "body", "div", "p", "ab"])

    def test_namespace_prefix_preserved_on_transformed_node(self):
        tree = etree.XML(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0">
            <text><body><p/><head>text</head></body></text>
            </TEI>"""
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in tree.iter()]
        expected = [
            "{http://www.tei-c.org/ns/1.0}TEI",
            "{http://www.tei-c.org/ns/1.0}text",
            "{http://www.tei-c.org/ns/1.0}body",
            "{http://www.tei-c.org/ns/1.0}p",
            "{http://www.tei-c.org/ns/1.0}ab",
        ]
        self.assertEqual(result, expected)

    def test_node_removed_if_text_is_empty(self):
        tree = etree.XML(
            """<TEI>
            <text><body><div><p/><head></head></div></body></text>
            </TEI>"""
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [etree.QName(node.tag).localname for node in tree.iter()]
        self.assertEqual(result, ["TEI", "text", "body", "div", "p"])

    def test_node_not_removed_if_tail_is_not_empty(self):
        tree = etree.XML(
            """<TEI>
            <text><body><div><p/><head></head>tail</div></body></text>
            </TEI>"""
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [etree.QName(node.tag).localname for node in tree.iter()]
        self.assertEqual(result, ["TEI", "text", "body", "div", "p", "ab"])

    def test_element_with_only_whitespace_in_tail_removed(self):
        tree = etree.XML("<div><p/><head/>    </div>")
        node = tree[1]
        self.observer.transform_node(node)
        self.assertEqual(len(tree), 1)

    def test_element_with_only_whitespace_text_removed(self):
        tree = etree.XML(
            """
            <div>
                <p/>
                <head>
                </head>
            </div>
            """
        )
        node = tree[1]
        self.observer.transform_node(node)
        self.assertTrue(len(tree), 1)

    def test_element_not_removed_if_children(self):
        tree = etree.XML(
            """
            <TEI xmlns="ns">
              <text>
                <body>
                  <div>
                    <p/>
                    <head><hi>text</hi></head>
                  </div>
                </body>
              </text>
            </TEI>
            """
        )
        node = tree.find(".//{*}head")
        self.observer.transform_node(node)
        self.assertTrue(tree.find(".//{*}ab") is not None)
