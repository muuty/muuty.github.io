import glob
import logging
import os

from jinja2 import Environment, FileSystemLoader, Template

from markdowns.markdown_parser import MarkdownParser

TEMPLATE_DIR = "src/templates"
POST_TEMPLATE = "post.html"
PAGE_TEMPLATE = "page.html"
HEADER_TEMPLATE = "header.html"
PAGES_FILE_PATTERN = "_pages/**/*.md"
PAGES_DIR = "pages"


class PageBuilder:
    def __init__(self) -> None:
        self.env = Environment(loader=FileSystemLoader(searchpath=TEMPLATE_DIR))

    def build_pages(self) -> None:
        post_template = self.env.get_template(POST_TEMPLATE)
        page_template = self.env.get_template(PAGE_TEMPLATE)
        header = self.env.get_template(HEADER_TEMPLATE).render()

        for markdown_file_name in glob.iglob(PAGES_FILE_PATTERN, recursive=True):
            print(markdown_file_name)
            try:
                with open(markdown_file_name, "r", encoding="utf-8") as file:
                    post_content = file.read()

                with open(
                    self.get_destination(markdown_file_name), "w", encoding="utf-8"
                ) as file:
                    template = (
                        post_template
                        if self._is_post(markdown_file_name)
                        else page_template
                    )
                    html = self._render_html(post_content, template, header)
                    file.write(html)
            except ValueError as e:
                logging.error("Error processing file %s: %s", markdown_file_name, e)

    def _is_post(self, file_name: str) -> bool:
        return file_name.split("\\")[1] == "posts"

    def get_destination(self, markdown_file_name: str) -> str:
        relative_path = os.path.relpath(markdown_file_name, "_pages")
        destination = os.path.join(
            PAGES_DIR, os.path.splitext(relative_path)[0] + ".html"
        )
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        return destination

    def _render_html(
        self, post_content: str, post_template: Template, header: str
    ) -> str:
        parser = MarkdownParser(post_content)
        rendered_html = post_template.render(
            header=header,
            title=parser.get_title(),
            description=parser.get_description(),
            content=parser.get_content(),
            table_of_contents=parser.extract_heading(),
        )
        return rendered_html


if __name__ == "__main__":
    PageBuilder().build_pages()
