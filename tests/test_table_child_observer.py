import unittest

from lxml import etree

from tei_transform.observer import TableChildObserver


class TableChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = TableChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<table><row/><p/></table>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<table><row><cell><p/></cell></row></table>")
        node = root.find(".//p")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<table><row/><p>text</p></table>"),
            etree.XML("<div><table><row/><p>text</p><row/></table></div>"),
            etree.XML("<table>text<row><cell>text</cell></row><p/></table>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <table>
                      <row>
                        <cell>text</cell>
                      </row>
                      <p>text</p>
                      <row/>
                    </table>
                  </div>
                </TEI>
                """
            ),
            etree.XML("<table><head/><p>text<hi/></p><row/></table>"),
            etree.XML("<table><p>text</p>tail<row/></table>"),
            etree.XML("<div><table><row/><p/>tail</table></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <table>
                        <head/>
                        <row>
                            <cell/>
                            <cell/>
                        </row>
                        <p>
                            <hi>text</hi>
                        </p>
                    </table>
                </TEI>
                """
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<table><row><cell><p/></cell></row></table>"),
            etree.XML("<div><p><table><row/></table></p></div>"),
            etree.XML("<div><table><row><p/></row></table><p/></div>"),
            etree.XML("<div><p><table/></p><table/></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><p/><table><row><cell/></row></table></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><table><head/><row><cell><p/>tail</cell></row></table></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><table><row/><fw/></table><p>text</p>tail</div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_empty_p_removed(self):
        root = etree.XML("<table><row/><p/></table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)

    def test_p_child_in_table_converted_to_fw(self):
        root = etree.XML("<table><row/><p>text</p><row/></table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//p") is None and root[1].tag == "fw")

    def test_empty_p_with_tail_resolved(self):
        root = etree.XML("<table><row/><p/>tail<row/></table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//fw").tail, "tail")

    def test_p_child_in_table_converted_to_fw_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <table>
                <row/>
                <p>text</p>
                <row>
                  <cell>text1</cell>
                </row>
              </table>
            </TEI>
            """
        )
        node = root.find(".//{*}p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}fw").text, "text")

    def test_p_element_in_nested_table_converted_to_fw(self):
        root = etree.XML(
            """
            <div>
              <table>
                <row>
                  <cell>
                    <table>
                      <row/>
                      <row>
                        <cell/>
                      </row>
                      <p>text</p>
                    </table>
                  </cell>
                </row>
              </table>
            </div>
            """
        )
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//fw").text, "text")

    def test_p_with_children_in_table_in_table_converted_to_fw(self):
        root = etree.XML(
            """
            <div>
              <table>
                <row/>
                <p>text1
                  <hi>text2</hi>
                </p>
              </table>
            </div>
            """
        )
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//fw/hi") is not None)

    def test_p_elements_that_are_not_child_of_table_not_converted(self):
        root = etree.XML(
            """
            <div>
              <table>
                <p>text</p>
                <row>
                  <cell>
                    <p>text2</p>
                  </cell>
                </row>
              </table>
              <p>text3</p>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root.findall(".//p")), 2)

    def test_p_with_only_whitespace_removed(self):
        root = etree.XML("<table><row/><p>   \n\t  </p></table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)

    def test_p_with_tail_not_removed(self):
        root = etree.XML("<table><row/><p></p>tail</table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//fw").tail, "tail")

    def test_p_with_child_not_removed(self):
        root = etree.XML("<table><row/><p><hi>text</hi></p></table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//fw/hi") is not None)

    def test_p_with_only_whitespace_tail_removed(self):
        root = etree.XML("<table><row/><p/>   \n\t  </table>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)
