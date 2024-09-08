from dataclasses import dataclass


@dataclass
class Heading:
    level: int
    text: str
    id: str

    def __init__(self, level: int, text: str):
        self.level = level
        self.text = text
        self.id = text.strip().replace(" ", "-").lower()
