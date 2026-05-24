from dataclasses import dataclass


@dataclass
class ListResponse[T]:
    items: list[T]
    total: int
    limit: int
    offset: int
