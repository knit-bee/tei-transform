class IdAttributeObserver:
    xpattern = "//*[@id]"

    def observe(self, node) -> bool:
        if node.xpath(self.xpattern):
            return True
        return False
