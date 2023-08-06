============
opytional
============


.. image:: https://img.shields.io/pypi/v/opytional.svg
        :target: https://pypi.python.org/pypi/opytional

.. image:: https://img.shields.io/travis/mmore500/opytional.svg
        :target: https://travis-ci.com/mmore500/opytional

.. image:: https://readthedocs.org/projects/opytional/badge/?version=latest
        :target: https://opytional.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




opytional makes working with values that might be None safer and easier


* Free software: MIT license
* Documentation: https://opytional.readthedocs.io.


Inspired by C++'s :code:`std::optional`.


.. code-block:: python3

  import opytional as opyt



  # opyt.or_value
  # provides a fallback value when value is None

  opyt.or_value(None, 'fallback') # returns 'fallback'

  opyt.or_value('value', 'fallback') # returns 'value'



  # opyt.or_else
  # provides a fallback callable when value is None

  opyt.or_else(None, lambda: 'fallback') # returns 'fallback'

  opyt.or_else('value', lambda: 'fallback') # returns 'value'



  # opyt.apply_if
  # applies an operator to value when value is not None

  opyt.apply_if(None, lambda x: x + ' world') # returns None

  opyt.apply_if('hello', lambda x: x + ' world') # returns 'hello world'



  # opyt.apply_if_or_value
  # applies an operator to value when value is not None
  # with a fallback value for when value is None

  opyt.apply_if_or_value(None, lambda x: x + ' world', 'fallback')
  # returns 'fallback'

  opyt.apply_if_or_value('hello', lambda x: x + ' world', 'fallback')
  # returns 'hello world'

  opyt.apply_if_or_value('hello', lambda x: None, 'fallback') # returns None



  # opyt.apply_if_or_else
  # applies an operator to value when value is not None
  # with a fallback callable for when value is None

  opyt.apply_if_or_else(None, lambda x: x + ' world', lambda: 'fallback')
  # returns 'fallback'

  opyt.apply_if_or_value('hello', lambda x: x + ' world', lambda: 'fallback')
  # returns 'hello world'

  opyt.apply_if_or_value('hello', lambda x: None, lambda: 'fallback')
  # returns None


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
