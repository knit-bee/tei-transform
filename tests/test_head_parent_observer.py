import unittest

from lxml import etree

from tei_transform.observer import HeadParentObserver


class HeadParentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HeadParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<item><head>text</head></item>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><head>text</head></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<p>text<head>text2</head></p>"),
            etree.XML("<ab>text<head>text2</head>text3</ab>"),
            etree.XML("<div><head>text<head>text2</head></head></div>"),
            etree.XML(
                "<div><list><item><head rendition='i'>text</head></item></list></div>"
            ),
            etree.XML(
                "<body><head/><p/><ab type='sth'>text<head rendition='a'>text2</head>text</ab></body>"
            ),
            etree.XML("<div><p>text<hi>ab<head>cd</head>text</hi></p></div>"),
            etree.XML("<div><p/><head>a<head/>b</head>c</div>"),
            etree.XML("<TEI xmlns='a'><div><p>a<list/><head/>b<p/></p></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><ab>text<head/></ab></div></TEI>"),
            etree.XML(
                "<TEI xmlsn='a'><div><list><item>a<head/>b</item></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>a<hi>b<head>c</head>d</hi></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><head>text</head><p/></div>"),
            etree.XML("<div><p/><p/><head><hi/></head></div>"),
            etree.XML("<div><list><head/><item/></list></div>"),
            etree.XML("<div><head/><ab/><p/></div>"),
            etree.XML("<div><head>text<hi rendition='i'>b</hi></head><p/></div>"),
            etree.XML("<div><p/><head rendition='b'>text</head>tail<ab/></div>"),
            etree.XML("<TEI xmlsn='a'><div><head>text</head><p/></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><list><head/><item><p/></item></list></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='A'><div><p/></div><div><head>a<hi>b</hi></head><p/></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
