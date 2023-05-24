import unittest

from lxml import etree

from tei_transform.observer import TableChildObserver


class TableChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TableChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<table><row/><p/></table>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<table><row><cell><p/></cell></row></table>")
        node = root.find(".//p")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<table><row/><p>text</p></table>"),
            etree.XML("<div><table><row/><p>text</p><row/></table></div>"),
            etree.XML("<table>text<row><cell>text</cell></row><p/></table>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <row>
                        <cell>text</cell>
                      </row>
                      <p>text</p>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML("<table><head/><p>text<hi/></p><row/></table>"),
            etree.XML("<table><p>text</p>tail<row/></table>"),
            etree.XML("<div><table><row/><p/>tail</table></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <table>
                        <head/>
                        <row>
                            <cell/>
                            <cell/>
                        </row>
                        <p>
                            <hi>text</hi>
                        </p>
                    </table>
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
            etree.XML("<table><row><cell><p/></cell></row></table>"),
            etree.XML("<div><p><table><row/></table></p></div>"),
            etree.XML("<div><table><row><p/></row></table><p/></div>"),
            etree.XML("<div><p><table/></p><table/></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><p/><table><row><cell/></row></table></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><table><head/><row><cell><p/>tail</cell></row></table></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><table><row/><fw/></table><p>text</p>tail</div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
