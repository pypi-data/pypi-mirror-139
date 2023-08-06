# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ncoreparser']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'ncoreparser',
    'version': '1.8.0',
    'description': 'Package to download from ncore.pro',
    'long_description': '![Build](https://img.shields.io/github/workflow/status/radaron/ncoreparser/Python%20application?style=for-the-badge)\n[![pypi](https://img.shields.io/pypi/v/ncoreparser?style=for-the-badge)](https://pypi.org/project/ncoreparser/)\n[![downloads](https://img.shields.io/pypi/dm/ncoreparser?style=for-the-badge)](https://pypi.org/project/ncoreparser/)\n![license](https://img.shields.io/github/license/radaron/ncoreparser?style=for-the-badge)\n\n# Ncoreparser\n\n## Introduction\n\nThis module provides python API-s to manage torrents from ncore.pro eg.: search, download, rssfeed, etc..\n\n\n## Install\n\n\n``` bash\npip install ncoreparser\n```\n\n## Examples\n\n\n\n### Search torrent\nGet most seeded torrents from all category\n\n``` python\nfrom ncoreparser import Client, SearchParamWhere, SearchParamType, ParamSort, ParamSeq\n\n\nif __name__ == "__main__":\n    client = Client()\n    client.login("<username>", "<password>")\n\n    for t_type in SearchParamType:\n        torrent = client.search(pattern="", type=t_type, number=1,\n                                sort_by=ParamSort.SEEDERS, sort_order=ParamSeq.DECREASING)[0]\n        print(torrent[\'title\'], torrent[\'type\'], torrent[\'size\'], torrent[\'id\'])\n\n    client.logout()\n```\n\n### Download torrent\nThis example download Forest gump torrent file and save it to temp folder\n\n``` python\nfrom ncoreparser import Client, SearchParamWhere, SearchParamType, ParamSort, ParamSeq\n\n\nif __name__ == "__main__":\n    client = Client()\n    client.login("<username>", "<password>")\n\n\n    torrent = client.search(pattern="Forrest gump", type=SearchParamType.SD_HUN, number=1,\n                            sort_by=ParamSort.SEEDERS, sort_order=ParamSeq.DECREASING)[0]\n\n    client.download(torrent, "/tmp")\n    client.logout()\n```\n\n### Download torrent by rssfeed\nThis example get all torrents and their informations from an ncore bookmark (rss feed)\n\n``` python\nfrom ncoreparser import Client\n\n\nif __name__ == "__main__":\n    client = Client()\n    client.login("<username>", "<password>")\n\n    torrents = client.get_by_rss("<rss url>")\n    for torrent in torrents:\n        print(torrent[\'title\'], torrent[\'type\'], torrent[\'size\'], torrent[\'id\'])\n\n    client.logout()\n```\n\n### Get torrents by activity\nThis example get all torrents and their informations from the Hit&run page\n\n``` python\nfrom ncoreparser import Client\n\n\nif __name__ == "__main__":\n    client = Client()\n    client.login("<username>", "<password>")\n\n    torrents = client.get_by_activity()\n    for torrent in torrents:\n        print(torrent[\'title\'], torrent[\'type\'], torrent[\'size\'],\n              torrent[\'id\'], torrent[\'rate\'], torrent[\'remaining\'])\n\n    client.logout()\n```\n\n### Get recommended torrents\nThis example get all torrents and their informations from the recommended page\n\n``` python\nfrom ncoreparser import Client, SearchParamType\n\n\nif __name__ == "__main__":\n    client = Client()\n    client.login("<username>", "<password>")\n\n    torrents = client.get_recommended(type=SearchParamType.SD_HUN)\n    for torrent in torrents:\n        print(torrent[\'title\'], torrent[\'type\'], torrent[\'size\'], torrent[\'id\'])\n\n    client.logout()\n```\n',
    'author': 'Aron Radics',
    'author_email': 'aron.radics.jozsef@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/radaron/ncoreparser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
