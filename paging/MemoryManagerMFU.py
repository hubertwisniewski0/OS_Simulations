from .MemoryManager import MemoryManager


class MemoryManagerMFU(MemoryManager):
    def remove_victim(self):
        self.cached_pages.sort(key=lambda p: p.uses, reverse=True)
        del self.cached_pages[0]
