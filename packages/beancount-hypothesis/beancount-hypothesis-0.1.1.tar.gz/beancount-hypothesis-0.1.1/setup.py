# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_hypothesis']

package_data = \
{'': ['*']}

install_requires = \
['RandomWords>=0.3.0,<0.4.0', 'beancount==2.3.4', 'hypothesis>=6.36.2,<7.0.0']

setup_kwargs = {
    'name': 'beancount-hypothesis',
    'version': '0.1.1',
    'description': 'A package which provides hypothesis strategies for generating beancount types',
    'long_description': '# beancount-hypothesis\n\n<p align="center">\n    <a href="https://github.com/jmgilman/beancount-hypothesis/actions/workflows/ci.yml">\n        <img src="https://github.com/jmgilman/beancount-hypothesis/actions/workflows/ci.yml/badge.svg"/>\n    </a>\n    <a href="https://pypi.org/project/beancount-hypothesis">\n        <img src="https://img.shields.io/pypi/v/beancount-hypothesis"/>\n    </a>\n</p>\n\n> A package which provides hypothesis strategies for generating beancount types.\n\n## Usage\n\nStrategies are provided for all of the core types present in `beancount`. The\nbelow example generates a random list of directives:\n\n```python\nimport beancount_hypothesis as h\nfrom hypothesis import given, strategies as s\n\n@given(\n    s.recursive(\n        h.balance()\n        | h.close()\n        | h.commodity()\n        | h.custom()\n        | h.document()\n        | h.event()\n        | h.note()\n        | h.open()\n        | h.query()\n        | h.pad()\n        | h.price()\n        | h.transaction(),\n        s.lists,\n        max_leaves=5,\n    )\n)\n```\n\nMost of the types have restrictions placed on them with the following\nphilosophy:\n\n* The value shouldn\'t break the `beancount` package\n* The value should be somewhat authentic (i.e. resemble user data)\n\nNote that the input generated from the strategies is not intended to be passed\nto any beancount functions. In other words, passing the above example to the\nloader will result in undefined behavior as it doesn\'t follow any sensible\nrules.\n\n## Testing\n\n```shell\ntox\n```\n\nWhile testing a package meant for tests seems slightly redundant, there are\nsome custom compositions present that benefit from testing. In most cases the\ntests just assert that generating data doesn\'t raise any exceptions (i.e. break\n`beancount` in some way).\n\n## Contributing\n\nCheck out the [issues][1] for items needing attention or submit your own and\nthen:\n\n1. [Fork the repo][2]\n2. Create your feature branch (git checkout -b feature/fooBar)\n3. Commit your changes (git commit -am \'Add some fooBar\')\n4. Push to the branch (git push origin feature/fooBar)\n5. Create a new Pull Request\n\n[1]: https://github.com/jmgilman/beancount-hypothesis/issues\n[2]: https://github.com/jmgilman/beancount-hypothesis/fork\n',
    'author': 'Joshua Gilman',
    'author_email': 'joshuagilman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmgilman/beancount-hypothesis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
