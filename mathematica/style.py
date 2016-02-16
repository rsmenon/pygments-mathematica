# -*- coding: utf-8 -*-
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

from pygments.style import Style

from mathematica.lexer import MToken


class MathematicaStyle(Style):
    default_style = ''
    background_color = '#fefefe'
    styles = {
        MToken.BUILTIN: '#353f42',
        MToken.COMMENT: 'italic #aaaaaa',
        MToken.GROUP: '#555555',
        MToken.MESSAGE: '#ab466a',
        MToken.NUMBER: '#b66a4b',
        MToken.OPERATOR: '#555555',
        MToken.PATTERN: 'italic #6E8413',
        MToken.SLOT: 'italic #6E8413',
        MToken.STRING: '#499A9F',
        MToken.SYMBOL: '#4b78b1',
        MToken.UNKNOWN: '#555555',
    }
