from copy import deepcopy
from typing import List, Optional

from utils.Serializable import Serializable
from .Page import Page


class MemoryFull(Exception):
    """
    Exception used to signal full memory when trying to load a new page
    """
    pass


class MemoryManager(Serializable):
    """
    General memory manager implementation
    """

    def __init__(self, access_list: List[int], memory_size: int):
        """
        :param access_list: list of sequentially accessed pages
        :param memory_size: size of physical memory in pages
        """
        assert memory_size > 0

        self.memory_size = memory_size
        self.access_list = access_list
        self.all_pages: List[Page] = []
        self.cached_pages: List[Page] = []
        self.page_faults = 0
        self.current_cycle = 0

        # Used to store snapshots of memory within each simulation cycle (mainly for debugging purposes)
        self.memory_states: List[List[Page]] = []

    def process_all(self):
        """
        Process all pages (perform full simulation)
        """
        for page_number in self.access_list:
            if not self.is_cached(page_number):
                self.page_faults += 1

                try:
                    self.load_page(page_number)
                except MemoryFull:
                    self.remove_victim()
                    self.load_page(page_number)

            self.use_page(page_number)
            self.memory_states.append(deepcopy(self.cached_pages))

            self.current_cycle += 1

    def is_cached(self, page_number: int) -> bool:
        """
        Check whether a page of given number exists in memory
        :param page_number: number of page to check
        """
        return self.get_page(page_number, self.cached_pages) is not None

    def page_exists(self, page_number) -> bool:
        """
        Check whether a page of given number exists at all
        :param page_number: number of page to check
        """
        return self.get_page(page_number, self.all_pages) is not None

    def use_page(self, page_number):
        """
        Use a page
        :param page_number: number of page to use
        """
        self.get_page(page_number, self.all_pages).use()

    def load_page(self, page_number):
        """
        Load a page to memory
        :param page_number: number of page to load
        """
        # Actual memory size should never exceed the limit
        assert len(self.cached_pages) <= self.memory_size

        if len(self.cached_pages) == self.memory_size:
            raise MemoryFull()

        # If the requested page does not exist, create it (and load). Otherwise, just get it from the pool and load.
        if not self.page_exists(page_number):
            new_page = Page(page_number)
            self.all_pages.append(new_page)
            self.cached_pages.append(new_page)
        else:
            self.cached_pages.append(self.get_page(page_number, self.all_pages))

    @staticmethod
    def get_page(page_number: int, page_list: List[Page]) -> Optional[Page]:
        """
        Find a page by its number
        :param page_number: number of page to search for
        :param page_list: list of pages to search in
        :return: a page or `None` if not found
        """
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
        """
        Select and remove a page from memory selected using a specific algorithm (implemented by a derived class)
        """
        raise NotImplementedError()
