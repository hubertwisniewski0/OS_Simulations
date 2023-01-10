from .MemoryManager import MemoryManager


class MemoryManagerOptimal(MemoryManager):
    def get_next_usage(self, page_number: int) -> int:
        check_cycle = self.current_cycle
        while check_cycle < len(self.access_list) and self.access_list[check_cycle] != page_number:
            check_cycle += 1
        return check_cycle

    def remove_victim(self):
        greatest_next_usage = 0
        greatest_next_usage_page = None

        for page in self.cached_pages:
            next_usage = self.get_next_usage(page.page_number)
            if next_usage > greatest_next_usage:
                greatest_next_usage = next_usage
                greatest_next_usage_page = page

        self.cached_pages.remove(greatest_next_usage_page)
