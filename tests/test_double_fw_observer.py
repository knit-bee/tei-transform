import unittest

from lxml import etree

from tei_transform.observer import DoubleFwObserver


class DoubleFwObserverTester(unittest.TestCase):
    def setUp(self):
        self.observer = DoubleFwObserver()

    def test_observer_returns_true_for_matching_element(self):
        root = etree.XML("<fw><fw><list/></fw></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertTrue(result)

    def test_observer_returns_false_for_non_matching_element(self):
        root = etree.XML("<fw><fw>text</fw><list/></fw>")
        node = root[0]
        result = self.observer.observe(node)
        self.assertEqual(result, False)

    def test_observer_recognises_matching_elements(self):
        elements = [
            etree.XML("<fw>text<fw>text<list/>tail</fw>tail</fw>"),
            etree.XML("<div><fw><fw>text<list><item/></list></fw></fw></div>"),
            etree.XML("<fw><fw><list/></fw><p/>tail</fw>"),
            etree.XML("<fw>text<fw/><fw><list/><fw/></fw></fw>"),
            etree.XML("<div><fw>text<fw/><fw><fw/><list/></fw></fw></div>"),
            etree.XML("<div><fw>text<fw><fw><p>text</p></fw></fw></fw></div>"),
            etree.XML("<div><fw><fw><quote>text</quote><fw/></fw></fw></div>"),
            etree.XML("<fw>text<fw>text<fw/></fw></fw>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <fw>text</fw>
                    <fw>
                      <fw></fw>
                      <fw>text
                        <list>
                          <item>text</item>
                        </list>tail
                      </fw>
                    </fw>
                    <p>text</p>
                  </div>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <div>
                    <fw>
                      <fw></fw>
                      <fw>text
                        <list>
                          <item>text</item>
                        </list>tail
                      </fw>
                      <fw>
                        <p>text</p>
                      </fw>
                    </fw>
                    <p>text</p>
                  </div>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text</fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <fw>text
                              <p>text</p>
                            </fw>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text</fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <fw>text
                              <hi>text</hi>
                            </fw>
                            <fw/>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = [self.observer.observe(node) for node in element.iter()]
            with self.subTest():
                self.assertEqual(sum(result), 1)

    def test_observer_ignores_non_matching_elements(self):
        elements = [
            etree.XML("<fw><fw>text</fw></fw>"),
            etree.XML("<fw><list/></fw>"),
            etree.XML("<fw>text<p>text</p></fw>"),
            etree.XML("<fw>a<fw>b</fw>c<list/>d</fw>"),
            etree.XML("<fw><fw><hi>text</hi></fw></fw>"),
            etree.XML("<fw><fw><quote>a</quote></fw></fw>"),
            etree.XML("<div><fw>text<list/></fw><fw>text<fw>text</fw></fw></div>"),
            etree.XML("<div><fw><list/><p/></fw><fw><fw/></fw></div>"),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text</fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <p>text</p>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text<fw/>tail</fw>
                        <fw>
                          <p>text</p>
                          <fw>text
                            <hi>text</hi>
                            <p>text</p>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
            etree.XML(
                """
                <TEI xmlns='a'>
                  <teiHeader/>
                  <text>
                      <div>
                        <fw>text
                          <fw>a</fw>
                          <fw>b</fw>
                        </fw>
                        <fw>
                          <fw></fw>
                          <p>text</p>
                          <fw>text
                            <quote>text</quote>
                          </fw>tail
                        </fw>
                        <p>text</p>
                      </div>
                  </text>
                </TEI>"""
            ),
        ]
        for element in elements:
            result = {self.observer.observe(node) for node in element.iter()}
            with self.subTest():
                self.assertEqual(result, {False})
