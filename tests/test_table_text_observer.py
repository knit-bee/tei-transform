import unittest

from lxml import etree

from tei_transform.observer import TableTextObserver


class TableTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TableTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<table>text</table>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><table><row><cell>text</cell></row></table></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<table><row/>tail</table>"),
            etree.XML("<table><row/><p>text</p></table>"),
            etree.XML("<div><table>text<row><cell/></row>tail</table></div>"),
            etree.XML("<div><table><head>text</head>tail<row/></table></div>"),
            etree.XML("<div><table><row/><p>text</p><row/></table></div>"),
            etree.XML("<table>text<row><cell>text</cell></row><p/></table>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>text
                      <row>
                        <cell>text</cell>
                      </row>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <row>
                        <cell>text</cell>
                      </row>tail
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <row>
                        <cell>text</cell>
                      </row>
                      <p>text</p>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <head>text</head>tail
                      <row>
                        <cell>text</cell>
                      </row>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><table/>tail</div>"),
            etree.XML("<table>  <row/></table>"),
            etree.XML("<div><table><row><cell><p/>tail</cell></row></table></div>"),
            etree.XML("<table><row/> <row/>\n  </table>"),
            etree.XML(
                "<div><table><head>text</head><row><cell/>tail</row></table></div>"
            ),
            etree.XML("<table><row/><fw>text</fw><row/></table>"),
            etree.XML("<table><row><cell><table/>tail</cell></row></table>"),
            etree.XML("<table><row><cell>text<p>text</p></cell></row></table>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text</cell>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text
                            <p>text</p>tail
                          </cell>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text</cell>
                        </row>
                      </table>tail
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <head>text</head>
                        <row>
                          <cell>text</cell>
                        </row>
                      </table>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text</cell>
                        </row>
                        <fw>text</fw>
                        <row/>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <table>
                        <row>
                          <cell>text
                            <table>
                              <row/>
                            </table>tail
                          </cell>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
