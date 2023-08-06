# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faker_food']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=12.0.0,<13.0.0']

setup_kwargs = {
    'name': 'faker-food',
    'version': '0.1.0',
    'description': 'Food related provider for the Python Faker library',
    'long_description': '# faker_food: food provider for Faker\n\nAn add-on provider for the Python Faker module to generate random and/or fake data for food-related categories.\n\n## Description\n\n`faker_food` provides food-related fake data for testing purposes.\n\n## Usage\nAdd as a provider to your Faker instance:\n``` python\n>>> from faker import Faker\n>>> from faker_food import FoodProvider\n>>> fake = Faker()\n>>> fake.add_provider(FoodProvider)\n```\nNow you can start to generate data:\n```python\n>>> fake.dish()\n>>> fake.dish_description()\n>>> fake.ethnic_category()\n>>> fake.fruit()\n>>> fake.ingredient()\n>>> fake.measurement()\n>>> fake.metric_measurement()\n>>> fake.measurement_size()\n>>> fake.spice()\n>>> fake.sushi()\n>>> fake.vegetable()\n```\n## Data Sources\n\nData for this project was sourced from many different areas. Special thanks to the following sources:\n* [faker-ruby/faker](https://github.com/faker-ruby/faker) ([food.yml](https://github.com/faker-ruby/faker/blob/master/lib/locales/en/food.yml))\n* [Elixirs/faker](https://github.com/elixirs/faker/) ([food/en.ex](https://github.com/elixirs/faker/blob/master/lib/faker/food/en.ex))',
    'author': 'Mark Adams',
    'author_email': 'madams74@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
