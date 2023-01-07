from copy import deepcopy
from typing import List, Optional
from .Page import Page
from utils.Serializable import Serializable


class MemoryFull(Exception):
    pass


class MemoryManager(Serializable):
    def __init__(self, access_list: List[int], memory_size: int):
        assert memory_size > 0

        self.memory_size = memory_size
        self.access_list = access_list
        self.all_pages: List[Page] = []
        self.cached_pages: List[Page] = []
        self.page_faults = 0
        self.memory_states: List[List[Page]] = []

    def process_all(self):
        for page_number in self.access_list:
            if not self.is_cached(page_number):
                self.page_faults += 1

                try:
                    self.load_page(page_number)
                except MemoryFull:
                    self.remove_victim()
                    self.load_page(page_number)

            self.memory_states.append(deepcopy(self.cached_pages))

    def is_cached(self, page_number: int) -> bool:
        return self.get_page(page_number, self.cached_pages) is not None

    def page_exists(self, page_number) -> bool:
        return self.get_page(page_number, self.all_pages) is not None

    def load_page(self, page_number):
        assert len(self.cached_pages) <= self.memory_size

        if len(self.cached_pages) == self.memory_size:
            raise MemoryFull()

        if not self.page_exists(page_number):
            new_page = Page(page_number)
            self.all_pages.append(new_page)
            self.cached_pages.append(new_page)
        else:
            self.cached_pages.append(self.get_page(page_number, self.all_pages))

    @staticmethod
    def get_page(page_number: int, page_list: List[Page]) -> Optional[Page]:
        for page in page_list:
            if page.page_number == page_number:
                return page
        return None

    def serialize(self):
        return {
            "page_faults": self.page_faults,
            "memory_states": self.memory_states
        }

    def remove_victim(self):
        raise NotImplementedError()
