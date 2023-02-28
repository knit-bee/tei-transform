import unittest

from lxml import etree

from tei_transform.observer import ChildlessBodyObserver


class ChildlessBodyObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = ChildlessBodyObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<body/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<body><div/></body>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<text><body></body></text>"),
            etree.XML("<text><front/><body/></text>"),
            etree.XML("<text><body>  </body></text>"),
            etree.XML("<text><body>abc</body></text>"),
            etree.XML("<text><front/><body/>tail<back/></text>"),
            etree.XML("<div><p><floatingText><body/></floatingText></p></div>"),
            etree.XML("<TEI xmlns='a'><text><body/></text></TEI>"),
            etree.XML("<TEI xmlns='a'><teiHeader/><text><body>  </body></text></TEI>"),
            etree.XML("<TEI xmlns='a'><text><front/><body/><back/></text></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><text><floatingText><body/></floatingText></text></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<text><body><p/></body></text>"),
            etree.XML("<text><front/><body><p/></body><back/></text>"),
            etree.XML("<text><body>abc<p/></body></text>"),
            etree.XML("<div><floatingText><body><div/></body></floatingText></div>"),
            etree.XML("<text><front/>tail<body>text<p/>tail</body>tail</text>"),
            etree.XML(
                "<TEI xmlns='a'><teiHeader/><text><body><div/></body></text></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><text><body><list/></body><back/></text></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><text><div><floatingText><body><p/></body></floatingText></div></text></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
