import unittest

from lxml import etree

from tei_transform.observer import DivTailObserver


class DivTailObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DivTailObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<body><div/>tail</body>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<body><div><p/>tail</div></body>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><div/>tail</div>"),
            etree.XML("<div><div><p/></div>tail</div>"),
            etree.XML("<div><p/><div/>tail</div>"),
            etree.XML("<div><div/>tail<list/></div>"),
            etree.XML("<body><div><p>text</p></div>tail</body>"),
            etree.XML("<div><div><list/>tail<p/></div>tail</div>"),
            etree.XML("<TEI xmlns='a'><body><div/>tail</body></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><table/></div>tail</TEI>"),
            etree.XML("<TEI xmlns='a'><div><p/><div><p/><div/>tail</div></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p/>tail</div>"),
            etree.XML("<div>text<div/></div>"),
            etree.XML("<div><p>text</p>tail</div>"),
            etree.XML("<body><div><list/>tail<p/>tail</div></body>"),
            etree.XML("<body><div><div>text<p/>tail</div><div/></div></body>"),
            etree.XML(
                "<body><div>text<p/>tail<div>text<table/>tail</div><p/></div></body>"
            ),
            etree.XML("<body><div>text<div/></div><div>a<p/>tail<p/>tail</div></body>"),
            etree.XML("<div>text<p/>tail<div/><div/><table/>tail</div>"),
            etree.XML(
                "<TEI xmlns='a'><body><div>text<p/>tail<div/></div></body></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><div><p>text<hi/>tail</p><div/></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><div>text<p/>tail<div>a<table/>b</div></div></body></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
