## Commits

Format: `:gitmoji: Message` — message starts uppercase, written in English.
No co-author lines — never add `Co-Authored-By` trailers.

## Code Style

Formatter: `ruff` (`make fix` to apply, `make check` to verify)
Line length: 124 · Target: Python 3.12 · Rules: E, F, I, W

## Testing

Run tests: `make test` (enforces ≥70% coverage via `--cov-fail-under=70`).

Every test function MUST follow the `# Setup / # Action / # Expected` pattern — these three comments are the only comments allowed in a test. No blank lines between sections.

```python
def test_create_something(client, workspace_id):
    # Setup
    payload = {"name": "Example", "description": "A description", "status": "active"}
    # Action
    response = client.post(f"/ws/{workspace_id}/things/", json=payload)
    # Expected
    expected = {
        "id": ANY,
        "created_at": ANY,
        "name": "Example",
        "description": "A description",
        "status": "active",
    }
    assert response.status_code == 201
    assert response.json() == expected


def test_get_something_not_found(client, workspace_id):
    # Action
    response = client.get(f"/ws/{workspace_id}/things/999999")
    # Expected
    expected = {"detail": "Thing not found."}
    assert response.status_code == 404
    assert response.json() == expected
```

Rules:
- Maximum 2 `assert` statements per test: one for status code, one for the complete JSON body.
- `expected` must declare every field explicitly. Use `unittest.mock.ANY` only for genuinely dynamic values (UUIDs, timestamps). Never use `ANY` for known static values.
- Never validate only keys or parse the response into a model — those patterns don't verify values.
- Omit `# Setup` if there is no setup code — never write two consecutive section comments.
- Tests are co-located with the module they cover: `<package>/<module>/tests/test_name.py`.
- Shared fixtures live in a `conftest.py` at the package root: `client` (`scope="session"`) and any shared resource fixture (`scope="module"`).

