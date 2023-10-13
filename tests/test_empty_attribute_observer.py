import unittest

from lxml import etree

from tei_transform.observer import EmptyAttributeObserver


class EmptyAttributeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyAttributeObserver(["atr1"])

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><p atr1=''/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><p atr1='sth'/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<div><p/><p atr1=''/></div>"),
            etree.XML("<div><title atr1=''/></div>"),
            etree.XML("<div><elem1 atr2='sth' atr1=''/></div>"),
            etree.XML("<div><p target='' atr1=''/></div>"),
            etree.XML("<TEI xmlns='a'><title atr1=''>text</title></TEI>"),
            etree.XML("<TEI xmlns='a'><div><p atr2='sth' atr1=''/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div atr1='b'><p atr1=''>c</p></div></TEI>"),
        ]

        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<p atr1='a'/>"),
            etree.XML("<div><p>text</p></div>"),
            etree.XML("<div><p atr1='a' atr2=''>text</p></div>"),
            etree.XML("<div><atr1></atr1></div>"),
            etree.XML("<TEI xmlns='a'><div><p atr1='b'/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><elem1 atr1='b' atr2=''/></div></TEI>"),
            etree.XML("<TEI xmlns='a'><div><atr1/></div></TEI>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_configure_observer(self):
        observer = EmptyAttributeObserver()
        cfg = {"target": "first, second, third"}
        observer.configure(cfg)
        self.assertEqual(observer.target_attributes, ["first", "second", "third"])

    def test_observer_not_configured_if_config_wrong(self):
        observer = EmptyAttributeObserver()
        cfg = {}
        observer.configure(cfg)
        self.assertEqual(observer.target_attributes, [])

    def test_invalid_config_triggers_logger_warning(self):
        observer = EmptyAttributeObserver()
        cfg = {}
        with self.assertLogs() as logger:
            observer.configure(cfg)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.empty_attribute_observer:"
                "Invalid configuration for EmptyAttributeObserver."
            ],
        )

    def test_all_elements_ignored_if_observer_not_configured(self):
        observer = EmptyAttributeObserver()
        root = etree.XML("<div atr1=''><p atr2=''><title atr3=''>a</title></p></div>")
        result = {observer.observe(node) for node in root.iter()}
        self.assertEqual(result, {False})

    def test_empty_attribute_removed(self):
        root = etree.XML("<div><elem1 atr1=''>text</elem1></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_empty_attribute_removed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><p><elem atr1=''>text</elem></p></div></TEI>"
        )
        node = root.find(".//{*}elem")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_multiple_empty_attributes_removed_from_element(self):
        observer = EmptyAttributeObserver(["first", "second"])
        root = etree.XML("<div><elem1 first='' second=''>text</elem1></div>")
        node = root[0]
        observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_other_attributes_not_removed(self):
        root = etree.XML("<div><elem atr1='' attr='val'>text</elem></div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"attr": "val"})

    def test_non_matching_targets_not_removed(self):
        observer = EmptyAttributeObserver(["first", "second"])
        root = etree.XML("<div><elem first='' second='val2'>text</elem></div>")
        node = root[0]
        observer.transform_node(node)
        self.assertEqual(node.attrib, {"second": "val2"})
