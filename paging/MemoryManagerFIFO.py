from .MemoryManager import MemoryManager


class MemoryManagerFIFO(MemoryManager):
    def remove_victim(self):
        del self.cached_pages[0]
