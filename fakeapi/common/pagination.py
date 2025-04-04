from dataclasses import dataclass


@dataclass(frozen=True)
class PaginatorConfig:
    default_page_size: int
    max_page_size: int


class PaginationPreset:
    STANDARD = PaginatorConfig(default_page_size=30, max_page_size=100)
    MEDIUM = PaginatorConfig(default_page_size=50, max_page_size=150)
    LARGE = PaginatorConfig(default_page_size=100, max_page_size=200)
