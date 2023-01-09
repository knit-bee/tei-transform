import unittest

from lxml import etree

from tei_transform.observer import LonelyCellObserver


class LonelyCellObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelyCellObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><cell/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><row><cell/></row></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><cell></cell></div>"),
            etree.XML("<div><cell>text</cell></div>"),
            etree.XML("<p><cell><p/></cell></p>"),
            etree.XML("<p><cell><p>text</p></cell></p>"),
            etree.XML("<div><table><cell/></table></div>"),
            etree.XML("<div><cell><cell>text</cell></cell></div>"),
            etree.XML("<table><row><cell><p><cell/></p></cell></row></table>"),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                       <p>text<cell>text</cell></p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                       <cell>text</cell>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                       <p>text<hi>text<cell>text</cell></hi></p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                    <text>
                      <div>
                        <p>text
                          <table>
                            <row>
                              <cell>
                                <p>
                                  <cell>text</cell>
                                </p>
                              </cell>
                            </row>
                          </table>tail
                        </p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <text>
                      <div>
                        <p>text
                          <table>
                            <row>
                              <cell>
                                <p>
                                  <cell>text</cell>
                                </p>
                              </cell>
                            </row>
                          </table>tail
                        </p>
                      </div>
                    </text>
                   </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <text>
                      <div>
                        <p>
                          <list>
                            <item>
                              <cell>text</cell>
                            </item>
                          </list>
                        </p>
                      </div>
                    </text>
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
            etree.XML("<row><cell/></row>"),
            etree.XML("<row><cell>text</cell></row>"),
            etree.XML("<row><cell><list/></cell></row>"),
            etree.XML("<table><row><cell>text</cell></row></table>"),
            etree.XML("<div><row><cell/></row></div>"),
            etree.XML(
                "<div><table><row><cell><cell>text</cell></cell></row></table></div>"
            ),
            etree.XML(
                "<table><row><cell><table><row><cell/></row></table></cell></row></table>"
            ),
            etree.XML("<p>text<hi>text<row><cell/></row>tail</hi>text</p>"),
            etree.XML(
                """
                <TEI>
                  <text>
                    <div>
                      <p>text</p>
                      <table>
                        <row>
                          <cell>text</cell>
                          <cell/>
                        </row>
                      </table>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <text>
                    <div>
                      <p>text
                          <table>
                            <row>
                              <cell>text</cell>
                              <cell/>
                            </row>
                          </table>tail
                      </p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <text>
                    <div>
                      <p>text</p>
                      <table>
                        <row>
                          <cell>text</cell>
                          <cell>
                            <table>
                              <row>
                               <cell>data</cell>
                              </row>
                            </table>
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
