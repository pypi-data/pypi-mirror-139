PHONY: test fmt typecheck lint package dev-requirements publish-test publish-prod

test: dev-requirements
	pytest

fmt: dev-requirements
	black src/oso_cloud

typecheck: dev-requirements
	mypy src/oso_cloud

lint: dev-requirements
	flake8 src/oso_cloud

package:
	rm -rf .eggs build dist
	python3 -m pip install --upgrade build
	python3 -m build

publish-test:
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository testpypi dist/*

publish-prod:
	python3 -m pip install --upgrade twine
	python3 -m twine upload --repository pypi dist/*

dev-requirements: .make.dev-requirements-install

.make.dev-requirements-install: requirements-dev.txt
	pip install -r requirements-dev.txt
	touch $@
