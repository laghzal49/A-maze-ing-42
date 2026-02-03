.PHONY: install run gui debug clean lint format lint-strict test build

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

gui:
	python3 a_maze_ing.py config.txt

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
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs --exclude tests

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
	@cp -f dist/mazegen-*.whl . 2>/dev/null || true
	@cp -f dist/mazegen-*.tar.gz . 2>/dev/null || true
	@echo "\n✓ Build complete! Package available at: dist/ (copied to repo root)"
