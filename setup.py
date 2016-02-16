# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

from setuptools import setup

setup(
    name='Mathematica Pygments Lexer',
    version='0.2.0',
    description='Mathematica/Wolfram Language Lexer for Pygments',
    author='rsmenon',
    author_email='rsmenon@icloud.com',
    license='MIT',
    packages=['mathematica'],
    entry_points="""[pygments.lexers]
MathematicaLexer = mathematica:MathematicaLexer

[pygments.styles]
mathematica = mathematica:MathematicaStyle
"""
)
