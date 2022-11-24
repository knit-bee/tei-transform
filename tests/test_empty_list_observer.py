import unittest

from lxml import etree

from tei_transform.observer import EmptyListObserver


class EmptyListObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyListObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><list/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><list><item/></list></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<list/>"),
            etree.XML("<div><list/><list><item/></list></div>"),
            etree.XML("<div><list><item><list/></item></list></div>"),
            etree.XML("<ab><list></list></ab>"),
            etree.XML("<p><list/>text</p>"),
            etree.XML("<p>text<list/>more text</p>"),
            etree.XML("<div><p>text<list/>more text</p></div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                <text><body>
                <list/>
                </body>
                </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <list></list>
                            </body>
                            </text></TEI>
                                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <div><p>text</p>
                            <list/>
                            </div>
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
            etree.XML("<list><item/></list>"),
            etree.XML("<list><item>text</item></list>"),
            etree.XML("<div><list><item/></list></div>"),
            etree.XML(
                "<div><list><item><list><item>text</item></list></item></list></div>"
            ),
            etree.XML("<ab><list><item/></list></ab>"),
            etree.XML("<p><list><item>text</item></list>text</p>"),
            etree.XML("<p>text<list><item>item text</item></list>more text</p>"),
            etree.XML("<div><p>text<table/>more text</p></div>"),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                <text><body>
                <list>
                  <item/>
                </list>
                </body>
                </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <list><item>text</item></list>
                            </body>
                            </text></TEI>
                                """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                            <text><body>
                            <div><p>text</p>
                            <list>
                            <item>text</item></list>
                            </div>
                            </body>
                            </text></TEI>
                                """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
