# -*- coding: utf-8 -*-
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

u"""This is the most up-to-date lexer and highlighter for Mathematica/Wolfram Language source code \
using the pygments engine.

It currently supports:

 - All builtin functions in the ``System`` context including unicode symbols like ``π`` except \
 those that use characters from the private unicode space (e.g. ``\[FormalA]``).
 - User defined symbols, including those in a context.
 - All operators including unicode operators like ``∈`` and ``⊕``.
 - Comments, including multi line and nested.
 - Strings, including multi line and escaped quotes.
 - Patterns, slots (including named slots ``#name`` introduced in version 10) and slot sequences.
 - Message names (e.g. the ivar in ``General::ivar``)
 - Numbers including base notation (e.g. ``8 ^^ 23 == 19``) and scientific notation \
 (e.g. ``1 *^ 3 == 1000``).
 - Local variables in ``Block``, ``With`` and ``Module``.

A Sass file containing the styles can be obtained from the package repository for use in static \
website generators such as Jekyll, Octopress, Pelican, etc.

© 2016 rsmenon
"""

from setuptools import setup

setup(
    name='pygments-mathematica',
    version='0.3.4',
    description='Mathematica/Wolfram Language Lexer for Pygments',
    long_description=__doc__,
    author='rsmenon',
    author_email='rsmenon@icloud.com',
    license='MIT',
    keywords='syntax highlighting mathematica',
    url='http://github.com/rsmenon/pygments-mathematica/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing',
        'Topic :: Utilities',
    ],
    packages=['mathematica'],
    install_requires=['Pygments >= 2'],
    include_package_data=False,
    platforms=['any'],
    entry_points={
        'pygments.lexers': [
            'MathematicaLexer = mathematica:MathematicaLexer'
        ],
        'pygments.styles': [
            'mathematica = mathematica:MathematicaStyle',
            'mathematicanotebook = mathematica:MathematicaNotebookStyle'
        ],
    },
    zip_safe=False
)
