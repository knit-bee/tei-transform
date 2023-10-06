import unittest

from lxml import etree

from tei_transform.observer import HLevelObserver


class HLevelObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HLevelObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p/><h2>text</h2></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><hi/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><h3><lb/>text</h3></div>"),
            etree.XML("<div><p/><h4>text</h4><p/></div>"),
            etree.XML("<div><p/><h5 class='sth'><lb/></h5></div>"),
            etree.XML("<div><h6 title='sth'><lb/>text</h6><p/></div>"),
            etree.XML("<body><div><p/><h7>text</h7></div></body>"),
            etree.XML("<div><h8/><p/></div>"),
            etree.XML("<TEI xlmns='a'><body><div><h2>ab</h2><p/></div></body></TEI>"),
            etree.XML(
                "<TEI xlmns='a'><body><div><h3 class='sth'><lb/>ab</h3><p/></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xlmns='a'><body><div><p/><h4>ab</h4><p/></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xlmns='a'><body><div><p/><h5><lb/></h5><p/></div></body></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p><hi/></p></div>"),
            etree.XML("<div><p/><hi/><p/></div>"),
            etree.XML("<div><head>txt</head><p>ab</p></div>"),
            etree.XML("<div><hi/><p/></div>"),
            etree.XML(
                "<TEI xlmns='a'><body><div><head>ab</head><p/></div></body></TEI>"
            ),
            etree.XML("<TEI xlmns='a'><body><div><hi>ab</hi><p/></div></body></TEI>"),
            etree.XML(
                "<TEI xlmns='a'><body><div><p><hi>ab</hi></p><p/></div></body></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
