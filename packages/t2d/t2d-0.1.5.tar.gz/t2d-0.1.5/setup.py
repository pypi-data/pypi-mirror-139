# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['t2d']

package_data = \
{'': ['*']}

install_requires = \
['discord.py>=1.7.3,<2.0.0', 'loguru>=0.5.3,<0.6.0', 'typer>=0.4.0,<0.5.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 't2d',
    'version': '0.1.5',
    'description': 'Seamless integration between Typer and Discord.py for CLI Discord bots',
    'long_description': '# t2d\n\n`t2d` is a short for Typer-to-Discord. It implements a seamless integration between Typer and Discord.py for CLI Discord bots development.\n\n## Installing\n\nJust install the package using `pip install t2d`.\n\n## How to use it?\n\nAssume that you have a Typer app that looks something like this:\n\n```py\nimport typer\napp = typer.Typer()\n\n@app.command()\ndef hello(name: str):\n    typer.echo(f"Hello {name}!")\n\n@app.command()\ndef bye(name: str):\n    typer.echo(f"Bye {name}!")\n```\n\nAll you have to do is:\n\n```py\nimport t2d\nbot = t2d.T2D(app)\nbot.run(YOUR_DISCORD_BOT_TOKEN)\n```\n\nAnd that\'s it! Now you can use your Typer app in Discord! Default commands are:\n\n```\n!help    Shows default help message for the bot\n!t2d     Runs Typer CLI app using T2D\n!version Prints T2D version\n```\n\nUsing the example above, you can do the following:\n\n```\n!t2d hello Gabriel -> Shows "Hello Gabriel!"\n!t2d bye Gabriel   -> Shows "Bye Gabriel!"\n```\n\n## Extending T2D\n\nOne can also extend T2D as it normally would using the `discord.ext.commands.Bot` API.\n',
    'author': 'Gabriel Gazola Milan',
    'author_email': 'gabriel.gazola@poli.ufrj.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gabriel-milan/t2d',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
