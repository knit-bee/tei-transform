import unittest

from lxml import etree

from tei_transform.observer import TailTextObserver


class TailTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TailTextObserver()

    def test_observer_returns_true_for_matching_element(self):
        element = etree.XML("<text><div><p/>text<p/></div></text>")
        result = self.observer.observe(element[0][0])
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        element = etree.XML("<text><p/></text>")[0]
        result = self.observer.observe(element)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        matching_elements = [
            etree.XML("<text><div><p>some text</p>and some more</div></text>"),
            etree.XML("<text><div><fw>heading</fw>some text<p/></div></text>"),
            etree.XML("<text><div><ab>heading</ab>some text<p>body</p></div></text>"),
            etree.XML("<text><body><div><p>text</p>tail</div></body></text>"),
            etree.XML(
                """<TEI>
            <teiHeader/>
            <text><div><p/>tail</div></text>
            </TEI>
            """
            ),
            etree.XML(
                """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader/>
            <text><body><div><ab/>tail<p>text</p></div></body></text>
            </TEI>"""
            ),
            etree.XML(
                """
            <text>
                <div>
                    <p>
                        <floatingText>
                          <body>
                            <p/>
                            <fw>text</fw>tail
                          </body>
                        </floatingText>
                    </p>
                </div>
            </text>
            """
            ),
            etree.XML(
                """
                <text>
                  <p>
                    <floatingText>
                      <fw>text</fw>tail
                    </floatingText>
                  </p>
                </text>
                """
            ),
            etree.XML("<div><list/>tail</div>"),
            etree.XML("<div><table/>tail</div>"),
            etree.XML("<body><list/>tail</body>"),
            etree.XML("<body><table/>tail</body>"),
            etree.XML("<div><table><row><cell>text</cell></row></table>tail</div>"),
            etree.XML(
                "<div><div><p>text</p><list><item>text</item></list>tail</div></div>"
            ),
            etree.XML("<floatingText><table/>tail</floatingText>"),
            etree.XML("<floatingText><list/>tail</floatingText>"),
            etree.XML("<TEI xmlns='a'><body><div><table/>tail</div></body></TEI>"),
            etree.XML("<TEI xmlns='a'><body><div><list/>tail</div></body></TEI>"),
            etree.XML("<TEI xmlns='a'><div><div><p/><list/>tail</div></div></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/><table/>tail</body></TEI>"),
            etree.XML("<div><quote/>tail</div>"),
            etree.XML("<div><quote>text<p/></quote>tail</div>"),
            etree.XML("<div><p/><quote/>tail<p/></div>"),
            etree.XML("<TEI xmlns='a'><div><quote/>tail</div></TEI>"),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p>text</p>"),
            etree.XML("<text><p>text</p></text>"),
            etree.XML("<text><div><p>some text</p></div></text>"),
            etree.XML("<text><div><p>some text</p><p>and some more</p></div></text>"),
            etree.XML("<text><div><fw>heading</fw><p/></div></text>"),
            etree.XML(
                "<text><div><ab>heading</ab><p>some text</p><p>body</p></div></text>"
            ),
            etree.XML(
                "<text><div><ab>heading</ab><p>some text</p><p>body</p></div></text>"
            ),
            etree.XML("<text><body><div><p>text</p></div></body></text>"),
            etree.XML(
                """<TEI>
                <teiHeader/>
                <text><div><p/><p>text</p></div></text>
                </TEI>
                """
            ),
            etree.XML(
                """<TEI>
                <teiHeader/>
                    <text>
                         <div>
                             <p/>\n
                             <p>text</p>
                         </div>\n
                    </text>
                </TEI>
                """
            ),
            etree.XML(
                """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader/>
                <text><body><div><head/><p>text</p></div></body></text>
                </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns="http://www.tei-c.org/ns/1.0">
                <teiHeader/>
                <text><body><div>
                <p><fw/>text</p>
                <p>text</p>
                </div></body></text>
                </TEI>"""
            ),
            etree.XML(
                """<TEI>
                <teiHeader/>
                <text><body><div>
                <p><fw/>text</p>
                <p>text</p>
                </div></body></text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns="http://www.tei-c.org/ns/1.0">
                    <teiHeader/>
                    <text><body><div>
                    <p><fw><fw>text</fw>tail</fw>tail</p>
                    <p>text</p>
                    </div></body></text>
                </TEI>"""
            ),
            etree.XML("<teiHeader><p/>tail</teiHeader>"),
            etree.XML(
                """
                <text>
                    <div>
                      <p>
                        <list>
                          <item>
                            <p>text</p>tail
                          </item>
                         </list>
                      </p>
                    </div>
                </text>"""
            ),
            etree.XML(
                """
                <text>
                  <div>
                    <table>
                      <row>
                        <cell>
                          <p>text</p>tail
                        </cell>
                      </row>
                    </table>
                  </div>
                </text>
                """
            ),
            etree.XML("<text><div><quote><p>text</p>tail</quote></div></text>"),
            etree.XML(
                """
                <text>
                  <div>
                    <p>
                      <list>
                        <item>
                          <fw>text</fw>tail
                        </item>
                      </list>
                    </p>
                  </div>
                </text>
                """
            ),
            etree.XML("<div><p><table/>tail</p></div>"),
            etree.XML("<div><p>text<list/>tail</p></div>"),
            etree.XML("<div><list><item><list/>tail</item></list></div>"),
            etree.XML("<div><list/></div>"),
            etree.XML("<div><table/></div>"),
            etree.XML("<TEI xmlns='a'><body><table/></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><floatingText><list>text</list></floatingText></TEI>"
            ),
            etree.XML("<TEI xmlns='A'><div><p><list/></p><p>text</p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div>text<p><table/>tail</p></div></TEI>"),
            etree.XML("<div><p><quote/>tail</p></div>"),
            etree.XML("<div><p>text<quote>text<p/>tail</quote></p></div>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_tail_text_removed(self):
        root = etree.XML("<div><p/>tail</div>")
        self.observer.transform_node(root[0])
        self.assertIsNone(root[0].tail)

    def test_new_sibling_added(self):
        root = etree.XML("<div><p/>tail</div>")
        self.observer.transform_node(root[0])
        self.assertEqual(len(root.getchildren()), 2)

    def test_new_sibling_contains_tail_text(self):
        root = etree.XML("<div><p/>tail</div>")
        self.observer.transform_node(root[0])
        self.assertEqual(root[1].text, "tail")

    def test_tail_removed_on_namespaced_element(self):
        root = etree.XML(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0">
            <text><div><fw/>tail</div></text>
        </TEI>"""
        )
        node = root.find(".//{*}fw")
        self.observer.transform_node(node)
        self.assertIsNone(node.tail)

    def test_new_sibling_added_on_namespaced_element(self):
        root = etree.XML(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0">
            <text><div><fw/>tail</div></text>
        </TEI>"""
        )
        node = root.find(".//{*}fw")
        self.observer.transform_node(node)
        self.assertEqual(node.getnext().tag, "{http://www.tei-c.org/ns/1.0}p")

    def test_tail_added_to_new_sibling_on_namespaced_element(self):
        root = etree.XML(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0">
            <text><div><fw/>tail</div></text>
        </TEI>"""
        )
        node = root.find(".//{*}fw")
        self.observer.transform_node(node)
        self.assertEqual(node.getnext().text, "tail")

    def test_tail_text_in_floating_text_not_added_under_p(self):
        root = etree.XML(
            """
            <TEI>
              <teiHeader/>
              <text>
                <body>
                  <p>
                    <floatingText>
                      <fw>text</fw>tail>
                    </floatingText>
                  </p>
                </body>
              </text>
            </TEI>
            """
        )
        node = root.find(".//fw")
        self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//fw")), 2)

    def test_tail_from_original_element_not_transfered_to_new_sibling(self):
        root = etree.XML(
            """<TEI xmlns="http://www.tei-c.org/ns/1.0">
                    <text><div><fw/>tail</div></text>
                </TEI>"""
        )
        node = root.find(".//{*}fw")
        self.observer.transform_node(node)
        self.assertEqual(node.getnext().tail, None)
