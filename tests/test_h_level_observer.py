import unittest

from lxml import etree

from tei_transform.observer import HLevelObserver


class HLevelObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HLevelObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p/><h2>text</h2></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><hi/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><h3><lb/>text</h3></div>"),
            etree.XML("<div><p/><h4>text</h4><p/></div>"),
            etree.XML("<div><p/><h5 class='sth'><lb/></h5></div>"),
            etree.XML("<div><h6 title='sth'><lb/>text</h6><p/></div>"),
            etree.XML("<body><div><p/><h7>text</h7></div></body>"),
            etree.XML("<div><h8/><p/></div>"),
            etree.XML("<TEI xlmns='a'><body><div><h2>ab</h2><p/></div></body></TEI>"),
            etree.XML(
                "<TEI xlmns='a'><body><div><h3 class='sth'><lb/>ab</h3><p/></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xlmns='a'><body><div><p/><h4>ab</h4><p/></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xlmns='a'><body><div><p/><h5><lb/></h5><p/></div></body></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p><hi/></p></div>"),
            etree.XML("<div><p/><hi/><p/></div>"),
            etree.XML("<div><head>txt</head><p>ab</p></div>"),
            etree.XML("<div><hi/><p/></div>"),
            etree.XML(
                "<TEI xlmns='a'><body><div><head>ab</head><p/></div></body></TEI>"
            ),
            etree.XML("<TEI xlmns='a'><body><div><hi>ab</hi><p/></div></body></TEI>"),
            etree.XML(
                "<TEI xlmns='a'><body><div><p><hi>ab</hi></p><p/></div></body></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_tag_changed_to_ab(self):
        root = etree.XML("<div><h3>text</h3></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.tag, "ab")

    def test_tag_changed_to_ab_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><h4>text</h4></div></TEI>"
        )
        node = root.find(".//{*}h4")
        self.observer.transform_node(node)
        self.assertEqual(etree.QName(node).localname, "ab")
        self.assertEqual(etree.QName(node).namespace, "http://www.tei-c.org/ns/1.0")

    def test_type_attribute_added(self):
        root = etree.XML("<div><h2>text</h2><p/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib.get("type"), "head")

    def test_rend_attribute_added_with_old_tag_name(self):
        for i in range(2, 9):
            tag_name = f"h{i}"
            root = etree.XML(f"<div><{tag_name}>text</{tag_name}></div>")
            node = root[0]
            self.observer.transform_node(node)
            with self.subTest():
                self.assertEqual(node.attrib.get("rend"), tag_name)

    def test_rend_attribute_added_with_old_tag_name_with_namespace(self):
        for i in range(2, 9):
            tag_name = f"h{i}"
            root = etree.XML(
                f"<TEI xmlns='http://www.tei-c.org/ns/1.0'><div><p/><{tag_name}>text</{tag_name}></div></TEI>"
            )
            node = root.find(".//{*}div")[1]
            self.observer.transform_node(node)
            with self.subTest():
                self.assertEqual(node.attrib.get("rend"), tag_name)

    def test_unwanted_attributes_removed(self):
        root = etree.XML("<div><h2 class='sth' title='a'>text</h2></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"type": "head", "rend": "h2"})

    def test_other_attributes_not_removed(self):
        root = etree.XML("<div><h4 xml:id='sth' class='a' n='a' rendition='#i'/></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(
            (node.attrib),
            {
                "{http://www.w3.org/XML/1998/namespace}id": "sth",
                "n": "a",
                "rendition": "#i",
                "rend": "h4",
                "type": "head",
            },
        )

    def test_element_with_children_renamed(self):
        root = etree.XML("<div><p/><h3><lb/>text</h3><p/></div>")
        node = root.find("h3")
        self.observer.transform_node(node)
        self.assertEqual(len(node), 1)
