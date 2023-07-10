# netreports

Stores device metadata and commands obtained from a device.

## Installation

The plugin is available as a Python package in pypi and can be installed with pip

```shell
pip install netreports
```

Databases supported:

- MongoDB

## Usage

### API

TODO

## Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python Github Actions.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within Github Actions.

The project is leveraging:

- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Pytest for unit and integration testing.

### Development Environment

#### Invoke

The [PyInvoke](http://www.pyinvoke.org/) library is used to provide some helper commands based on the environment. There are a few configuration parameters which can be passed to PyInvoke to override the default configuration:

- `project_name`: the default docker compose project name (default: netreports)
- `python_ver`: the version of Python to use as a base for any built docker containers (default: 3.10)
- `mongo_ver`: the version of MongoDB (default: 5.0.14)
- `mongo_express_ver`: the of Mongo Express (default: 0.54.0)
- `local`: a boolean flag indicating if invoke tasks should be run on the host or inside the docker containers (default: False, commands will be run in docker containers)
- `compose_dir`: the full path to a directory containing the project compose files
- `compose_files`: a list of compose files applied in order (see [Multiple Compose files](https://docs.docker.com/compose/extends/#multiple-compose-files) for more information)
- `compose_http_timeout`: used to control timeout for the **invoke loogs** commands (default: 86400)

Using **PyInvoke** these configuration options can be overridden using [several methods](http://docs.pyinvoke.org/en/stable/concepts/configuration.html). Perhaps the simplest is simply setting an environment variable `INVOKE_netreports_VARIABLE_NAME` where `VARIABLE_NAME` is the variable you are trying to override. The only exception is `compose_files`, because it is a list it must be overridden in a yaml file. There is an example `invoke.yml` (`invoke.example.yml`) in this directory which can be used as a starting point.

#### Docker Development Environment

This project is managed by [Python Poetry](https://python-poetry.org/) and has a few requirements to setup your development environment:

1. Install Poetry, see the [Poetry Documentation](https://python-poetry.org/docs/#installation) for your operating system.
2. Install Docker, see the [Docker documentation](https://docs.docker.com/get-docker/) for your operating system.

Once you have Poetry and Docker installed you can run the following commands to install all other development dependencies in an isolated python virtual environment:

```shell
poetry shell
poetry install
invoke start
```

netreports server can now be accessed at [http://localhost:8080](http://localhost:8080).

To either stop or destroy the development environment use the following options.

- **invoke stop** - Stop the containers, but keep all underlying systems intact
- **invoke destroy** - Stop and remove all containers, volumes, etc. (This results in data loss due to the volume being deleted)

### CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`.

Each command can be executed with `invoke <command>`. Environment variables `INVOKE_netreports_PYTHON_VER` and `INVOKE_netreports_MONGO_VER` may be specified to override the default versions. Each command also has its own help `invoke <command> --help`

#### Docker dev environment

```no-highlight
  build        Build netreports docker image.
  debug        Start FastAPI and its dependencies in debug mode.
  destroy      Destroy all containers and volumes.
  restart      Gracefully restart all containers.
  start        Start netreports and its dependencies in detached mode.
  stop         Stop netreports and its dependencies.
```

#### Utility

```no-highlight
  cli          Launch a bash shell inside the running netreports container.
  ipython      Launch an interactive ipython session.
  logs         View the logs of a docker-compose service.
```

#### Testing

```no-highlight
  bandit       Run bandit to validate basic static code security analysis.
  black        Check Python code style with Black.
  flake8       Check for PEP8 compliance and other style issues.
  hadolint     Check Dockerfile for hadolint compliance and other style issues.
  pydocstyle   Run pydocstyle to validate docstring formatting.
  pylint       Run pylint code analysis.
  pytest       Run netreports unit tests.
  yamllint     Run yamllint to validate formatting.
```

### Project Documentation

## Questions

## Screenshots

TODO
