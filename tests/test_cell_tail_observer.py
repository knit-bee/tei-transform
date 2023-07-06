import unittest

from lxml import etree

from tei_transform.observer import CellTailObserver


class CellTailObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = CellTailObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<row><cell/>tail</row>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<row><cell/>  </row>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<row><cell>text</cell>tail</row>"),
            etree.XML("<row><cell/><cell/>tail</row>"),
            etree.XML("<table><row><cell>a</cell>b</row></table>"),
            etree.XML("<table><row><cell/>a<cell/></row><row><cell/></row></table>"),
            etree.XML(
                "<table><row><cell/></row><row><cell><p/>a</cell>b</row></table>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><table><row><cell>a</cell>b</row></table></div></TEI>"
            ),
            etree.XML(
                """
                <TEI xmlsn='a'>
                    <div>
                        <table>
                        text
                        <row>
                            <cell>text
                                <p>text2</p>tail
                            </cell>tail
                            <cell>text</cell>
                        </row>tail
                        </table>
                    </div>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <text>
                        <div>
                            <table>
                                <row/>
                                <row>
                                    <cell>
                                        <hi>text</hi>
                                    </cell>
                                    <cell/>
                                </row>
                                <row>
                                    <cell/>
                                    <cell>text</cell>tail
                                </row>
                            </table>
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

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<row><cell>text<p/>tail</cell></row>"),
            etree.XML("<row><cell><cell/>\n  </cell></row>"),
            etree.XML("<table><row><cell>text</cell></row>tail</table>"),
            etree.XML("<table><row><cell><cell/>  \n\t </cell></row><fw/>tail</table>"),
            etree.XML("<row><cell><p/>a</cell></row>"),
            etree.XML(
                "<TEI xmlns='a'><table><row><cell/><cell>text</cell></row></table></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><table><row><cell/><cell><hi>text</hi>ab</cell></row></table></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><table><row><cell><cell>text</cell>\t\n  </cell></row></table></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><table>text<row><cell/><cell>text</cell></row>tail</table></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
