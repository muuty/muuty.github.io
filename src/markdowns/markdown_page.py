from typing import Iterable, Any, Tuple
from dataclasses import dataclass
import os

import markdown
from bs4 import BeautifulSoup

from elements.heading import Heading

TABLE_OF_CONTENTS_HEADINGS = ("h2", "h3")  # h1 is title
MARKDOWN_EXTENSIONS = ("meta", "tables")
REQUIRED_METADATA_FIELDS = ("title", "description", "created_at")


@dataclass
class MarkdownPage:
    title: str
    description: str
    created_at: str
    tags: Tuple[str]
    source_path: str

    def __init__(self, source: str, source_path: str):
        md = markdown.Markdown(extensions=MARKDOWN_EXTENSIONS)
        self.html_content: str = md.convert(source)
        self.metadata: dict[str, Any] = md.Meta  # type: ignore[attr-defined]
        self._validate_metadata(self.metadata)
        self.source_path = source_path

        self.soup = BeautifulSoup(self.html_content, "html.parser")

        self.title = self.metadata["title"][0]
        self.description = self.metadata["description"][0]
        self.created_at = self.metadata["created_at"][0]
        self.tags = self.metadata["tags"] if "tags" in self.metadata else []

    def is_post(self) -> bool:
        return self.source_path.split("\\")[1] == "posts"

    def _validate_metadata(self, metadata: dict[str, Any]):
        not_filled_fields = [
            field for field in REQUIRED_METADATA_FIELDS if field not in metadata
        ]

        if not_filled_fields:
            raise ValueError(
                f"Markdown post must contain a valid {','.join(not_filled_fields)}."
            )

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

    def get_page_path(self) -> str:
        relative_path = os.path.relpath(self.source_path, "_pages")
        destination = os.path.join(
            os.path.splitext(relative_path)[0].replace("\\", "/")
        )
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        return destination
