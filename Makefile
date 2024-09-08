.PHONY: lint format mypy build preview

# Linting using pylint
lint:
	@echo "Running lint..."
	uv run ruff check src

# Formatting using Black
format:
	@echo "Running black and isort"
	uv run ruff format src

# Type checking using MyPy
mypy:
	@echo "Running mypy..."
	uv run mypy src

# Build Static Pages from markdown posts
build:
	@echo "Running build..."
	uv run src/scripts.py build


preview:
	@echo "Starting local server with live reload..."
	@cd pages && uv run livereload .
