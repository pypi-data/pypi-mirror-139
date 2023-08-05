# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plinkliftover']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'rich>=10.2.1,<11.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['bed2map = plinkliftover.bed2map:bed2mapapp',
                     'map2bed = plinkliftover.map2bed:map2bedapp',
                     'plinkliftover = plinkliftover.__main__:app']}

setup_kwargs = {
    'name': 'plinkliftover',
    'version': '0.3.0',
    'description': "Converts genotype data stored in plink's PED+MAP format from one genome build to another, using liftOver",
    'long_description': '# PLINKLiftOver\n\n[![Build status](https://github.com/milescsmith/plinkliftover/workflows/build/badge.svg?branch=master&event=push)](https://github.com/milescsmith/plinkliftover/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/plinkliftover.svg)](https://pypi.org/project/plinkliftover/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/milescsmith/plinkliftover/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/milescsmith/plinkliftover/releases)\n[![License](https://img.shields.io/github/license/milescsmith/plinkliftover)](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE)\n![Alt](https://repobeats.axiom.co/api/embed/8d9c682229fb45f45eef3f300367eb33a44bd347.svg "Repobeats analytics image")\n\n**PLINKLiftOver** is a utility enabling [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver)\nto work on genomics files from [PLINK](https://www.cog-genomics.org/plink/),\nallowing one to update the coordinates from one genome reference version to\nanother.\n\n\n## Installation\n\nPLINKLiftOver requires\n* Python 3.8 \n* The command line version of [liftOver](http://genome.ucsc.edu/cgi-bin/hgLiftOver),\ninstalled and on the system path\n* An appropriate [chain file](http://hgdownload.soe.ucsc.edu/downloads.html#liftover)\n* The [MAP file](https://zzz.bwh.harvard.edu/plink/data.shtml) from a PLINK\ndataset\n\nInstall from [pypi](https://pypi.org/project/plinkliftover/)\n```bash\npip install -U plinkliftover\n```\n\nor install the development version with\n\n```bash\npip install -U git+https://github.com/milescsmith/plinkliftover.git\n```\n\n## Usage\n\nplinkliftover has three subcommands:\n* liftover: Fully convert the genomic coordinates from one version to another \nin a PLINK file\n* map2bed: Convert a PLINK MAP file to a BED file\n* bed2map: Convert a BED file to a MAP file\n\nThe latter two subcommands are most useful in situations where it is not \npossible to run the liftOver executable locally (i.e. you are on Windows) but \ncan use [UCSC\'s online version](https://genome.ucsc.edu/cgi-bin/hgLiftOver) \nor you otherwise need/want a BED file.\n\n\n### liftover:\n\n```bash\nUsage: plinkliftover liftover [OPTIONS] MAPFILE CHAINFILE\n\n  Converts genotype data stored in the PLINK PED+MAP format from one genome\n  build to another, using liftOver.\n\nArguments:\n  MAPFILE    The plink MAP file to `liftOver`.  [required]\n  CHAINFILE  The location of the chain files to provide to `liftOver`.\n             [required]\n\nOptions:\n  --pedfile TEXT             Optionally remove "unlifted SNPs" from the plink\n                             PED file after running `liftOver`.\n  --datfile TEXT             Optionally remove \'unlifted SNPs\' from a data\n                             file containing a list of SNPs (e.g. for\n                             --exclude or --include in `plink`)\n  --prefix TEXT              The prefix to give to the output files.\n  --liftoverexecutable TEXT  The location of the `liftOver` executable.\n  -v, --version              Prints the version of the plinkliftover package.\n  --help                     Show this message and exit.\n```\n\nFor example\n\n```bash\nplinkliftover liftover updating.map hg19ToHg38.over.chain.gz --prefix updated\n```\n\n### map2bed:\n\n```bash\nUsage: plinkliftover map2bed [OPTIONS] MAPFILE\n\n  Convert genotype data stored in a PLINK MAP file into a BED file, allowing\n  one to use the online version of liftOver should the local executable is\n  unavailable\n\nArguments:\n  MAPFILE  A PLINK MAP file.  [required]\n\nOptions:\n  -o, --output PATH  Location to save BED file to.  If one is not provided,\n                     then it will be saved to where the MAP file is.\n  -v, --version      Prints the version of the plinkliftover package.\n  --help             Show this message and exit.\n```\n\n### bed2map:\n\n```bash\nUsage: plinkliftover bed2map [OPTIONS] BEDFILE\n\n  Convert genotype data stored in a PLINK MAP file into a BED file, allowing\n  one to use the online version of liftOver should the local executable is\n  unavailable\n\nArguments:\n  BEDFILE  A BED file.  [required]\n\nOptions:\n  -o, --output PATH  Location to save MAP file to.  If one is not provided,\n                     then it will be saved to where the BED file is.\n  -v, --version      Prints the version of the plinkliftover package.\n  --help             Show this message and exit.\n```\n\n### Note!\n\nBy default, [PLINK 2.0](https://www.cog-genomics.org/plink/2.0/) does not \nuse/create the required MAP file.  It can be generated using PLINK 1.9 by\n\n```bash\nplink --bfile original --recode --out to_update\n```\n\nwhere `original` is the prefix for the bed/bim/fam files and `to_update` is the prefix to give the new files.\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/milescsmith/plinkliftover)](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `GNU GPL v3.0` license. See [LICENSE](https://github.com/milescsmith/plinkliftover/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{plinkliftover,\n  author = {Miles Smith <miles-smith@omrf.org>},\n  title = {Awesome `plinkliftover` is a Python cli/package created with https://github.com/TezRomacH/python-package-template},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/milescsmith/plinkliftover}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'Miles Smith',
    'author_email': 'miles-smith@omrf.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/milescsmith/plinkliftover',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.3,<4.0',
}


setup(**setup_kwargs)
