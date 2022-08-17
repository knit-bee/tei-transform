import unittest

from lxml import etree

from tei_transform.double_cell_observer import DoubleCellObserver


class DoubleCellObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DoubleCellObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<cell><cell/></cell>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<cell><p/></cell>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_elements(self):
        elements = [
            etree.XML("<cell><cell></cell></cell>"),
            etree.XML("<cell><cell>text</cell></cell>"),
            etree.XML("<row><cell><cell>text</cell><p/></cell></row>"),
            etree.XML("<row><cell>text</cell><cell><cell>text</cell></cell></row>"),
            etree.XML(
                "<table><row><cell>text</cell></row><row><cell><cell>text</cell></cell></row></table>"
            ),
            etree.XML("<cell><cell>text</cell><fw>more text</fw></cell>"),
            etree.XML("<div><p/><table><row><cell><cell/></cell></row></table></div>"),
            etree.XML(
                """<TEI><teiHeader/>
            <text><body>
                <table><row><cell><cell>text</cell><p/></cell><cell/></row><row/></table>
            </body>
            </text></TEI>
            """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>
                    <text><body>
                        <table><row><cell><cell>text</cell><p/></cell><cell/></row><row/></table>
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
            etree.XML("<cell><p></p></cell>"),
            etree.XML("<cell><p>text</p></cell>"),
            etree.XML("<row><cell><p>text</p><p/></cell><cell/></row>"),
            etree.XML("<row><cell>text</cell><cell><p>text</p></cell></row>"),
            etree.XML(
                "<table><row><cell>text</cell></row><row><cell><p>text</p></cell></row></table>"
            ),
            etree.XML("<cell><p>text</p><fw>more text</fw></cell>"),
            etree.XML(
                "<div><p/><table><row><cell><p/></cell><cell/></row></table></div>"
            ),
            etree.XML(
                """<TEI><teiHeader/>
                    <text><body>
                        <table><row><cell>text<p/></cell><cell/></row><row/></table>
                    </body>
                    </text></TEI>
                    """
            ),
            etree.XML(
                """<TEI xmlns='namespace'><teiHeader/>git
                    <text><body>
                        <table><row><cell><p>text</p><p/></cell><cell/></row><row/></table>
                    </body>
                    </text></TEI>
                        """
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_inner_cell_renamed(self):
        root = etree.XML("<row><cell><cell>text</cell></cell></row>")
        node = root[0][0]
        self.observer.transform_node(node)
        result = [node.tag for node in root.iter()]
        self.assertEqual(result, ["row", "cell", "p"])

    def test_inner_cell_renamed_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><row><cell><cell>text</cell></cell></row></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root.iter()]
        self.assertEqual(result, ["TEI", "row", "cell", "p"])

    def test_namespace_prefix_preserved_after_change_on_target_node(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><row><cell><cell>text</cell></cell></row></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        result = root.find(".//{*}p").tag
        self.assertEqual(result, "{namespace}p")

    def test_role_attribute_removed_on_p_after_transformation(self):
        root = etree.XML(
            "<row><cell role='data'><cell role='data'>text</cell></cell></row>"
        )
        node = root[0][0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_role_attribute_removed_after_transformation_on_namespaced_node(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><row><cell role='data'><cell role='data'>text</cell></cell></row></TEI>"
        )
        node = root[0][0][0]
        self.observer.transform_node(node)
        self.assertEqual(node.attrib, {})

    def test_observer_action_on_node_with_children(self):
        root = etree.XML("<row><cell><cell><p/></cell></cell></row>")
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.tag for node in root.getchildren()]
        self.assertEqual(result, ["cell", "cell"])

    def test_observer_action_on_namespaced_node_with_children(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><row><cell><cell><p/></cell></cell></row></TEI>"
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [etree.QName(node).localname for node in root[0].getchildren()]
        self.assertEqual(result, ["cell", "cell"])

    def test_attributes_preserved_after_transformation_on_node_with_children(self):
        root = etree.XML(
            "<TEI xmlns='namespace'><row><cell role='cell1'><cell role='cell2'><p/></cell></cell></row></TEI>"
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [node.attrib for node in root[0].getchildren()]
        self.assertEqual(result, [{"role": "cell2"}, {"role": "cell1"}])

    def test_cell_transformation_with_multiple_double_cells(self):
        root = etree.XML(
            """<table>
        <row1><cell><cell>text</cell><lb/>text</cell></row1>
        <row2><cell><cell>more text<p/></cell></cell></row2>
        <row3><cell>text</cell></row3>
        <row4><cell><cell>text1<ab/></cell><p>text2</p></cell></row4>
        </table>
        """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = {
            node.tag: [child.tag for child in node.iterdescendants()]
            for node in root.getchildren()
        }
        self.assertEqual(
            result,
            {
                "row1": ["cell", "p", "lb"],
                "row2": ["cell", "p", "cell"],
                "row3": ["cell"],
                "row4": ["cell", "ab", "cell", "p"],
            },
        )
