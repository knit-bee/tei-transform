import unittest

from lxml import etree

from tei_transform.observer import PParentObserver


class PParentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = PParentObserver(target_elems=["code"])

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p>text</p><code>text2</code></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><p>text<code>text</code></p></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><code>text</code>tail</div>"),
            etree.XML("<div><p/><code>text</code>tail<p/></div>"),
            etree.XML("<div><p><code/></p><code>text</code>tail</div>"),
            etree.XML("<div><p/><p/><code/><p/></div>"),
            etree.XML("<TEI xmlns='a'><div><p>a</p><code>b</code>c<p/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><code>a</code>b<p/><p/></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_recognises_matching_elements_generic_elems(self):
        observer = PParentObserver(target_elems=["elem", "elem1"])
        elements = [
            etree.XML("<div><item><elme1/></item><elem>text</elem>tail</div>"),
            etree.XML("<div><p/><elem>text</elem>tail<p><elem/></p></div>"),
            etree.XML("<div><p><elem1/></p><elem1>text</elem1>tail</div>"),
            etree.XML("<div><p/><p><elem1>text</elem1></p><elem/><p/></div>"),
            etree.XML("<TEI xmlns='a'><div><p>a</p><elem>b</elem>c<p/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><elem>a</elem>b<p/><p/></div></TEI>"),
        ]
        for element in elements:
            result = [observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p>text<code>ab</code>cd</p></div>"),
            etree.XML("<div><p/><p/><p><code>text</code>tail</p></div>"),
            etree.XML("<div><p>ab<hi>text</hi><code>bc</code>de</p></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>av</p><p><code>bc</code>de</p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>ab</p><list/><p>cd<code>text</code><hi/></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>a<hi/>b<code>c</code>d<list/>e</p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
