import unittest

from lxml import etree

from tei_transform.observer import HeadChildObserver


class HeadChildObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = HeadChildObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<head><p>text</p></head>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<div><head/><p/></div>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<div><head>text<hi/><p/></head></div>"),
            etree.XML("<body><head>text<ab>text</ab></head><p/></body>"),
            etree.XML("<div><p/><head>a<p>b</p>c</head><list/></div>"),
            etree.XML("<body><head/><head>text<ab>text</ab>tail</head><head/></body>"),
            etree.XML(
                "<body><div><head><p/></head></div><div><head/><p/></div></body>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><head>ab<p>c</p>d</head><list/></div></TEI>"
            ),
            etree.XML("<TEI xmlns='a'><div><head><quote/><ab/>tail</head></div></TEI>"),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<div><head><quote/></head><p/><ab/></div>"),
            etree.XML("<div><p/><head><hi>text</hi></head><p/></div>"),
            etree.XML("<div><p>text</p><div><head><del/></head><p/></div></div>"),
            etree.XML("<body><head/><p/><ab/></body>"),
            etree.XML("<body><div><head><list/></head><p/></div></body>"),
            etree.XML("<div><head/><p><list><head/><item/></list></p><p/></div>"),
            etree.XML(
                "<TEI xmlns='a'><div><head/><p/><ab/><div><head/></div></div></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><div><ab/><head>text<hi/></head><p/></div></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_child_removed(self):
        root = etree.XML("<div><head><p>text</p></head></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//p"))

    def test_child_removed_with_namespace(self):
        root = etree.XML("<TEI xmlns='a'><div><head><ab>text</ab></head></div></TEI>")
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//{*}ab"))

    def test_text_of_child_not_removed(self):
        root = etree.XML("<head><p>text</p></head>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.text, "text")

    def test_tail_of_child_not_removed(self):
        root = etree.XML("<head><p/>text</head>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.text, "text")

    def test_lb_added_to_separate_text_parts(self):
        root = etree.XML("<div><head>text1<p>text2</p>tail</head></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//lb").tail, "text2 tail")

    def test_lb_added_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><div><head>text1<ab>text2</ab></head></div></TEI>"
        )
        node = root.find(".//{*}ab")
        self.observer.transform_node(node)
        self.assertEqual(root.find(".//{*}lb").tail, "text2")

    def test_multiple_children_resolved(self):
        root = etree.XML(
            """
            <div>
                <head>text1
                    <p>text2</p>
                    <p>text3</p>
                    <ab>text4</ab>text5
                    <p/>text6
                </head>
            </div>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        head_elem = root[0]
        self.assertEqual(len(head_elem.findall("lb")), 4, len(head_elem))
        result = [(node.tag, node.text, node.tail.strip()) for node in head_elem.iter()]
        self.assertEqual(
            result,
            [
                ("head", "text1", ""),
                ("lb", None, "text2"),
                ("lb", None, "text3"),
                ("lb", None, "text4 text5"),
                ("lb", None, "text6"),
            ],
        )

    def test_no_lb_added_if_child_empty(self):
        root = etree.XML("<div><head>text<p/></head></div>")
        node = root.find(".//p")
        self.observer.transform_node(node)
        self.assertIsNone(root.find(".//lb"))

    def test_no_lb_added_if_text_only_whitespace(self):
        roots = [
            etree.XML("<head>  \n\t<p>text</p></head>"),
            etree.XML("<head>  \n\t<p>text</p>tail</head>"),
            etree.XML("<head>  <p>   </p></head>"),
            etree.XML("<head>text<p>   </p></head>"),
            etree.XML("<head>    <p/>tail</head>"),
            etree.XML("<head>text<p>    </p></head>"),
            etree.XML("<head>text<p/>   \n\n\t</head>"),
        ]
        for root in roots:
            self.observer.transform_node(root[0])
            with self.subTest():
                self.assertIsNone(root.find("lb"))
                self.assertEqual(len(root), 0)

    def test_no_lb_added_if_child_has_no_text_but_children(self):
        root = etree.XML("<head>text<p><hi>text2</hi></p></head>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertIsNone(root.find("lb"))

    def test_test_lb_added_if_child_has_only_tail(self):
        root = etree.XML("<head>text<p/>tail</head>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertEqual(root.find("lb").tail, "tail")
