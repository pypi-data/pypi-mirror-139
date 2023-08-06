# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['get_passphrase', 'get_passphrase.resolvers']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=23.5.0,<24.0.0', 'sentinel>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['get-passphrase = get_passphrase.__main__:run']}

setup_kwargs = {
    'name': 'get-passphrase',
    'version': '1.0.0',
    'description': 'Extensible passphrase resolver, supporting prompting as well as passphrases stored in environment variables, files or keychains',
    'long_description': '# get-passphrase\n\nExtensible passphrase resolver, supporting prompting as well as passphrases stored in environment variables, files or keyrings\n\nSome examples of smart passphrase descriptors:\n\n- `pass:<passphrase>`  to directly provide a passphrase inline\n- `env:<env-var-name>` to get the passphrase from an environment variable. The application may configure a custom environment dictionary, or `os.osenviron()` is used\n- `file:<file-name>` to get the passphrase from the file at location pathname. The application may configure a base directory for relative paths, or the current working directory is used.\n- `fd:<file-descriptor-number>` read the passphrase from the provided file descriptor number\n- `stdin:` to read from standard input\n- `prompt:` to prompt the user with "Password: " and read from console with typed characters hidden (uses [getpass](https://docs.python.org/3/library/getpass.html))\n- `prompt:<prompt-string>` to prompt the user with a custom prompt string and read from console with typed characters hidden (uses [getpass](https://docs.python.org/3/library/getpass.html))\n- `keyring:<service-name>,<key-name>` to load the passphrase from [keyring](https://pypi.org/project/keyring/). The application may configure a prefix that will be prepended to either the service-name or the key-name or both, to define a unique namespace for the application.\n- `keyring:<key-name>` to load the passphrase from [keyring](https://pypi.org/project/keyring/), using a default service name configured by the application. The application may configure a prefix that will be prepended to key-name, to define a unique namespace for the application.\n- `none:`  To provide a `None` value for the passphrase (useful for chaining defaults)\n- `empty:`  To provide an empty passphrase\n\n## Command tool\nA command tool, `get-passphrase`, is provided that will expand a smart passphrase descriptor provided as an argument.\n\n### Usage:\n```\nusage: get-passphrase [-h] [--version] [passphrase [passphrase ...]]\n\nResolve a passphrase in a number of ways.\n\npositional arguments:\n  passphrase  A list of smart passphrase descriptors to be checked in order. The first one that produces a passphrase is used.\n\noptional arguments:\n  -h, --help  show this help message and exit\n  --version   Display version\n```\n\n## Library\n\n### Usage\n\n```python\nfrom get_passphrase import resolve_passphrase\n\ndescriptor = input("Enter smart passphrase descriptor:")\n\nprint("Passphrase is: ", resolve_passphrase(descriptor).get_cleartext())\n```\n',
    'author': 'Sam McKelvie',
    'author_email': 'dev@mckelvie.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sammck/get-passphrase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
