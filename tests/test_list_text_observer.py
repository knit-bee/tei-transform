import unittest

from lxml import etree

from tei_transform.observer import ListTextObserver


class ListTextObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = ListTextObserver()

    def test_observer_returns_true_for_matching_node(self):
        root = etree.XML("<div><list>text<item/></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        root = etree.XML("<div><list><item>text</item></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<list>text</list>"),
            etree.XML("<list>text<item>text</item></list>"),
            etree.XML("<list><item/>text</list>"),
            etree.XML("<list><item/><item/>text</list>"),
            etree.XML("<div><p/><list><item/>text</list></div>"),
            etree.XML("<div><p/><list>text<item/>text</list><p/></div>"),
            etree.XML("<div><list><item><list>text</list></item></list></div>"),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>text</item>
                        text2
                        <item>text3</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        text
                        <item>text</item>
                        text2
                        <item>text3</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>
                          <list>text
                            <item/>
                            <item/>
                          </list>
                        </item>
                        <item>text3</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <table>
                        <row>
                          <cell>
                            <list>text
                              <item/>
                              <item/>
                            </list>
                          </cell>
                        </row>
                      </table>
                      <p>text</p>
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

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<list/>"),
            etree.XML("<list><item/></list>"),
            etree.XML("<list><item>text</item></list>"),
            etree.XML("<list><item/><item/><item/></list>"),
            etree.XML("<div><p>text<list><item/></list></p></div>"),
            etree.XML("<div><list><item/></list><p>text</p></div>"),
            etree.XML("<div><p/><list><item>text</item></list><p>text</p></div>"),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>text</item>
                        <item>text</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text</p>
                      <list>
                        <item>
                          <list>
                            <item>text</item>
                            <item/>
                          </list>
                        </item>
                        <item>text</item>
                      </list>
                      <p>text</p>
                    </div>
                  </text>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='ns'>
                  <teiHeader/>
                  <text>
                    <div>
                      <p>text
                      <list>
                        <item>text</item>
                        <item>text2</item>
                      </list>
                      <list>
                        <item>text</item>
                      </list>
                      text</p>
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
