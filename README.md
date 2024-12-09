# <img src="resources/icon.jpeg" width="5%"> Plugin Blueprint

This is the README for your plugin.
Please fill it in with all the necessary information for other contributors.

To get started building your plugin, follow the instructions in [README.START.md](README.START.md).

## Development setup

To run your plugin locally requires the following setup:

1. Set up the [infrastructure](https://gitlab.heigit.org/climate-action/infrastructure) locally in `devel` mode
2. Copy your [.env.base_template](.env.base_template) to `.env.base` and update it
3. Run `poetry run python {plugin-name}/plugin.py`

If you want to run your plugin through Docker, refer to
the [Plugin Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase).

## Releasing a new plugin version

To release a new plugin version

1. Update the [CHANGELOG.md](CHANGELOG.md).
   It should already be up to date but give it one last read and update the heading above this upcoming release
2. Decide on the new version number.
   Once your plugin outgrew the 'special versions' `dummy` and `mvp`, we suggest you adhere to
   the [Semantic Versioning](https://semver.org/) scheme,
   based on the changes since the last release.
   You can think of your plugin methods (info method, input parameters and artifacts) as the public API of your plugin.
3. Update the version attribute in the [pyproject.toml](pyproject.toml) (e.g. by running
   `poetry version {patch|minor|major}`)
4. Create a [release]((https://docs.gitlab.com/ee/user/project/releases/#create-a-release-in-the-releases-page)) on
   GitLab, including a changelog
