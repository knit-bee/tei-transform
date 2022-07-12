from lxml import etree


class NoteStmtObserver:
    """Find 'type' attribute in <noteStmt> elements"""

    xpattern = "//noteStmt[@type]"

    def observe(self, node: etree._Element) -> bool:
        if node.tag == "noteStmt" and "type" in node.attrib:
            return True
        return False
