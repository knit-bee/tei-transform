import unittest

from lxml import etree

from tei_transform.observer import ClasscodeObserver


class ClasscodeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = ClasscodeObserver()

    def test_observer_returns_true_for_matching_node(self):
        node = etree.XML("<classcode/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        node = etree.XML("<classCode/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        matching_elements = [
            etree.XML("<classcode></classcode>"),
            etree.XML("<textClass><classcode>text</classcode></textClass>"),
            etree.XML(
                "<textClass><classcode>news</classcode><keywords><term/></keywords></textClass>"
            ),
            etree.XML(
                """<TEI>
                <teiHeader><textClass><classcode><idno/></classcode></textClass></teiHeader><text/></TEI>"""
            ),
            etree.XML(
                """<TEI><teiHeader><textClass><classcode attrib='b'/></textClass></teiHeader><text/></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                <teiHeader><textClass><classcode/></textClass></teiHeader>
                <text/>
                </TEI>"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<classCode></classCode>"),
            etree.XML("<classCode><idno/></classCode>"),
            etree.XML(
                "<textClass><classCode>news</classCode><keywords><term/></keywords></textClass>"
            ),
            etree.XML(
                """<TEI><teiHeader><textClass><classCode>text</classCode></textClass></teiHeader><text/></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
                        <teiHeader><textClass><classCode/></textClass></teiHeader>
                        <text/>
                        </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(set(result), {False})

    def test_observer_action_performed_correctly(self):
        node = etree.XML("<classcode/>")
        self.observer.transform_node(node)
        self.assertEqual(node.tag, "classCode")

    def test_observer_action_performed_on_nested_node(self):
        tree = etree.XML(
            "<profileDesc><textClass><classcode><idno/></classcode><keywords/></textClass></profileDesc>"
        )
        node = tree[0]
        self.observer.transform_node(node)
        self.assertEqual(node.tag, "classCode")

    def test_observer_action_performed_on_namespaced_node(self):
        tree = etree.XML(
            """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            <profileDesc><textClass><classcode/><keywords/></textClass></profileDesc></TEI>"""
        )
        node = tree[0][0][0]
        self.observer.transform_node(node)
        result = etree.QName(node.tag).localname
        self.assertEqual(result, "classCode")

    def test_attributes_of_node_not_removed_after_transformation(self):
        node = etree.XML("<classcode attrib='b'/>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attrib": "b"})

    def test_namespace_of_node_preserved_after_transformation(self):
        xml = etree.XML(
            """
        <TEI xmlns="http://www.tei-c.org/ns/1.0">
            <profileDesc><textClass><classcode/></textClass></profileDesc>
        </TEI>
        """
        )
        for node in xml.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in xml.iter()]
        self.assertEqual(
            result,
            [
                "{http://www.tei-c.org/ns/1.0}TEI",
                "{http://www.tei-c.org/ns/1.0}profileDesc",
                "{http://www.tei-c.org/ns/1.0}textClass",
                "{http://www.tei-c.org/ns/1.0}classCode",
            ],
        )
