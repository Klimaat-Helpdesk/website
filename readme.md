# Klimaathelpdesk

This is the repository for website https://klimaathelpdesk.org

## Repositories

This project consists of the following repositories:

- A [repository on gitlab](https://gitlab.com/fourdigits/klimaat-helpdesk/) that is used for general development and deployment of the website. This repository is private and contains code in a separate `ci-utils` branch, as it is internal machinery for deployment to Four Digits infrastructure.
- A [public repository on github](https://github.com/Klimaat-Helpdesk/website) that publishes the `main` branch of the above repository.
- The [wagtail-helpdesk project on github](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk) contains the reusable Django `wagtail-helpdesk` app that comprises the main functionality of Klimaathelpdesk: asking questions, and answering, tagging, reviewing and publishing them. This package can be used to implement similar-working websites.

## Requirements

The Klimaathelpdesk.org website uses `wagtail-helpdesk`, which builds on `wagtail`, for its main functionality.

### Database

We assume you have Postgres on your $PATH, for example:

    PATH=$PATH:/Applications/Postgres.app/Contents/Versions/13/bin/

Create a database:

    createdb klimaat-helpdesk


### Front-end build

We require:

- NodeJS (see [package.json](./package.json) for which version)


## Installation

    make develop

Possibly, create a superuser by activating the virtualenv and:

    ./manage.py createsuperuser


### Running

To start the Django server:

    make run

Note that `manage.py` assumes the default settings file to be `settings/development.py`. (Production configs don't use that, see the "Deployment and environments" section below.)


## Development

### Development workflow

#### Setup your local sources

- Clone `klimaat-helpdesk` from gitlab:

```shell
git clone git@gitlab.com:fourdigits/klimaat-helpdesk.git
```

- Create default development setup:

```shell
createdb klimaat-helpdesk
make develop
```

- Get data from `acceptance` environment and test the website:

```shell
# The fabfile is in a different branch to ensure we don't push it to the public github repo
git checkout ci-utils
fab get_data acceptance
git checkout main
make run
firefox http://localhost:8000
```

- Replace the pip-installed `wagtail-helpdesk` package with a local git checkout:

```shell
# This checks out the repository next to the klimaat-helpdesk repo
git clone git@github.com:Klimaat-Helpdesk/wagtail-helpdesk.git ../wagtail-helpdesk
pip install -e ../wagtail-helpdesk
make run
```

#### Make development changes

Changes to the `klimaat-helpdesk` repo can be handled as a regular development change.

For changes to `wagtail-helpdesk`:

- Run `make run` in the `klimaat-helpdesk` repo to get to see changes on http://localhost:8000
- Run `yarn start` in the `wagtail-helpdesk` repo to rebuild frontend files automatically, refresh the page for updates.

If you made changes to frontend files, after all files have been updated, run `yarn build` and commit the produced changes to the repo (yes, in the `static` folder).


#### Deploy a new version

- Create a new release for wagtail-helpdesk (if you made changes to the repo). After all changes are merged, [update the version in \_\_init\_\_.py](https://github.com/Klimaat-Helpdesk/wagtail-helpdesk/blob/main/wagtail_helpdesk/__init__.py) and create a corresponding git tag.

- Update the used version of the `wagtail-helpdesk` package [in the `website` requirements](https://gitlab.com/fourdigits/klimaat-helpdesk/-/blob/main/requirements/base.in) if needed, and run `make requirements`. Commit the new requirements.

- After all other changes are done, create a development tag (`x.y.zdevN`) and deploy to test/acceptance. If the changes are accepted, add a production tag (`x.y.z`) and deploy to acceptance and production.

- Push the updated `klimaat-helpdesk` `main` branch to the github repo by adding an additional remote in git:

```shell
git remote add github git@github.com:Klimaat-Helpdesk/website.git
git push github main
git push github --tags
```

### Testing

Run:

    make test

For more control locally:

    make test PYTEST_ADDOPTS="-k test_only_this_test --pdb"

Note: You can also run ``pytest`` directly, but `make test` also runs Python in
[development mode](https://docs.python.org/3/library/devmode.html), which provides
more warnings (for example, about unclosed files).

#### Test coverage

Running `pytest` or `make test` will also generate a coverage report.
An HTML version will be placed in `htmlcov/`.

The file `.gitlab-ci.yml` uses the generated `coverage.xml` to show
(in the MR on Gitlab) which code changes are being hit by automatic tests,
making code review easier.

### Code conventions

#### Python

Flake-8 is enforced by the test suite.

You can configure the exceptions to ignore in `setup.cfg`, for example if
you want change the maximum allowed line length.

You can easily fix all code convention errors with `make fix-codestyle`.

#### Frontend

[Prettier](https://prettier.io/) is enforced for code formatting. The easiest way to apply prettier is to install a [plugin for your editor](https://prettier.io/docs/en/editors.html) and apply the formatting on save.
For linting we use [ESLint](https://eslint.org/) and [Stylelint](https://stylelint.io/).

To check formating and linting run `yarn lint` and to automatically fix things (if possible) run `yarn lint:fix`.

### Dependency management

Our dependencies are managed with [pip-tools](https://github.com/jazzband/pip-tools).
In `requirements/base.in`, we pin as few packages as we can, and pip-tools generates the rest for us.

To upgrade dependencies, run:

```shell
make requirements
```

By default, all dependencies that can be upgraded to a newer version are automatically pinned to
the newest available version.

If you only changed a pinning of a single package, or only added a new dependency, use:

```shell
make requirements UPGRADE=no
```

## Deployment and environments

Test is deployed automatically when the `main` branch is updated, for acceptance and production you can use the
deploy button in gitlab, available after you add a tag (and a successful build).

It's also possible to run deployment manually from you own command line with::

    fab deploy production --ref=<tag/branch>
