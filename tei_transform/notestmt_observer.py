from lxml import etree


class NoteStmtObserver:
    """Find 'type' attribute in <noteStmt> elements"""

    xpattern = "//noteStmt[@type]"

    def observe(self, node: etree._Element) -> bool:
        if node.xpath(self.xpattern):
            if "type" in node.attrib:
                return True
        return False
