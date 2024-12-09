# Getting Started

This repository is a blueprint for operator creators.
Operators are science2production facilitators that will make it easy for you to bring your ideas and research results to
the Climate Action (CA) platform.
Operators are the main workers inside plugins.
You will create a plugin but all you need to do is code the operator functionality, the plugin wrapper is already set to
go.
The terms Operator and Plugin are therefore mostly synonymous for you.
For more information on the architecture, please contact the [CA team](https://heigit.org/).

**For an example of a fully developed plugin with all possible input and output types, check out
the [Plugin Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase).**

Please follow these steps to bring your plugin to life:

## Preparation

A new plugin should be thoroughly discussed with the CA team.
But don't be hesitant, they are very welcoming to new ideas :-) !

### Git

The CA team will fork **this** repository for you and you will get full access to the fork (see below for admins).
You can then `git clone` the fork and work on it as in any other git project.

Create a new branch by running `git checkout -b <my_new_plugin_name>`.
After you have finished your implementation, you can create a merge request (MR) to the `main` branch that can be
reviewed by the CA team.
Yet, we highly encourage you to create smaller intermediate MRs for review!

### Plugin name

We have to replace `"plugin-blueprint"` with the name of your plugin in multiple places.

1. Update your [pyproject.toml](pyproject.toml).
   In that file, replace the name, description and author attributes with your
   plugin's information.
   If you don't want to get creative you can simply mimic the repository name for your project name.
2. Update your plugin's name in [info.py](plugin_blueprint/core/info.py).
3. Refactor the name of the package itself ([plugin_blueprint/](plugin_blueprint)).
   Rename it to the project name you have defined above in your `pyproject.toml`.
4. Your plugin directory is also copied to the Docker container we use for deployment.
   Therefore, you have to change the name also in the [Dockerfile.Kaniko](Dockerfile.Kaniko).
5. Finally, update your plugin name and details in [README.md](README.md).

### Python Environment

We use [poetry](https://python-poetry.org) as an environment management system.
Make sure you have it installed.
Apart from some base dependencies, there is only one fixed dependency for you, which is
the [climatoology](https://gitlab.heigit.org/climate-action/climatoology) package that holds all the infrastructure
functionality.
Make sure you have read-access to the climatoology repository (i.e. you can clone it).

Now run

```shell
poetry install
```

and you are ready to code within your poetry environment.

### Testing

We use [pytest](https://pytest.org) as a testing engine.
Ensure all tests are passing by running `poetry run pytest`.
If any tests are failing, you've missed renaming from `plugin_blueprint` somewhere, so look for references to that in
the code.

### Linting and formatting

It is important that the code created by the different plugin developers adheres to a certain standard.
We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting the code as part of our pre-commit hooks.
Please activate pre-commit by running `poetry run pre-commit install`.
It will now run automatically before each commit and apply fixes for a variety of lint errors to your code.
Note that we have increased the maximum number of characters per line to be 120 to make better use of large modern
displays.
If you want to keep short lines explicitly separate (e.g. in the definition of functions or list) please
use ["magic trailing commas"](https://docs.astral.sh/ruff/settings/#format_skip-magic-trailing-comma).

### Logging

Please make sure to use logging throughout your plugin.
This will make debugging easier at a later stage.

## Development setup

You may want to run your plugin locally to see it in action.
Follow the [Development Setup](README.md#development-setup) instructions to do this.

## Start Coding

### First merge request

Now that your project naming is updated for your plugin, and you've run the tests, you are ready to **make this your
first merge request**.
Add your CA-team contact as reviewer.

### Structure

We have structured the code into two main categories based on their functionality:

1. [core](plugin_blueprint/core/): holds the critical infrastructure for hosting the plugin on the platform.
   As a plugin developer, you will mostly only change the definition of your plugin's inputs and outputs in these files.
2. [components](plugin_blueprint/components/): is for the implementation of your plugin, which you will develop
   Most of your coding should go in this submodule.

The following steps will help you get started with developing your plugin.

#### Describe your plugin in [info.py](plugin_blueprint/core/info.py)

The `get_info()` function here provides key information about your plugin including:

- The plugin's name
- The version number
- The plugin's purpose and methodology

Before you start coding your plugin operator, you should edit the [purpose.md](resources/info/purpose.md),
[methodology.md](resources/info/methodology.md), [icon.jpeg](resources/info/icon.jpeg) and this `get_info` function,
which together describe your plugin and its intended behaviour.
You can of course adapt this later, but it is useful to write out these intentions at the start.

#### Tests in [test_plugin.py](test/app/test_plugin.py)

We highly encourage [test driven development](https://en.wikipedia.org/wiki/Test-driven_development).
In fact, we require two predefined tests to successfully run on your plugin.

- The first test confirms that your plugin's info method returns an `_Info` artifact (`test_plugin_info_request`).
- The second test ensures that your computation returns the expected number of outputs as `_Artifact` types (
  `test_plugin_compute_request`).

These tests ensure that the plugin will run on the Climate Action platform.

The existing test only asserts that your plugin returns the expected number of outputs, and that these are of the
expected type (`_Artifact`).
It does not assert the intended functionality of the operator.
The [Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase) includes a variety of example tests for
testing actual results.
We expect you to thoroughly test your code in a similar way.
Your tests should be sorted into test scripts following the same structure as your plugin.

##### Compute Method in [operator_worker.py](plugin_blueprint/core/operator_worker.py)

Now, *finally*, comes the main coding part.
This method is where you process data and do the computations behind your plugin's results.
You are free to create additional classes or methods as needed to call from the `compute` method.
The only requirement of this method is to return a list of Artifacts (i.e. results).

The actual implementation of your plugin should be in the [components](plugin_blueprint/components/) submodule.
Feel free to create as many scripts and submodules as you need for your implementation (refactor often).
If you write functions or classes that will be useful for multiple indicators in your plugin,
we recommend putting them in a `utils` file (or folder) within [components](plugin_blueprint/components/).

You will probably also use external services like [ohsome-py](https://github.com/GIScience/ohsome-py).
In addition, you can use the provided utilities of the CA team.
A list of utilities can be found in the [climatoology](https://gitlab.heigit.org/climate-action/climatoology)
repository, but we also provide examples for their usage in
the [Showcase](https://gitlab.heigit.org/climate-action/plugins/plugin-showcase).

#### Input parameters in [input.py](plugin_blueprint/core/input.py)

Remember to update the input parameter class while you are coding away.
This must include any inputs or options the user can make when running your plugin.

### Development stages

The first MR you created above paves the way for the future development of the plugin.

#### Dummy

Your next step will be to create a dummy version of your plugin.
The dummy version will help you formalise the data creation pipeline early in the process
and will serve as a basic example of what the final plugin might return.
It will _not_ create real output but rather return a mocked result that in its type, color etc. resembles the real
output.
Therefore, it will not be shared outside the climate action group!

To accomplish this goal, hand-craft a dummy result in the code and return it from the `compute` method as an artifact.
Don't forget to adapt the tests and update the documentation.
If you are satisfied with the results and the tests pass, you have succeeded!
Please create a MR to `main` and ask the CA team for a review.
Make sure to follow the [company's guidelines](https://heigit.atlassian.net/wiki/spaces/SD/pages/3735635/Guidelines) on
commits and merge requests.

After your MR was accepted and merged, [create a release](README.md#releasing-a-new-plugin-version) called `dummy` .
Then ask the climate action admins to deploy your plugin to
the [staging environment](https://staging.climate-action.heigit.org).

#### Minimum Viable Product (MVP)

The next step is your Minimum Viable Product (MVP).
You should have established an outline and a definition of the content of your MVP content with your content supervisor.
The goal of the MVP is to create output that has real content but is extremely limited.
It will be the first version that is also communicated to the respective partners.

Follow the same process as for the dummy release.

1. Add the tests, methods, dependencies and documentation required to accomplish the goal
2. Create a MR
3. Create a release called `mvp`

#### Version 1 and beyond

From now on you can repeat this process for each release target that you, your content supervisor and the partner
define.

By now your plugin should be up and running on the climate action infrastructure.
Because you are doing rigorous testing, we can trust the code and be sure it works in deployment.

**Please now delete this file. If you need to review these steps again in the future,
you can access them from the [Plugin Blueprint](https://gitlab.heigit.org/climate-action/plugins/plugin-blueprint)
repository.**

## Forking this repository (for admins)

To enable a plugin contribution [fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html) this
repository and set a reasonable name and icon.
The following changes are necessary in the new fork:

1. [Unlink the fork](https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html#unlink-a-fork) to make it
   an independent repository
2. In the Merge-Request settings set
    1. Fast-forward merge
    2. Delete source branch by default
    3. Require squashing
    4. Pipelines must be successful
3. Allow developers to be able to merge to main
4. [Protect tags](https://docs.gitlab.com/ee/user/project/protected_tags.html) in order to have access to the protected
   docker credentials when creating releases
5. Create an issue stating `Finalise setup following README.START.md instructions`

The required docker repositories will be automatically created by the CI after the first merge into main.
