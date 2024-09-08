.PHONY: lint black mypy

# Linting using pylint
lint:
	@echo "Running lint..."
	poetry run ruff check src

# Formatting using Black
format:
	@echo "Running black and isort"
	poetry run ruff format src

# Type checking using MyPy
mypy:
	@echo "Running mypy..."
	poetry run mypy src

# Build Static Pages from markdown posts
build:
	@echo "Running build..."
	poetry run scripts build


preview:
	@echo "Starting local server with live reload..."
	@cd pages && poetry run livereload .
