import glob
import os


from elements.page import PageList
from markdowns.markdown_page import MarkdownPage
from templates.template import POST_TEMPLATE, PAGE_TEMPLATE, POSTS_TEMPLATE
from jinja2 import Template


HEADER_TEMPLATE = "header.html"
PAGES_FILE_PATTERN = "_pages/**/*.md"
PAGES_DIR = "pages"
MARKDOWN_PAGES_DIR = "_pages"


class PageBuilder:
    def __init__(self) -> None:
        self.post_list = PageList()

    def build_pages(self) -> None:
        for file_path in glob.iglob(PAGES_FILE_PATTERN, recursive=True):
            with open(file_path, "r", encoding="utf-8") as file:
                post_content = file.read()

            page = MarkdownPage(post_content, file_path)
            if page.is_post():
                self.post_list.add(page)
            else:
                template = self._get_template(page)
                page_in_html = self.render(
                    page=page,
                    previous_page=None,
                    next_page=None,
                    template=template,
                )
                self.write_page_on_destination(
                    self.get_destination(page.source_path), page_in_html
                )

        sorted_pages = self.post_list.get_sorted_pages()
        for i, page in enumerate(sorted_pages):
            previous_page = sorted_pages[i - 1] if i > 0 else None
            next_page = sorted_pages[i + 1] if i < len(sorted_pages) - 1 else None

            template = self._get_template(page)

            page_in_html = self.render(
                page=page,
                previous_page=previous_page,
                next_page=next_page,
                template=template,
            )

            self.write_page_on_destination(
                self.get_destination(page.source_path), page_in_html
            )

        posts_page = self.render_posts(PAGE_TEMPLATE, self.post_list)

        with open("pages\posts.html", "w", encoding="utf-8") as file:
            file.write(posts_page)

    def render_posts(self, template: Template, post_list: PageList) -> str:
        rendered_html = template.render(
            title=None,
            description=None,
            content=POSTS_TEMPLATE.render(post_list=post_list),
            table_of_contents=None,
            previous_page=None,
            next_page=None,
        )

        return rendered_html

    def write_page_on_destination(self, destination: str, page_in_html: str) -> None:
        with open(destination, "w", encoding="utf-8") as file:
            print(f"{destination} is wrote")
            file.write(page_in_html)

    def render(
        self,
        page: MarkdownPage,
        previous_page: MarkdownPage | None,
        next_page: MarkdownPage | None,
        template: Template,
    ) -> str:
        rendered_html = template.render(
            title=page.title,
            description=page.description,
            content=page.get_content(),
            table_of_contents=page.extract_heading(),
            previous_page=previous_page,
            next_page=next_page,
        )

        return rendered_html

    def _get_template(self, page: MarkdownPage) -> Template:
        return POST_TEMPLATE if page.is_post() else PAGE_TEMPLATE

    def get_destination(self, markdown_file_name: str) -> str:
        relative_path = os.path.relpath(markdown_file_name, MARKDOWN_PAGES_DIR)
        destination = os.path.join(
            PAGES_DIR, os.path.splitext(relative_path)[0] + ".html"
        )
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        return destination


if __name__ == "__main__":
    PageBuilder().build_pages()
