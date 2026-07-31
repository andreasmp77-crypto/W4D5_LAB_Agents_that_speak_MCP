# Standard library imports for file-system traversal and typed return values.
from pathlib import Path
from typing import Any

# FastMCP is the small MCP server wrapper used for this local document source.
from mcp.server.fastmcp import FastMCP

# Resolve the repository root from this file's location.
LAB_ROOT = Path(__file__).resolve().parent
# The only folder this MCP server is allowed to expose.
ETS_DOCS_DIR = (LAB_ROOT / "lab_docs" / "ets_fueleu").resolve()

# Create an MCP server named for the ETS fuel document set.
mcp = FastMCP("ets-fuel")


def _ensure_inside_docs_dir(candidate: Path) -> Path:
    # Resolve the candidate so path checks cannot be bypassed with `..`.
    resolved = candidate.resolve()
    # Reject any path that escapes the ETS folder.
    if ETS_DOCS_DIR not in resolved.parents and resolved != ETS_DOCS_DIR:
        raise ValueError("Path must stay inside lab_docs/ets_fueleu")
    # Ensure the final path is a real file.
    if not resolved.is_file():
        raise FileNotFoundError(f"Document not found: {resolved.name}")
    # Return the validated path for reading.
    return resolved


def _read_text(path: Path) -> str:
    # Read text defensively so encoding issues do not crash the server.
    return path.read_text(encoding="utf-8", errors="replace")


def _iter_documents() -> list[Path]:
    # Collect every file recursively inside the ETS source folder.
    return sorted(
        path
        for path in ETS_DOCS_DIR.rglob("*")
        if path.is_file()
    )


@mcp.tool()
def list_ets_documents() -> list[str]:
    """List all documents available in the local ETS folder."""
    # Return each file path relative to the ETS root for easy reading.
    return [str(path.relative_to(ETS_DOCS_DIR).as_posix()) for path in _iter_documents()]


@mcp.tool()
def read_ets_document(path: str) -> str:
    """Read one local ETS document by relative path."""
    # Join the provided relative path to the ETS root and validate it.
    resolved = _ensure_inside_docs_dir(ETS_DOCS_DIR / path)
    # Return the full text content of the file.
    return _read_text(resolved)


@mcp.tool()
def search_ets_documents(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search local ETS documents for a string query and return matching excerpts."""
    # Empty queries should not waste time scanning files.
    if not query.strip():
        return []

    # Store the best match for each document.
    matches: list[dict[str, Any]] = []
    # Normalize the query into token-like words so overlap scoring is robust.
    keywords = {
        token
        for token in "".join(
            ch.lower() if ch.isalnum() else " " for ch in query
        ).split()
        if len(token) >= 4
    }

    # Scan each document for the line with the highest overlap to the query.
    for document in _iter_documents():
        # Load the current document text once.
        text = _read_text(document)
        # Keep track of the strongest line match in this file.
        best_line = None
        best_score = 0

        # Score every line by shared query tokens.
        for line_number, line in enumerate(text.splitlines(), start=1):
            # Normalize the current line into comparable tokens.
            line_tokens = {
                token
                for token in "".join(
                    ch.lower() if ch.isalnum() else " " for ch in line
                ).split()
                if len(token) >= 4
            }
            # Count token overlap as a simple relevance score.
            score = len(keywords & line_tokens)
            # Keep the strongest matching line found so far.
            if score > best_score:
                best_score = score
                best_line = {
                    "path": str(document.relative_to(ETS_DOCS_DIR).as_posix()),
                    "line": line_number,
                    "excerpt": line.strip(),
                    "score": score,
                }

        # Keep only documents with at least one useful match.
        if best_line and best_score > 0:
            matches.append(best_line)

        # Stop once enough candidate documents have been found.
        if len(matches) >= limit:
            break

    # Sort results so the highest-scoring matches appear first.
    return sorted(matches, key=lambda item: (-item["score"], item["path"], item["line"]))


if __name__ == "__main__":
    # Refuse to start if the ETS folder is missing.
    if not ETS_DOCS_DIR.is_dir():
        raise RuntimeError(f"Expected ETS source folder at: {ETS_DOCS_DIR}")

    # Launch the MCP server process and wait for tool calls.
    mcp.run()
