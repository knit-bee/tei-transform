import unittest

from lxml import etree

from tei_transform.observer import RelatedItemObserver


class RelatedItemObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = RelatedItemObserver()

    def test_observer_returns_true_for_matching_element(self):
        node = etree.XML("<relatedItem>text</relatedItem>")
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        node = etree.XML("<relatedItem><bibl/></relatedItem>")
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<relatedItem type='file'>path/to/file</relatedItem>"),
            etree.XML("<relatedItem></relatedItem>"),
            etree.XML("<relatedItem/>"),
            etree.XML("<notesStmt><relatedItem>text</relatedItem></notesStmt>"),
            etree.XML(
                "<notesStmt><relatedItem type='file'>text</relatedItem></notesStmt>"
            ),
            etree.XML(
                """<teiHeader>
                      <biblFull>
                        <notesStmt><relatedItem>text</relatedItem></notesStmt>
                      </biblFull>
                    </teiHeader>"""
            ),
            etree.XML(
                """<teiHeader><biblFull><notesStmt>
                    <relatedItem type='file'>text</relatedItem>
                </notesStmt></biblFull></teiHeader>"""
            ),
            etree.XML(
                """<teiHeader><biblFull><titleStmt/><notesStmt>
                    <relatedItem>text</relatedItem>
                </notesStmt></biblFull></teiHeader>"""
            ),
            etree.XML(
                """<TEI><teiHeader><titleStmt/><biblFull><titleStmt/>
                    <notesStmt><note/><relatedItem>text</relatedItem></notesStmt>
                    </biblFull></teiHeader><text/></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader><titleStmt/><biblFull><titleStmt/>
                                <notesStmt><note/><relatedItem>text</relatedItem></notesStmt>
                                </biblFull></teiHeader><text/></TEI>"""
            ),
            etree.XML(
                """<TEI><teiHeader><titleStmt/><biblFull><titleStmt/>
                                            <notesStmt><note/><relatedItem type='orig'>text</relatedItem></notesStmt>
                                            </biblFull></teiHeader><text/></TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'><teiHeader><titleStmt/><biblFull><titleStmt/>
                                                        <notesStmt><note/><relatedItem type='type'>text</relatedItem></notesStmt>
                                                        </biblFull></teiHeader><text/></TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<relatedItem><el/></relatedItem>"),
            etree.XML("<relatedItem target='other'/>"),
            etree.XML("<relatedItem><biblFull/></relatedItem>"),
            etree.XML(
                "<relatedItem><biblFull><titleStmt><title/></titleStmt></biblFull></relatedItem>"
            ),
            etree.XML("<notesStmt><relatedItem><ptr/></relatedItem></notesStmt>"),
            etree.XML("<biblFull><relatedItem target='preprint'/></biblFull>"),
            etree.XML(
                "<notesStmt><relatedItem type='other'><ptr/></relatedItem></notesStmt>"
            ),
            etree.XML(
                "<teiHeader><notesStmt><relatedItem><bibl/></relatedItem></notesStmt></teiHeader>"
            ),
            etree.XML(
                """<TEI>
                <teiHeader><notesStmt>
                    <relatedItem><bibl/></relatedItem>
                </notesStmt></teiHeader>
                </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                        <teiHeader><notesStmt>
                        <relatedItem><bibl/></relatedItem>
                        </notesStmt></teiHeader>
                    </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                        <teiHeader><notesStmt>
                            <relatedItem type='orig'><bibl/></relatedItem>
                            </notesStmt></teiHeader>
                        <text/>
                    </TEI>"""
            ),
            etree.XML(
                """<TEI xmlns='ns'>
                        <teiHeader><notesStmt>
                            <relatedItem target='other'/>
                        </notesStmt></teiHeader>
                    </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
