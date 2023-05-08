import unittest

from lxml import etree

from tei_transform.observer import LinebreakDivObserver


class LinebreakDivObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = LinebreakDivObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<div><lb/>text</div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><lb/></div>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><p>text</p><lb/>tail</div>"),
            etree.XML("<div><lb/>a<list/></div>"),
            etree.XML(
                "<body><div><div><head/><lb/>a<p>text<lb/>tail</p></div></div></body>"
            ),
            etree.XML("<div><p>text<lb/>tail</p>tail<lb/>tail</div>"),
            etree.XML("<div><p/><div><p/><lb/>tail</div></div>"),
            etree.XML("<TEI xmlns='a'><body><div><lb/>tail</div></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><div><p>text<lb/>tail</p><lb/>tl</div></body></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><p><lb/>tail</p><lb/>tail<list/></div></TEI>"
            ),
            etree.XML("<body><p/><lb/>tail</body>"),
            etree.XML("<body><p/>tail<lb/>tail2</body>"),
            etree.XML("<body><p>text<lb/>a</p>b<lb/>c</body>"),
            etree.XML("<TEI xmlns='a'><body><p/><lb/>tail<div/></body></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><p>text<lb/>tail</p>tail<lb/>tail</body></TEI>"
            ),
            etree.XML("<div><lb/>\n\n  \t \xa0</div>"),
            etree.XML("<body><p/><lb/>  \u2028  </body>"),
        ]

        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><p>text<lb/>tail</p></div>"),
            etree.XML("<p><lb/>tail</p>"),
            etree.XML("<div><lb/><p/></div>"),
            etree.XML("<div><lb/><p>text</p><lb/></div>"),
            etree.XML("<body><div><lb/><p>text</p></div></body>"),
            etree.XML("<p>text<lb/>tail<div/></p>"),
            etree.XML("<div><p><hi>text<lb/>ab</hi></p><p/>tail</div>"),
            etree.XML("<TEI xmlns='a'><text><div><p>text</p><lb/></div></text></TEI>"),
            etree.XML(
                "<TEI xmlns='a'><body><lb/><p><lb/>tail</p><div><lb/></div></body></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><lb/><p>tex</p><p><lb/>tail</p></div></TEI>"
            ),
            etree.XML("<body><p>text<lb/>tail</p></body>"),
            etree.XML("<body><lb/><p>text</p><lb/></body>"),
            etree.XML("<body><p>text</p>tail<lb/></body>"),
            etree.XML("<TEI xmlns='a'><body><p>text<lb/>tail</p></body></TEI>"),
            etree.XML("<TEI xmlns='a'><body><p/>tail<lb/><lb/></body></TEI>"),
            etree.XML("<div><p><lb/>  \xa0</p><p>text<lb/>\u2028</p></div>"),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_new_p_added_as_parent_of_lb(self):
        root = etree.XML("<div><lb/>text</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p")[0].tag, "lb")

    def test_tail_of_lb_not_transfered(self):
        root = etree.XML("<div>text<lb/>tail</div>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//p/lb").tail, "tail")

    def test_new_p_added_as_parent_of_lb_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><lb/>tail</div></TEI>")
        node = root.find(".//{*}lb")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}p/{*}lb") is not None)

    def test_multiple_adjacent_lb_added_under_same_p(self):
        root = etree.XML("<body><div><lb/>one<lb/>two<lb/>three</div></body>")
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        target = root.find(".//p")
        self.assertEqual(len(target.findall("lb")), 3)

    def test_multiple_adjacent_lb_added_under_same_p_with_namespace(self):
        root = etree.XML(
            """
            <TEI xmlns='a'>
              <body>
                <div>
                text
                  <lb/>one
                  <lb/>two
                  <lb/>three
                  <lb/>four
                  <lb/>five
                </div>
              </body>
            </TEI>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = len(root.find(".//{*}p").findall("{*}lb"))
        self.assertEqual(result, 5)

    def test_older_siblings_of_lb_not_added_to_new_p_if_not_matching(self):
        root = etree.XML("<div><p>text</p><lb/>tail</div>")
        node = root[1]
        self.observer.transform_node(node)
        result = [child.tag for child in root.findall(".//p")[1]]
        self.assertEqual(result, ["lb"])

    def test_following_siblings_of_lb_not_changed(self):
        root = etree.XML("<div><lb/>tail<p>text</p></div>")
        node = root[0]
        self.observer.transform_node(node)
        result = [child.tag for child in root.find(".//p")]
        self.assertEqual(["lb"], result)

    def test_multiple_p_added_if_lb_not_adjacent(self):
        root = etree.XML(
            """
            <body>
              <div>
                <p>text</p>
                <lb/>tail1
                <lb/>tail2
                <p>text2</p>
                <lb/>tail3
                <p>text3</p>
                <lb/>tail4
                <list/>
                <lb/>tail5
                <div>
                  <lb/>tail6
                </div>
              </div>
            </body>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [(node.tag, [child.tag for child in node]) for node in root[0]]
        self.assertEqual(
            result,
            [
                ("p", []),
                ("p", ["lb", "lb"]),
                ("p", []),
                ("p", ["lb"]),
                ("p", []),
                ("p", ["lb"]),
                ("list", []),
                ("p", ["lb"]),
                ("div", ["p"]),
            ],
        )

    def test_tail_with_problematic_whitespace_cleaned(self):
        root = etree.XML(
            """
        <div>
            <lb/>   \xa0
            <lb/>\t  \t
            <lb/>\n\n\n
            <lb/>  \u2028
        </div>
        """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [child.tail.strip(" ") for child in root]
        self.assertEqual(["", "\t  \t\n", "\n\n\n\n", ""], result)
        self.assertEqual(len(root), 4)
