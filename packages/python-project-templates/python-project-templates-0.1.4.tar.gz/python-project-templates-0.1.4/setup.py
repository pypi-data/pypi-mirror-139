# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['package_1', 'package_2']

package_data = \
{'': ['*']}

install_requires = \
['optext-python==0.1.1']

extras_require = \
{'docs': ['furo',
          'myst-parser',
          'pdoc3',
          'pydata-sphinx-theme',
          'python-docs-theme',
          'sphinx',
          'sphinx-book-theme',
          'sphinx-theme-pd',
          'sphinx_rtd_theme<=2.0.0',
          'sphinxcontrib-mermaid']}

entry_points = \
{'console_scripts': ['add-1-2 = package_1.__main__:main',
                     'sample-command = package_2.__main__:main'],
 'pseudo_package.plugin': ['sample-plugin = package_1.plugins:plugin_call']}

setup_kwargs = {
    'name': 'python-project-templates',
    'version': '0.1.4',
    'description': 'This is a template for python projects.',
    'long_description': "# Python Project Template\n\nThis is a template repository for python project.\n\ncheck [GitHub document](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository) aboud template repository.\n\n## CI/CD\n\n[![Python package][ci-badge]][ci-url]\n[![readthedocs build status][docs-badge]][docs-url]\n[![pre-commit][pre-commit-badge]][pre-commit-url]\n[![CodeQL][codeql-badge]][codeql-url]\n[![License: MIT][mit-badge]][mit-url]\n[![PyPI version][pypi-badge]][pypi-url]\n[![Github pages][gh-pages-badge]][gh-pages-url]\n\n[ci-badge]: https://github.com/kagemeka/python-project-template/actions/workflows/python-package.yml/badge.svg\n[ci-url]: https://github.com/kagemeka/python-project-template/actions/workflows/python-package.yml\n[docs-badge]: https://readthedocs.org/projects/python-project-templates/badge/?version=latest\n[docs-url]: https://python-project-templates.readthedocs.io\n[pre-commit-badge]: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n[pre-commit-url]: https://github.com/pre-commit/pre-commit\n[codeql-badge]: https://github.com/kagemeka/python-project-template/actions/workflows/codeql-analysis.yml/badge.svg\n[codeql-url]: https://github.com/kagemeka/python-project-template/actions/workflows/codeql-analysis.yml\n[mit-badge]: https://img.shields.io/badge/License-MIT-blue.svg\n[mit-url]: https://opensource.org/licenses/MIT\n[pypi-badge]: https://badge.fury.io/py/python-project-templates.svg\n[pypi-url]: https://badge.fury.io/py/python-project-templates\n[gh-pages-badge]: https://github.com/kagemeka/python-project-template/actions/workflows/pages/pages-build-deployment/badge.svg\n[gh-pages-url]: https://kagemeka.github.io/python-project-template\n\nfor detail about badges, see\n* [GitHub documentation](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge)\n* [readthedocs build badges](https://docs.readthedocs.io/en/stable/badges.html)\n\nThis project is integrated with `./scripts/ci.sh` \\\nYou should run the script every time before git commit.\n\n## docker environment\n\nUse docker to avoid annoying environment conflicts. \\\nFirst, you must set the project name in `docker/.env` file. \\\nthen you can run `docker-compose up -d` command\nto build an docker image with default Dockerfile.\n\n```bash\n$ cd docker \\\n    && docker-compose up -d\n```\n\nfor details about docker, see official documentations\n* [Docker](https://docs.docker.com/)\n* [Docker Compose](https://docs.docker.com/compose/)\n\n## Documenting\n\nYou can use documenting tools like\n* [sphinx](https://www.sphinx-doc.org/en/master/)\n* [mkdocs](https://www.mkdocs.org/)\n\nand host it on [readthedocs](https://docs.readthedocs.io/)\n\n[ `Python Project Template` 's documentation](https://python-project-templates.readthedocs.io/)\n---\n\n### sphinx\n\n#### [shpinx-apidoc](https://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html)\n\ngenerate document with sphinx-apidoc command.\n[script](scripts/generate_sphinx_docs.sh)\n\n#### configurations (todo)\n\nsphinx extensions\nhttps://www.sphinx-doc.org/en/master/usage/extensions/index.html\n\nnapoleon\nhttps://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#module-sphinx.ext.napoleon\n\nnumpy style\nhttps://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard\n\ngoogle style\nhttps://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings\n\n## publish package to Pypi\n\nhit this command on terminal to publish the current version to Pypi.\n\n```bash\n$ ./scripts/publish.sh\n```\n\n* [ ] auto updating with github actions is coming soon.\n\n## Quick Start using this template.\n\n* edit project name for docker environment.\n* edit project configuration\n  + edit `pyproject.toml`'s metadata section.\n  + delete such as `tool.poetry.scripts` and so on needless.\n* edit documentation configuration.\n  + `docs/_*.conf.py` files.\n  + `scripts/generate_sphinx_docs_headers.py`\n  + `.readthedocs.yaml`'s `sphinx.configuration` option (optional).\n* Rewrite your own project README.\n* delete `src/package_*` directories.\n* now it's time to start make your own package.\n",
    'author': 'Hiroshi Tsuyuki',
    'author_email': 'kagemeka1@gmail.com',
    'maintainer': 'Hiroshi Tsuyuki',
    'maintainer_email': 'kagemeka1@gmail.com',
    'url': 'https://github.com/kagemeka/python-project-template/#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
