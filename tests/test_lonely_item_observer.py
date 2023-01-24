import unittest

from lxml import etree

from tei_transform.observer import LonelyItemObserver


class LonelyItemObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LonelyItemObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<p><item/></p>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<list><item/></list>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p><item>text</item></p>"),
            etree.XML("<ab><item/>tail</ab>"),
            etree.XML("<div><item><list><item/></list></item></div>"),
            etree.XML("<p>text<item/>tail</p>"),
            etree.XML("<div><p>text<item>text</item></p></div>"),
            etree.XML("<p><item><item/></item></p>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <p>text
                      <hi>text</hi>
                      <item>text</item>
                    </p>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <item>
                      <list>
                        <item>text</item>
                        <item>text</item>
                      </list>
                    </item>
                    <p/>
                    <ab/>
                  </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <p/>
                    <table>
                      <row>
                        <cell>
                          <item>text</item>
                        </cell>
                      </row>
                    </table>
                    <ab/>
                    <list>
                      <item>text</item>
                    </list>
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
            etree.XML("<list><item>text</item></list>"),
            etree.XML("<list><item>text</item><item/><item/></list>"),
            etree.XML("<div><list><item/></list></div>"),
            etree.XML("<p><list><item>text<list/></item></list></p>"),
            etree.XML(
                "<p><list><item>text<list><item>text</item><item/></list></item></list></p>"
            ),
            etree.XML("<p><list>text<item/>tail</list></p>"),
            etree.XML("<div><p/><list><item rend='ol'>text</item></list></div>"),
            etree.XML("<div><list attr='val'><item>text<table/></item></list></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                    <div>
                      <head>text</head>
                      <list attr='val'>
                        <item>text</item>
                        <item>text</item>
                        <item>text</item>
                      </list>
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
                      <list attr='val'>
                        <item>text</item>
                        <item>text</item>
                        <item>
                          <list>
                            <item/>
                            <item/>
                          </list>
                        </item>
                      </list>
                      <p>text</p>
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
