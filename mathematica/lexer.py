# -*- coding: utf-8 -*-
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Token as PToken

import mathematica.builtins as mma


class Regex:
    IDENTIFIER = r'[a-zA-Z\$][a-zA-Z0-9\$]*'
    NAMED_CHARACTER = r'\\[{identifier}]'.format(identifier=IDENTIFIER)
    SYMBOLS = (r'[`]?({identifier}|{named_character})(`({identifier}|{named_character}))*'
               .format(identifier=IDENTIFIER, named_character=NAMED_CHARACTER))
    INTEGER = r'[0-9]+'
    FLOAT = r'({integer})?\.[0-9]+|{integer}\.'.format(integer=INTEGER)
    REAL = r'({integer}|{float})`({integer}|{float})?|{float}'.format(integer=INTEGER, float=FLOAT)
    BASE_NUMBER = r'{integer}\s*\^\^\s*({real}|{integer})'.format(integer=INTEGER, real=REAL)
    SCIENTIFIC_NUMBER = r'({real}|{integer})\s*\*\^\s*{integer}'.format(real=REAL, integer=INTEGER)
    PATTERNS = r'{symbol}\_{{1,3}}({symbol})?|({symbol})?\_{{1,3}}{symbol}'.format(symbol=SYMBOLS)
    SLOTS = r'#{symbol}|#\"{symbol}\"|#{{1,2}}[0-9]*'.format(symbol=SYMBOLS)
    MESSAGES = r'(::)(\s*)({symbol})'.format(symbol=SYMBOLS)
    GROUPINGS = words(mma.GROUPINGS).get()
    OPERATORS = words(mma.OPERATORS).get()


class MToken:
    BUILTIN = PToken.Name.Builtin
    COMMENT = PToken.Comment
    GROUP = PToken.Punctuation
    MESSAGE = PToken.Name.Exception
    NUMBER = PToken.Number
    OPERATOR = PToken.Operator
    PATTERN = PToken.Name.Tag
    SLOT = PToken.Name.Function
    STRING = PToken.String
    SYMBOL = PToken.Name.Variable
    UNKNOWN = PToken.Error
    WHITESPACE = PToken.Text.Whitespace


class MathematicaLexer(RegexLexer):
    name = 'Mathematica'
    aliases = ['mathematica', 'mma', 'nb', 'wl', 'wolfram', 'wolfram-language']
    filenames = ['*.cdf', '*.m', '*.ma', '*.nb', '*.wl']
    mimetypes = [
        'application/mathematica',
        'application/vnd.wolfram.mathematica',
        'application/vnd.wolfram.mathematica.package',
        'application/vnd.wolfram.cdf',
        'application/vnd.wolfram.cdf.text',
    ]
    tokens = {
        'root': [
            (r'\(\*', MToken.COMMENT, 'comments'),
            (r'"', MToken.STRING, 'strings'),
            include('numbers'),
            (Regex.PATTERNS, MToken.PATTERN),
            (Regex.SLOTS, MToken.SLOT),
            (Regex.GROUPINGS, MToken.GROUP),
            (Regex.MESSAGES, bygroups(MToken.OPERATOR, MToken.WHITESPACE, MToken.MESSAGE)),
            (Regex.OPERATORS, MToken.OPERATOR),
            (Regex.SYMBOLS, MToken.SYMBOL),
            (r'\s+', MToken.WHITESPACE),
        ],
        'comments': [
            (r'[^\*\(\)]+', MToken.COMMENT),
            (r'\*[^\)]', MToken.COMMENT),
            (r'\(\*', MToken.COMMENT, '#push'),
            (r'\*\)', MToken.COMMENT, '#pop'),
            (r'\([^\*]?|[^\*]?\)', MToken.COMMENT),
        ],
        'numbers': [
            (Regex.BASE_NUMBER, MToken.NUMBER),
            (Regex.SCIENTIFIC_NUMBER, MToken.NUMBER),
            (Regex.REAL, MToken.NUMBER),
            (Regex.INTEGER, MToken.NUMBER),
        ],
        'strings': [
            (r'[^"\\]+', MToken.STRING),
            (r'^[\\"]', MToken.STRING),
            (r'(\\n|\\r)', MToken.STRING),
            (r'\\"', MToken.STRING),
            (r'"', MToken.STRING, '#pop'),
        ],
    }

    def get_tokens_unprocessed(self, text, stack=('root', )):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            if token is MToken.SYMBOL and value in mma.SYSTEM_SYMBOLS:
                # Annotate builtin symbols from System`
                yield index, MToken.BUILTIN, value
            elif token is MToken.UNKNOWN:
                # Annotate recognized unicode symbols
                if value in mma.UNICODE_SYSTEM_SYMBOLS:
                    new_token = MToken.BUILTIN
                elif value in mma.UNICODE_GROUPINGS:
                    new_token = MToken.GROUP
                elif value in mma.UNICODE_OPERATORS:
                    new_token = MToken.OPERATOR
                elif value in mma.UNICODE_SYSTEM_UNDEFINED_SYMBOLS:
                    new_token = MToken.SYMBOL
                else:
                    new_token = MToken.UNKNOWN
                yield index, new_token, value
            else:
                yield index, token, value
