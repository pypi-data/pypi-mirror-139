# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dictencli']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.11.2,<3.0.0',
 'certifi>=2021.10.8,<2022.0.0',
 'charset-normalizer>=2.0.12,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'commonmark>=0.9.1,<0.10.0',
 'idna>=3.3,<4.0',
 'playsound>=1.2.2,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.2.0,<12.0.0',
 'typer>=0.4.0,<0.5.0',
 'urllib3>=1.26.8,<2.0.0']

entry_points = \
{'console_scripts': ['dictencli = dictencli.dictencli:dict_app']}

setup_kwargs = {
    'name': 'dictencli',
    'version': '0.1.2',
    'description': 'A simple commandline dictionary app.',
    'long_description': "# dictencli\n\n---\n\n*A command line dictionary, for those who spend their day in terminal. Get definitons, origin, example and many more information inside your terminal. You are just one command away* 😊 ...\n\n  \n\n### Features\n\nwith functionalities like:\n\n- word definition\n\n- example\n\n- origin\n\n- synonyms\n\n- antonyms\n\n- phrases\n\n- pronunciation\n\n  \n\n### Installation\n\n`pip install dictencli`\n\n  \n\n#### Usage\n\n`dictencli [commands] [optional flags] word(required with look command)`\n\n  \n\n##### **Commands:**\n\n1. look - used with optional flags below provided.\n\n`dictencli look word`\n\n2. help - will just show you the help options dicussed above\n\n`dictencli help`\n\n3. about\n\n`dictencli about`\n\n  \n\n##### **Optional flags:**\n\n- orgin: use either '-origin' or '-or'\n\n- example: use either '-example' or '-ex'\n\n- synonyms: use either 'synonyms' or '-syn'\n\n- antonyms: use either '-antonyms' or '-ant'\n\n- pronunciation: use either '-pronunciation' or '-pro'\n\n- phrases: use either '-phrases' or '-phr'\n\n  \n  \n\n### Note\n\n#### **Windows**\n\nIf pronunciation doesn't work:\n\n`pip uninstall playsound`\n\n`pip install playsound == 1.2.2`\n\n  \n\nunicode symbols might not be displayed correctly in cmd.\n\n  \n\n#### **Linux**\n\nIf pronunciation doesn't work:\n\n`sudo apt install libgirepository1.0-dev`\n\n`pip install pygobject`\n\n  \n\nNamespace Gst not available:\n\n`sudo apt install python3-gst-1.0`\n\n  \n\n*These are the known issues that I had encountered in 'pronunciation', if you face any other issue or wan't to get in contact, feel free to mail at 'nikhilomkar99@gmail.com'. Thanks* 🙌🏻.\n\n  \n\n---",
    'author': 'Nikhil',
    'author_email': 'nikhilomkar99@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
