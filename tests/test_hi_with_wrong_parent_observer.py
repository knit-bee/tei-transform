import unittest

from lxml import etree

from tei_transform.observer import HiWithWrongParentObserver


class HiOutsidePObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HiWithWrongParentObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<body><hi/></body>")
        result = self.observer.observe(root[0])
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<body><p><hi/></p></body>")
        result = self.observer.observe(root[0])
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><hi>text</hi></div>"),
            etree.XML("<body><hi/></body>"),
            etree.XML("<body><p/><hi/></body>"),
            etree.XML("<div1><hi/></div1>"),
            etree.XML("<div2><hi/></div2>"),
            etree.XML("<div3><hi/></div3>"),
            etree.XML("<div4><hi/></div4>"),
            etree.XML("<div5><hi/></div5>"),
            etree.XML("<div6><hi/></div6>"),
            etree.XML("<div7><hi/></div7>"),
            etree.XML("<body><div><hi>text</hi><p/></div></body>"),
            etree.XML("<TEI><teiHeader/><text><body><hi/><p/></body></text></TEI>"),
            etree.XML(
                "<TEI xmlns='namespace'><teiHeader/><text><body><hi/><p/></body></text></TEI>"
            ),
            etree.XML(
                "<TEI><teiHeader/><text><body><div><hi/><p/></div></body></text></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p><hi/></p>"),
            etree.XML("<fw><hi/></fw>"),
            etree.XML("<div><p>text text <hi rend='#i'>text</hi></p></div>"),
            etree.XML("<div><p><hi/></p></div>"),
            etree.XML("<classCode><hi/></classCode>"),
            etree.XML("<ab><hi/></ab>"),
            etree.XML("<TEI><teiHeader/><text><body><p><hi/></p></body></text></TEI>"),
            etree.XML(
                "<TEI xmlns='namespace'><teiHeader/><text><body><p><hi/></p></body></text></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
