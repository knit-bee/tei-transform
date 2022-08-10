import unittest

from lxml import etree

from tei_transform.tail_text_observer import TailTextObserver


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
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
