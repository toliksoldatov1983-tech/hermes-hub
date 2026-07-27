from __future__ import annotations

from hermes_core.memory.memory_source import MemorySource


class MemoryRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, MemorySource] = {}

    def register(self, source: MemorySource) -> None:
        self._sources[source.name] = source

    def trusted_sources(self) -> list[MemorySource]:
        return [source for source in self._sources.values() if source.trusted]

    def get(self, name: str) -> MemorySource | None:
        return self._sources.get(name)
