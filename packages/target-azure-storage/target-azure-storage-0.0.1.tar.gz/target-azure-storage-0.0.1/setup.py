# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['target_azure_storage', 'target_azure_storage.tests']

package_data = \
{'': ['*']}

install_requires = \
['adlfs>=2022.2.0,<2023.0.0',
 'azure-storage-file-datalake>=12.5.0,<13.0.0',
 'fsspec>=2022.1.0,<2023.0.0',
 'pandas>=1.4.1,<2.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['target-azure-storage = '
                     'target_azure_storage.target:TargetAzureStorage.cli']}

setup_kwargs = {
    'name': 'target-azure-storage',
    'version': '0.0.1',
    'description': '`target-azure-storage` is a Singer target for Azure Storage, built with the Meltano SDK for Singer Targets.',
    'long_description': None,
    'author': 'Jules Huisman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
