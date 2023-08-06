# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sunspecdemo']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0',
 'click>=7.0,<8.0',
 'importlib-metadata>=4.10.1,<5.0.0',
 'importlib>=1.0.4,<2.0.0',
 'pyserial==3.4',
 'pysunspec==2.0.0',
 'setuptools>=53.0.0',
 'toml>=0.10.2,<0.11.0',
 'toolz==0.9.0',
 'tqdm==4.32.1',
 'typing-extensions>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['sunspecdemo = sunspecdemo.cli:cli']}

setup_kwargs = {
    'name': 'sunspecdemo',
    'version': '0.1.9990',
    'description': 'EPC SunSpec demonstration tool',
    'long_description': '================\nEPC SunSpec Demo\n================\n\n.. image:: https://img.shields.io/github/workflow/status/epcpower/sunspec-demo/CI/main?color=seagreen&logo=GitHub-Actions&logoColor=whitesmoke\n   :alt: tests on GitHub Actions\n   :target: https://github.com/epcpower/sunspec-demo/actions?query=branch%3Amain\n\n.. image:: https://img.shields.io/github/last-commit/epcpower/sunspec-demo/main.svg\n   :alt: source on GitHub\n   :target: https://github.com/epcpower/sunspec-demo\n\nThe EPC SunSpec demo implements basic SunSpec communications with EPC converters.\nSunSpec is built on Modbus and works with both Modbus RTU (direct serial) and Modbus TCP connections.\nAdditionally this program acts as a basic example of using the `pysunspec`_ Python library.\n\n.. _pysunspec: https://github.com/sunspec/pysunspec\n\n\n------------\nInstallation\n------------\n\nThe ``poetry`` & ``poetry-dynamic-versioning`` packages must be installed.\n\n::\n\n    pip install poetry\n    pip install poetry-dynamic-versioning\n\nWindows & Linux\n===============\n\n::\n\n    poetry install\n    poetry run sunspecdemo get-models\n\n\n-------\nRunning\n-------\n\nA list of commands and options will be reported if ``--help`` is passed.\nThis can be done at any layer in the tree of subcommands.\nWhen options provide defaults they will be listed in the help output.\n\n\n``get-models``\n==============\n\n``get-models`` will download the EPC custom models needed for our specific features.\n\n\n``list-ports``\n==============\n\nAs an aid to selecting the proper serial port this subcommand will report a list of those available.\nIn some cases extra identifying information may be provided as well.\n\n\n``scan``\n========\n\nScan for responding nodes in a given node ID range.\nProvides both direct ``serial`` and ``tcp`` subcommands\n\n\n``gridtied``, ``dcdc``\n=========================\n\nConverters can be run over either Modbus RTU or Modbus TCP.\nA subcommand is provided for each: ``serial`` and ``tcp``.\nWhen running a fully selected command a basic demo sequence will be run to confirm communication with the device.\n\n\n``serial``\n----------\n\nFor a Modbus RTU connection to the converter.\nAt a minimum the serial port connected to the converter must be specified.\n\n\n``tcp``\n-------\n\nFor a Modbus TCP connection to the converter.\nAt a minimum the IP address or hostname of the converter must be specified.\n',
    'author': 'Alex Anker',
    'author_email': 'alex.anker@epcpower.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '==3.7.9',
}


setup(**setup_kwargs)
