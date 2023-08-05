PyAnsys Sphinx Theme
====================

Introduction and Purpose
------------------------
The PyAnsys Sphinx theme is an extension of the popular `PyData
Sphinx Theme <https://pydata-sphinx-theme.readthedocs.io/>`_ used by
`numpy <https://numpy.org/doc/stable/>`_, `pandas
<https://pandas.pydata.org/docs/>`_, `PyVista
<https://docs.pyvista.org>`_ and a variety other packages.  This theme
was packaged so that all PyAnsys packages would look and behave
consistently. 


Documentation
~~~~~~~~~~~~~
Full documentation can found at `PyAnsys Sphinx Theme Documentation <https://sphinxdocs.pyansys.com>`_. The webpage was
also built using the ``pyansys-sphinx-theme``, so visit the site for a
preview of the theme.

Other PyAnsys packages using the PyAnsys theme include:

- `PyMAPDL <https://mapdldocs.pyansys.com/>`__
- `PyAEDT <https://aedtdocs.pyansys.com/>`__
- `DPF-Core <https://dpfdocs.pyansys.com/>`__
- `DPF-Post <https://postdocs.pyansys.com/>`__
- `Legacy PyMAPDL Reader <https://readerdocs.pyansys.com/>`__


Getting Started
~~~~~~~~~~~~~~~
Install this theme with:

.. code::

   pip install pyansys-sphinx-theme

Next, modify your sphinx ``conf.py`` to use ``html_theme =
'pyansys_sphinx_theme'``.  If you are new to using
Sphinx, see `Sphinx Getting Started
<https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_
documentation.

For usage information, seee `Using this Theme
<https://sphinxdocs.pyansys.com/usage.html>`_


Development and Contributing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Feel free to add features or post issues. To develop this theme::

   git clone https://github.com/pyansys/pyansys-sphinx-theme.git
   pip install -r requirements_docs.txt
   make -C doc html

Or for Windows::

   cd doc
   ./make.bat

We use `pre-commit <https://pre-commit.com/>`_ to simplfy style checks. You can
optionally use this by following the `installation
<https://pre-commit.com/#install>`_ and `usage
<https://pre-commit.com/#usage>`_ guides.


License
~~~~~~~
This theme is licened under the `MIT License
<https://raw.githubusercontent.com/pyansys/pyansys-sphinx-theme/main/LICENSE>`_.
