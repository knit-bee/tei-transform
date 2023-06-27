import unittest

from lxml import etree

from tei_transform.observer import RowChildObserver


class RowChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = RowChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<row><p/></row>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<row><cell><p/></cell></row>")
        node = root.find(".//p")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<row><cell/><cell/><p>text</p></row>"),
            etree.XML("<table><row><cell/><p>  </p><cell/></row></table>"),
            etree.XML("<row><p>  </p><cell>text</cell></row>"),
            etree.XML("<row><p> text</p><cell/></row>"),
            etree.XML("<row><p>text</p></row>"),
            etree.XML("<table><row><cell>text</cell><p>  </p></row></table>"),
            etree.XML("<table><row><cell>text</cell><p>text</p></row></table>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><row><p/><cell/></row></text></TEI>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <table>
                        <row>
                            <cell>text</cell>
                            <p>  </p>
                        </row>
                    </table>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <table>
                        <row>
                            <cell>text</cell>
                            <p/>
                        </row>
                    </table>
                </TEI>
                """
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <table>
                        <row>
                            <cell><p>text</p>text</cell>
                            <p>text</p>
                        </row>
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
            etree.XML("<row><cell/></row>"),
            etree.XML("<row><cell><p>text</p></cell></row>"),
            etree.XML("<table><row><cell/></row><row><cell><p/></cell></row></table>"),
            etree.XML("<div><p/><table><row><cell/></row></table></div>"),
            etree.XML("<table><p/><row><cell/></row></table>"),
            etree.XML("<table><p>text</p><row><cell><p/></cell></row><fw/></table>"),
            etree.XML("<div><p><table><row><cell/></row></table></p></div>"),
            etree.XML(
                "<TEI xmlns='a'><table><row><cell><p/></cell></row></table></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><table><row><cell>text<p/></cell></row></table></div></TEI>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <teiHeader/>
                    <text>
                        <div>
                            <p>text</p>
                            <table>
                                <p>text</p>
                                <row>
                                    <cell>text</cell>
                                    <cell>
                                        <p>text</p>
                                    </cell>
                                </row>
                            </table>
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
