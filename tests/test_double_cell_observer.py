import unittest

from lxml import etree

from tei_transform.double_cell_observer import DoubleCellObserver


class DoubleCellObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DoubleCellObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<cell><cell/></cell>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<cell><p/></cell>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<cell><cell></cell></cell>"),
            etree.XML("<cell><cell>text</cell></cell>"),
            etree.XML("<row><cell><cell>text</cell><p/></cell></row>"),
            etree.XML("<row><cell>text</cell><cell><cell>text</cell></cell></row>"),
            etree.XML(
                "<table><row><cell>text</cell></row><row><cell><cell>text</cell></cell></row></table>"
            ),
            etree.XML("<cell><cell>text</cell><fw>more text</fw></cell>"),
            etree.XML("<div><p/><table><row><cell><cell/></cell></row></table></div>"),
            etree.XML(
                """<TEI><teiHeader/>
            <text><body>
                <table><row><cell><cell>text</cell><p/></cell><cell/></row><row/></table>
            </body>
            </text></TEI>
            """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                        <table><row><cell><cell>text</cell><p/></cell><cell/></row><row/></table>
                    </body>
                    </text></TEI>
                        """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<cell><p></p></cell>"),
            etree.XML("<cell><p>text</p></cell>"),
            etree.XML("<row><cell><p>text</p><p/></cell><cell/></row>"),
            etree.XML("<row><cell>text</cell><cell><p>text</p></cell></row>"),
            etree.XML(
                "<table><row><cell>text</cell></row><row><cell><p>text</p></cell></row></table>"
            ),
            etree.XML("<cell><p>text</p><fw>more text</fw></cell>"),
            etree.XML(
                "<div><p/><table><row><cell><p/></cell><cell/></row></table></div>"
            ),
            etree.XML(
                """<TEI><teiHeader/>
                    <text><body>
                        <table><row><cell>text<p/></cell><cell/></row><row/></table>
                    </body>
                    </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                        <table><row><cell><p>text</p><p/></cell><cell/></row><row/></table>
                    </body>
                    </text></TEI>
                        """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
