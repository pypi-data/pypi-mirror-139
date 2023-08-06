# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semmy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'semmy',
    'version': '1.0.0',
    'description': 'Semantic versioning made easy for Python',
    'long_description': '<h1>🐊 Semmy</h1>\n\n> [Semantic versioning](https://semver.org) made easy for Python.\n\n* [Features](#features)\n* [Prerequisites](#prerequisites)\n* [Install](#install)\n* [Usage](#usage)\n  * [Importing](#importing)\n  * [Initializing a raw object](#initializing-a-raw-object)\n  * [Initializing from string](#initializing-from-string)\n  * [Exporting as tuple](#exporting-as-tuple)\n  * [Validating input](#validating-input)\n  * [Comparing versions](#comparing-versions)\n  * [Bumping versions](#bumping-versions)\n* [Contributing](#contributing)\n\n## Features\n\nWith `semmy` you can...\n\n* Parse semantic version domain objects from valid strings\n* Check if two versions are equal\n* Check if version is greater (newer) or lesser (older) than other version\n* Check if version is a pre-release\n* Bump (pre-)major, (pre-)minor, and (pre-)patch versions\n\n## Prerequisites\n\n* **Python** >=3.8 or later\n\n## Install\n\n```sh\npoetry add semmy\n```\n\nAlternatively, for older projects.\n\n```sh\npip install semmy\npip freeze > requirements.txt\n```\n\n## Usage\n\nBelow are the most common use cases. Please, check [**the unit tests**](tests/test_semmy.py) for complete examples.\n\n### Importing\n\n```python\n>>> from semmy import Semver\n```\n\n### Initializing a raw object\n\nPlain objects are easy to initialize given three semantic version components.\n\n```python\n>>> Semver(1, 2, 3)\nVersion (1.2.3)\n```\n\nKeyword arguments are supported, too.\n\n```python\n>>> Semver(major=1, minor=2, patch=3)\nVersion (1.2.3)\n```\n\nVersions may contain pre-release tag and build number.\n\n```python\n>>> Semver(1, 0, 0, pre_release="rc-1")\nVersion (1.0.0-rc-1)\n\n>>> Semver(1, 0, 0, build="6c231887917e472da7f299c934b20f29")\nVersion (1.0.0+6c231887917e472da7f299c934b20f29)\n```\n\n### Initializing from string\n\nYou can pass a string and have it transformed to a valid object.\n\n```python\n>>> Semver.from_string("1.0.0")\nVersion (1.0.0)\n```\n\n### Exporting as tuple\n\nVersions can be exported as integer tuples.\n\n```python\n>>> Semver(1, 2, 3).as_tuple()\n(1, 2, 3)\n```\n\n### Validating input\n\nI recommend using `Semver.from_string()` whenever possible as it includes a strict input validation.\n\nFor invalid inputs, instance of `SemverException` is raised, which should be caught.\n\n```python\n>>> from semmy import Semver, SemverException\n>>> try:\n...     Semver.from_string("not-a-version")\n... except SemverException as e:\n...     print(e)\n...\nVersion string not-a-version is not a valid semantic version\n```\n\n### Comparing versions\n\nTwo versions are ordered by comparing their major, minor, and patch numbers respectively.\n\n```python\n>>> Semver.from_string("1.2.3") == Semver(1, 2, 3)\nTrue\n\n>>> Semver.from_string("1.1.0") > Semver(1, 0, 0)\nTrue\n\n>>> Semver.from_string("0.9.0") < Semver(0, 9, 1)\nTrue\n```\n\nYou may also want to sort a list of versions where Python\'s tuple ordering is helpful.\n\n```python\n>>> versions: list[Semver] = [\n...     Semver(1, 2, 3),\n...     Semver(2, 0, 0),\n...     Semver(0, 1, 0),\n... ]\n>>>\n>>> sorted(versions, key=lambda v: v.as_tuple(), reverse=True)\n[Version (2.0.0), Version (1.2.3), Version (0.1.0)]\n```\n\n### Bumping versions\n\nTypically, you want to bump major version for breaking changes, minor version for new features, and patch version for new fixes. These are supported.\n\n```python\n>>> Semver(0, 1, 0).bump_major()\nVersion (1.0.0)\n\n>>> Semver(1, 0, 0).bump_minor()\nVersion (1.1.0)\n\n>>> Semver(1, 1, 0).bump_patch()\nVersion (1.1.1)\n```\n\n## Contributing\n\nSee [**here**](CONTRIBUTING.md) for instructions.\n',
    'author': 'Niko Heikkilä',
    'author_email': 'yo@nikoheikkila.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/semmy/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
