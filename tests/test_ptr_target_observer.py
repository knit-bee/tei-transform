import unittest

from lxml import etree

from tei_transform.observer import PtrTargetObserver


class PtrTargetObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = PtrTargetObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<ptr target=''/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<ptr target='link'/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML(
                "<publicationStmt><publisher/><ptr target=''/></publicationStmt>"
            ),
            etree.XML("<date>text<ptr target='' type='sth'/></date>"),
            etree.XML("<p>text<ptr target=''/></p>"),
            etree.XML("<name>text<ptr target=''/></name>"),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><publisher/><ptr target=''/></publicationStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<ptr target='' type='b'/>text</p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><titleStmt><title>text<ptr target=''/></title></titleStmt></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<name>text<ptr target='link'/></name>"),
            etree.XML(
                "<publicationStmt><publisher/><ptr target='link' type='b'/></publicationStmt>"
            ),
            etree.XML("<p>text<ptr type='b' target='#123'/></p>"),
            etree.XML(
                "<TEI xmlns='a'><div><p>text<ptr type='b' attr='val' target='sth'/>tail</p></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><publicationStmt><publisher/><date/><ptr target='a'/></publicationStmt></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><list><item>text<ptr target='#p1' cRef='b'/></item></list></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_remove_attribute(self):
        root = etree.XML("<p>text<ptr target=''/></p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_remove_attribute_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><publicationStmt><publisher/><ptr target='>'/></publicationStmt></TEI>"
        )
        node = root.find(".//{*}ptr")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed(self):
        root = etree.XML("<p><ptr type='sth' attr='val' target=''/></p>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val", "type": "sth"})
