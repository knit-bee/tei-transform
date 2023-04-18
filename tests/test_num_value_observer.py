import unittest

from lxml import etree

from tei_transform.observer import NumValueObserver


class NumValueObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = NumValueObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><num value='percent'/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<p><num type='sth'/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p><num value='percent'>100</num></p>"),
            etree.XML("<ab>text<num value='percent'>2000</num>text</ab>"),
            etree.XML(
                "<div><p/><p>text<num value='percent'>3×10<hi rend='sup'>10</hi></num></p></div>"
            ),
            etree.XML("<list><cell>text<num value='percent'>200</num></cell></list>"),
            etree.XML("<publisher>Name<num value='percent'>100</num></publisher>"),
            etree.XML("<TEI xmlns='a'><p>text<num value='percent'>100</num></p></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><publisher>Name<num value='percent'>100</num></publisher></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text<num value='100'>hundred</num></p>"),
            etree.XML("<p>text<num type='percentage'>30</num></p>"),
            etree.XML("<publisher>Name<num type='percent'>50</num></publisher>"),
            etree.XML(
                "<div><ab>text<num type='percentage' value='30'>thirty</num></ab></div>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<num type='ordinal' value='1'>first</num></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publisher>Name<num type='percent'>100</num></publisher></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<num value='3e10'>3x10</num></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
