# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['radios']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0',
 'aiohttp>=3.0.0',
 'awesomeversion>=21.10.1',
 'backoff>=1.9.0',
 'cachetools>=4.0.0',
 'pycountry>=22.1.10,<23.0.0',
 'pydantic>=1.9,<2.0',
 'yarl>=1.6.0']

setup_kwargs = {
    'name': 'radios',
    'version': '0.1.0',
    'description': 'Asynchronous Python client for the Radio Browser API',
    'long_description': '# Python: Radio Browser API Client\n\n[![GitHub Release][releases-shield]][releases]\n[![Python Versions][python-versions-shield]][pypi]\n![Project Stage][project-stage-shield]\n![Project Maintenance][maintenance-shield]\n[![License][license-shield]](LICENSE.md)\n\n[![Build Status][build-shield]][build]\n[![Code Coverage][codecov-shield]][codecov]\n[![Code Quality][code-quality-shield]][code-quality]\n\n[![Sponsor Frenck via GitHub Sponsors][github-sponsors-shield]][github-sponsors]\n\n[![Support Frenck on Patreon][patreon-shield]][patreon]\n\nAsynchronous Python client for the Radio Browser API.\n\n## About\n\n[Radio Browser](https://www.radio-browser.info) community driven effort\n(like WikiPedia) with the aim of collecting as many internet radio and\nTV stations as possible.\n\nThis Python library is an async API client for that, originally developed\nfor use with the [Home Assistant](https://www.home-assistant.io) project.\n\n## Installation\n\n```bash\npip install radios\n```\n\n## Usage\n\n```python\n# pylint: disable=W0621\n"""Asynchronous Python client for the Radio Browser API."""\n\nimport asyncio\n\nfrom radios import FilterBy, Order, RadioBrowser\n\n\nasync def main() -> None:\n    """Show example on how to query the Radio Browser API."""\n    async with RadioBrowser(user_agent="MyAwesomeApp/1.0.0") as radios:\n        # Print top 10 stations\n        stations = await radios.stations(\n            limit=10, order=Order.CLICK_COUNT, reverse=True\n        )\n        for station in stations:\n            print(f"{station.name} ({station.click_count})")\n\n        # Get a specific station\n        print(await radios.station(uuid="9608b51d-0601-11e8-ae97-52543be04c81"))\n\n        # Print top 10 stations in a country\n        stations = await radios.stations(\n            limit=10,\n            order=Order.CLICK_COUNT,\n            reverse=True,\n            filter_by=FilterBy.COUNTRY_CODE_EXACT,\n            filter_term="NL",\n        )\n        for station in stations:\n            print(f"{station.name} ({station.click_count})")\n\n        # Register a station "click"\n        await radios.station_click(uuid="9608b51d-0601-11e8-ae97-52543be04c81")\n\n        # Tags, countries and codes.\n        print(await radios.tags(limit=10, order=Order.STATION_COUNT, reverse=True))\n        print(await radios.countries(limit=10, order=Order.NAME))\n        print(await radios.languages(limit=10, order=Order.NAME))\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\n## Changelog & Releases\n\nThis repository keeps a change log using [GitHub\'s releases][releases]\nfunctionality.\n\nReleases are based on [Semantic Versioning][semver], and use the format\nof `MAJOR.MINOR.PATCH`. In a nutshell, the version will be incremented\nbased on the following:\n\n- `MAJOR`: Incompatible or major changes.\n- `MINOR`: Backwards-compatible new features and enhancements.\n- `PATCH`: Backwards-compatible bugfixes and package updates.\n\n## Contributing\n\nThis is an active open-source project. We are always open to people who want to\nuse the code or contribute to it.\n\nWe\'ve set up a separate document for our\n[contribution guidelines](CONTRIBUTING.md).\n\nThank you for being involved! :heart_eyes:\n\n## Setting up development environment\n\nThis Python project is fully managed using the [Poetry][poetry] dependency\nmanager. But also relies on the use of NodeJS for certain checks during\ndevelopment.\n\nYou need at least:\n\n- Python 3.9+\n- [Poetry][poetry-install]\n- NodeJS 14+ (including NPM)\n\nTo install all packages, including all development requirements:\n\n```bash\nnpm install\npoetry install\n```\n\nAs this repository uses the [pre-commit][pre-commit] framework, all changes\nare linted and tested with each commit. You can run all checks and tests\nmanually, using the following command:\n\n```bash\npoetry run pre-commit run --all-files\n```\n\nTo run just the Python tests:\n\n```bash\npoetry run pytest\n```\n\n## Authors & contributors\n\nThe original setup of this repository is by [Franck Nijhof][frenck].\n\nFor a full list of all authors and contributors,\ncheck [the contributor\'s page][contributors].\n\n## License\n\nMIT License\n\nCopyright (c) 2022 Franck Nijhof\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n[build-shield]: https://github.com/frenck/python-radios/actions/workflows/tests.yaml/badge.svg\n[build]: https://github.com/frenck/python-radios/actions/workflows/tests.yaml\n[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/frenck/python-radios.svg?logo=lgtm&logoWidth=18\n[code-quality]: https://lgtm.com/projects/g/frenck/python-radios/context:python\n[codecov-shield]: https://codecov.io/gh/frenck/python-radios/branch/master/graph/badge.svg\n[codecov]: https://codecov.io/gh/frenck/python-radios\n[contributors]: https://github.com/frenck/python-radios/graphs/contributors\n[frenck]: https://github.com/frenck\n[github-sponsors-shield]: https://frenck.dev/wp-content/uploads/2019/12/github_sponsor.png\n[github-sponsors]: https://github.com/sponsors/frenck\n[license-shield]: https://img.shields.io/github/license/frenck/python-radios.svg\n[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg\n[patreon-shield]: https://frenck.dev/wp-content/uploads/2019/12/patreon.png\n[patreon]: https://www.patreon.com/frenck\n[poetry-install]: https://python-poetry.org/docs/#installation\n[poetry]: https://python-poetry.org\n[pre-commit]: https://pre-commit.com/\n[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg\n[pypi]: https://pypi.org/project/radios/\n[python-versions-shield]: https://img.shields.io/pypi/pyversions/radios\n[releases-shield]: https://img.shields.io/github/release/frenck/python-radios.svg\n[releases]: https://github.com/frenck/python-radios/releases\n[semver]: http://semver.org/spec/v2.0.0.html\n',
    'author': 'Franck Nijhof',
    'author_email': 'opensource@frenck.dev',
    'maintainer': 'Franck Nijhof',
    'maintainer_email': 'opensource@frenck.dev',
    'url': 'https://github.com/frenck/python-radios',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
