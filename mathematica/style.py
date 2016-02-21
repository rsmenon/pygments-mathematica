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
        MToken.LOCAL_SCOPE: '#5d9066',
        MToken.MESSAGE: '#ab466a',
        MToken.NUMBER: '#b66a4b',
        MToken.OPERATOR: '#555555',
        MToken.PATTERN: 'italic #6E8413',
        MToken.SLOT: 'italic #6E8413',
        MToken.STRING: '#499A9F',
        MToken.SYMBOL: '#4b78b1',
        MToken.UNKNOWN: '#555555',
    }


class MathematicaNotebookStyle(Style):
    default_style = ''
    background_color = '#ffffff'
    styles = {
        MToken.BUILTIN: 'bold #000000',
        MToken.COMMENT: 'bold #999999',
        MToken.GROUP: 'bold #000000',
        MToken.LOCAL_SCOPE: 'bold #3C7D91',
        MToken.MESSAGE: 'bold #666666',
        MToken.NUMBER: 'bold #000000',
        MToken.OPERATOR: 'bold #000000',
        MToken.PATTERN: 'bold italic #438958',
        MToken.SLOT: 'bold italic #438958',
        MToken.STRING: 'bold #666666',
        MToken.SYMBOL: 'bold #002CC3',
        MToken.UNKNOWN: 'bold #000000',
    }
