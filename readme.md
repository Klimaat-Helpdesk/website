# klimaat-helpdesk

(Initial README generated from https://gitlab.com/fourdigits/utils/cookiecutter-wagtail/)

The layout of this project and some assumptions are documented here: https://fourdigits.atlassian.net/wiki/spaces/IM1/pages/61344106/Opzetten+van+een+Django+Wagtail+site


## Requirements

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

```bash
make requirements
```

By default, all dependencies that can be upgraded to a newer version are automatically pinned to
the newest available version.

If you only changed a pinning of a single package, or only added a new dependency, use:

```bash
make requirements UPGRADE=no
```

## Deployment and environments

Here we document where the TST/ACC/PRD environments live, and how to update them.

Before deployment, you add an entry to the changelog (see "Changelog location" below).

To be able to deploy you create a tag with the release and link to the changelog in its annotation.

Examples:

- `git tag -a 1.2.1 -m "https://support.fourdigits.nl/organisaties/<organisatie>/documenten/releases/<versie>"`
- `git tag -a 1.2.1 -m "See changes.rst"`


Test is deployed automatically when main is updated, for acceptance and production you can use the
deploy button in gitlab.

It's also possible to run deployment manually from you own command line with::

    fab deploy production --ref=<tag/branch>

### Configure Gitlab

In your Gitlab project you need two CI/CD variables for deployment:

- **SSH_PRIVATE_KEY**: A private key that can connect to servers (you can find this in 1password)
- **SSH_KNOWN_HOSTS**: List of servers it connects to and their RSA key (you can find this in 1password)

Go to Settings -> CI/CD -> Variables to add them.

Both variables need to *not* be [Protected](https://docs.gitlab.com/ee/ci/variables/index.html#protect-a-cicd-variable)
(Gitlab's default is to make them Protected).


### Slack integration

On successful deployment you can send the message to a Slack channel.
You need to create a Slack webhook url: https://api.slack.com/apps/AT9A3736D/incoming-webhooks

This webhook url needs to be configured as `SLACK_WEBHOOK` variable in Gitlab CI/CD `your project -> settings -> CI/CD -> Variables`


### Changelog location

The changelog can be kept in, for example:

- On `https://support.fourdigits.nl/organisaties/<organisatie>/documenten`
- In a file in this repository, eg. `CHANGES.txt` / `changes.md`
- Some other place that you agree on with the team

After deciding on where to keep the changelog, update this file.
