import unittest

from lxml import etree

from tei_transform.observer import DoublePlikeObserver


class ObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DoublePlikeObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p><p>text</p></p></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><quote><p>text</p></quote></div>")
        node = root[0][0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><p><p/></p></div>"),
            etree.XML("<div><ab><p/></ab></div>"),
            etree.XML("<div><p><ab/></p></div>"),
            etree.XML("<div><ab><ab/></ab></div>"),
            etree.XML("<div><p>text<list/><p>text</p></p></div>"),
            etree.XML("<div><p>text<table/><p>text</p><table/></p></div>"),
            etree.XML("<div><p>text<list/><ab>text</ab></p></div>"),
            etree.XML("<div><p>text<list/><ab><hi>text</hi></ab></p></div>"),
            etree.XML("<div><ab>text<quote/><p>text</p></ab></div>"),
            etree.XML("<div><ab>text<list/><p>text</p><quote/></ab></div>"),
            etree.XML(
                "<table><row><cell><p>text</p><p><ab>text</ab></p></cell></row></table>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><p><ab>text</ab>text<list/></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><p><p><hi>text</hi></p>text<list/></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab><ab>text<list/></ab>text</ab></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab>ab<p>text<list/>c</p>text</ab></div></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                  <div>
                    <p>text</p>
                    <ab>text<p>
                      <table>
                        <row>
                          <cell/>
                        </row>
                      </table>
                      </p>
                    </ab>
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
            etree.XML("<p><quote><ab>text</ab></quote></p>"),
            etree.XML("<div><p/><p>text<fw><p>text</p></fw></p></div>"),
            etree.XML(
                "<div><ab>text<table><row><cell><p/></cell></row></table></ab></div>"
            ),
            etree.XML("<div><p/><ab/><p/></div>"),
            etree.XML("<div><ab><list><item><p>text</p></item></list></ab></div>"),
            etree.XML("<div><ab>text<quote>text<ab/>tail</quote></ab></div>"),
            etree.XML("<div><p><hi/></p><ab/></div>"),
            etree.XML(
                "<TEI xmlns='ns'><div><p>text<quote><ab/></quote></p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab><list><p>text</p></list></ab></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='ns'><div><ab>text</ab><p>text<fw/>tail</p></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
