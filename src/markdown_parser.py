import markdown


class MarkdownParser:
    def __init__(self, raw: str):
        md = markdown.Markdown(extensions=["meta"])
        self.content: str = md.convert(raw)
        self.metadata: dict[str, str] = md.Meta  # type: ignore[attr-defined]

    def get_title(self) -> str:
        if "title" not in self.metadata or len(self.metadata["title"]) != 1:
            raise ValueError("Markdown post must contain a valid title.")

        return self.metadata["title"][0]

    def get_description(self) -> str:
        if "description" not in self.metadata or len(self.metadata["description"]) != 1:
            raise ValueError("Markdown post must contain a valid description.")

        return self.metadata["description"][0]

    def get_content(self) -> str:
        return self.content
