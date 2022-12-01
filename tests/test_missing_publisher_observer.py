import unittest

from lxml import etree

from tei_transform.observer import MissingPublisherObserver


class MissingPublisherObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MissingPublisherObserver()

    def test_observer_returns_true_for_matching_node(self):
        node = etree.XML("<publicationStmt/>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_node(self):
        node = etree.XML("<publicationStmt><publisher/></publicationStmt>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_identifies_matching_nodes(self):
        elements = [
            etree.XML("<publicationStmt><pubPlace/></publicationStmt>"),
            etree.XML("<publicationStmt></publicationStmt>"),
            etree.XML("<publicationStmt><idno>val</idno></publicationStmt>"),
            etree.XML(
                "<publicationStmt><pubPlace/><address>street</address></publicationStmt>"
            ),
            etree.XML("<publicationStmt><ab><publisher/></ab></publicationStmt>"),
            etree.XML(
                """<teiHeader><fileDesc>
                <publicationStmt>
                <date>today</date><address>street</address>street<pubPlace/>
                </publicationStmt>
                </fileDesc></teiHeader>"""
            ),
            etree.XML(
                """<fileDesc>
                <publicationStmt><date/><ab/><idno/><availability><license/></availability></publicationStmt>
                </fileDesc>"""
            ),
            etree.XML(
                "<fileDesc><publicationStmt><pubPlace>city</pubPlace></publicationStmt></fileDesc>"
            ),
            etree.XML("<teiHeader><fileDesc><publicationStmt/></fileDesc></teiHeader>"),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader><fileDesc>
                <publicationStmt><pubPlace>city</pubPlace></publicationStmt>
                </fileDesc></teiHeader></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader><fileDesc>
                        <publicationStmt>
                        <pubPlace>city</pubPlace>
                        <ab/><idno/>
                        </publicationStmt>
                        </fileDesc></teiHeader></TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_nodes(self):
        elements = [
            etree.XML("<publicationStmt><publisher>name</publisher></publicationStmt>"),
            etree.XML("<publicationStmt><publisher/><pubPlace/></publicationStmt>"),
            etree.XML("<publicationStmt><authority/></publicationStmt>"),
            etree.XML("<publicationStmt><distributor/></publicationStmt>"),
            etree.XML("<publicationStmt><publisher/></publicationStmt>"),
            etree.XML(
                "<publicationStmt><publisher><orgName/><country/><idno/></publisher><pubPlace/></publicationStmt>"
            ),
            etree.XML(
                "<fileDesc><publicationStmt><authority/><date/></publicationStmt></fileDesc>"
            ),
            etree.XML(
                "<fileDesc><publicationStmt><distributor/><availability/><idno/></publicationStmt></fileDesc>"
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader>
                <fileDesc><publicationStmt><publisher/><date/><idno/><pubPlace>city</pubPlace></publicationStmt>
                </fileDesc></teiHeader></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader>
                        <fileDesc><publicationStmt><authority><name>Name</name><note/></authority><date/><idno/><pubPlace>city</pubPlace></publicationStmt>
                        </fileDesc></teiHeader></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader>
                        <fileDesc><publicationStmt>
                            <distributor>name<email>email@domain.org</email></distributor>
                            <date/><idno/><pubPlace>city</pubPlace>
                        </publicationStmt>
                        </fileDesc></teiHeader></TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_publisher_inserted_on_empty_publicationStmt(self):
        root = etree.XML("<fileDesc><publicationStmt/></fileDesc>")
        node = root[0]
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//publisher") is not None)

    def test_publisher_inserted_on_publicationStmt_with_children(self):
        root = etree.XML(
            "<fileDesc><publicationStmt><pubPlace>city</pubPlace></publicationStmt></fileDesc>"
        )
        node = root.find(".//pubPlace")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//publisher") is not None)

    def test_publisher_inserted_on_empty_publicationStmt_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='ns'><teiHeader><fileDesc><publicationStmt/></fileDesc></teiHeader></TEI>"
        )
        node = root.find(".//{*}publicationStmt")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}publisher") is not None)

    def test_publisher_inserted_on_complex_publicationStmt_with_namespace(self):
        root = etree.XML(
            """<TEI xmlns='ns'>
                <teiHeader><fileDesc>
                    <publicationStmt>
                        <pubPlace/>
                        <address>street</address>
                        <date>today</date>
                        <ab>some note</ab>
                        <availability><license/></availability>
                    </publicationStmt>
                    </fileDesc></teiHeader>
            </TEI>"""
        )
        node = root.find(".//{*}publicationStmt")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}publisher") is not None)
