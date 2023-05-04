import unittest

from lxml import etree

from tei_transform.observer import HeadChildObserver


class HeadChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HeadChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<head><p>text</p></head>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><head/><p/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><head>text<hi/><p/></head></div>"),
            etree.XML("<body><head>text<ab>text</ab></head><p/></body>"),
            etree.XML("<div><p/><head>a<p>b</p>c</head><list/></div>"),
            etree.XML("<body><head/><head>text<ab>text</ab>tail</head><head/></body>"),
            etree.XML(
                "<body><div><head><p/></head></div><div><head/><p/></div></body>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><head>ab<p>c</p>d</head><list/></div></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><div><head><quote/><ab/>tail</head></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><head><quote/></head><p/><ab/></div>"),
            etree.XML("<div><p/><head><hi>text</hi></head><p/></div>"),
            etree.XML("<div><p>text</p><div><head><del/></head><p/></div></div>"),
            etree.XML("<body><head/><p/><ab/></body>"),
            etree.XML("<body><div><head><list/></head><p/></div></body>"),
            etree.XML("<div><head/><p><list><head/><item/></list></p><p/></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><head/><p/><ab/><div><head/></div></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><ab/><head>text<hi/></head><p/></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
