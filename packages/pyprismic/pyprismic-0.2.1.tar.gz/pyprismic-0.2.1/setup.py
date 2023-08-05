# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyprismic']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pyprismic',
    'version': '0.2.1',
    'description': 'A simple Prismic client',
    'long_description': '# pyprismic: a simple python Prismic client\n\nThis is a very simple Prismic python client.\n\nIt uses the REST API from prismic.\n\nRight now it only supports public Prismic repositories.\n\n## Installing\n\n```\npip install pyprismic\n```\n\n## Using it\n\n```\nfrom pyprismic import Client, as_html\n\nc = Client("your-repo")\n\nres = c.query(predicate="""[[at(document.type, "faq")]]""")\n\ndocument = res[\'results][0]\n\nrich_text = document[\'data\'][\'rich_text_field\']\n\nhtml = as_html(rich_text)\n\n```\n\n## Querying Prismic\n\nFor querying prismic, you only need to follow the predicates system that they have in place.\n\nCheck the [official documentation](https://prismic.io/docs/technologies/query-predicates-reference-rest-api).\n\n**NOTE**: it is important to use the triple quote so you can properly use the " for the strings.\n',
    'author': 'Daniel Lombraña González',
    'author_email': 'daniel.lombrana@b4motion.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
