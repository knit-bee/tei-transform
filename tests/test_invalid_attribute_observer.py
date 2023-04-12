import unittest

from lxml import etree

from tei_transform.observer import InvalidAttributeObserver


class InvalidAttributeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = InvalidAttributeObserver({"target": {"p"}})

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><elem1 target='val'/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><p target='val'/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><p><elem1 target='val'/></p></div>"),
            etree.XML("<p><elem2 attr='a' target='b'>text</elem2></p>"),
            etree.XML("<list><item><elem1 target='val'>a</elem1></item></list>"),
            etree.XML("<TEI xmlns='a'><div><elem2 target='b'>a</elem2></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><p><elem1/><elem2 target='a' attr='b'>c</elem2></p></div></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p target='a'>text</p></div>"),
            etree.XML("<div><elem1>text</elem1></div>"),
            etree.XML("<div><elem2 attr='val'/></div>"),
            etree.XML("<TEI xlmns='a'><div><elem1/><elem2 attr='a'/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p target='a'>text</p></div></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><div><elem1 attr='val'>text<elem2/></elem1></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_all_elements_ignored_if_observer_not_configured(self):
        observer = InvalidAttributeObserver()
        root = etree.XML("<div><p><list><item attr='val'/></list></p></div>")
        result = {observer.observe(node) for node in root.iter()}
        self.assertEqual(result, {False})

    def test_configure_observer(self):
        observer = InvalidAttributeObserver()
        cfg = {"first": "elem1", "second": "elem2, elem1", "third": ""}
        observer.configure(cfg)
        self.assertEqual(
            observer.target_attributes,
            {"first": {"elem1"}, "second": {"elem1", "elem2"}, "third": set()},
        )

    def test_observer_not_configured_if_config_wrong(self):
        observer = InvalidAttributeObserver()
        cfg = {}
        observer.configure(cfg)
        self.assertIsNone(observer.target_attributes)

    def test_invalid_config_triggers_logger_warning(self):
        observer = InvalidAttributeObserver()
        cfg = {}
        with self.assertLogs() as logger:
            observer.configure(cfg)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.invalid_attribute_observer:"
                "Invalid configuration for InvalidAttributeObserver."
            ],
        )

    def test_invalid_attribute_removed(self):
        root = etree.XML("<div><elem1 target='val'>text</elem1></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_invalid_attribute_removed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><p><elem2 target='a'>text</elem2></p></div></TEI>"
        )
        node = root.find(".//{*}elem2")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_multiple_invalid_attributes_removed_from_element(self):
        observer = InvalidAttributeObserver({"first": {}, "second": {}})
        root = etree.XML("<div><elem1 first='val' second='val2'>text</elem1></div>")
        node = root[0]
        observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed(self):
        root = etree.XML("<div><elem1 target='val' attr='val2'>text</elem1></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val2"})

    def test_non_matching_targets_not_removed(self):
        observer = InvalidAttributeObserver({"first": {}, "second": {"elem1"}})
        root = etree.XML("<div><elem1 first='val' second='val2'>text</elem1></div>")
        node = root[0]
        observer.transform_node(node)
        self.assertEqual(node.attrib, {"second": "val2"})
