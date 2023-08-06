============
iterify
============


.. image:: https://img.shields.io/pypi/v/iterify.svg
        :target: https://pypi.python.org/pypi/iterify

.. image:: https://img.shields.io/travis/mmore500/iterify.svg
        :target: https://travis-ci.com/mmore500/iterify

.. image:: https://readthedocs.org/projects/iterify/badge/?version=latest
        :target: https://iterify.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




iterify streamlines making one-off iterators over one or a few values


* Free software: MIT license
* Documentation: https://iterify.readthedocs.io.


.. code-block:: python3

  import iterify as itfy



  # itfy.iterify
  [*itfy.iterify('a')] # -> ['a']

  [*itfy.iterify('a', 'b', 'c')] # -> ['a', 'b', 'c']


  # itfy.cyclify
  [*zip([1, 2, 3], itfy.cyclify('a', 'b'))] # -> [(1, 'a'), (2, 'b'), (3, 'a')]


  # itfy.samplify
  [*zip(
    [1, 2, 3],
    itfy.samplify('a', 'b')
  )]
  # -> [(1, 'a'), (2, 'a'), (3, 'b')]
  # or -> [(1, 'b'), (2, 'a'), (3, 'b')]
  # or -> [(1, 'b'), (2, 'b'), (3, 'b')]
  # etc.


  # itfy.shufflify
  [*itfy.shufflify('a', 'b')]
  # -> ['a', 'b']
  # or -> ['b', 'a']

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
