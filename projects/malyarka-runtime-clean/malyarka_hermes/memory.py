"""Read-only helpers for Hermes memory documents."""

from pathlib import Path

DEFAULT_STATE_PATH = str(Path(__file__).resolve().parents[1] / "MALYARKA_CURRENT_STATE.md")


def read_text_file(path: str) -> str:
    """Read a UTF-8 text file."""
    return Path(path).read_text(encoding="utf-8")


def extract_markdown_section(text: str, heading: str) -> str:
    """Extract a markdown section by exact heading line."""
    lines = text.splitlines()
    start_index: int | None = None
    heading_level = heading_level_of(heading)

    for index, line in enumerate(lines):
        if line.strip() == heading:
            start_index = index
            break

    if start_index is None:
        return ""

    section_lines = [lines[start_index]]
    for line in lines[start_index + 1 :]:
        if is_heading_at_or_above_level(line, heading_level):
            break
        section_lines.append(line)

    return "\n".join(section_lines).strip()


def extract_first_status_block(text: str, max_chars: int = 500) -> str:
    """Return the first text block before the first second-level heading."""
    before_second_heading = text.split("\n##", 1)[0].strip()
    if not before_second_heading:
        return ""
    return before_second_heading[:max_chars].strip()


def read_current_state(path: str | None = None) -> str:
    if path is None:
        path = DEFAULT_STATE_PATH
    return read_text_file(path)


def heading_level_of(heading: str) -> int:
    stripped = heading.lstrip()
    return len(stripped) - len(stripped.lstrip("#"))


def is_heading_at_or_above_level(line: str, level: int) -> bool:
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return False
    current_level = len(stripped) - len(stripped.lstrip("#"))
    if current_level <= 0 or current_level > level:
        return False
    return len(stripped) > current_level and stripped[current_level] == " "
