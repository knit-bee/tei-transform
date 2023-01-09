import unittest

from lxml import etree

from tei_transform.observer import LonelyRowObserver


class LonelyRowObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelyRowObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<div><row/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<div><table><row/></table></div>")
        node = root.find(".//row")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<p><row/></p>"),
            etree.XML("<div><row></row></div>"),
            etree.XML("<div><row><cell/></row></div>"),
            etree.XML("<div><row><cell>text</cell></row></div>"),
            etree.XML("<table><row><cell><row/></cell></row></table>"),
            etree.XML("<div><row>text</row></div>"),
            etree.XML(
                """
                <TEI>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text
                          <hi>text
                            <row>
                              <cell>text</cell>
                            </row>
                          </hi>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                          <head>text
                            <row>
                              <cell>text</cell>
                            </row>tail
                        </head>
                        <p>text
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <row>
                          <cell>text</cell>
                        </row>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <row>
                          <cell>text</cell>
                        </row>
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
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <table>
                          <row>
                            <cell>text
                              <row>
                                <cell>text</cell>tail
                              </row>tail
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
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                        <row>
                          <cell>text</cell>
                        </row>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                          <list>
                            <item>
                              <row>
                                <cell>text</cell>
                              </row>
                            </item>
                          </list>
                        </p>
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

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<table><row/></table>"),
            etree.XML("<table><row/><row><cell/></row></table>"),
            etree.XML("<div><table><row><cell>text</cell></row></table></div>"),
            etree.XML(
                "<table><row><cell><table><row><cell/></row></table></cell></row></table>"
            ),
            etree.XML("<table><row><cell>text</cell><cell>text</cell></row></table>"),
            etree.XML("<div><head><table><row/></table></head></div>"),
            etree.XML(
                "<div><p>text<table><row><cell>text</cell><cell/></row></table></p></div>"
            ),
            etree.XML(
                "<div><p><table><row><cell/><cell/></row><row><cell>text</cell></row></table></p></div>"
            ),
            etree.XML(
                """
                <TEI>
                <teiHeader/>
                <text>
                  <body>
                    <div>
                      <p>text<table><row><cell>text</cell></row></table>tail</p>
                    </div>
                  </body>
                </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <p>
                          <table>
                            <row>
                              <cell>
                                <table>
                                  <row/>
                                </table>
                              </cell>
                            </row>
                          </table>
                        </p>tail
                        <p>more text</p>
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
