# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
    ['roboworld']

install_requires = \
    ['matplotlib>=3.2.1,<4.0.0', 'rich>=3.3.1,<4.0.0']

package_data = \
    {'': ['*']}

keywords = ['education', 'cellular automaton', 'roboter', 'learning', 'beginners', 'computational thinking']

#long_description=long_description,
#long_description_content_type='text/x-rst',

long_description="""
``roboworld`` is an educational ``Python``-package designed for students to learn the basic programming concepts, such as,

+ variables,
+ function calls,
+ conditionals, 
+ loops and
+ recursion.

It consists of a ``World`` and the ``Agent``, a roboter that can be moved within the ``World``.
The ``World`` is a two-dimensional grid consisting of an ``Agent``, a spatial goal (a special gridpoint), movable and immovable objects.
The ``World`` can be seen as a cellular atomaton.
Students have to design algorithm that move the ``Agent`` to its goal.

However, the ``Agent`` only offers very basic methods, such as,

+ move one step forward, 
+ turn left by 90 degree, 
+ check if there is an obstacle in front.

Therefore, students have to prorgamm more sophisticated methods by themselves.
The learning goal is that they, step by step, build a set of function to navigate within different worlds.
And by doing so, they hopefully pick up the most important programming fundamentals.
"""

setup_kwargs = {
    'name': 'roboworld',
    'version': '0.1.1',
    'description': 'Educational roboter world for learning the basic programming concepts.',
    'long_description': long_description,
    'author': 'Benedikt Zoennchenpip',
    'author_email': 'benedikt.zoennchen@web.de',
    'maintainer': 'BZoennchen',
    'maintainer_email': 'benedikt.zoennchen@web.de',
    'url': 'https://github.com/BZoennchen/robo-world',
    'packages': packages,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
    'keywords': keywords
}

setup(**setup_kwargs)
