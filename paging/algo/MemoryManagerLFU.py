from ..core.MemoryManager import MemoryManager


class MemoryManagerLFU(MemoryManager):
    """
    Least Frequently Used page replacement algorithm implementation
    """

    def remove_victim(self):
        # Sort the pages ascending by their use counts and remove the first one
        self.cached_pages.sort(key=lambda p: p.uses)
        del self.cached_pages[0]
