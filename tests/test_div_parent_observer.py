import unittest

from lxml import etree

from tei_transform.observer import DivParentObserver


class DivParentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><div/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><div/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<quote><div/></quote>"),
            etree.XML("<code><div/></code>"),
            etree.XML("<p><div><p>text</p></div></p>"),
            etree.XML("<table><row><cell><div/></cell></row></table>"),
            etree.XML("<p>text<div>text</div>text</p>"),
            etree.XML("<p><quote><div><p>text</p></div></quote></p>"),
            etree.XML("<div><table><row><cell>text<div/></cell></row></table></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                       <p>text</p>
                       <quote>
                         <div>
                           <p>text</p>
                         </div>
                        </quote>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <div>
                         <table>
                           <row>
                            <cell>
                              <div>
                                <p>text</p>
                              </div>
                            </cell>
                          </row>
                         </table>
                        </div>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <list>
                          <item>
                            <div/>
                          </item>
                        </list>
                        <p/>
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
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p/><div/></div>"),
            etree.XML("<app><lem><div/></lem></app>"),
            etree.XML("<cell><app><rdg><div><p>text</p></div></rdg></app></cell>"),
            etree.XML("<text><back><div/></back></text>"),
            etree.XML("<text><front><div/></front></text>"),
            etree.XML(
                "<div><p><floatingText><body><div/></body></floatingText></p></div>"
            ),
            etree.XML("<div><quote><p/></quote><div><p>text</p></div></div>"),
            etree.XML(
                """<body>
                    <div>
                        <table>
                            <row>
                                <cell>
                                    <floatingText>
                                        <body><div/></body>
                                    </floatingText>
                                </cell>
                            </row>
                        </table>
                    </div>
                  </body>"""
            ),
            etree.XML("<body><div><p/><div><p>text</p></div></div></body>"),
            etree.XML("<body><div><quote/><p/><div><table/></div></div></body>"),
            etree.XML(
                "<body><p><floatingText><body><div><p/></div></body></floatingText></p></body>"
            ),
            etree.XML("<div><list/><div><p/><div><p/></div></div></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>text</p>
                        <div>
                          <p/>
                        </div>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                          <floatingText>
                            <body>
                              <div>
                                <p>text</p>
                              </div>
                            </body>
                          </floatingText>
                        </p>
                      </div>
                    </body>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <body>
                      <div>
                        <p>
                          <floatingText>
                            <body>
                              <div>
                                <p>text</p>
                              </div>
                            </body>
                          </floatingText>
                        </p>
                        <div>
                          <p>text</p>
                          <table>
                            <row>
                              <cell>
                                <p>text
                                </p>
                              </cell>
                            </row>
                          </table>
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
