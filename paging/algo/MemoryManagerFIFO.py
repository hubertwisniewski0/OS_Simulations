from ..core.MemoryManager import MemoryManager


class MemoryManagerFIFO(MemoryManager):
    """
    First In First Out page replacement algorithm implementation
    """

    def remove_victim(self):
        # Just remove the first page from memory. Pages are loaded by appending them to the end of this list,
        # so effectively this implementation uses this list as a queue.
        del self.cached_pages[0]
