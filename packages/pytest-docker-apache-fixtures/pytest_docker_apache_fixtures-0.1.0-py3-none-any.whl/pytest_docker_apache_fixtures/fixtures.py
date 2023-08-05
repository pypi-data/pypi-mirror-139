#!/usr/bin/env python

# pylint: disable=redefined-outer-name,too-many-arguments,too-many-locals

"""The actual fixtures, you found them ;)."""

import logging
import itertools

from base64 import b64encode
from functools import partial
from pathlib import Path
from ssl import create_default_context, SSLContext
from string import Template
from time import sleep, time
from typing import Dict, Generator, List, NamedTuple

import pytest

from lovely.pytest.docker.compose import Services
from _pytest.tmpdir import TempPathFactory

from .utils import (
    check_url_secure,
    generate_cacerts,
    generate_htpasswd,
    generate_keypair,
    get_docker_compose_user_defined,
    get_embedded_file,
    get_user_defined_file,
    APACHE_PORT_INSECURE,
    APACHE_PORT_SECURE,
    APACHE_SERVICE,
    APACHE_SERVICE_PATTERN,
    start_service,
)

# Caching is needed, as singular-fixtures and list-fixtures will conflict at scale_factor=1
# This appears to only matter when attempting to start the docker secure apache service
# for the second time.
CACHE = {}

LOGGER = logging.getLogger(__name__)


class ApacheCerts(NamedTuple):
    # pylint: disable=missing-class-docstring
    ca_certificate: Path
    ca_private_key: Path
    certificate: Path
    private_key: Path


class ApacheInsecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    docker_compose: Path
    endpoint: str
    endpoint_name: str
    service_name: str


# Note: NamedTuple does not support inheritance :(
class ApacheSecure(NamedTuple):
    # pylint: disable=missing-class-docstring
    auth_header: Dict[str, str]
    cacerts: Path
    certs: ApacheCerts
    docker_compose: Path
    endpoint: str
    endpoint_name: str
    htpasswd: Path
    password: str
    service_name: str
    ssl_context: SSLContext
    username: str


def _pdaf_docker_compose_insecure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure apache service.
    """
    cache_key = _pdaf_docker_compose_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = APACHE_SERVICE_PATTERN.format("insecure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            # TODO: lovely-docker-compose uses the file for teardown ...
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def pdaf_docker_compose_insecure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure apache service.
    """
    for lst in _pdaf_docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def pdaf_docker_compose_insecure_list(
    docker_compose_files: List[str],
    pdaf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the docker-compose configuration file containing the insecure apache service.
    """
    yield from _pdaf_docker_compose_insecure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _pdaf_docker_compose_secure(
    *,
    docker_compose_files: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure apache
    service.
    """
    cache_key = _pdaf_docker_compose_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = APACHE_SERVICE_PATTERN.format("secure", i)
        chain = itertools.chain(
            get_docker_compose_user_defined(docker_compose_files, service_name),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="docker-compose.yml"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find docker compose for: %s", service_name)
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def pdaf_docker_compose_secure(
    docker_compose_files: List[str], tmp_path_factory: TempPathFactory
) -> Generator[Path, None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure apache
    service.
    """
    for lst in _pdaf_docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def pdaf_docker_compose_secure_list(
    docker_compose_files: List[str],
    pdaf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of the templated docker-compose configuration file containing the secure apache
    service.
    """
    yield from _pdaf_docker_compose_secure(
        docker_compose_files=docker_compose_files,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


@pytest.fixture(scope="session")
def pdaf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 1


def _apache_auth_header(
    *,
    apache_password_list: List[str],
    apache_username_list: List[str],
    scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure apache service."""
    cache_key = _apache_auth_header.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        auth = b64encode(
            f"{apache_username_list[i]}:{apache_password_list[i]}".encode("utf-8")
        ).decode("utf-8")
        result.append({"Authorization": f"Basic {auth}"})
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def apache_auth_header(apache_password: str, apache_username: str) -> Dict[str, str]:
    """Provides an HTTP basic authentication header containing credentials for the secure apache service."""
    return _apache_auth_header(
        apache_password_list=[apache_password],
        apache_username_list=[apache_username],
        scale_factor=1,
    )[0]


@pytest.fixture(scope="session")
def apache_auth_header_list(
    apache_password_list: List[str],
    apache_username_list: List[str],
    pdaf_scale_factor: int,
) -> List[Dict[str, str]]:
    """Provides an HTTP basic authentication header containing credentials for the secure apache service."""
    return _apache_auth_header(
        apache_password_list=apache_password_list,
        apache_username_list=apache_username_list,
        scale_factor=pdaf_scale_factor,
    )


def _apache_cacerts(
    *,
    apache_certs_list: List[ApacheCerts],
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure apache
    service.
    """
    cache_key = _apache_cacerts.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "cacerts"),
            generate_cacerts(
                tmp_path_factory,
                certificate=apache_certs_list[i].ca_certificate,
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate cacerts!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def apache_cacerts(
    apache_certs: ApacheCerts,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure apache
    service.
    """
    for lst in _apache_cacerts(
        apache_certs_list=[apache_certs],
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_cacerts_list(
    apache_certs_list: List[ApacheCerts],
    pdaf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """
    Provides the location of a temporary CA certificate trust store that contains the certificate of the secure apache
    service.
    """
    yield from _apache_cacerts(
        apache_certs_list=apache_certs_list,
        pytestconfig=pytestconfig,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _apache_certs(
    *, scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[ApacheCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure apache service."""
    # TODO: Augment to allow for reading certificates from /test ...
    cache_key = _apache_certs.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        tmp_path = tmp_path_factory.mktemp(__name__)
        service_name = APACHE_SERVICE_PATTERN.format("secure", i)
        keypair = generate_keypair(service_name=service_name)
        apache_cert = ApacheCerts(
            ca_certificate=tmp_path.joinpath(f"{APACHE_SERVICE}-ca-{i}.crt"),
            ca_private_key=tmp_path.joinpath(f"{APACHE_SERVICE}-ca-{i}.key"),
            certificate=tmp_path.joinpath(f"{APACHE_SERVICE}-{i}.crt"),
            private_key=tmp_path.joinpath(f"{APACHE_SERVICE}-{i}.key"),
        )
        apache_cert.ca_certificate.write_bytes(keypair.ca_certificate)
        apache_cert.ca_private_key.write_bytes(keypair.ca_private_key)
        apache_cert.certificate.write_bytes(keypair.certificate)
        apache_cert.private_key.write_bytes(keypair.private_key)
        result.append(apache_cert)
    CACHE[cache_key] = result
    yield result
    for apache_cert in result:
        apache_cert.ca_certificate.unlink(missing_ok=True)
        apache_cert.ca_private_key.unlink(missing_ok=True)
        apache_cert.certificate.unlink(missing_ok=True)
        apache_cert.private_key.unlink(missing_ok=True)


@pytest.fixture(scope="session")
def apache_certs(
    tmp_path_factory: TempPathFactory,
) -> Generator[ApacheCerts, None, None]:
    """Provides the location of temporary certificate and private key files for the secure apache service."""
    for lst in _apache_certs(scale_factor=1, tmp_path_factory=tmp_path_factory):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_certs_list(
    pdaf_scale_factor: int, tmp_path_factory: TempPathFactory
) -> Generator[List[ApacheCerts], None, None]:
    """Provides the location of temporary certificate and private key files for the secure apache service."""
    yield from _apache_certs(
        scale_factor=pdaf_scale_factor, tmp_path_factory=tmp_path_factory
    )


def _apache_htpasswd(
    *,
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    apache_password_list: List[str],
    apache_username_list: List[str],
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure apache service."""
    cache_key = _apache_htpasswd.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "htpasswd"),
            generate_htpasswd(
                tmp_path_factory,
                username=apache_username_list[i],
                password=apache_password_list[i],
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find or generate htpasswd!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def apache_htpasswd(
    pytestconfig: "_pytest.config.Config",
    apache_password: str,
    apache_username: str,
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the htpasswd file for the secure apache service."""
    for lst in _apache_htpasswd(
        pytestconfig=pytestconfig,
        scale_factor=1,
        apache_password_list=[apache_password],
        apache_username_list=[apache_username],
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_htpasswd_list(
    pdaf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    apache_password_list: List[str],
    apache_username_list: List[str],
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the htpasswd file for the secure apache service."""
    yield from _apache_htpasswd(
        pytestconfig=pytestconfig,
        scale_factor=pdaf_scale_factor,
        apache_username_list=apache_username_list,
        apache_password_list=apache_password_list,
        tmp_path_factory=tmp_path_factory,
    )


def _apache_insecure(
    *,
    docker_compose_insecure_list: List[Path],
    docker_services: Services,
    apache_apachecfg_insecure_list: List[Path],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[ApacheInsecure], None, None]:
    """Provides the endpoint of a local, insecure, apache."""
    cache_key = _apache_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = APACHE_SERVICE_PATTERN.format("insecure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        # Create a secure apache service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_insecure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    # Note: Needed to correctly populate the embedded, consolidated, service template ...
                    "PATH_CERTIFICATE": "/dev/null",
                    "PATH_HTPASSWD": "/dev/null",
                    "PATH_KEY": "/dev/null",
                    "PATH_APACHECFG": apache_apachecfg_insecure_list[i],
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting insecure apache service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  service name   : %s", service_name)
        LOGGER.debug("  apachecfg       : %s", apache_apachecfg_insecure_list[i])

        endpoint = start_service(
            docker_services,
            docker_compose=path_docker_compose,
            private_port=APACHE_PORT_INSECURE,
            service_name=service_name,
        )
        LOGGER.debug("Insecure apache endpoint [%d]: %s", i, endpoint)

        result.append(
            ApacheInsecure(
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                endpoint_name=f"{service_name}:{APACHE_PORT_INSECURE}",
                service_name=service_name,
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def apache_insecure(
    docker_services: Services,
    apache_apachecfg_insecure: Path,
    pdaf_docker_compose_insecure: Path,
    tmp_path_factory: TempPathFactory,
) -> Generator[ApacheInsecure, None, None]:
    """Provides the endpoint of a local, insecure, apache."""
    for lst in _apache_insecure(
        docker_compose_insecure_list=[pdaf_docker_compose_insecure],
        docker_services=docker_services,
        apache_apachecfg_insecure_list=[apache_apachecfg_insecure],
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_insecure_list(
    docker_services: Services,
    apache_apachecfg_insecure_list: List[Path],
    pdaf_docker_compose_insecure_list: List[Path],
    pdaf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[ApacheInsecure], None, None]:
    """Provides the endpoint of a local, insecure, apache."""
    yield from _apache_insecure(
        docker_compose_insecure_list=pdaf_docker_compose_insecure_list,
        docker_services=docker_services,
        apache_apachecfg_insecure_list=apache_apachecfg_insecure_list,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _apache_password(*, scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure apache service."""
    cache_key = _apache_password.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.password.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def apache_password() -> str:
    """Provides the password to use for authentication to the secure apache service."""
    return _apache_password(scale_factor=1)[0]


@pytest.fixture(scope="session")
def apache_password_list(pdaf_scale_factor: int) -> List[str]:
    """Provides the password to use for authentication to the secure apache service."""
    return _apache_password(scale_factor=pdaf_scale_factor)


def _apache_secure(
    *,
    docker_compose_secure_list: List[Path],
    docker_services: Services,
    apache_auth_header_list: List[Dict[str, str]],
    apache_cacerts_list: List[Path],
    apache_certs_list: List[ApacheCerts],
    apache_htpasswd_list: List[Path],
    apache_password_list: List[str],
    apache_apachecfg_secure_list: List[Path],
    apache_ssl_context_list: List[SSLContext],
    apache_username_list: List[str],
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[ApacheSecure], None, None]:
    """Provides the endpoint of a local, secure, apache."""
    cache_key = _apache_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        service_name = APACHE_SERVICE_PATTERN.format("secure", i)
        tmp_path = tmp_path_factory.mktemp(__name__)

        # Create a secure apache service from the docker compose template ...
        path_docker_compose = tmp_path.joinpath(f"docker-compose-{i}.yml")
        template = Template(docker_compose_secure_list[i].read_text("utf-8"))
        path_docker_compose.write_text(
            template.substitute(
                {
                    "CONTAINER_NAME": service_name,
                    "PATH_CERTIFICATE": apache_certs_list[i].certificate,
                    "PATH_HTPASSWD": apache_htpasswd_list[i],
                    "PATH_KEY": apache_certs_list[i].private_key,
                    "PATH_APACHECFG": apache_apachecfg_secure_list[i],
                }
            ),
            "utf-8",
        )

        LOGGER.debug("Starting secure apache service [%d] ...", i)
        LOGGER.debug("  docker-compose : %s", path_docker_compose)
        LOGGER.debug("  ca certificate : %s", apache_certs_list[i].ca_certificate)
        LOGGER.debug("  certificate    : %s", apache_certs_list[i].certificate)
        LOGGER.debug("  apachecfg       : %s", apache_apachecfg_secure_list[i])
        LOGGER.debug("  private key    : %s", apache_certs_list[i].private_key)
        LOGGER.debug("  password       : %s", apache_password_list[i])
        LOGGER.debug("  service name   : %s", service_name)
        LOGGER.debug("  username       : %s", apache_username_list[i])

        check_server = partial(
            check_url_secure,
            auth_header=apache_auth_header_list[i],
            ssl_context=apache_ssl_context_list[i],
        )
        endpoint = start_service(
            docker_services,
            check_server=check_server,
            docker_compose=path_docker_compose,
            private_port=APACHE_PORT_SECURE,
            service_name=service_name,
        )
        LOGGER.debug("Secure apache endpoint [%d]: %s", i, endpoint)

        result.append(
            ApacheSecure(
                auth_header=apache_auth_header_list[i],
                cacerts=apache_cacerts_list[i],
                certs=apache_certs_list[i],
                docker_compose=path_docker_compose,
                endpoint=endpoint,
                endpoint_name=f"{service_name}:{APACHE_PORT_SECURE}",
                htpasswd=apache_htpasswd_list[i],
                password=apache_password_list[i],
                service_name=service_name,
                ssl_context=apache_ssl_context_list[i],
                username=apache_username_list[i],
            )
        )
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def apache_secure(
    docker_services: Services,
    apache_auth_header,
    apache_cacerts: Path,
    apache_certs: ApacheCerts,
    apache_htpasswd: Path,
    apache_password: str,
    apache_apachecfg_secure: Path,
    apache_ssl_context: SSLContext,
    apache_username: str,
    pdaf_docker_compose_secure: Path,
    tmp_path_factory: TempPathFactory,
) -> Generator[ApacheSecure, None, None]:
    """Provides the endpoint of a local, secure, apache."""
    for lst in _apache_secure(
        docker_compose_secure_list=[pdaf_docker_compose_secure],
        apache_auth_header_list=[apache_auth_header],
        apache_cacerts_list=[apache_cacerts],
        apache_certs_list=[apache_certs],
        apache_htpasswd_list=[apache_htpasswd],
        apache_password_list=[apache_password],
        apache_apachecfg_secure_list=[apache_apachecfg_secure],
        apache_ssl_context_list=[apache_ssl_context],
        apache_username_list=[apache_username],
        docker_services=docker_services,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_secure_list(
    docker_services: Services,
    apache_auth_header_list,
    apache_cacerts_list: List[Path],
    apache_certs_list: List[ApacheCerts],
    apache_htpasswd_list: List[Path],
    apache_password_list: List[str],
    apache_apachecfg_secure_list: List[Path],
    apache_ssl_context_list: List[SSLContext],
    apache_username_list: List[str],
    pdaf_docker_compose_secure_list: List[Path],
    pdaf_scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[ApacheSecure], None, None]:
    """Provides the endpoint of a local, secure, apache."""
    yield from _apache_secure(
        docker_compose_secure_list=pdaf_docker_compose_secure_list,
        apache_auth_header_list=apache_auth_header_list,
        apache_cacerts_list=apache_cacerts_list,
        apache_certs_list=apache_certs_list,
        apache_htpasswd_list=apache_htpasswd_list,
        apache_password_list=apache_password_list,
        apache_apachecfg_secure_list=apache_apachecfg_secure_list,
        apache_ssl_context_list=apache_ssl_context_list,
        apache_username_list=apache_username_list,
        docker_services=docker_services,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _apache_apachecfg_insecure(
    *,
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the apache configuration file for the insecure apache service."""
    cache_key = _apache_apachecfg_insecure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "apache.insecure.cfg"),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="apache.insecure.cfg"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find insecure apache.cfg!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def apache_apachecfg_insecure(
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the apache configuration  file for the insecure apache service."""
    for lst in _apache_apachecfg_insecure(
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_apachecfg_insecure_list(
    pdaf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the apache configuration file for the insecure apache service."""
    yield from _apache_apachecfg_insecure(
        pytestconfig=pytestconfig,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _apache_apachecfg_secure(
    *,
    pytestconfig: "_pytest.config.Config",
    scale_factor: int,
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the apache configuration file for the secure apache service."""
    cache_key = _apache_apachecfg_secure.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        chain = itertools.chain(
            get_user_defined_file(pytestconfig, "apache.secure.cfg"),
            get_embedded_file(
                tmp_path_factory, delete_after=False, name="apache.secure.cfg"
            ),
        )
        for path in chain:
            result.append(path)
            break
        else:
            LOGGER.warning("Unable to find secure apache.cfg!")
            result.append("-unknown-")
    CACHE[cache_key] = result
    yield result


@pytest.fixture(scope="session")
def apache_apachecfg_secure(
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[Path, None, None]:
    """Provides the location of the apache configuration  file for the secure apache service."""
    for lst in _apache_apachecfg_secure(
        pytestconfig=pytestconfig,
        scale_factor=1,
        tmp_path_factory=tmp_path_factory,
    ):
        yield lst[0]


@pytest.fixture(scope="session")
def apache_apachecfg_secure_list(
    pdaf_scale_factor: int,
    pytestconfig: "_pytest.config.Config",
    tmp_path_factory: TempPathFactory,
) -> Generator[List[Path], None, None]:
    """Provides the location of the apache configuration file for the secure apache service."""
    yield from _apache_apachecfg_secure(
        pytestconfig=pytestconfig,
        scale_factor=pdaf_scale_factor,
        tmp_path_factory=tmp_path_factory,
    )


def _apache_ssl_context(
    *, apache_cacerts_list: List[Path], scale_factor: int
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure apache service.
    """
    cache_key = _apache_ssl_context.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(create_default_context(cafile=str(apache_cacerts_list[i])))
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def apache_ssl_context(apache_cacerts: Path) -> SSLContext:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure apache service.
    """
    return _apache_ssl_context(apache_cacerts_list=[apache_cacerts], scale_factor=1)[0]


@pytest.fixture(scope="session")
def apache_ssl_context_list(
    apache_cacerts_list: List[Path],
    pdaf_scale_factor: int,
) -> List[SSLContext]:
    """
    Provides an SSLContext referencing the temporary CA certificate trust store that contains the certificate of the
    secure apache service.
    """
    return _apache_ssl_context(
        apache_cacerts_list=apache_cacerts_list,
        scale_factor=pdaf_scale_factor,
    )


def _apache_username(*, scale_factor: int) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure apache service."""
    cache_key = _apache_username.__name__
    result = CACHE.get(cache_key, [])
    for i in range(scale_factor):
        if i < len(result):
            continue

        result.append(f"pytest.username.{time()}")
        sleep(0.05)
    CACHE[cache_key] = result
    return result


@pytest.fixture(scope="session")
def apache_username() -> str:
    """Retrieve the name of the user to use for authentication to the secure apache service."""
    return _apache_username(scale_factor=1)[0]


@pytest.fixture(scope="session")
def apache_username_list(
    pdaf_scale_factor: int,
) -> List[str]:
    """Retrieve the name of the user to use for authentication to the secure apache service."""
    return _apache_username(scale_factor=pdaf_scale_factor)
