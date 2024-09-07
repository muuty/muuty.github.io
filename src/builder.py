import glob
import logging
import os

from jinja2 import Environment, FileSystemLoader, Template

from markdown_parser import MarkdownParser

TEMPLATE_DIR = "src/templates"
POST_TEMPLATE = "post.html"
POSTS_FILE_PATTERN = "_posts/*.md"
PAGES_DIR = "pages"


class PageBuilder:
    def __init__(self) -> None:
        self.env = Environment(loader=FileSystemLoader(searchpath=TEMPLATE_DIR))

    def build_posts(self) -> None:
        template = self.env.get_template("post.html")

        for markdown_file_name in glob.iglob(POSTS_FILE_PATTERN):
            try:
                with open(markdown_file_name, "r", encoding="utf-8") as file:
                    post_contents = file.read()

                html_file_name = os.path.basename(markdown_file_name)
                destination = os.path.join(
                    PAGES_DIR, os.path.splitext(html_file_name)[0] + ".html"
                )

                with open(destination, "w", encoding="utf-8") as file:
                    html = self._render_html(post_contents, template)
                    file.write(html)
            except ValueError as e:
                logging.error("Error processing file %s: %s", markdown_file_name, e)

    def _render_html(self, post_contents: str, template: Template) -> str:
        parser = MarkdownParser(post_contents)
        rendered_html = template.render(
            title=parser.get_title(),
            description=parser.get_description(),
            content=parser.get_content(),
        )
        return rendered_html


if __name__ == "__main__":
    PageBuilder().build_posts()
