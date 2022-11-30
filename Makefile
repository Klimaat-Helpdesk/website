ENV = env
BIN = $(ENV)/bin
PYTHON_VERSION = 3.10
PYTHON = $(BIN)/python
GIT_STATUS = "$(shell git status --porcelain)"

UPGRADE = yes
ifeq ($(UPGRADE),yes)
	REQUIREMENTS_UPGRADE=--upgrade
else
	REQUIREMENTS_UPGRADE=--no-upgrade
endif

$(ENV):
	$(shell which python$(PYTHON_VERSION)) -m venv $(ENV)

requirements.txt.done: $(ENV) requirements.txt
	$(PYTHON) -m pip install --upgrade pip wheel setuptools
	$(PYTHON) -m pip install -r requirements.txt
	touch $@

build-frontend:
	yarn
	yarn build

develop: requirements.txt.done
	$(PYTHON) -m manage migrate
	make build-frontend

makemigrations: requirements.txt.done
	$(PYTHON) -m manage makemigrations

run: requirements.txt.done
	$(PYTHON) -m manage runserver

fix-codestyle: requirements.txt.done
	$(BIN)/black apps
	$(BIN)/isort apps

test: requirements.txt.done
	$(PYTHON) -m pip check
	$(BIN)/safety check --bare
	$(BIN)/flake8 apps
	$(PYTHON) -X dev -m pytest $(ARGS)

makemessages: requirements.txt.done
	cd apps/frontend && ../$(PYTHON) ../manage.py makemessages

compilemessages: requirements.txt.done
	cd apps/frontend && ../$(PYTHON) ../manage.py compilemessages

fixtures: requirements.txt.done
	$(PYTHON) -m manage build_fixtures

deploy_prd:
	$(BIN)/fab deploy production

deploy_acc:
	$(BIN)/fab deploy acceptance

clean:
	rm -f requirements.txt.done

realclean: clean
	rm -f -r $(ENV)

# Exit with error if git repo is dirty
.PHONY: test-repo-clean
test-repo-clean:
ifneq ($(GIT_STATUS), "")
	@echo "Repo has new or modified files. Either commit them or add to .gitgnore."
	@exit 1
endif

.PHONY: requirements
INFILES=production development deploy
requirements: $(ENV)
	$(PYTHON) -m pip install --upgrade pip-tools
	for INFILE in $(INFILES); do \
 		CUSTOM_COMPILE_COMMAND="make requirements" $(BIN)/pip-compile $(REQUIREMENTS_UPGRADE) --generate-hashes --output-file requirements/$${INFILE}.txt requirements/$${INFILE}.in; \
	done
