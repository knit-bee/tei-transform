import unittest

from lxml import etree

from tei_transform.head_element_observer import HeadElementObserver


class HeadElementObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HeadElementObserver()

    def test_observer_returns_true_for_matching_element(self):
        tree = etree.XML("<body><p/><head></head></body>")
        node = tree[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        tree = etree.XML("<div><head/><p/></div>")
        node = tree[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        matching_elements = [
            etree.XML("<div><p>text</p><head/></div>"),
            etree.XML("<div><p/><head></head><p/></div>"),
            etree.XML("<TEI><text><body><p/><head/></body></text></TEI>"),
            etree.XML("<div><p/><head rendition='#b'></head></div>"),
            etree.XML(
                "<TEI><text><body><div><head/><p/><head/><p/></div></body></text></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
            # <text>
            # <body><p/><head>text</head><p/></body>
            # </text>
            # </TEI>"""
            ),
        ]
        for element in matching_elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        non_matching_elements = [
            etree.XML("<div><head/></div>"),
            etree.XML("<div1><head>text</head></div1>"),
            etree.XML("<div><head/></div>"),
            etree.XML("<div1><div2><head/></div2></div1>"),
            etree.XML("<div><head/><p/></div>"),
            etree.XML("<text><body><div><head/><p/></div></body></text>"),
            etree.XML(
                """<TEI xmlns='http://www.tei-c.org/ns/1.0'>
        <text>
        <body><div><head>text</head></div><p/></body>
        </text>
        </TEI>"""
            ),
        ]
        for element in non_matching_elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual((result), {False})
