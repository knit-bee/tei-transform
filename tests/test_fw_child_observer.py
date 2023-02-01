import unittest

from lxml import etree

from tei_transform.observer import FwChildObserver


class FwChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = FwChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<fw><p/></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<fw>text<hi>text</hi></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<fw><list/></fw>"),
            etree.XML("<fw>text<p>text</p>text</fw>"),
            etree.XML("<div><fw>text<list><item/></list></fw></div>"),
            etree.XML("<div><fw>text<p><hi>text</hi></p></fw></div>"),
            etree.XML("<div><p>text<fw><p>text</p></fw>tail</p></div>"),
            etree.XML("<div>text<fw>text<list/></fw><p/><p/></div>"),
            etree.XML("<div><p>txt</p><fw><p><table/></p></fw></div>"),
            etree.XML("<TEI xmlns='a'><div><fw><list/></fw></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><fw>text<p>text</p>text</fw></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><fw>text<p>text<table/>tail</p>a</fw><p/></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><fw>a</fw><div><fw><list/>tail</fw></div></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<fw>text</fw>"),
            etree.XML("<fw>a<hi>b</hi>c</fw>"),
            etree.XML("<div><p>a</p><fw>b</fw>c<p/>d</div>"),
            etree.XML("<div><fw>text<fw>text</fw>tail</fw><p/></div>"),
            etree.XML("<div><fw/><p><fw>text</fw></p></div>"),
            etree.XML("<div><list><item><fw>a</fw></item></list></div>"),
            etree.XML("<div><fw/><p><list/><fw/></p>tail</div>"),
            etree.XML("<TEI xmlns='a'><div><fw>text</fw><p><list/></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><list><fw>text</fw></list>tail</TEI>"),
            etree.XML("<TEI xmlns='a'><p>b<fw>a<hi>c</hi>d</fw>e</p></TEI>"),
            etree.XML("<TEI xmlns='a'><div><list/><p/><fw>text</fw></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
