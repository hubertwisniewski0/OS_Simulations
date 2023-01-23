from ..core.MemoryManager import MemoryManager


class MemoryManagerOptimal(MemoryManager):
    """
    Optimal page replacement algorithm implementation
    """

    def get_next_usage(self, page_number: int) -> int:
        """
        Determine when a page will be used next
        :param page_number: number of page to search for
        :return: number of simulation cycle when the page will be used next,
        or the request list length if the page will never be used
        """
        # Search for the nearest page access starting from the current cycle
        check_cycle = self.current_cycle
        while check_cycle < len(self.access_list) and self.access_list[check_cycle] != page_number:
            check_cycle += 1
        return check_cycle

    def remove_victim(self):
        # Search for a page with the largest next usage time (which will not be requested for the greatest period of
        # time from all cached pages)
        greatest_next_usage = 0
        greatest_next_usage_page = None

        for page in self.cached_pages:
            next_usage = self.get_next_usage(page.page_number)
            if next_usage > greatest_next_usage:
                greatest_next_usage = next_usage
                greatest_next_usage_page = page

        self.cached_pages.remove(greatest_next_usage_page)
