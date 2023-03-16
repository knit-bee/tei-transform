import unittest

from lxml import etree

from tei_transform.observer import SchemeAttributeObserver


class SchemeAttributeObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = SchemeAttributeObserver()
        self.valid_config = {"scheme": "scheme.path"}

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<classCode scheme=''/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<classCode scheme='some.scheme'/>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<classcode scheme=''>text</classcode>"),
            etree.XML("<textClass><classCode scheme=''>text</classCode></textClass>"),
            etree.XML("<textclass><classcode scheme=''>text</classcode></textclass>"),
            etree.XML("<classCode scheme=''><term>term</term></classCode>"),
            etree.XML(
                "<textClass><classCode scheme='' attr='val'>code</classCode></textClass>"
            ),
            etree.XML(
                "<profileDesc><textclass><classcode scheme=''>code</classcode></textclass></profileDesc>"
            ),
            etree.XML(
                "<teiHeader><fileDesc/><profileDesc><classCode scheme=''>code</classCode></profileDesc></teiHeader>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><profileDesc><classCode scheme=''/></profileDesc></teiHeader></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><classcode scheme=''>text</classcode></teiHeader></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<classcode scheme='a'>text</classcode>"),
            etree.XML("<classCode scheme='a'><code/></classCode>"),
            etree.XML("<classCode scheme='http/...'>text</classCode>"),
            etree.XML(
                "<textclass><classcode scheme='path'>text</classcode></textclass>"
            ),
            etree.XML(
                "<teiHeader><textclass><classcode scheme='a'><term/></classcode></textclass></teiHeader>"
            ),
            etree.XML(
                "<textClass><classCode scheme='path/to/scheme'>code</classCode></textClass>"
            ),
            etree.XML(
                "<TEI xmlns='a'><teiHeader><classCode scheme='path'/></teiHeader></TEI>"
            ),
            etree.XML(
                """<TEI xmlns='a'>
                  <profileDesc>
                    <textClass>
                      <classCode scheme='b'>code</classCode>
                      <keywords/>
                    </textClass>
                  </profileDesc>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_configure_observer(self):
        self.observer.configure(self.valid_config)
        self.assertEqual(self.observer.scheme, "scheme.path")

    def test_observer_not_configured_if_config_wrong(self):
        config = {"schema": "scheme.path"}
        self.observer.configure(config)
        self.assertIsNone(self.observer.scheme)

    def test_observer_not_configured_if_section_missing(self):
        config = {}
        self.observer.configure(config)
        self.assertIsNone(self.observer.scheme)

    def test_element_not_transformed_when_observer_not_configured(self):
        root = etree.XML("<teiHeader><classCode scheme=''>code</classCode></teiHeader>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"scheme": ""})

    def test_change_attribute_value(self):
        self.observer.configure(self.valid_config)
        root = etree.XML("<textClass><classCode scheme=''>term</classCode></textClass>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"scheme": "scheme.path"})

    def test_change_attribute_value_with_namespace(self):
        self.observer.configure(self.valid_config)
        root = etree.XML(
            "<TEI xmlns='a'><teiHeader><element scheme=''/></teiHeader></TEI>"
        )
        node = root.find(".//{*}element")
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {"scheme": "scheme.path"})

    def test_other_attributes_on_element_not_changed(self):
        self.observer.configure(self.valid_config)
        root = etree.XML(
            "<textclass><classcode attr='a' scheme='' other='b'>code</classcode></textclass>"
        )
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(
            node.attrib, {"scheme": "scheme.path", "attr": "a", "other": "b"}
        )

    def test_remove_element(self):
        config = {"action": "remove"}
        self.observer.configure(config)
        root = etree.XML("<textClass><classCode scheme=''>term</classCode></textClass>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 0)

    def test_set_attribute_overrides_removal(self):
        config = {"action": "remove", "scheme": "scheme.path"}
        self.observer.configure(config)
        root = etree.XML("<textClass><classCode scheme=''>term</classCode></textClass>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)
        self.assertEqual(node.attrib, {"scheme": "scheme.path"})

    def test_invalid_action_from_config_ignored(self):
        config = {"action": "some_action"}
        self.observer.configure(config)
        root = etree.XML("<textClass><classCode scheme=''>term</classCode></textClass>")
        node = root[0]
        self.assertEqual(node.attrib, {"scheme": ""})
        self.assertEqual(len(root), 1)

    def test_invalid_action_trigger_log_warning(self):
        config = {"action": "some_action"}
        self.observer.configure(config)
        root = etree.XML("<textClass><classCode scheme=''>term</classCode></textClass>")
        node = root[0]
        with self.assertLogs() as logger:
            self.observer.transform_node(node)
        self.assertEqual(
            logger.output,
            [
                "WARNING:tei_transform.observer.scheme_attribute_observer:"
                "Invalid configuration for SchemeAttributeObserver"
            ],
        )
