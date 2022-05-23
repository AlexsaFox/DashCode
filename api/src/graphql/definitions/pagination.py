from typing import Generic, TypeVar

import strawberry


T = TypeVar('T')
Cursor = str


@strawberry.type
class Page:
    has_next_page: bool
    start_cursor: Cursor | None
    end_cursor: Cursor | None


@strawberry.type
class Edge(Generic[T]):
    node: T
    cursor: Cursor


@strawberry.type
class Connection(Generic[T]):
    page_info: Page
    edges: list[Edge[T]]
