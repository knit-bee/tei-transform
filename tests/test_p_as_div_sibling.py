import unittest

from lxml import etree

from tei_transform.p_as_div_sibling_observer import PAsDivSiblingObserver


class PAsDivSiblingObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = PAsDivSiblingObserver()

    def test_observer_returns_true_for_matching_node(self):
        p_node = etree.XML("<body><div/><p/></body>")[1]
        result = self.observer.observe(p_node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_nodes(self):
        p_node = etree.XML("<body><div><p/></div></body>")[0][0]
        result = self.observer.observe(p_node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        matching_elements = [
            etree.XML("<body><div/><p>text</p></body>"),
            etree.XML("<div><div/><p/></div>"),
            etree.XML("<body><div><p>text></p></div><p>more text></p></body>"),
            etree.XML("<div><div/><div><div/></div><p/></div>"),
            etree.XML(
                """<div><div><p/></div>
                <p>some text</p>
                <p>more text</p>
                <p>more text that shouldn't be here</p>
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
          <p>new paragraph</p>
        </div></div></body></text>"""
            ),
            etree.XML(
                """<text>
    <body>
      <div type="entry">
        <fw rend="h1" type="header">heading </fw>
        <div>
          <p>text
          <lb/>more text
          </p>
        </div>
        <p/>
        </div></body></text>
"""
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
              <p>text
              <lb/>more text
              </p>
            </div>
            <p/>
            </div>
        </body></text>
        </TEI>
"""
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
            <p/>
            </div>
        </body></text>
        </TEI>
"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertTrue(any(result))

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div></div>"),
            etree.XML("<div><div><p/></div></div>"),
            etree.XML("<div><p>some text</p><p>more text</p></div>"),
            etree.XML(
                "<body><div><p>text></p></div><div><p>more text></p></div></body>"
            ),
            etree.XML("<text><body><div><p/><p/><p/></div></body></text>"),
            etree.XML(
                """<div>
                <div><p>text</p></div>
                <div><p>more text</p></div>
                <div><div><p/></div></div>
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
                  <p>text</p>
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
          <p>text
          <lb/>more text
          </p>
        </div>
        <div>
        <p/>
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
