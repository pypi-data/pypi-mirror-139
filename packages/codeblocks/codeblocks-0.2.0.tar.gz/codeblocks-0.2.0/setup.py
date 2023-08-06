# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codeblocks']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['codeblocks = codeblocks:main']}

setup_kwargs = {
    'name': 'codeblocks',
    'version': '0.2.0',
    'description': 'Extract and process code blocks from Markdown files.',
    'long_description': '# codeblocks\n\nExtract and process code blocks from Markdown files. Now you can keep code examples automatically:\n\n* formatted (e.g. using [black][] for Python)\n* type checked\n* unit tested\n* linted\n* up-to-date with `--help`\n* etc\n\n# Usage\n\n```usage\nUsage: codeblocks [OPTIONS] LANGUAGE FILE [COMMAND]...\n\n  Extract or process LANGUAGE code blocks in Markdown FILE.\n\n  Extract Python code blocks:\n      codeblocks python README.md\n\n  Reformat Python code blocks using black, in place:\n      codeblocks python README.md -- black -\n\nOptions:\n  --wrap   Wrap each code block in a function.\n  --check  Do not modify the file, just return the status. Return code 0 means\n           block matches the command output. Return code 1 means block would\n           be modified.\n  --help   Show this message and exit.\n```\n\n# Examples\n\nExtract Python code blocks:\n```\ncodeblocks python README.md\n```\n\nCheck formatting of Python code blocks with black:\n```\ncodeblocks --check python README.md -- black -\n```\n\nReformat Python code blocks with black, **in place**:\n```\ncodeblocks python README.md -- black -\n```\n\nType check Python code blocks with mypy (`--wrap` puts each code block into its own function):\n```\nmypy somemodule anothermodule <(codeblocks python --wrap README.md)\n```\n\nInsert the output of `codeblock --help` into `usage` block in this README.md:\n```\ncodeblocks usage README.md -- codeblocks --help\n```\n\nMake sure `usage` block in this README.md is up-to-date with `--help` output:\n```\ncodeblocks --check usage README.md -- codeblocks --help\n```\n\n# Full type checking example\n\n```python\ndef plus(x: int, y: int) -> int:\n    return x + y\n\nplus(1, \'2\')\n```\n\n```\n$ mypy --pretty --strict <(codeblocks python README.md)\n/dev/fd/63:5: error: Argument 2 to "plus" has incompatible type "str"; expected "int"\n        plus(1, \'2\')\n                ^\nFound 1 error in 1 file (checked 1 source file)\n```\n\n# Rationale\n\nThere are alternative tools, but none of them supported all of the cases above.\n\n* [prettier][] [can reformat Markdown code blocks][prettier-md] ([PR][prettier-pr]), but it works only for supported languages like JavaScript. It does not support Python. No lint or unit test support.\n* [blacken-docs][] can reformat Python code blocks, but it does not support all [black][] options. For example, [`black --check`][blacken-check] is not supported. No lint or unit test support. In addition, `codeblocks` implementation is much simpler and is not coupled with black.\n* [excode][] is very similar, but does not support in place modifications.\n* [gfm-code-blocks][] does not have command line interface.\n\n[black]: https://github.com/psf/black\n[prettier]: https://prettier.io\n[prettier-md]: https://prettier.io/blog/2017/11/07/1.8.0.html#markdown-support\n[prettier-pr]: https://github.com/prettier/prettier/pull/2943\n[blacken-docs]: https://github.com/asottile/blacken-docs\n[blacken-check]: https://github.com/asottile/blacken-docs/issues/42\n[excode]: https://github.com/nschloe/excode\n[gfm-code-blocks]: https://github.com/jonschlinkert/gfm-code-blocks\n',
    'author': 'Alexey Shamrin',
    'author_email': 'shamrin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shamrin/codeblocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
