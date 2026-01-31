.PHONY: install run gui debug clean lint format lint-strict test build

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

gui:
	python3 -m mazegen.render

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	rm -rf mazegen/__pycache__ tests/__pycache__
	rm -rf *.egg-info dist build
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -delete

lint:
	flake8 .
	mypy . --check-untyped-defs --exclude tests

lint-strict:
	flake8 .
	mypy . --strict --exclude tests

test:
	pytest tests/

format:
	black .

format-check:
	black --check .

build:
	python3 -m build
	@echo "\n✓ Build complete! Package available at: dist/"
