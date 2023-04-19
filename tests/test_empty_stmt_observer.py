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
