from typing import Iterable

import markdown
from bs4 import BeautifulSoup

from markdowns.elements import Heading

TABLE_OF_CONTENTS_HEADINGS = ("h1", "h2")
MARKDOWN_EXTENSIONS = ("meta", "tables")


class MarkdownParser:
    def __init__(self, source: str):
        md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
        self.html_content: str = md.convert(source)
        self.metadata: dict[str, str] = md.Meta  # type: ignore[attr-defined]
        self.soup = BeautifulSoup(self.html_content, "html.parser")

    def get_title(self) -> str:
        if "title" not in self.metadata or len(self.metadata["title"]) != 1:
            raise ValueError("Markdown post must contain a valid title.")

        return self.metadata["title"][0]

    def get_description(self) -> str:
        if "description" not in self.metadata or len(self.metadata["description"]) != 1:
            raise ValueError("Markdown post must contain a valid description.")

        return self.metadata["description"][0]

    def get_content(self) -> str:
        for heading in self.soup.find_all(TABLE_OF_CONTENTS_HEADINGS):
            heading["id"] = Heading(
                level=int(heading.name[1]),
                text=heading.get_text(),
            ).id
        return str(self.soup)

    def extract_heading(self) -> Iterable[Heading]:
        return tuple(
            Heading(
                level=int(heading.name[1]),
                text=heading.get_text(),
            )
            for heading in self.soup.find_all(TABLE_OF_CONTENTS_HEADINGS)
        )
