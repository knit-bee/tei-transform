import unittest

from lxml import etree

from tei_transform.head_with_type_attr_observer import HeadWithTypeAttrObserver


class HeadWithTypeAttrObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HeadWithTypeAttrObserver()

    def test_observer_returns_true_for_matching_node(self):
        node = etree.XML("<head type='val'/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        node = etree.XML("<head/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognizes_matching_nodes(self):
        matching_elements = [
            etree.XML("<head type='val'/>"),
            etree.XML("<head type='t'><p/></head>"),
            etree.XML("<div><head type='v'/><p/></div>"),
            etree.XML(
                "<text><body><div><head type='t'><p/></head><p/></div></body></text>"
            ),
            etree.XML("<div1><head type='val'/><p/></div1>"),
            etree.XML(
                """<text><body><div><head type='val'>Text</head><p/></div>
                     <div><head/><p/></div></body></text>"""
            ),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><text><body><head type='t'/></body></text></TEI>",
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <text><body>
            <div><head type='val'/><p/></div>
            <div><head/></div>
            </body></text>
            </TEI>"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        not_matching_elements = [
            etree.XML("<head/>"),
            etree.XML("<text><body><head/><p/></body></text>"),
            etree.XML("<text><body><head>Heading</head><p/></body></text>"),
            etree.XML("<head attr='val'/>"),
            etree.XML("<body><head rendition='#b'>text</head></body>"),
            etree.XML("<head attr='val'>text</head>"),
            etree.XML(
                "<TEI xmlns='http://www.tei-c.org/ns/1.0'><text><body><head/></body></text></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <text><body>
            <div><head/><p/></div>
            <div><head/></div>
            </body></text>
            </TEI>"""
            ),
        ]
        for element in not_matching_elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_observer_action_performed_correctly(self):
        node = etree.Element("head", attrib={"type": "val"})
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_node_attributes_not_changed(self):
        node = etree.Element("head", attrib={"type": "val", "attr": "val2"})
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val2"})

    def test_observer_performed_action_on_nested_nodes(self):
        tree = etree.XML(
            "<text><body><div type='n'><head type='val'/><p/></div></body></text>"
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.attrib for node in tree.iter()]
        self.assertEqual(result, [{}, {}, {"type": "n"}, {}, {}])

    def test_observer_action_performed_on_element_with_namespace_prefix(self):
        tree = etree.XML(
            """<TEI xmlns=''>
        <text><body><head type='val'>Heading</head><p/></body></text>
        </TEI>"""
        )
        for node in tree.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.attrib for node in tree.iter()]
        self.assertEqual(result, [{}, {}, {}, {}, {}])
