from lxml import etree


class FilenameElementObserver:
    xpattern = "//filename"

    def observe(self, node: etree._Element) -> bool:
        if node.tag == "filename":
            return True
        return False
