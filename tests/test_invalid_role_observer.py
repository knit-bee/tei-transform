import unittest

from lxml import etree

from tei_transform.observer import InvalidRoleObserver


class InvalidRoleObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = InvalidRoleObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p role='val'>text</p></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><p rend='i'>text</p></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div role='content'><p>text</p></div>"),
            etree.XML("<body><div><p/><p role='a'/><p/></div></body>"),
            etree.XML("<div><list><item><p role='a'>text</p>tail</item></list></div>"),
            etree.XML("<body><div role='a'><p/></div></body>"),
            etree.XML("<TEI xmlns='a'><div><p role='val'>text<hi/></p></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><div role='content'><p>text</p></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><table><row><cell><p role='a'><hi>text</hi></p></cell></row></table></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p xml:id='n'>text</p></div>"),
            etree.XML("<body><div n='1'><p/></div></body>"),
            etree.XML("<div n='1' type='content'><p>text</p><p/></div>"),
            etree.XML("<body><div type='a'><p n='1'>text<hi/>tail</p></div></body>"),
            etree.XML(
                "<TEI xmlns='a'><body><div n='1' type='a'><p/></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><list><item><p n='1'>text</p></item></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div type='c'><p xml:id='ab'>text</p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_role_attribute_removed(self):
        root = etree.XML("<div><p role='a'>text</p></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed(self):
        root = etree.XML(
            "<body><div xml:id='a' role='b' type='c'><p>text</p></div></body>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(
            node.attrib, {"{http://www.w3.org/XML/1998/namespace}id": "a", "type": "c"}
        )
