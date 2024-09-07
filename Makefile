.PHONY: lint black mypy

# Linting using pylint
lint:
	@echo "Running lint..."
	poetry run flake8 src

# Formatting using Black
format:
	@echo "Running black and isort"
	poetry run black src
	poetry run isort src

# Type checking using MyPy
mypy:
	@echo "Running mypy..."
	poetry run mypy src

# Build Static Pages from markdown posts
build:
	@echo "Running build..."
	poetry run scripts build
