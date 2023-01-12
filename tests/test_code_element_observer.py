import unittest

from lxml import etree

from tei_transform.observer import CodeElementObserver


class CodeElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = CodeElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><code><p>text</p></code></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><p>text<code>x=y</code></p></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><code/></div>"),
            etree.XML("<div><code>text</code></div>"),
            etree.XML("<div><p>text<code>text<lb/>text</code></p></div>"),
            etree.XML("<div><p><code>text<p/></code></p></div>"),
            etree.XML("<div><div><code>text</code></div></div>"),
            etree.XML("<body><div><p>text<code><p>text</p></code></p></div></body>"),
            etree.XML("<p><code><ab>text</ab></code></p>"),
            etree.XML("<p><code><list/></code></p>"),
            etree.XML("<TEI xmlns='ns'><div><code/></div></TEI>"),
            etree.XML("<TEI xmlns='ns'><div><code>text</code></div></TEI>"),
            etree.XML("<TEI xmlns='ns'><div><p>text<code><p/></code></p></div></TEI>"),
            etree.XML(
                "<TEI xmlns='ns'><div><p><code><ab>text</ab>tail</code>tail</p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab><code><list/>tail</code></ab></div></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                  <div>
                    <table>
                      <row>
                        <cell>
                          <code><p/>text</code>
                        </cell>
                      </row>
                    </table>
                  </div>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p><code>abc</code></p></div>"),
            etree.XML("<quote>text<lb/><code>abc</code><lb/>text</quote>"),
            etree.XML("<p>a<hi>b<code>c</code>d</hi>e</p>"),
            etree.XML("<table><row><cell>text<code/></cell></row></table>"),
            etree.XML("<div><ab>ad<code>b</code></ab></div>"),
            etree.XML("<div><fw>text<code/>tail</fw></div>"),
            etree.XML("<div><p>text<code>ab</code>text</p></div>"),
            etree.XML("<body><div><ab><code/></ab></div></body>"),
            etree.XML(
                "<TEI xmlns='ns'><body><div><p><code>text</code></p></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><quote>text<code/>text</quote></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><list><item><code>text</code></item></list></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
