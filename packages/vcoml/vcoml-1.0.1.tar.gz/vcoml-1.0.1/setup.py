# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcoml']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vcoml',
    'version': '1.0.1',
    'description': 'Imagine a markup language, but worse',
    'long_description': '# vcoml\n\nImagine a markup language, but worse\n\n## Syntax Example\n\nVcoML:\n\n```vcoml\n:"members"\n  :297045071457681409\n    :"username"\n      "vcokltfre"\n    :"discriminator"\n      6868\n    :"mfa"\n      ya\n    :"verified"\n      na\n    :"email"\n      idk\n    :"roles"\n      >\n        :"id"\n          1234\n        :"name"\n          "Admin"\n      >\n        :"id"\n          5678\n        :"name"\n          "Moderator"\n```\n\nYAML:\n\n```yml\nmembers:\n  297045071457681409:\n    username: vcokltfre\n    discriminator: 6868\n    mfa: true\n    verified: false\n    email: null\n    roles:\n      - id: 1234\n        name: Admin\n      - id: 5678\n        name: Moderator\n```\n\n## Usage\n\n```py\nfrom vcoml import pack, unpack\n\n\ndata = unpack("""\n:"abc"\n  123\n:"def"\n  >\n    "list"\n  >\n    "more list"\n""")\n\nprint(data)\n\n# Re-pack the data\nprint(pack(data))\n```\n\n## Todo\n\n- CLI\n',
    'author': 'vcokltfre',
    'author_email': 'vcokltfre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vcokltfre/vcoml',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
