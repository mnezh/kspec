K8S_CONTEXT ?=
ENV_CONFIG ?=
MARKERS ?=
TESTS ?= tests


PYTEST_ARGS = $(if $(K8S_CONTEXT),--k8s-context $(K8S_CONTEXT),) $(if $(ENV_CONFIG),--env-config $(ENV_CONFIG),) $(if $(MARKERS),-m "$(MARKERS)",)

venv: 
	python -m venv venv
	./venv/bin/python -m pip install --upgrade pip

.PHONY: setup
setup: requirements.txt venv
	./venv/bin/python -m pip install -r requirements.txt

.PHONY: style
style: setup
	./venv/bin/python -m yamllint -d "{extends: default, ignore: venv}"  --strict -f parsable .
	./venv/bin/python -m ruff .


.PHONY: format
format: setup
	./venv/bin/python -m ruff --fix .
	./venv/bin/python -m black --exclude venv .

reports:
	mkdir reports

reports/allure: reports
	mkdir reports/allure

.PHONY: test
test-k8s: reports/allure
	./venv/bin/python -m pytest \
		$(PYTEST_ARGS) \
		$(TESTS)


.PHONY: test
test-k8s-junit: reports/allure
	./venv/bin/python -m pytest \
		$(PYTEST_ARGS) \
		$(TESTS) \
		--junitxml=reports/result.xml


.PHONY: test
test-k8s-debug: reports/allure
	./venv/bin/python -m pytest \
		-s \
		$(PYTEST_ARGS) \
		$(TESTS)

.PHONY: allure
allure: reports/allure
	allure serve reports/allure

.PHONY: clean-reports
clean-reports:
	rm -rf reports

.PHONY: clean
clean: clean-reports
	rm -rf venv
