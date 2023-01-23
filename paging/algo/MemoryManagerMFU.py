from ..core.MemoryManager import MemoryManager


class MemoryManagerMFU(MemoryManager):
    """
    Most Frequently Used page replacement algorithm implementation
    """

    def remove_victim(self):
        # Sort the pages descending by their use counts and remove the first one
        self.cached_pages.sort(key=lambda p: p.uses, reverse=True)
        del self.cached_pages[0]
