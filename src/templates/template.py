from abc import ABCMeta, abstractmethod

from markdowns.markdown_page import MarkdownPage
from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = "src/templates"
ENV = Environment(loader=FileSystemLoader(searchpath=TEMPLATE_DIR))
POST_TEMPLATE = ENV.get_template("post.html")
PAGE_TEMPLATE = ENV.get_template("page.html")
POSTS_TEMPLATE = ENV.get_template("posts.html")


class Template(metaclass=ABCMeta):
    @abstractmethod
    def render(self, page: MarkdownPage) -> str:
        pass


class PostTemplate(Template):
    def __init__(self) -> None:
        self.template = POST_TEMPLATE

    def render(self, page: MarkdownPage) -> str:
        rendered_html = self.template.render(
            title=page.title,
            description=page.description,
            content=page.get_content(),
            table_of_contents=page.extract_heading(),
        )

        return rendered_html


class PageTemplate(Template):
    def __init__(self) -> None:
        self.template = PAGE_TEMPLATE

    def render(self, page: MarkdownPage) -> str:
        rendered_html = self.template.render(
            title=page.title,
            description=page.description,
            content=page.get_content(),
            table_of_contents=page.extract_heading(),
        )

        return rendered_html
