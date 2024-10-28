from typing import List

from markdowns.markdown_page import MarkdownPage


class PageList:
    pages: List[MarkdownPage]

    def __init__(self):
        self.pages = []

    def add(self, page: MarkdownPage):
        self.pages.append(page)

    def get_sorted_pages(self):
        return sorted(self.pages, key=lambda page: page.created_at)
