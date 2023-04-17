import unittest

from lxml import etree

from tei_transform.observer import MisplacedNotesstmtObserver


class MisplacedNotesstmtObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = MisplacedNotesstmtObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<fileDesc><sourceDesc/><notesStmt/></fileDesc>")
        node = root[1]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<fileDesc><notesStmt/><sourceDesc/></fileDesc>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML(
                "<fileDesc><sourceDesc/><notesStmt><note/></notesStmt></fileDesc>"
            ),
            etree.XML("<biblFull><titleStmt/><sourceDesc/><notesStmt/></biblFull>"),
            etree.XML(
                "<fileDesc><titleStmt/><publicationStmt/><sourceDesc/><notesStmt/></fileDesc>"
            ),
            etree.XML(
                "<teiHeader><fileDesc><sourceDesc/><notesStmt attr='val'/></fileDesc></teiHeader>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fileDesc><sourceDesc/><notesStmt/></fileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><biblFull><titleStmt/><sourceDesc/><notesStmt/></biblFull></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><biblFull><sourceDesc/><notesStmt attr='val'/></biblFull></TEI>"
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<fileDesc><titleStmt/><notesStmt/><sourceDesc/></fileDesc>"),
            etree.XML(
                "<fileDesc><titleStmt/><publicationStmt/><notesStmt/><sourceDesc/></fileDesc>"
            ),
            etree.XML("<biblFull><titleStmt/><notesStmt/><sourceDesc/></biblFull>"),
            etree.XML(
                "<biblFull><titleStmt/><notesStmt><note/></notesStmt></biblFull>"
            ),
            etree.XML(
                "<teiHeader><fileDesc><titleStmt/><notesStmt attr='val'/><sourceDesc/></fileDesc><encodingDesc/></teiHeader>"
            ),
            etree.XML(
                "<TEI xmlns='a'><fileDesc><titleStmt/><notesStmt><note/></notesStmt><sourceDesc/></fileDesc></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><biblFull><titleStmt/><publicationStmt/><notesStmt><note/></notesStmt></biblFull></TEI>"
            ),
            etree.XML(
                "<TEI xmlns='a'><biblFull><titleStmt/><notesStmt att='val'><note/></notesStmt><sourceDesc/></biblFull></TEI>"
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})

    def test_element_inserted_before_sourceDesc(self):
        root = etree.XML("<fileDesc><sourceDesc/><notesStmt/></fileDesc>")
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(root[0].tag, "notesStmt")

    def test_element_inserted_before_sourceDesc_with_namespace(self):
        root = etree.XML(
            "<TEI xmlns='a'><biblFull><sourceDesc/><notesStmt/></biblFull></TEI>"
        )
        node = root.find(".//{*}notesStmt")
        self.observer.transform_node(node)
        self.assertEqual(etree.QName(node.getnext()).localname, "sourceDesc")

    def test_relocating_notesStmt_with_other_siblings(self):
        root = etree.XML(
            """
            <fileDesc>
                <titleStmt/>
                <publicationStmt/>
                <seriesStmt/>
                <sourceDesc/>
                <notesStmt/>
            </fileDesc>
            """
        )
        node = root.find("notesStmt")
        self.observer.transform_node(node)
        self.assertEqual(node.getnext().tag, "sourceDesc")

    def test_children_note_changed(self):
        root = etree.XML(
            "<fileDesc><sourceDesc/><notesStmt><note>one</note><note>two</note></notesStmt></fileDesc>"
        )
        node = root[1]
        self.observer.transform_node(node)
        self.assertEqual(len(node), 2)

    def test_transformation_during_iteration(self):
        root = etree.XML(
            """
            <teiHeader>
                <fileDesc>
                    <titleStmt/>
                    <publicationStmt/>
                    <seriesStmt/>
                    <sourceDesc>
                        <bibl/>
                        <biblFull>
                            <titleStmt/>
                            <publicationStmt/>
                            <sourceDesc/>
                            <notesStmt/>
                        </biblFull>
                    </sourceDesc>
                    <notesStmt>
                        <note/>
                        <note/>
                        <note/>
                    </notesStmt>
                </fileDesc>
                <encodingDesc/>
            </teiHeader>
            """
        )
        for node in root.iter():
            if self.observer.observe(node):
                self.observer.transform_node(node)
        result = [elem.getnext().tag for elem in root.findall(".//notesStmt")]
        self.assertEqual(result, ["sourceDesc", "sourceDesc"])

    def test_transformation_with_muliple_sourceDesc_siblings(self):
        root = etree.XML(
            "<fileDesc><titleStmt/><sourceDesc/><sourceDesc/><sourceDesc/><notesStmt/></fileDesc>"
        )
        node = root.find("notesStmt")
        self.observer.transform_node(node)
        result = root.index(node)
        self.assertEqual(result, 1)
