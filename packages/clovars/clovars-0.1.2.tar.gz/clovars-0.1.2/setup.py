# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clovars',
 'clovars.IO',
 'clovars._deprecated',
 'clovars.abstract',
 'clovars.bio',
 'clovars.gui',
 'clovars.scientific',
 'clovars.simulation',
 'clovars.simulation.analysis',
 'clovars.simulation.combined',
 'clovars.simulation.run',
 'clovars.simulation.view',
 'clovars.utils',
 'clovars.utils.mixins']

package_data = \
{'': ['*'], 'clovars': ['default_settings/*']}

install_requires = \
['ete3>=3.1.2,<4.0.0',
 'matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['clovars = clovars.main:main']}

setup_kwargs = {
    'name': 'clovars',
    'version': '0.1.2',
    'description': 'Clonal Variability Simulation',
    'long_description': '# CloVarS: a clonal variability simulation\nThis repository contains the source code accompanying the article "CloVarS: a simulation of clonal variability in single cells" (in preparation).\n\n<p align="center" width="100%">\n    <img src="docs/_static/clovars_overview.png" alt="CloVarS basic workflow">\n</p>\n\n## What is CloVarS\nThe **Clo**nal **Var**iability **S**imulation (CloVarS) is a cell culture simulation that generates synthetic single-cell lineage data, as normally obtained from time-lapse microscopy experiments.\n\nThe example below depicts a single colony, starting from a single cell, which grows over 7 days:\n\n<p align="center" width="100%">\n    <img width="80%" src="docs/_static/family_tree_01.gif" alt="Simulation Family Tree">\n</p>\n\n## Installation\nCloVarS requires **Python version 3.8+** in order to run. You can install CloVarS in your Python environment with the command:\n```shell\npip install clovars\n```\nThis adds the `clovars` command to your Python environment, and also installs the necessary [dependencies](#dependencies).\n\n## How to use CloVarS\nCloVarS can be executed in the following modes: \n- `run` - run a simulation with the given settings;\n- `view` - visualize the results of a previous simulation run (figures, images, videos);\n- `analyse` - run analytical tools on the result of a previous simulation run.\n\nYou also need to provide the necessary [settings files](settings). These files use the [TOML](https://toml.io/en/) syntax, which makes it easy to open and edit them in any text editor.\n\n[This folder](settings) has examples for the structure of the settings files. **CloVarS will likely run into errors if the setting files have missing / wrong values!**\n### Run CloVarS\n```shell\nclovars run <path-to-run-settings> <path-to-colonies>\n```\nwhere: \n- `path-to-run-settings` is the path for a TOML file with the run settings;\n- `path-to-colonies` is the path for a TOML file with the colony description.\n### View CloVarS\n```shell\nclovars view <path-to-view-settings>\n```\nwhere:\n- `path-to-view-settings` is the path for a TOML file with the view settings.\n### Analyse CloVarS\n```shell\nclovars analyse <path-to-analysis-settings>\n```\nwhere: \n- `path-to-analysis-settings` is the path for a TOML file with the analysis settings.\n\n## Dependencies\nCloVarS depends on the following third-party packages:\n- ete3\n- matplotlib\n- numpy\n- pandas\n- scipy\n- seaborn\n\n## License\nCloVarS is distributed under the MIT license. Read the `LICENSE.md` file for details.\n\n## Cite us\nIf you use CloVarS, cite us: *Faccioni, JL; Lenz, G.* (in preparation).\n',
    'author': 'Juliano Faccioni',
    'author_email': 'julianofaccioni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://www.ufrgs.br/labsinal/clovars/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
