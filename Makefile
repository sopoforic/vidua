clean: clean-build clean-pyc clean-test clean-docs

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test:
	rm -rf .tox/
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache

clean-docs:
	rm -f docs/vidua.rst
	rm -f docs/modules.rst

coverage:
	coverage run --source . -m pytest
	@coverage report -m
	@coverage html
	@open htmlcov/index.html

docs: clean-docs
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

test:
	bandit vidua -rq --config bandit.yml --exit-zero
	flake8 . --exit-zero --max-complexity=10 --max-line-length=100
	pytest -q

prerelease:
	@bandit vidua -rq --config bandit.yml
	@flake8 . --max-line-length=100
	@pytest

dist: clean
	@python3 setup.py sdist bdist_wheel

release: prerelease dist
	@twine upload dist/*

.PHONY: test prerelease coverage dist prerelease release clean clean-build clean-test clean-pyc clean-docs docs
