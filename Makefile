.PHONY: help install test lint run doc

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python2

.DEFAULT: help
help:
	@echo "make install"
	@echo "       prepare development environment, use only once"
	@echo "make test"
	@echo "       run tests"
	@echo "make lint"
	@echo "       run pylint and mypy"
	@echo "make run"
	@echo "       run project"
	@echo "make doc"
	@echo "       build sphinx documentation"

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate:
	test -d $(VENV_NAME) || virtualenv $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -r requirements.txt
	touch $(VENV_NAME)/bin/activate

install:
	rm -rf venv
	make venv

test: venv
	${PYTHON} -m pytest -v

lint: venv
	${PYTHON} -m pylint \
	./main.py \
	./main_test.py \
	./workspan/base.py \
	./workspan/tests/base_test.py \
	./workspan/clone.py \
	./workspan/tests/integration/clone_test.py \
	./workspan/formats.py \
	./workspan/entity.py \
	./workspan/tests/entity_test.py \
	./workspan/tests/formats_test.py \
	./workspan/tests/integration/formats_test.py \
	./workspan/graph.py \
	./workspan/tests/graph_test.py \
	./workspan/tests/integration/graph_test.py \
	./workspan/link.py \
	./workspan/processors.py \
	./workspan/tests/processors_test.py \
	./workspan/tests/integration/processors_test.py

run: venv
	${PYTHON} main.py input.json 5

doc: venv
	$(VENV_ACTIVATE) && cd docs; make html