from utils.Serializable import Serializable


class Page(Serializable):
    def __init__(self, page_number: int):
        self.page_number = page_number

    def serialize(self):
        return {
            "page_number": self.page_number
        }
