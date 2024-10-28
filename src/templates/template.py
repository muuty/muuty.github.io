from abc import ABCMeta

from markdowns.markdown_page import MarkdownPage
from jinja2 import Environment, FileSystemLoader


TEMPLATE_DIR = "src/templates"
POST_TEMPLATE = "post.html"
PAGE_TEMPLATE = "page.html"
POSTS_TEMPLATE = "posts.html"

ENV = Environment(loader=FileSystemLoader(searchpath=TEMPLATE_DIR))
POST_TEMPLATE = ENV.get_template(POST_TEMPLATE)
PAGE_TEMPLATE = ENV.get_template(PAGE_TEMPLATE)
POSTS_TEMPLATE = ENV.get_template(POSTS_TEMPLATE)


class Template(metaclass=ABCMeta):
    def render(self, page: MarkdownPage) -> str:
        pass


class PostTemplate(Template):
    def __init__(self):
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
    def __init__(self):
        self.template = PAGE_TEMPLATE

    def render(self, page: MarkdownPage) -> str:
        rendered_html = self.template.render(
            title=page.title,
            description=page.description,
            content=page.get_content(),
            table_of_contents=page.extract_heading(),
        )

        return rendered_html
