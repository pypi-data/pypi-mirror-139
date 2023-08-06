# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tyson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tyson',
    'version': '0.1.0',
    'description': 'Typed Simple Object Notation',
    'long_description': "## TySON\n\n![Neil deGrasse Tyson](https://pbs.twimg.com/profile_images/74188698/NeilTysonOriginsA-Crop_400x400.jpg)\n\n*Neil deGrasse Tyson - an astrophysicist, planetary scientist, author, and science communicator.*\n\nTyped Simple Object Notation (TySON) is a text-based type-customizable data-serialization format. The key feature of this format is typing. Each value (primitive and container) contains a type, which can be mapped to a specific data structure during implementation. This expands the ways of processing and storing data.\n\n\n## Grammar\n\nA TySON text is a sequence of tokens wrapped into a document. There are 3 types of tokens: vector, map, and primitive\n\n### Document\n\nThe document is key/value pairs separated with commas or semicolons. Key is primitive, value could be any TySON token.  A single colon comes after each key. Keys can be not unique.\n\n```\nk|foo|: v|bar|;\nk|one|: l[n|1|, n|2|, n|3|];\nk|two|: o{n|1|:s|uno|, n|2|:s|dos|};\n```\n\n### Map\n\nThe map consists of a type and a pair of curly brackets surrounding zero or more key/value pairs. Type represented as strings, which consists of letters. Key is primitive, value could be any TySON token. A single colon comes after each key. Keys can be not unique.\n\n```\nk|two|: o{n|1|:s|uno|, n|2|:s|dos|};\n```\n\n### Vector\n\nThe vector consists of a type and a pair of square brackets surrounding zero or more values. Type represented as strings, which consists of letters. Value could be any TySON token.\n\n```\nk|one|: l[n|1|, n|2|, n|3|];\n```\n\n### Primitive\n\nPrimitive consists of a type and is surrounded by vertical bars value. If the value is empty, vertical bars don't exist. If the type is empty, the value must be surrounded by bars. Type is a string of letters, value is any string.\n\nValid primitives\n```\ntype|value|\ntype\n|value|\n```\n",
    'author': 'Roman Right',
    'author_email': 'roman-right@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://roman-right.github.io/tyson/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
