# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypy_typing_asserts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mypy-typing-asserts',
    'version': '0.1.0',
    'description': 'Adds the ability to _assert_ types when typechecking to mypy',
    'long_description': "# mypy-typing-asserts\n\nAdds the ability to _assert_ types when typechecking to `mypy`.\n\n```python\nassert_type[MyType[tuple[int, ...]]](myobject.attribute)\n```\n\n## Support\n\n`mypy-typing-asserts` is supported in `mypy >= 0.700`.\n\nFor `pyright` support, use `reveal_type(expression, expected_type=...)`. (See [this discussion](https://github.com/python/typing/discussions/1030#discussioncomment-1988476)). (Supported in version 1.1.211+)\n\n## Installation\n\n`mypy-typing-asserts` should be installed in to the same environment as your typechecker.\n\nIt can be installed by running `pip install mypy-typing-asserts`.\n\nAlternatively if you're using `poetry`, `poetry add -D mypy-typing-asserts`.\n\n## Usage\n\nTo use, just call `assert_type` providing a type-parameter and an argument. This will assert that\nthe type of the argument is __exactly__ the same type as the type-parameter (type-hierarchies are\nnot traversed) when typechecking (assuming you have enabled this functionality).\n\n```python\nfrom mypy_typing_asserts import assert_type\n\n...\n\nassert_type[MyType](my_expression)\n\n# `assert_type` also returns the argument (but does no runtime checking)\nvar = assert_type[int](my_function())\n```\n\nNote that you may need to hide your import and usage behind `if typing.TYPE_CHECKING` if the\nenvironment you're running the code in isn't the same that you typecheck in.\n\n```python\nfrom typing import TYPE_CHECKING\n\nif TYPE_CHECKING:\n    from mypy_typing_asserts import assert_type\n\n...\n\nif TYPE_CHECKING:\n    assert_type[MyType](my_expression)\n```\n\n### Pitfalls\n\nThis plugin only gets executed for code that is being typechecked. Dependening on your configuration,\nyopur typechecker might be skipping function bodies (e.g. `mypy` will skip unannotated function bodies\nby default unless `--check-untyped-defs` is enabled).\n\nIf you're putting the `assert_type` calls inside a `pytest` test, make sure to annotate the `-> None`\nreturn type to avoid this!\n\n### Enabling the `mypy` plugin\n\nIn your mypy config, add `mypy_typing_asserts.mypy_plugin` to your `plugins` declaration.\n\nSee [mypy's documentation](https://mypy.readthedocs.io/en/stable/extending_mypy.html#configuring-mypy-to-use-plugins)\n\n\n## Alternatives\n\nAll of the alternatives today ensure types are deduced correctly by running `mypy` in a subprocess,\nwhich isn't always feasible or ideal. These include:\n\n- [mypy-test](https://github.com/orsinium-labs/mypy-test) - standalone `mypy` wrapper\n- [pytest-mypy-plugins](https://github.com/typeddjango/pytest-mypy-plugins) - pytest plugin, test cases described in a YAML file.\n- [pytest-mypy-testing](https://github.com/davidfritzsche/pytest-mypy-testing) - pytest plugin, tests are described like pytest test cases (but they actually don't get run).\n",
    'author': 'Joshua Cannon',
    'author_email': 'joshdcannon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thejcannon/mypy-typing-asserts',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
