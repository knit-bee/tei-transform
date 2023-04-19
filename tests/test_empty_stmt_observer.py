import unittest

from lxml import etree

from tei_transform.observer import EmptyStmtObserver


class EmptyStmtObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = EmptyStmtObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<biblFull><notesStmt/></biblFull>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<biblFull><notesStmt><note/></notesStmt></biblFull>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<biblFull><titleStmt/><seriesStmt/></biblFull>"),
            etree.XML(
                "<fileDesc><titleStmt/><publicationStmt/><seriesStmt/></fileDesc>"
            ),
            etree.XML("<fileDesc><titleStmt/><seriesStmt/><sourceDesc/></fileDesc>"),
            etree.XML("<biblFull><titleStmt/><notesStmt/><sourceDesc/></biblFull>"),
            etree.XML(
                "<biblFull><titleStmt/><publicationStmt/><notesStmt/><sourceDesc/></biblFull>"
            ),
            etree.XML(
                "<teiHeader><fileDesc><titleStmt/><notesStmt/><sourceDesc/></fileDesc></teiHeader>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fileDesc><publicationStmt/><seriesStmt/><sourceDesc/></fileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><biblFull><publicationStmt/><notesStmt/></biblFull></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fileDesc><editionStmt/><notesStmt/><sourceDesc/></fileDesc></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<biblFull><seriesStmt><title/></seriesStmt></biblFull>"),
            etree.XML("<biblFull><notesStmt><note/></notesStmt></biblFull>"),
            etree.XML(
                "<fileDesc><titleStmt/><notesStmt><note/></notesStmt></fileDesc>"
            ),
            etree.XML(
                "<fileDesc><publicationStmt/><seriesStmt><p/></seriesStmt><sourceDesc/></fileDesc>"
            ),
            etree.XML(
                "<fileDesc><seriesStmt><title/></seriesStmt><sourceDesc/></fileDesc>"
            ),
            etree.XML(
                "<teiHeader><fileDesc><titleStmt/><seriesStmt><p/></seriesStmt></fileDesc></teiHeader>"
            ),
            etree.XML(
                "<teiHeader><biblFull><editionStmt/><notesStmt><note/></notesStmt></biblFull></teiHeader>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fileDesc><editionStmt/><notesStmt><note/><note/></notesStmt></fileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><biblFull><titleStmt/><seriesStmt><title/></seriesStmt></biblFull></TEI>"
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                    <teiHeader>
                        <biblFull>
                            <notesStmt>
                                <note/>
                            </notesStmt>
                            <sourceDesc/>
                        </biblFull>
                    </teiHeader>
                </TEI>"""
            ),
            etree.XML(
                "<TEI xmlns='a'><fileDesc><titleStmt/><seriesStmt><title/><idno/></seriesStmt></fileDesc></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_remove_element(self):
        root = etree.XML("<fileDesc><titleStmt/><notesStmt/></fileDesc>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(len(root), 1)

    def test_remove_element_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><teiHeader><fileDesc><titleStmt/><seriesStmt/></fileDesc></teiHeader></TEI>"
        )
        node = root.find(".//{*}seriesStmt")
        self.observer.transform_node(node)
        self.assertTrue(root.find(".//{*}seriesStmt") is None)

    def test_remove_multiple_elements_during_iteration(self):
        root = etree.XML(
            """
            <teiHeader>
                <fileDesc>
                    <titleStmt/>
                    <publicationStmt/>
                    <seriesStmt/>
                    <seriesStmt/>
                    <notesStmt/>
                    <notesStmt>
                        <note>text</note>
                    </notesStmt>
                    <notesStmt/>
                    <notesStmt/>
                    <sourceDesc/>
                </fileDesc>
            </teiHeader>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        self.assertEqual(len(root[0]), 4)
        self.assertEqual(len(root.findall(".//notesStmt")), 1)
