import unittest

from lxml import etree

from tei_transform.observer import UnfinishedElementObserver


class UnfinishedElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = UnfinishedElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><table><head/></table></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><table><row/></table></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><list><head/></list></div>"),
            etree.XML("<div><table><head>text</head></table></div>"),
            etree.XML("<div><list><byline/></list></div>"),
            etree.XML("<div><list><note/></list></div>"),
            etree.XML("<div><list><fw/></list></div>"),
            etree.XML("<div><table><index/></table></div>"),
            etree.XML("<div><table><byline/></table></div>"),
            etree.XML("<div><table><index/></table></div>"),
            etree.XML("<TEI xmlns='a'><table><head/></table></TEI>"),
            etree.XML("<TEI xmlns='a'><list><head/></list></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><table><head/></table></div></TEI>"),
            etree.XML("<TEI xmlns='a'><p>text<table><byline/></table></p></TEI>"),
            etree.XML("<TEI xmlns='a'><div><list><head/></list></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<table><head/></table></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<list><byline/></list></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><table><head/><row/></table></div>"),
            etree.XML("<div><table><row/></table></div>"),
            etree.XML("<div><table></table></div>"),
            etree.XML("<div><list><head/><item/></list></div>"),
            etree.XML("<div><table><head/><fw/><row/><row/></table></div>"),
            etree.XML("<div><table><row><cell/></row><byline/></table></div>"),
            etree.XML("<div><p><list><head/><item>text</item></list></p></div>"),
            etree.XML("<TEI xmlns='a'><div><table><head/><row/></table></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><list><head/><item/></list></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<table><head/><row/></table></p></div></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><div><p>text<list/></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p>text<table/></p></div></TEI>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <p>text
                      <table>
                        <row>
                          <cell>
                            <list/>
                          </cell>
                        </row>
                      </table>
                    </p>
                  </div>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
