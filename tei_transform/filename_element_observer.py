class FilenameElementObserver:
    xpattern = "//filename"

    def observe(self, node) -> bool:
        if node.xpath(self.xpattern):
            return True
        return False
