# Contribution Guidelines

Thank you for considering to help this project.

We welcome all support, whether on bug reports, code, design, reviews, tests, documentation, and more.

Please note that this project is released with a [Contributor Code of Conduct](docs/CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## Development

### Installation

> Requirements: `virtualenv`, `pyenv`

```bash
git clone git@github.com:thibaudcolas/kontrasto.git
cd kontrasto/
# Install required Python versions
pyenv install --skip-existing 3.7.8
# Make required Python versions available globally.
pyenv global system 3.7.8
# Install the Python environment.
virtualenv .venv -p python3.7
source ./.venv/bin/activate
make init
nvm use
npm install
```

### Commands

```bash
python manage.py runserver
npm run start
```

```bash
make help           # See what commands are available.
make init           # Install dependencies and initialise for development.
make lint           # Lint the project.
make format         # Format project files.
make test           # Test the project.
make clean-pyc      # Remove Python file artifacts.
make dump-demo     # One-off fixtures dump command to bootstrap demo sites from.
make build-demo     # Builds the demo site for static hosting.
make sdist          # Builds package version
make publish        # Publishes a new version to pypi.
make publish-test   # Publishes a new version to test pypi.
```

## Releases

- Make a new branch for the release of the new version.
- Update the [CHANGELOG](https://github.com/thibaudcolas/kontrasto/blob/main/CHANGELOG.md).
- Update the version number in `kontrasto/__init__.py`, following semver.
- Make a PR and squash merge it.
- Back on the `main` branch with the PR merged, use `make publish-test` (confirm, and enter your password, confirm everything good on test.pypi.org).
- Back on the `main` branch with the PR merged, use `make publish` (confirm, and enter your password).
- Finally, go to GitHub and create a release and a tag for the new version.
- Done!
