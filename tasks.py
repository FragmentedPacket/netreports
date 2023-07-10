"""Tasks for use with Invoke."""

from distutils.util import strtobool
from invoke import Collection, task as invoke_task
import os


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg
    return bool(strtobool(arg))


# Use pyinvoke configuration for default values, see http://docs.pyinvoke.org/en/stable/concepts/configuration.html
# Variables may be overwritten in invoke.yml or by the environment variables INVOKE_netreports_xxx
namespace = Collection("netreports")
namespace.configure(
    {
        "netreports": {
            "project_name": "netreports",
            "python_ver": "3.10",
            "mongo_ver": "5.0.18",
            "mongo_express_ver": "0.54.0",
            "local": False,
            "compose_dir": os.path.join(os.path.dirname(__file__), "development"),
            "compose_files": [
                "docker-compose.base.yml",
                "docker-compose.db.yml",
            ],
            "compose_http_timeout": "86400",
        }
    }
)


def task(function=None, *args, **kwargs):
    """Task decorator to override the default Invoke task decorator and add each task to the invoke namespace."""

    def task_wrapper(function=None):
        """Wrapper around invoke.task to add the task to the namespace as well."""
        if args or kwargs:
            task_func = invoke_task(*args, **kwargs)(function)
        else:
            task_func = invoke_task(function)
        namespace.add_task(task_func)
        return task_func

    if function:
        # The decorator was called with no arguments
        return task_wrapper(function)
    # The decorator was called with arguments
    return task_wrapper


def docker_compose(context, command, **kwargs):
    """Helper function for running a specific docker-compose command with all appropriate parameters and environment.

    Args:
        context (obj): Used to run specific commands
        command (str): Command string to append to the "docker-compose ..." command, such as "build", "up", etc.
        **kwargs: Passed through to the context.run() call.
    """
    build_env = {
        # Note: 'docker-compose logs' will stop following after 60 seconds by default,
        # so we are overriding that by setting this environment variable.
        "COMPOSE_HTTP_TIMEOUT": context.netreports.compose_http_timeout,
        "PYTHON_VER": context.netreports.python_ver,
        "MONGO_VER": context.netreports.mongo_ver,
        "MONGO_EXPRESS_VER": context.netreports.mongo_express_ver,
    }
    compose_command = f'docker-compose --project-name {context.netreports.project_name} --project-directory "{context.netreports.compose_dir}"'
    for compose_file in context.netreports.compose_files:
        compose_file_path = os.path.join(context.netreports.compose_dir, compose_file)
        compose_command += f' -f "{compose_file_path}"'
    compose_command += f" {command}"
    print(f'Running docker-compose command "{command}"')
    return context.run(compose_command, env=build_env, **kwargs)


def run_command(context, command, **kwargs):
    """Wrapper to run a command locally or inside the netreports container."""
    if is_truthy(context.netreports.local):
        context.run(command, **kwargs)
    else:
        # Check if netreports is running, no need to start another netreports container to run a command
        docker_compose_status = "ps --services --filter status=running"
        results = docker_compose(context, docker_compose_status, hide="out")
        if "fastapi" in results.stdout:
            compose_command = f"exec fastapi {command}"
        else:
            compose_command = f"run --entrypoint '{command}' fastapi"

        docker_compose(context, compose_command, pty=True)


# ------------------------------------------------------------------------------
# BUILD
# ------------------------------------------------------------------------------
@task(
    help={
        "force_rm": "Always remove intermediate containers",
        "cache": "Whether to use Docker's cache when building the image (defaults to enabled)",
    }
)
def build(context, force_rm=False, cache=True):
    """Build netreports docker image."""
    command = "build"

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    print(f"Building netreports with Python {context.netreports.python_ver}...")
    docker_compose(context, command)


# ------------------------------------------------------------------------------
# START / STOP / DEBUG
# ------------------------------------------------------------------------------
@task
def debug(context):
    """Start FastAPI and its dependencies in debug mode."""
    print("Starting FastAPI in debug mode...")
    docker_compose(context, "up")


@task
def start(context):
    """Start netreports and its dependencies in detached mode."""
    print("Starting netreports in detached mode...")
    docker_compose(context, "up --detach")


@task
def restart(context):
    """Gracefully restart all containers."""
    print("Restarting netreports...")
    docker_compose(context, "restart")


@task
def stop(context):
    """Stop netreports and its dependencies."""
    print("Stopping netreports...")
    docker_compose(context, "down")


@task
def destroy(context):
    """Destroy all containers and volumes."""
    print("Destroying netreports...")
    docker_compose(context, "down --volumes")


@task(
    help={
        "service": "Docker-compose service name to view (default: netreports)",
        "follow": "Follow logs",
        "tail": "Tail N number of lines or 'all'",
    }
)
def logs(context, service="fastapi", follow=False, tail=None):
    """View the logs of a docker-compose service."""
    command = "logs "

    if follow:
        command += "--follow "
    if tail:
        command += f"--tail={tail} "

    command += service
    docker_compose(context, command)


# ------------------------------------------------------------------------------
# ACTIONS
# ------------------------------------------------------------------------------
@task
def ipython(context):
    """Launch an interactive ipython session."""
    command = "ipython"
    run_command(context, command)


@task
def cli(context):
    """Launch a bash shell inside the running netreports container."""
    run_command(context, "bash")


# ------------------------------------------------------------------------------
# TESTS
# ------------------------------------------------------------------------------
@task(
    help={
        "autoformat": "Apply formatting recommendations automatically, rather than failing if formatting is incorrect.",
    }
)
def black(context, autoformat=False):
    """Check Python code style with Black."""
    if autoformat:
        black_command = "black"
    else:
        black_command = "black --check --diff"

    command = f"{black_command} ."

    run_command(context, command)


@task
def flake8(context):
    """Check for PEP8 compliance and other style issues."""
    command = "flake8 netreports"
    run_command(context, command)


@task
def hadolint(context):
    """Check Dockerfile for hadolint compliance and other style issues."""
    command = "hadolint development/Dockerfile"
    run_command(context, command)


@task
def pylint(context):
    """Run pylint code analysis."""
    command = "pylint --rcfile pyproject.toml netreports"
    run_command(context, command)


@task
def pydocstyle(context):
    """Run pydocstyle to validate docstring formatting."""
    command = "pydocstyle ."
    run_command(context, command)


@task
def bandit(context):
    """Run bandit to validate basic static code security analysis."""
    command = "bandit --recursive . --configfile .bandit.yml"
    run_command(context, command)


@task
def yamllint(context):
    """Run yamllint to validate formatting.

    Args:
        context (obj): Used to run specific commands
    """
    command = "yamllint netreports/ --format standard"
    run_command(context, command)


@task
def pytest(context):
    """Run netreports unit tests."""
    command = "pytest"

    run_command(context, command)


@task
def tests(context):
    """Run all tests for this plugin."""
    # If we are not running locally, start the docker containers so we don't have to for each test
    if not is_truthy(context.netreports.local):
        print("Starting Docker Containers...")
        start(context)
    # Sorted loosely from fastest to slowest
    print("Running black...")
    black(context)
    print("Running flake8...")
    flake8(context)
    print("Running bandit...")
    bandit(context)
    print("Running pydocstyle...")
    pydocstyle(context)
    print("Running yamllint...")
    yamllint(context)
    print("Running pylint...")
    pylint(context)
    print("Running unit tests...")
    pytest(context)
    print("All tests have passed!")
