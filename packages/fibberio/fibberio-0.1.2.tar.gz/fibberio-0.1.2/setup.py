# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fibberio']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'click>=8.0.3,<9.0.0',
 'numpy>=1.22.2,<2.0.0',
 'parsimonious>=0.8.1,<0.9.0']

entry_points = \
{'console_scripts': ['fibber = fibberio.cli:cli']}

setup_kwargs = {
    'name': 'fibberio',
    'version': '0.1.2',
    'description': '',
    'long_description': '# fibber\nLib for generating fake data\n\n# Sources\nSources can be either:\n1. Pointer to an inline source description\n2. A collection of items (`List`)\n```\n["cat", "dog", "horse"]\n[1, 2, 3]\n...\n```\n\n3. Range description (with optional type `[int, float(precision)]` otherwise inferred)\n```\n[12000, 32000) -> float   # without type inferred as int\n(.01, .9)                 # inferred as float\n(25, 45] -> int           # without type inferred as int (unecessary)\n(100, 200) -> float(2)    # cast to float with 2 decimal places\n```\nFor reference (helpful for ranges):\n- $[a, b]$ the closed interval $\\{ x \\in \\mathbb{R}: a \\le x \\le b \\}$\n- $[a, b)$ the interval $\\{ x \\in \\mathbb{R}: a \\le x \\lt b \\}$\n- $(a, b]$ the interval $\\{ x \\in \\mathbb{R}: a \\lt x \\le b \\}$\n- $(a, b)$ the open interval $\\{ x \\in \\mathbb{R}: a \\lt x \\lt b \\}$\n\n# Distributions\nDistributions fall into two categories: discrete and continuous\n\n1. (**Discrete**) The cardinality of discrete probability densities need to match the inherent cardinality of the source classes. For example:\n```\n{\n  "feature": "TabsVSpaces",\n  "source": ["tabs", "spaces", "dots"],\n  "distribution": [25, 75, 200],\n}\n```\nThe `TabsVSpaces` feature has three discrete items in the source. The distributional densities need to also have a cardinality of 3. These values are normalized in the system and selected using a uniform distribution mapped to the respective densities.\n\n2.  (**Continuous**) Continuous distributions are sampled according to the respective distribution class. For example:\n```\ndistribution_class(prop1=2, prop2=seismic)\n```\nwill create \'distribution_class\' class by extracting `argsv` as\n```\n{\n  "prop1": 2,\n  "prop2": "seismic"\n}\n```\nand instantiating by:\n```\ndistribution_class(**argsv)\n```\n\nI am optimizing for readibility as opposed to brevity. This requires the class to have an `__init()__` with default named parameters.\n\n## Conditionals\n\nThis can change when having a conditional from a continous range source to a discrete range source. Consider the following Feature :\n```\n{\n  "feature": "NumberFeature",\n  "source": "(100000, 200000] -> float(2)",\n  "distribution": "uniform",\n  "conditional": {\n    "feature": "subfeature",\n    "source": ["carts", "horses", "wheels"],\n    "distribution": [\n      "(150000, 18000]",\n      "[*, 15000)",\n      "*"\n    ]\n  }\n}\n```\nIn this case the `NumberFeature` is generated uniformly at random from the interval $\\{ x \\in \\mathbb{R}: 100000 \\lt x \\le 200000 \\}$. When projecting into the discrete conditional distribution we need to scope the original distribution _onto_ the three classes in the conditional. The distribution rules are applied in the order in which they appear with _truthiness_ being a measure of whether the class is selected or not. A `*` indicates a placeholder on either the min, max, or as a catch all.\nIn this case, as fibber generates a data point if `NumberFeature` fits the first distribution rule, it will also output `carts`. If it fails it proceeds to the next. If this rule is true it will produce `horses`. If none of them fit, then it will proceed to the catch-all and produce `wheels`. If it cannot find a successful match, fibber will throw an exception.\n\n# Task Description\n```\n{\n  "sources": [\n    {\n      "id": "names",\n      "data": "./full_names.csv"\n    }\n  ],\n  "features": [\n    {\n      "feature": "FirstName,LastName",\n      "source": "names",\n      "distribution": "uniform"\n    },\n    {\n      "feature": "Age",\n      "source": "(14, 85] -> int",\n      "distribution:": "normal"\n    },\n    {\n      "feature": "TabsVSpaces",\n      "source": ["tabs", "spaces", "dots"],\n      "distribution": [25, 75, 200],\n      "conditional": {\n        "feature": "subtabspaces",\n        "source": "[12, 59] -> float(2)",\n        "distribution": ["uniform", "normal(0.2)", "normal(12.2, 0.5)"]\n      }\n    },\n    {\n      "feature": "ScrumVAgile",\n      "source": ["scrum", "agile"],\n      "distribution": [25, 75],\n      "conditional": {\n        "feature": "subfeature",\n        "source": ["cheese", "pepper", "macaroni", "pretzels"],\n        "distribution": [\n          [0, 0, 2, 20], \n          [10, 20, 2, 1]\n        ],\n        "conditional": {\n          "feature": "subsubfeature",\n          "source":"(100000, 200000] -> float",\n          "distribution": [\n            "uniform",\n            "normal(0.2)",\n            "uniform",\n            "normal(.01)"\n          ]\n        }\n      }\n    },\n    {\n      "feature": "NumberFeature",\n      "source": "(100000, 200000] -> float(2)",\n      "distribution": "uniform",\n      "conditional": {\n        "feature": "subfeature",\n        "source": ["carts", "horses", "wheels"],\n        "distribution": [\n          "(150000, 18000]",\n          "[*, 15000)",\n          "*"\n        ],\n        "conditional": {\n          "feature": "subsubfeature",\n          "source":"(100000, 200000]->float",\n          "distribution": [\n            "uniform",\n            "normal(0.2)",\n            "uniform",\n            "normal(.01)"\n          ]\n        }\n      }\n    }\n  ]\n}\n```',
    'author': 'sethjuarez',
    'author_email': 'me@sethjuarez.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
