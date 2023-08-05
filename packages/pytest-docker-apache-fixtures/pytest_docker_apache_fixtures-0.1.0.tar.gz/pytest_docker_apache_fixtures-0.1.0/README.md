# pytest-docker-apache-fixtures

## Overview

Pytest fixtures to instantiate and utilize local apache (httpd) docker containers, using [lovely-pytest-docker](https://pypi.org/project/lovely-pytest-docker) and [docker-py](https://pypi.org/project/docker-py), for testing.

## Getting Started

Update <tt>setup.py</tt> to include:

```python
from distutils.core import setup

setup(
	tests_require=["pytest-docker-apache-fixtures"]
)
```

All fixtures should be automatically included via the <tt>pytest11</tt> entry point.
```python
import requests
import pytest
from pytest_docker_apache_fixtures import ApacheInsecure, ApacheSecure  # Optional, for typing

def test_apache_secure(apache_secure: ApacheSecure):
    response = requests.head(f"https://{apache_secure.endpoint}/",
        headers=apache_secure.auth_header,
        verify=str(apache_secure.cacerts),
    )
    assert response.status_code == 200

def test_apache_insecure(apache_insecure: ApacheInsecure):
    response = requests.head(f"http://{apache_insecure.endpoint}/")
    assert response.status_code == 200
```

The `push_image` mark can optionally be added to stage images in the apache prior to testing. See [Markers](#markers) for details.
## Compatibility

* Tested with python 3.8

## Installation
### From [pypi.org](https://pypi.org/project/pytest-docker-apache-fixtures/)

```
$ pip install pytest_docker_apache_fixtures
```

### From source code

```bash
$ git clone https://github.com/crashvb/pytest-docker-apache-fixtures
$ cd pytest-docker-apache-fixtures
$ virtualenv env
$ source env/bin/activate
$ python -m pip install --editable .[dev]
```

## <a name="fixtures"></a>Fixtures

### <a name="apache_auth_header"></a> apache_auth_header

Retrieves an HTTP basic authentication header that is populated with credentials that can access the secure apache service. The credentials are retrieved from the [apache_password](#apache_password) and [apache_username](#apache_username) fixtures. This fixture is used to replicate docker images into the secure apache service.

### <a name="apache_cacerts"></a> apache_cacerts

Locates a user-defined CA trust store (<tt>tests/cacerts</tt>) to use to verify connections to the secure apache service. If one cannot be located, a temporary trust store is created containing certificates from <tt>certifi</tt> and the [apache_certs](#apache_certs) fixture. This fixture is used to instantiate the secure apache service.

### <a name="apache_certs"></a> apache_certs

Returns the paths of the self-signed certificate authority certificate, certificate, and private key that are used by the secure apache service. This fixture is used to instantiate the secure apache service.

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **ca_certificate** - Path to the self-signed certificate authority certificate.
* **ca_private_key** - Path to the self-signed certificate authority private key.
* **certificate** - Path to the certificate.
* **private_key** - Path to the private key.

Typing is provided by `pytest_docker_apache_fixtures.ApacheCerts`.

### <a name="apache_hwpasswd"></a> apache_htpasswd

Provides the path to a htpasswd file that is used by the secure apache service. If a user-defined htpasswd file (<tt>tests/htpasswd</tt>) can be located, it is used. Otherwise, a temporary htpasswd file is created using credentials from the [apache_password](#apache_password) and [apache_username](#apache_username) fixtures. This fixture is used to instantiate the secure apache ervice.

### <a name="apache_apachecfg_insecure"></a> apache_apachecfg_insecure

Provides the path to an insecure apache.cfg file that is used by the insecure apache service. If a user-defined apache.cfg file (<tt>tests/apache.insecure.cfg</tt>) can be located, it is used. Otherwise, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the insecure apache service.

### <a name="apache_apachecfg_secure"></a> apache_apachecfg_secure

Provides the path to a secure apache.cfg file that is used by the secure apache service. If a user-defined apache.cfg file (<tt>tests/apache.secure.cfg</tt>) can be located, it is used. Otherwise, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the secure apache service.

### <a name="apache_insecure"></a> apache_insecure

Configures and instantiates a apache service without TLS or authentication.

```python
import requests
from pytest_docker_apache_fixtures import ApacheInsecure  # Optional, for typing

def test_apache_insecure(apache_insecure: ApacheInsecure):
    response = requests.head(f"http://{apache_insecure.endpoint}/")
    assert response.status_code == 200
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the insecure apache service.
* **endpoint_name** - Endpoint of the insecure apache service, by service name.
* **service_name** - Name of the service within the docker-compose configuration.

Typing is provided by `pytest_docker_apache_fixtures.ApacheInsecure`.

### <a name="apache_password"></a> apache_password

Provides a generated password to use for authentication to the secure apache service. This fixture is used to replicate docker images into the secure apache service.

### <a name="apache_secure"></a> apache_secure

Configures and instantiates a TLS enabled apache service with HTTP basic authorization.

```python
import requests
from pytest_docker_apache_fixtures import ApacheSecure  # Optional, for typing

def test_apache_secure(apache_secure: ApacheSecure):
    response = requests.head(
        f"https://{apache_secure.endpoint}/",
        headers=apache_secure.auth_header,
        verify=str(apache_secure.cacerts),
    )
    assert response.status_code == 200
```

#### NamedTuple Fields

The following fields are defined in the tuple provided by this fixture:

* **auth_header** - from [apache_auth_header](#apache_auth_header).
* **cacerts** - from [apache_cacerts](#apache_cacerts).
* **certs** - from [apache_certs](#apache_certs).
* **docker_compose** - Path to the fully instantiated docker-compose configuration.
* **endpoint** - Endpoint of the secure apache service.
* **endpoint_name** - Endpoint of the secure apache service, by service name.
* **htpasswd** - from [apache_htpasswd](#apache_htpasswd)
* **password** - from [apache_password](#apache_password).
* **service_name** - Name of the service within the docker-compose configuration.
* **ssl_context** - from [apache_ssl_context](#apache_ssl_context).
* **username** - from [apache_username](#apache_username).

Typing is provided by `pytest_docker_apache_fixtures.ApacheSecure`.

### <a name="apache_ssl_context"></a> apache_ssl_context

Provides an SSL context containing the CA trust store from the  [apache_cacerts](#apache_cacerts) fixture. This fixture is used to instantiate the secure apache service.

### <a name="apache_username"></a> apache_username

Provides a generated username to use for authentication to the secure apache service. This fixture is used to replicate docker images into the secure apache service.

### <a name="pdhf_docker_compose_insecure"></a> pdhf_docker_compose_insecure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-apache-insecure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the insecure apache service. The configuration will be treated as a template; the <tt>$PATH_APACHECFG</tt> token will be populated with the absolute path provided by the [apache_apachecfg](#apache_apachecfg) fixture.

### <a name="pdhf_docker_compose_secure"></a> pdhf_docker_compose_secure

This fixture uses the `docker_compose_files` fixture to locate a user-defined docker-compose configuration file (typically <tt>tests/docker-compose.yml</tt>) that contains the <tt>pytest-docker-apache-secure</tt> service. If one cannot be located, an embedded configuration is copied to a temporary location and returned. This fixture is used to instantiate the secure apache service. The configuration will be treated as a template; the <tt>$PATH_CERTIFICATE</tt>, <tt>$PATH_HTPASSWD</tt>, <tt>$PATH_KEY</tt>, and <tt>$PATH_APACHECFG</tt> tokens will be populated with the absolute paths provided by the [apache_certs](#apache_certs), [apache_htpasswd](#apache_htpasswd), and [apache_apachecfg](#apache_apachecfg) fixtures, as appropriate.

## <a name="enumerated_fixtures"></a>Enumerated Fixtures

It is possible to instantiate multiple apache instances using the corresponding enumerated fixtures. All [fixtures](#fixtures) listed above have _*_list_ (e.g. `apache_secure` -> `apache_secure_list`) versions that will return enumerated lists of corresponding data type.

For example:

```python
import requests
from typing import List  # Optional, for typing
from pytest_docker_apache_fixtures import ApacheSecure  # Optional, for typing

def test_apache_secure_list(apache_secure_list: List[ApacheSecure]):
    for apache_secure in apache_secure_list:
        response = requests.head(
            f"https://{apache_secure.endpoint}/",
            headers=apache_secure.auth_header,
            verify=str(apache_secure.cacerts),
        )
        assert response.status_code == 200
```

It is possible to use both singular and enumerated fixtures within the same test context; however, the same values will be returned for the singular fixture as the first enumerated list value (i.e. apache_secure == apache_secure_list[0]). To avoid complications with lower layers, mainly docker-compose, and to allow for this interchangeability, caching is used internally.

By default, the scale factor of the enumerated instances is set to one (n=1). This value can be changed by overriding the `pdhf_scale_factor` fixture, as follows:

```python
import pytest

@pytest.fixture(scope="session")
def pdhf_scale_factor() -> int:
    return 4
```

This fixture will be used to scale both the insecure and secure docker registries.

## <a name="limitations"></a>Limitations

1. All the fixtures provided by this package are <tt>session</tt> scoped; and will only be executed once per test execution.
2. At most 10 insecure and 10 secure apache instances are supported using the embedded docker compose.

## Development

[Source Control](https://github.com/crashvb/pytest-docker-apache-fixtures)
