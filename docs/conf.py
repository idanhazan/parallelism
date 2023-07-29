import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import parallelism

project = 'parallelism'
author = 'Idan Hazan'
copyright = f'2023, {author}'
html_theme = 'sphinx_rtd_theme'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.napoleon',
    # 'sphinx_autodoc_typehints',
]
napoleon_numpy_docstring = True
# autodoc_typehints = 'description'
