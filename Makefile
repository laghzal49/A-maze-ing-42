.PHONY: install run debug clean lint lint-strict

install:
    pip install -r requirements.txt

run:
    python3 a_maze_ing.py config.txt

debug:
    python3 -m pdb a_maze_ing.py config.txt

clean:
    rm -rf __pycache__ .mypy_cache .pytest_cache
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -delete

lint:
    flake8 .
    mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
    flake8 .
    mypy . --strict

test:
    pytest tests/

build:
    python3 -m build