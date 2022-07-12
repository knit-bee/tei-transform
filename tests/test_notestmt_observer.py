import unittest

from lxml import etree

from tei_transform.notestmt_observer import NoteStmtObserver
from tei_transform.observer_constructor import check_if_observer_pattern_is_valid_xpath


class NoteStmtObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = NoteStmtObserver()

    def test_observer_pattern_is_valid_xpath(self):
        result = check_if_observer_pattern_is_valid_xpath(self.observer.xpattern)
        self.assertTrue(result)

    def test_observer_identifies_matching_element(self):
        matching_elements = [
            etree.XML("<sourceDesc><noteStmt type='bibl'></noteStmt></sourceDesc>"),
            etree.XML("<noteStmt type='bibl'/>"),
            etree.XML("<noteStmt type='bibl'> <note> text</note> </noteStmt>"),
            etree.XML(
                "<sourceDesc><biblFull><noteStmt type='val'><note/></noteStmt></biblFull></sourceDesc>"
            ),
        ]
        for element in matching_elements:
            res = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertTrue(any(res))

    def test_observer_ignores_non_matching_elements(self):
        non_matching_elements = [
            etree.XML("<noteStmt/>"),
            etree.XML("<sourceDesc><noteStmt xml:id='bibl'></noteStmt></sourceDesc>"),
            etree.XML("<noteStmt> <note type='bibl'> text</note> </noteStmt>"),
            etree.XML(
                "<sourceDesc><biblFull><noteStmt xml:id='val'><note/></noteStmt></biblFull></sourceDesc>"
            ),
        ]
        for element in non_matching_elements:
            res = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertFalse(any(res))
