from utils.Serializable import Serializable


class Page(Serializable):
    """
    Page class
    """
    def __init__(self, page_number: int):
        """
        :param page_number: unique number of page
        """
        self.page_number = page_number
        self.uses = 0

    def use(self):
        """
        Use the page (increment its usage counter)
        """
        self.uses += 1

    def serialize(self):
        return {
            "page_number": self.page_number,
            "uses": self.uses
        }
