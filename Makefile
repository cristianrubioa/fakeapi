# Define default shell
SHELL := /bin/bash

# Define source directory
SRC := fakeapi

# 🐍 Install dependencies
install:
	poetry install

# 🚀 Format code
format:
	poetry run black $(SRC)
	poetry run isort $(SRC)

# 🔍 Linting
lint:
	poetry run ruff check $(SRC) --preview

# 🧪 Run tests
test:
	poetry run pytest fakeapi --cov=fakeapi --cov-report=term-missing --cov-fail-under=70 --disable-warnings

# 🏆 Run all checks before commit
check: format lint test

# 🚀 Run dev server
run:
	poetry run uvicorn fakeapi.main:app --reload

# 📦 Update dependencies
update:
	poetry update

# 📌 Help
help:
	@echo "Available commands:"
	@echo "  install      Install dependencies using Poetry"
	@echo "  format       Format code using black and isort"
	@echo "  lint         Run ruff linter"
	@echo "  test         Run pytest"
	@echo "  check        Run format, linting, and tests"
	@echo "  run          Start uvicorn dev server with auto-reload"
	@echo "  update       Update all Poetry-managed dependencies"
