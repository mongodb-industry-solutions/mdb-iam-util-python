install:
	pip install -r requirements.txt

test:
	pytest

build:
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/*
