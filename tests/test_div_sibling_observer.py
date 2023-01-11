import unittest
from lxml import etree

from tei_transform.observer import DivSiblingObserver


class DivSiblingObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivSiblingObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<body><div/><table/></body>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<body><div/><div/></body>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, result)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><div/><table></table></div>"),
            etree.XML("<div><div><p/></div><quote/></div>"),
            etree.XML("<div><div/><quote/></div>"),
            etree.XML("<body><p/><div><p/></div><table><row/></table></body>"),
            etree.XML(
                "<div><p>text</p><div><p>text</p></div><quote>text</quote></div>"
            ),
            etree.XML(
                "<text><div><fw/><div><p>a</p></div><quote><p/></quote></div></text>"
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <div>
                            <p>text</p>
                          </div>
                          <table>
                            <row>
                              <cell>text</cell>
                            </row>
                          </table>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <div>
                            <p>text</p>
                          </div>
                          <quote>text<p>text</p></quote>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <p>text</p>
                          <div>
                            <list>
                              <item>text</item>
                            </list>
                          </div>
                          <table>
                            <row>
                              <cell>
                                <table>
                                  <row/>
                                </table>
                              </cell>
                            </row>
                          </table>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <div>
                            <p>text</p>
                            <table>
                              <row>
                                <cell>text</cell>
                              </row>
                            </table>
                          </div>
                          <div>
                            <p>text</p>
                          </div>
                          <table>
                            <row>
                              <cell>text</cell>
                            </row>
                          </table>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                print(etree.tostring(element))
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><div><table/></div></div>"),
            etree.XML("<div><quote/></div>"),
            etree.XML("<body><table/><div><p/></div></body>"),
            etree.XML("<div><quote>text</quote><div><p>text</p></div></div>"),
            etree.XML("<div><table><row><cell>text</cell></row></table><div/></div>"),
            etree.XML(
                "<div><div><quote>text</quote></div><div><p>text</p></div></div>"
            ),
            etree.XML("<body><p>text</p><table/><div><p/></div></body>"),
            etree.XML("<div><table><row><cell/></row></table><div/><div/></div>"),
            etree.XML("<body><div><p>text</p></div><div><table/></div></body>"),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <table>
                            <row>
                              <cell>text</cell>
                            </row>
                          </table>
                          <div>
                            <p>text</p>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <div>
                            <table>
                              <row>
                                <cell>text</cell>
                              </row>
                            </table>
                          </div>
                          <div>
                            <p>text</p>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text</p>
                          <quote>
                            <p>text</p>
                          </quote>
                          <div>
                            <p>text</p>
                            <quote/>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                    <teiHeader/>
                    <text>
                      <body>
                        <div>
                          <head/>
                          <p>text
                            <quote>text</quote>
                          </p>
                          <table>
                            <row>
                              <cell>text</cell>
                            </row>
                          </table>
                          <div>
                            <p>text</p>
                          </div>
                          <div>
                            <quote/>
                          </div>
                        </div>
                      </body>
                    </text>
                  </TEI>
                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
