import unittest
from lxml import etree

from tei_transform.list_as_div_sibling_observer import ListAsDivSiblingObserver


class ListAsDivSiblingObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = ListAsDivSiblingObserver()

    def test_observer_returns_true_for_matching_element(self):
        p_node = etree.XML("<body><div/><list/></body>")[1]
        result = self.observer.observe(p_node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        p_node = etree.XML("<body><div><list/></div></body>")[0][0]
        result = self.observer.observe(p_node)
        self.assertEqual(result, False)

    def test_obserer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><div/><list/></div>"),
            etree.XML("<body><div/><list></list></body>"),
            etree.XML("<body><div/><list><item/></list></body>"),
            etree.XML("<div><div/><div><div/></div><list/></div>"),
            etree.XML(
                """<div><div><list/></div>
            <p>some text</p>
            <list>
            <item>more text</item>
            </list>
            </div>"""
            ),
            etree.XML(
                """<text>
                <body>
                  <div>
                    <div>
                      <fw rend="h1" type="header">header</fw>
                      <div>
                        <p>Some text</p>
                      </div>
                      <div/>
                      <list/>
                    </div></div></body></text>"""
            ),
            etree.XML(
                """<text>
                    <body>
                      <div type="entry">
                        <fw rend="h1" type="header">heading </fw>
                        <div>
                          <list><item/><item/></list>
                        </div>
                        <list/>
                        </div></body></text>"""
            ),
            etree.XML(
                """
            <TEI>
            <teiHeader/>
            <text>
            <body>
              <div type="entry">
                <fw rend="h1" type="header">heading </fw>
                <div>
                  <p/>
                </div>
                <list/>
                </div>
            </body></text>
            </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='namespace'>
                <teiHeader/>
                <text>
                <body>
                  <div type="entry">
                    <fw rend="h1" type="header">heading </fw>
                    <div>
                      <p>text
                      <lb/>more text
                      </p>
                    </div>
                    <list/>
                    </div>
                </body></text>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertTrue(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><list/></div>"),
            etree.XML("<div><div><list/></div></div>"),
            etree.XML(
                "<div><list><item>some text</item><item>more text</item></list></div>"
            ),
            etree.XML("<body><div><list><item/></list></div><div><list/></div></body>"),
            etree.XML("<text><body><div><list/><p/><list/></div></body></text>"),
            etree.XML(
                """<div>
            <div><p>text</p></div>
            <div><list><item/></list></div>
            <div><div><list/></div></div>
            </div>"""
            ),
            etree.XML(
                """
                <TEI>
                <teiHeader/>
                <text>
                <body>
                  <div type="entry">
                    <div>
                      <list/>
                    </div>
                    </div>
                </body></text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='namespace'>
                <teiHeader/>
                <text>
                <body>
                  <div>
                    <fw rend="h1" type="header">heading </fw>
                    <div>
                      <p>text</p>
                      <list><item/></list>
                    </div>
                    <div>
                     <list/>
                    </div>
                    </div>
                </body></text>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
