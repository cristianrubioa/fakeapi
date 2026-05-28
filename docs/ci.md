# CI

The project enforces a three-stage quality pipeline locally via `make`.

```mermaid
flowchart TD
    Commit(["git commit · :gitmoji: Capitalized message"]) --> Fmt

    Fmt["make format · black + isort"]
    Fmt -->|pass| Lint["make lint · ruff check"]
    Fmt -->|fail| XF(["blocked"])

    Lint -->|pass| Tests["make test · pytest · coverage >= 70%"]
    Lint -->|fail| XL(["blocked"])

    Tests -->|pass| Done(["ready to push"])
    Tests -->|fail| XT(["blocked"])
```

| Step | Command | Tool |
|---|---|---|
| Format | `make format` | black · isort |
| Lint | `make lint` | ruff |
| Test | `make test` | pytest · pytest-cov |
| All | `make check` | format → lint → test |

Commit format enforced: `:gitmoji: Capitalized message in English`
