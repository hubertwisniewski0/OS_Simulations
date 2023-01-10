from utils.Serializable import Serializable


class Page(Serializable):
    def __init__(self, page_number: int):
        self.page_number = page_number
        self.uses = 0

    def serialize(self):
        return {
            "page_number": self.page_number,
            "uses": self.uses
        }

    def use(self):
        self.uses += 1
