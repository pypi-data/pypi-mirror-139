# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphviz_py']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['graphviz-py = graphviz_py.cli:main']}

setup_kwargs = {
    'name': 'graphviz-py',
    'version': '1.0.3',
    'description': 'Allows Python code execution inside of graphviz diagrams.',
    'long_description': '# graphviz-py\n[![package version](https://img.shields.io/pypi/v/graphviz-py?style=flat-square&color=%2300AA00)](https://pypi.org/project/graphviz-py/)\n[![py versions](https://img.shields.io/pypi/pyversions/graphviz-py?style=flat-square)](https://pypi.org/project/graphviz-py/)\n[![pypi](https://img.shields.io/github/workflow/status/Alwinator/graphviz-py/Publish%20to%20PyPi?label=Build%20%26%20Publish&style=flat-square)](https://github.com/Alwinator/graphviz-py/actions)\n[![license](https://img.shields.io/github/license/Alwinator/graphviz-py?style=flat-square&color=%23006699)](LICENSE)\n\nAllows Python code execution inside of [graphviz](https://graphviz.org/) diagrams\n\n## Example\n```dot\ngraph python_graph {\n{{\nimport math\n\nvalue = 0.5\nsin = math.sin(value)\ncos = math.cos(value)\n}}\n\nA [label="{{= value }}"];\nB [label="{{= sin }}"];\nC [label="{{= cos }}"];\n\nA -- B [headlabel="sin"];\nA -- C [headlabel="cos"];\n\n}\n```\n\n### Output\n![output](https://raw.githubusercontent.com/Alwinator/graphviz-py/main/assets/output_file.svg)\n\n## Installation\n```bash\npip install graphviz-py\n```\n\n**Important: Make sure graphviz is installed!** See [graphviz installation instructions](https://graphviz.org/download/).\n\n\n## Usage\n### Using files\n```bash\ngraphviz-py -Tsvg example/example.py.dot -o output.svg\ngraphviz-py -Tpng example/example.py.dot -o output.png\n```\n\n### Using stdin / pipes\n[comment]: <> (echo \'digraph { node [fontname="Arial"]; edge [fontname="Arial"];  A -> B [label="  {{= 38 * 73 }}"] }\' | graphviz-py -Tsvg > output.svg)\n```bash\necho \'digraph { A -> B [label="  {{= 38 * 73 }}"] }\' | graphviz-py -Tsvg > output.svg\n```\ngraphviz-py passes all unknown arguments to graphviz. So you can use all [graphviz arguments](https://graphviz.org/doc/info/command.html).\n\n### Output\n![output](https://raw.githubusercontent.com/Alwinator/graphviz-py/main/assets/output_pipe.svg)\n\n## Variables\n```bash\ngraphviz-py -Tsvg -a myvalue=5 example/variable_example.py.dot -o output.svg\n```\nHere we pass a variable called "myvalue" with the value 5\n\n### Output\n![output](https://raw.githubusercontent.com/Alwinator/graphviz-py/main/assets/output_variable.svg)\n\n## Security\nPlease keep in mind that graphviz-py executes all Python code in the diagram. So make sure that your diagrams dies not include harmful code.\n\n## Coming soon\n- Compartibility with asciidoctor-diagram\n',
    'author': 'Alwin Schuster',
    'author_email': 'contact@alwinschuster.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Alwinator/graphviz-py',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0',
}


setup(**setup_kwargs)
