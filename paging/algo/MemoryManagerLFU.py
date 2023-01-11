from ..core.MemoryManager import MemoryManager


class MemoryManagerLFU(MemoryManager):
    def remove_victim(self):
        self.cached_pages.sort(key=lambda p: p.uses)
        del self.cached_pages[0]
