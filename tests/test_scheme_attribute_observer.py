import unittest

from lxml import etree

from tei_transform.observer import SchemeAttributeObserver


class SchemeAttributeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = SchemeAttributeObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<classCode scheme=''/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<classCode scheme='some.scheme'/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<classcode scheme=''>text</classcode>"),
            etree.XML("<textClass><classCode scheme=''>text</classCode></textClass>"),
            etree.XML("<textclass><classcode scheme=''>text</classcode></textclass>"),
            etree.XML("<element scheme=''/>"),
            etree.XML("<textClass scheme=''><classCode>code</classCode></textClass>"),
            etree.XML(
                "<profileDesc><textclass><classcode scheme=''>code</classcode></textclass></profileDesc>"
            ),
            etree.XML(
                "<teiHeader><fileDesc/><profileDesc><classCode scheme=''>code</classCode></profileDesc></teiHeader>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><profileDesc><classCode scheme=''/></profileDesc></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><element scheme=''>text</element></teiHeader></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<classcode scheme='a'>text</classcode>"),
            etree.XML("<classCode scheme='a'><code/></classCode>"),
            etree.XML("<element scheme='http/...'>text</element>"),
            etree.XML(
                "<textclass><classcode scheme='path'>text</classcode></textclass>"
            ),
            etree.XML(
                "<teiHeader><textclass><code scheme='a'><term/></code></textclass></teiHeader>"
            ),
            etree.XML(
                "<textClass><classCode scheme='path/to/scheme'>code</classCode></textClass>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><element scheme='path'/></teiHeader></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='a'>
                  <profileDesc>
                    <textClass>
                      <classCode scheme='b'>code</classCode>
                      <keywords/>
                    </textClass>
                  </profileDesc>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_attribute_removed(self):
        root = etree.XML("<teiHeader><classCode scheme=''>code</classCode></teiHeader>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_attribute_removed_for_element_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><teiHeader><element scheme=''/></teiHeader></TEI>"
        )
        node = root.find(".//{*}element")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed(self):
        root = etree.XML(
            "<textclass><classcode attr='a' scheme='' other='b'>code</classcode></textclass>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "a", "other": "b"})
