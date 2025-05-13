install:
	pip install -r requirements.txt

init:
	python -m pip install --upgrade pip setuptools wheel twine

test:
	pytest

build:
	python setup.py sdist bdist_wheel

publish:
	python -m twine upload dist/*

