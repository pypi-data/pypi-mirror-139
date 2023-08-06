# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mounty']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'mounty',
    'version': '1.0.0',
    'description': 'A simple Python client for Mountebank',
    'long_description': '[![codecov](https://codecov.io/gh/vicusbass/mounty/branch/main/graph/badge.svg?token=7Y76GKTW5L)](https://codecov.io/gh/vicusbass/mounty)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/vicusbass/mounty.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/vicusbass/mounty/context:python)\n# mounty\n\nA wrapper for Mountebank REST API, can be used for existing instances or for testing in CI/CD ephemeral Mountebank instances.\n\nWho/what is Mountebank? Mountebank is an amazing open-source stub/service virtualisation tool, see more [here](http://www.mbtest.org/).\nIt can be used as a stub service for any external dependency, it can run as proxy (recording and replaying requests), it can be used for load testing services in isolation (stub external requests, so no more latency added)\n\n\n## Installation\n\n```bash\n$ pip install mounty\n```\n\n## Usage examples:\n\n```python\nimport requests\nfrom mounty import Mountebank\nfrom mounty.models import Imposter, Stub\n\nSIMPLE_IMPOSTER = {\n "port": 4555,\n "protocol": "https",\n "stubs": [{"responses": [{"is": {"statusCode": 201}}]}],\n}\n\n# the url must contain the port on which Mountebank is listening\nmountebank = Mountebank(url="http://mountebank.foo:2525")\n# or, if MOUNTEBANK_URL variable is defined:\nmountebank_from_env = Mountebank.from_env()\n\nimposter = mountebank.add_imposter(imposter=SIMPLE_IMPOSTER)\n\nother_imposter = mountebank.add_imposter(\n imposter=Imposter(\n  port=4556,\n  protocol="http",\n  stubs=[Stub(responses=[{"is": {"statusCode": 201}}])],\n )\n)\n\n# peform 2 requests\nrequests.post(url="http://mountebank.foo:4545")\nrequests.post(url="http://mountebank.foo:4545")\n# wait for maximum 2 seconds for the imposter to contain 2 recorded requests\nreqs = mountebank.wait_for_requests(port=4555, count=2, timeout=2)\n```\n\n#### Local development\n\nYou will first need to clone the repository using git and place yourself in its directory:\n\n```bash\n$ poetry install -vv\n$ poetry run pytest tests/\n```\n\nTo make sure that you don\'t accidentally commit code that does not follow the coding style:\n\n```bash\n$ poetry run pre-commit autoupdate\n$ poetry run pre-commit install\n$ poetry run pre-commit run --all-files\n```\n\n#### TODOs\n\n- Add integration tests which will create scenarios in several versions of Mountebank running as docker containers\n- MORE examples\n',
    'author': 'Vasile Pop',
    'author_email': 'vasile.pop@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vicusbass/mounty',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
