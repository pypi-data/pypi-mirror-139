# robo-world

## Installation

``sudo python setup.py install``

## Purpose

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
