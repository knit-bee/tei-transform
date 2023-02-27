import unittest

from lxml import etree

from tei_transform.observer import MeasureQuantityAttributeObserver


class MeasureQuantityAttributeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MeasureQuantityAttributeObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<term measure_quantity='1'>Term</term>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<term type='val'>Term</term>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<term measure_quantity='1'/>"),
            etree.XML("<keywords><term measure_quantity='1'>Term</term></keywords>"),
            etree.XML(
                "<keywords><term/><term measure_quantity='3'>'A</term></keywords>"
            ),
            etree.XML(
                "<textClass><keywords><term measure_quantity='3'>A</term></keywords></textClass>"
            ),
            etree.XML("<classCode><term measure_quantity='2'>A</term></classCode>"),
            etree.XML(
                "<textClass><classCode><term measure_quantity='4'>a</term><term/></classCode></textClass>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader>
                    <textClass>
                      <keywords>
                        <term measure_quantity='1'>A</term>
                        <term type='a'/>
                      </keywords>
                    </textClass>
                  </teiHeader>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <textClass>
                    <classCode/>
                    <term measure_quantity='1'/>
                  </textClass>
                 </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='a'>
                  <textClass>
                    <keywords>
                      <term/>
                      <term measure_quantity='1' type='val'>A</term>
                    </keywords>
                  </textClass>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<term/>"),
            etree.XML("<term type='a'>Term</term>"),
            etree.XML("<keywords><term attr='val'>A</term></keywords>"),
            etree.XML(
                "<textClass><keywords><term/><term atrr='val'>a</term></keywords></textClass>"
            ),
            etree.XML(
                "<classCode><term attr='a'>Term</term><term>Term2</term></classCode>"
            ),
            etree.XML(
                "<textClass><keywords measure_quantity='1'>KW</keywords></textClass>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <textClass>
                    <classCode>
                      <term a='b' b='c'>ABC</term>
                      <term b='c'>BC</term>
                    </classCode>
                  </textClass>
                </TEI>"""
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><textClass><term>A</term><term>B</term></textClass></teiHeader></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_attribute_removed(self):
        node = etree.XML("<term measure_quantity='1'>Term</term>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed(self):
        node = etree.XML("<term attr='val' measure_quantity='1' other='b'>Term</term>")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val", "other": "b"})

    def test_attribute_removed_on_nested_element(self):
        root = etree.XML(
            "<textClass><keywords><term/><term measure_quantity='1'>A</term></keywords></textClass>"
        )
        node = root.findall(".//term")[1]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_attribute_removed_on_element_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <textClass>
                <classCode/>
                <keywords>
                  <term measure_quantity='1'>A</term>
                  <term/>
                </keywords>
              </textClass>
            </TEI>"""
        )
        node = root.find(".//{*}term")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})
