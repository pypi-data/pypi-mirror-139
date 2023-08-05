#!/usr/bin/env python

# pylint: disable=redefined-outer-name

"""pytest fixture tests."""

import logging

from base64 import b64decode
from http.client import HTTPResponse
from pathlib import Path
from ssl import SSLContext
from typing import Dict, List
from urllib import request as urllibrequest
from urllib.error import HTTPError, URLError

import pytest

from pytest_docker_apache_fixtures import (
    __version__,
    ApacheCerts,
    ApacheInsecure,
    ApacheSecure,
    APACHE_SERVICE_PATTERN,
)

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def get_headers() -> Dict[str, str]:
    """Provides HTTP headers to be used when testing."""
    return {"User-Agent": f"pytest-docker-apache-fixtures/{__version__}"}


# Override fixture for testing
@pytest.fixture(scope="session")
def pdaf_scale_factor() -> int:
    """Provides the number enumerated instances to be instantiated."""
    return 4


def no_duplicates(lst: List) -> bool:
    """Tests if a list contains duplicate values."""
    return len(lst) == len(set(lst))


def test_pdaf_docker_compose_insecure(pdaf_docker_compose_insecure: Path):
    """Test that the embedded docker-compose for insecure apache can be copied to a temporary file."""
    service_name = APACHE_SERVICE_PATTERN.format("insecure", 0)
    assert service_name in pdaf_docker_compose_insecure.read_text()


def test_pdaf_docker_compose_insecure_list(
    pdaf_docker_compose_insecure_list: List[Path], pdaf_scale_factor: int
):
    """Test that the embedded docker-compose for insecure apache can be copied to a temporary file."""
    for i in range(pdaf_scale_factor):
        service_name = APACHE_SERVICE_PATTERN.format("insecure", i)
        assert service_name in pdaf_docker_compose_insecure_list[i].read_text()
    assert no_duplicates(pdaf_docker_compose_insecure_list)


def test_pdaf_docker_compose_secure(pdaf_docker_compose_secure: Path):
    """Test that the embedded docker-compose for secure apache can be copied to a temporary file."""
    service_name = APACHE_SERVICE_PATTERN.format("secure", 0)
    assert service_name in pdaf_docker_compose_secure.read_text()


def test_pdaf_docker_compose_secure_list(
    pdaf_docker_compose_secure_list: List[Path], pdaf_scale_factor: int
):
    """Test that the embedded docker-compose for secure apache can be copied to a temporary file."""
    for i in range(pdaf_scale_factor):
        service_name = APACHE_SERVICE_PATTERN.format("secure", i)
        assert service_name in pdaf_docker_compose_secure_list[i].read_text()
    assert no_duplicates(pdaf_docker_compose_secure_list)


def test_apache_auth_header(
    apache_auth_header,
    apache_password: str,
    apache_username: str,
):
    """Test that an HTTP basic authentication header can be provided."""
    assert "Authorization" in apache_auth_header
    string = b64decode(
        apache_auth_header["Authorization"].split()[1].encode("utf-8")
    ).decode("utf-8")
    assert apache_password in string
    assert apache_username in string


def test_apache_auth_header_list(
    apache_auth_header_list,
    apache_password_list: List[str],
    apache_username_list: List[str],
    pdaf_scale_factor: int,
):
    """Test that an HTTP basic authentication header can be provided."""
    for i in range(pdaf_scale_factor):
        assert "Authorization" in apache_auth_header_list[i]
        string = b64decode(
            apache_auth_header_list[i]["Authorization"].split()[1].encode("utf-8")
        ).decode("utf-8")
        assert apache_password_list[i] in string
        assert apache_username_list[i] in string
    assert no_duplicates([str(i) for i in apache_auth_header_list])
    assert no_duplicates(apache_password_list)
    assert no_duplicates(apache_username_list)


def test_apache_cacerts(apache_cacerts: Path, apache_certs: ApacheCerts):
    """Test that a temporary CA certificate trust store can be provided."""
    assert apache_cacerts.exists()
    cacerts = apache_cacerts.read_text("utf-8")

    ca_cert = apache_certs.ca_certificate.read_text("utf-8")
    assert ca_cert in cacerts

    ca_key = apache_certs.ca_private_key.read_text("utf-8")
    assert ca_key not in cacerts

    cert = apache_certs.certificate.read_text("utf-8")
    assert cert not in cacerts

    key = apache_certs.private_key.read_text("utf-8")
    assert key not in cacerts


def test_apache_cacerts_list(
    apache_cacerts_list: List[Path],
    apache_certs_list: List[ApacheCerts],
    pdaf_scale_factor: int,
):
    """Test that a temporary CA certificate trust store can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_cacerts_list[i].exists()
        cacerts = apache_cacerts_list[i].read_text("utf-8")

        ca_cert = apache_certs_list[i].ca_certificate.read_text("utf-8")
        assert ca_cert in cacerts

        ca_key = apache_certs_list[i].ca_private_key.read_text("utf-8")
        assert ca_key not in cacerts

        cert = apache_certs_list[i].certificate.read_text("utf-8")
        assert cert not in cacerts

        key = apache_certs_list[i].private_key.read_text("utf-8")
        assert key not in cacerts
    assert no_duplicates(apache_cacerts_list)
    assert no_duplicates(apache_certs_list)


def test_apache_certs(apache_certs: ApacheCerts):
    """Test that a certificate and private key can be provided."""
    assert apache_certs.ca_certificate.exists()
    assert "BEGIN CERTIFICATE" in apache_certs.ca_certificate.read_text("utf-8")
    assert apache_certs.ca_private_key.exists()
    assert "BEGIN PRIVATE KEY" in apache_certs.ca_private_key.read_text("utf-8")
    assert apache_certs.certificate.exists()
    assert "BEGIN CERTIFICATE" in apache_certs.certificate.read_text("utf-8")
    assert apache_certs.private_key.exists()
    assert "BEGIN PRIVATE KEY" in apache_certs.private_key.read_text("utf-8")


def test_apache_certs_list(
    apache_certs_list: List[ApacheCerts], pdaf_scale_factor: int
):
    """Test that a certificate and private key can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_certs_list[i].ca_certificate.exists()
        assert "BEGIN CERTIFICATE" in apache_certs_list[i].ca_certificate.read_text(
            "utf-8"
        )
        assert apache_certs_list[i].ca_private_key.exists()
        assert "BEGIN PRIVATE KEY" in apache_certs_list[i].ca_private_key.read_text(
            "utf-8"
        )
        assert apache_certs_list[i].certificate.exists()
        assert "BEGIN CERTIFICATE" in apache_certs_list[i].certificate.read_text(
            "utf-8"
        )
        assert apache_certs_list[i].private_key.exists()
        assert "BEGIN PRIVATE KEY" in apache_certs_list[i].private_key.read_text(
            "utf-8"
        )
    assert no_duplicates(apache_certs_list)


def test_apache_htpasswd(
    apache_htpasswd: Path,
    apache_password: str,
    apache_username: str,
):
    """Test that a htpasswd can be provided."""
    assert apache_htpasswd.exists()
    content = apache_htpasswd.read_text("utf-8")
    assert apache_username in content
    assert apache_password not in content


def test_apache_htpasswd_list(
    apache_htpasswd_list: List[Path],
    apache_password_list: List[str],
    apache_username_list: List[str],
    pdaf_scale_factor: int,
):
    """Test that a htpasswd can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_htpasswd_list[i].exists()
        content = apache_htpasswd_list[i].read_text("utf-8")
        assert apache_username_list[i] in content
        assert apache_password_list[i] not in content
    assert no_duplicates(apache_htpasswd_list)
    assert no_duplicates(apache_password_list)
    assert no_duplicates(apache_username_list)


@pytest.mark.online
def test_apache_insecure(get_headers: Dict[str, str], apache_insecure: ApacheInsecure):
    """Test that an insecure apache can be instantiated."""
    assert "127.0.0.1" in apache_insecure.endpoint

    request = urllibrequest.Request(
        headers=get_headers, method="HEAD", url=f"http://{apache_insecure.endpoint}/"
    )
    with urllibrequest.urlopen(url=request) as response:
        assert response.code == 200


@pytest.mark.online
def test_apache_insecure_content(
    get_headers: Dict[str, str], apache_insecure: ApacheInsecure
):
    """Test that an insecure apache can be instantiated."""
    assert "127.0.0.1" in apache_insecure.endpoint

    request = urllibrequest.Request(
        headers=get_headers, url=f"http://{apache_insecure.endpoint}/"
    )
    with urllibrequest.urlopen(url=request) as response:
        assert response.code == 200
        # TODO: Why doesn't decoding to utf-8 work?
        assert "it works!" in str(response.read()).lower()


@pytest.mark.online
def test_apache_insecure_list(
    get_headers: Dict[str, str],
    apache_insecure_list: List[ApacheInsecure],
    pdaf_scale_factor: int,
):
    """Test that an insecure apache can be instantiated."""
    for i in range(pdaf_scale_factor):
        assert "127.0.0.1" in apache_insecure_list[i].endpoint

        request = urllibrequest.Request(
            headers=get_headers,
            method="HEAD",
            url=f"http://{apache_insecure_list[i].endpoint}/",
        )
        with urllibrequest.urlopen(url=request) as response:
            assert response.code == 200

    assert no_duplicates([str(i) for i in apache_insecure_list])


def test_apache_password(apache_password: str):
    """Test that a password can be provided."""
    assert apache_password


def test_apache_password_list(apache_password_list: List[str], pdaf_scale_factor: int):
    """Test that a password can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_password_list[i]
    assert no_duplicates(apache_password_list)


@pytest.mark.online
def test_apache_secure(
    get_headers: Dict[str, str],
    apache_secure: ApacheSecure,
):
    """Test that an secure apache can be instantiated."""
    assert "127.0.0.1" in apache_secure.endpoint

    request = urllibrequest.Request(
        headers={**get_headers, **apache_secure.auth_header},
        method="HEAD",
        url=f"https://{apache_secure.endpoint}/",
    )
    with urllibrequest.urlopen(
        context=apache_secure.ssl_context, url=request
    ) as response:
        assert response.code == 200

    # Error: Unauthenticated
    with pytest.raises(HTTPError) as exception_info:
        request = urllibrequest.Request(
            headers=get_headers, method="HEAD", url=f"https://{apache_secure.endpoint}/"
        )
        urllibrequest.urlopen(context=apache_secure.ssl_context, url=request)
    assert "401" in str(exception_info.value)

    # Error: CA not trusted
    with pytest.raises(URLError) as exception_info:
        request = urllibrequest.Request(
            headers={**get_headers, **apache_secure.auth_header},
            method="HEAD",
            url=f"https://{apache_secure.endpoint}/",
        )
        urllibrequest.urlopen(url=request)
    assert "CERTIFICATE_VERIFY_FAILED" in str(exception_info.value)


@pytest.mark.online
def test_apache_secure_content(
    get_headers: Dict[str, str],
    apache_secure: ApacheSecure,
):
    """Test that an secure apache can be instantiated."""
    assert "127.0.0.1" in apache_secure.endpoint

    request = urllibrequest.Request(
        headers={**get_headers, **apache_secure.auth_header},
        url=f"https://{apache_secure.endpoint}/",
    )
    with urllibrequest.urlopen(
        context=apache_secure.ssl_context, url=request
    ) as response:
        assert response.code == 200
        # TODO: Why doesn't decoding to utf-8 work?
        assert "it works!" in str(response.read()).lower()


@pytest.mark.online
def test_apache_secure_list(
    get_headers: Dict[str, str],
    apache_secure_list: List[ApacheSecure],
    pdaf_scale_factor: int,
):
    """Test that an secure apache can be instantiated."""
    for i in range(pdaf_scale_factor):
        assert "127.0.0.1" in apache_secure_list[i].endpoint

        request = urllibrequest.Request(
            headers={**get_headers, **apache_secure_list[i].auth_header},
            method="HEAD",
            url=f"https://{apache_secure_list[i].endpoint}/",
        )
        with urllibrequest.urlopen(
                context=apache_secure_list[i].ssl_context, url=request
        ) as response:
            assert response.code == 200

        # Error: Unauthenticated
        with pytest.raises(HTTPError) as exception_info:
            request = urllibrequest.Request(
                headers=get_headers, method="HEAD", url=f"https://{apache_secure_list[i].endpoint}/"
            )
            urllibrequest.urlopen(context=apache_secure_list[i].ssl_context, url=request)
        assert "401" in str(exception_info.value)

        # Error: CA not trusted
        with pytest.raises(URLError) as exception_info:
            request = urllibrequest.Request(
                headers={**get_headers, **apache_secure_list[i].auth_header},
                method="HEAD",
                url=f"https://{apache_secure_list[i].endpoint}/",
            )
            urllibrequest.urlopen(url=request)
        assert "CERTIFICATE_VERIFY_FAILED" in str(exception_info.value)
    assert no_duplicates([str(i) for i in apache_secure_list])


def test_apache_apachecfg_insecure(
    apache_apachecfg_insecure: Path,
):
    """Test that an insecure apache.cfg can be provided."""
    assert apache_apachecfg_insecure.exists()
    content = apache_apachecfg_insecure.read_text("utf-8")
    assert len(content) > 0


def test_apache_apachecfg_insecure_list(
    apache_apachecfg_insecure_list: List[Path],
    pdaf_scale_factor: int,
):
    """Test that an insecure apache.cfg can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_apachecfg_insecure_list[i].exists()
        content = apache_apachecfg_insecure_list[i].read_text("utf-8")
        assert len(content) > 0
    assert no_duplicates(apache_apachecfg_insecure_list)


def test_apache_apachecfg_secure(apache_apachecfg_secure: Path):
    """Test that a secure apache.cfg can be provided."""
    assert apache_apachecfg_secure.exists()
    content = apache_apachecfg_secure.read_text("utf-8")
    assert len(content)


def test_apache_apachecfg_secure_list(
    apache_apachecfg_secure_list: List[Path], pdaf_scale_factor: int
):
    """Test that a secure apache.cfg can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_apachecfg_secure_list[i].exists()
        content = apache_apachecfg_secure_list[i].read_text("utf-8")
        assert len(content)
    assert no_duplicates(apache_apachecfg_secure_list)


def test_apache_ssl_context(apache_ssl_context: SSLContext):
    """Test that an ssl context can be provided."""
    assert isinstance(apache_ssl_context, SSLContext)


def test_apache_ssl_context_list(
    apache_ssl_context_list: List[SSLContext], pdaf_scale_factor: int
):
    """Test that an ssl context can be provided."""
    for i in range(pdaf_scale_factor):
        assert isinstance(apache_ssl_context_list[i], SSLContext)
    assert no_duplicates(apache_ssl_context_list)


def test_apache_username(apache_username: str):
    """Test that a username can be provided."""
    assert apache_username


def test_apache_username_list(apache_username_list: List[str], pdaf_scale_factor: int):
    """Test that a username can be provided."""
    for i in range(pdaf_scale_factor):
        assert apache_username_list[i]
    assert no_duplicates(apache_username_list)
