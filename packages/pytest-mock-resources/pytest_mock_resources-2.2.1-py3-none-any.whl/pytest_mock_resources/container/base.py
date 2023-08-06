import contextlib
import functools
import json
import pathlib
import time

import responses

from pytest_mock_resources.config import get_env_config
from pytest_mock_resources.hooks import use_multiprocess_safe_mode

DEFAULT_RETRIES = 40
DEFAULT_INTERVAL = 0.5


class ContainerCheckFailed(Exception):
    """Unable to connect to a Container."""


def retry(func=None, *, args=(), kwargs={}, retries=1, interval=DEFAULT_INTERVAL, on_exc=Exception):
    while retries:
        retries -= 1
        try:
            result = func(*args, **kwargs)
        except on_exc:
            if not retries:
                raise
            time.sleep(interval)
        else:
            return result


def get_container(
    pytestconfig,
    config,
    *,
    check_fn,
    ports=None,
    environment=None,
    retries=DEFAULT_RETRIES,
    interval=DEFAULT_INTERVAL
):
    import docker
    import docker.errors

    multiprocess_safe_mode = use_multiprocess_safe_mode(pytestconfig)

    # XXX: moto library may over-mock responses. SEE: https://github.com/spulec/moto/issues/1026
    responses.add_passthru("http+docker")

    # Recent versions of the `docker` client make API calls to `docker` at this point
    # if provided the "auto" version. This leads to potential startup failure if
    # the docker socket isn't yet available.
    version = get_env_config("docker", "api_version", "auto")
    client = retry(docker.from_env, kwargs=dict(version=version), retries=5, interval=1)

    # The creation of container can fail and leave us in a situation where it's
    # we will need to know whether it's been created already or not.
    container = None

    check_fn = functools.partial(check_fn, config)

    try:
        container = wait_for_container(
            client,
            check_fn,
            run_args=(config.image,),
            run_kwargs=dict(ports=ports, environment=environment),
            retries=retries,
            interval=interval,
        )
        if container and multiprocess_safe_mode:
            record_container_creation(pytestconfig, container)
        yield
    finally:
        if container and not multiprocess_safe_mode:
            container.kill()

        client.close()


def wait_for_container(
    client,
    check_fn,
    *,
    run_args,
    run_kwargs,
    retries=DEFAULT_RETRIES,
    interval=DEFAULT_INTERVAL
):
    """Wait for evidence that the container is up and healthy.

    The caller must provide a `check_fn` which should `raise ContainerCheckFailed` if
    it finds that the container is not yet up.
    """
    import docker.errors

    try:
        # Perform a single attempt, for the happy-path where the container already exists.
        retry(check_fn, retries=1, interval=interval, on_exc=ContainerCheckFailed)
    except ContainerCheckFailed:
        # In the event it doesn't exist, we attempt to start the container
        try:
            container = client.containers.run(
                *run_args, **run_kwargs, detach=True, remove=True
            )
        except docker.errors.APIError as e:
            container = None
            # This sometimes happens if multiple container fixtures race for the first
            # creation of the container, we want to still retry wait in this case.
            if "port is already allocated" not in str(e):
                raise

        # And then we perform more lengthy retry cycle.
        retry(check_fn, retries=retries, interval=interval, on_exc=ContainerCheckFailed)
        return container
    return None


def record_container_creation(pytestconfig, container):
    """Record the fact of the creation of a container.

    Record both a local reference to the container in pytest's `config` fixture,
    as well as a global PMR lock file of created containers.
    """
    pytestconfig._pmr_containers.append(container)

    fn = get_tmp_root(pytestconfig, parent=True)
    with load_container_lockfile(fn) as data:
        data.append(container.id)
        fn.write_text(json.dumps(data))


def get_tmp_root(pytestconfig, *, parent=False):
    """Get the path to the PMR lock file."""
    tmp_path_factory = pytestconfig._tmp_path_factory

    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    if parent:
        root_tmp_dir = root_tmp_dir.parent

    return root_tmp_dir / "pmr.json"


@contextlib.contextmanager
def load_container_lockfile(path: pathlib.Path):
    """Produce the contents of the given file behind a file lock."""
    import filelock

    with filelock.FileLock(str(path) + ".lock"):
        if path.is_file():
            with open(path, "rb") as f:
                yield json.load(f)
        else:
            yield []
