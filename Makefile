.PHONY: install browsers lint format test test-smoke test-api test-ui test-parallel allure-clean clean

install:
	python -m pip install -r requirements.txt
	python -m pip install -e .

browsers:
	python -m playwright install --with-deps

lint:
	ruff check .
	black --check .
	isort --check-only .

format:
	ruff check . --fix
	black .
	isort .

test:
	pytest

test-smoke:
	pytest -m smoke

test-api:
	pytest tests/api -m api

test-ui:
	pytest tests/ui -m ui

test-parallel:
	pytest -n auto

allure-clean:
	rm -rf reports/allure-results/* reports/allure-report/*

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage coverage.xml
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
