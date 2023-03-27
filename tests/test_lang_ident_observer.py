import unittest

from lxml import etree

from tei_transform.observer import LangIdentObserver


class LangIdentObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LangIdentObserver()
        self.valid_config = {"ident": "de"}

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<langUsage><language/></langUsage>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<langUsage><language ident='en-US'/></langUsage>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<langUsage><language>text</language></langUsage>"),
            etree.XML("<langUsage><p/><language/></langUsage>"),
            etree.XML(
                "<profileDesc><langUsage><p/><ab/><language/></langUsage></profileDesc>"
            ),
            etree.XML("<langUsage><language usage='90'>text</language></langUsage>"),
            etree.XML(
                "<TEI xmlns='a'><profileDesc><langUsage><ab/><p/><language/></langUsage></profileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><langUsage><language usage='33'>sth</language><p/><ab/></langUsage></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<langUsage><language ident='de'/></langUsage>"),
            etree.XML("<langUsage><language ident=''/></langUsage>"),
            etree.XML(
                "<langUsage><p/><language ident='en'>text</language></langUsage>"
            ),
            etree.XML(
                "<profileDesc><langUsage><language usage='100' ident='de'>text</language></langUsage></profileDesc>"
            ),
            etree.XML("<langUsage><language ident='tr'/><p/><ab/></langUsage>"),
            etree.XML(
                "<TEI xmlns='a'><langUsage><p/><language ident='en'>text</language><ab/></langUsage></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><profileDesc><langUsage><language ident='fr' usage='100'/></langUsage></profileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><langUsage><p/><p/><language usage='100' ident='tr'>metin</language></langUsage></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_configure_observer(self):
        self.observer.configure(self.valid_config)
        self.assertEqual(self.observer.ident, "de")

    def test_observer_not_configured_if_config_wrong(self):
        config = {"lang-id": "de"}
        self.observer.configure(config)
        self.assertEqual(self.observer.ident, "")

    def test_invalid_config_triggers_log_warning(self):
        config = {"lang-id": "de"}
        with self.assertLogs() as logger:
            self.observer.configure(config)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.lang_ident_observer:"
                "Invalid configuration for LangIdentObserver, setting empty string for @ident."
            ],
        )

    def test_attribute_value_set(self):
        self.observer.configure(self.valid_config)
        root = etree.XML("<langUsage><language/></langUsage>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"ident": "de"})

    def test_attribute_value_set_with_namespace(self):
        self.observer.configure(self.valid_config)
        root = etree.XML("<TEI xmlns='a'><langUsage><language/></langUsage></TEI>")
        node = root.find(".//{*}language")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"ident": "de"})

    def test_other_attributes_on_element_not_changed(self):
        self.observer.configure(self.valid_config)
        root = etree.XML(
            "<langUsage><language usage='90'>dialect</language><language ident='fr' usage='10'>quotes</language></langUsage>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"ident": "de", "usage": "90"})

    def test_empty_string_set_as_value_if_config_missing_or_invalid(self):
        root = etree.XML("<langUsage><language/></langUsage>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"ident": ""})
