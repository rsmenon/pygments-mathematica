# -*- coding: utf-8 -*-
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

from collections import defaultdict

from pygments.lexer import RegexLexer, include, words, bygroups
from pygments.token import Token as PToken

import mathematica.builtins as mma


class Regex:
    IDENTIFIER = r'[a-zA-Z\$][a-zA-Z0-9\$]*'
    NAMED_CHARACTER = r'\\[{identifier}]'.format(identifier=IDENTIFIER)
    SYMBOLS = (r'[`]?({identifier}|{named_character})(`({identifier}|{named_character}))*[`]?'
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
    LOCAL_SCOPE = PToken.Name.Variable.Class
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
            (r'\\', MToken.STRING),
            (r'"', MToken.STRING, '#pop'),
        ],
    }

    def get_tokens_unprocessed(self, text, stack=('root', )):
        ma = MathematicaAnnotations()
        annotations = (ma.builtins, ma.unicode, ma.lexical_scope)
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text):
            result = (index, token, value)
            for func in annotations:
                result = func(*result)

            yield result


class _State(dict):
    def __getattr__(self, attr):
        return self.get(attr)

    __setattr__ = dict.__setitem__


class MathematicaAnnotations:
    def __init__(self):
        self.scope = _State()
        self._reset_scope_state()

    @staticmethod
    def builtins(index, token, value):
        if token is MToken.SYMBOL and value in mma.SYSTEM_SYMBOLS:
            return index, MToken.BUILTIN, value
        else:
            return index, token, value

    @staticmethod
    def unicode(index, token, value):
        if token is MToken.UNKNOWN:
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
            return index, new_token, value
        else:
            return index, token, value

    def _reset_scope_state(self):
        # keyword = True denotes the presence of a trigger symbol such as Block, With, Module
        # When keyword is True and is followed by a [, then the parser enters an active state
        self.scope.keyword = False
        self.scope.active = False

        # level tracks the nestedness of local scopes (e.g. Block[{x = Block[{y = ...}, ...]}, ...])
        self.scope.level = 0

        # The next three variables are stacks that track opening and closing brackets, braces and
        # and other groupings (associations, angle brackets, etc.) at each level.
        # Braces are tracked only immediately after entering an active scope, which is where the
        # local variables are defined.
        self.scope.brackets = defaultdict(int)
        self.scope.braces = defaultdict(int)
        self.scope.other_groups = defaultdict(int)

        # stack_state is a tuple of the above three counters at each level when the parser is inside
        # a local variable definition region. i.e. when the parser is at { in Block[{x = 1}, x]
        self.scope.stack_state = defaultdict(int)

        # variables is the set of symbols/builtins that have been identified as being in a local
        # scope at each level. rhs is True when the parser is in the RHS of an assignment (= or :=)
        self.scope.variables = defaultdict(set)
        self.scope.rhs = defaultdict(bool)

    def _reset_scope_level(self, level):
        scope_vars = (self.scope.brackets, self.scope.braces, self.scope.other_groups,
                      self.scope.stack_state, self.scope.variables, self.scope.rhs)
        [var.pop(level) for var in scope_vars if level in var]

    def _get_stack_state(self, level):
        return (
            self.scope.brackets[level],
            self.scope.braces[level],
            self.scope.other_groups[level],
        )

    def lexical_scope(self, index, token, value):
        level = self.scope.level
        if token is MToken.WHITESPACE:
            return index, token, value

        if self.scope.active and token is MToken.GROUP and value in ('<|', u'〈', u'〚'):
            self.scope.other_groups[level] += 1
            return index, token, value
        elif self.scope.active and token is MToken.GROUP and value in ('|>', u'〛', u'〉'):
            self.scope.other_groups[level] -= 1
            return index, token, value

        if self.scope.active and token is MToken.GROUP and value == '}':
            if self.scope.braces[level]:
                self.scope.braces[level] -= 1

            if not self.scope.braces[level]:
                self.scope.rhs[level] = False

            return index, token, value

        if self.scope.active and token is MToken.GROUP and value == ']':
            if self.scope.brackets[level]:
                self.scope.brackets[level] -= 1
                if not self.scope.brackets[level] and level:
                    self._reset_scope_level(level)
                    self.scope.level -= 1

                if not self.scope.level:
                    self._reset_scope_state()

            return index, token, value

        if token is MToken.BUILTIN and value in ('Block', 'With', 'Module'):
            self.scope.keyword = True
            return index, token, value

        if token is MToken.GROUP and value == '[':
            # Enter an active state only if the preceding non-whitespace token is one of the scope
            # keyword symbols. If it is already in an active state, the counter is incremented.
            if self.scope.keyword:
                self.scope.active = True
                self.scope.level += 1
                self.scope.keyword = False

            if self.scope.active:
                self.scope.brackets[self.scope.level] += 1

            return index, token, value

        if self.scope.active and token is MToken.GROUP and value == '{':
            if level not in self.scope.variables:
                # The parser is not yet in the local variables section so initialize counters and
                # containers and take a snapshot of the stack state. The frozen stack state is used
                # later to identify the end of the RHS in an assignment expression.
                self.scope.variables[level] = set()
                self.scope.braces[level] += 1
                self.scope.stack_state[level] = self._get_stack_state(level)
            elif level in self.scope.variables and self.scope.braces[level]:
                # The parser is inside the local variables section.
                self.scope.braces[level] += 1
            else:
                # In all other cases don't modify the stack.
                pass

            return index, token, value

        if (self.scope.active and self.scope.braces[level] and
                token in (MToken.SYMBOL, MToken.BUILTIN)):
            # The parser is inside the local variables section and on a builtin or a generic symbol
            # token. If it isn't in the RHS of an assignment expression, then modify the token and
            # add the value to the list of local scope variables at this level.
            if not self.scope.rhs[level]:
                self.scope.variables[level].add(value)
                return index, MToken.LOCAL_SCOPE, value
            else:
                return index, token, value

        elif self.scope.active and self.scope.braces[level]:
            # If the parser is on an assignment operator, mark rhs = True so that symbols from the
            # RHS of the assignment are not considered as local variables. The rhs value is reset
            # when:
            #   1. the parser is on a , inside the local variables section and the stack state
            #      is the same as when it entered the section. For example, in
            #      Block[{x = 1, y = 2}, x + y], the stack state is the same at { and the first ,.
            #      But in Block[{x = {1, a}, y = 2}, x + y], the stack state is not the same at {
            #      and the first , so it is still part of the RHS.
            #   2. if it has exited the local variables section (handled earlier)
            if token is MToken.OPERATOR and value in ('=', ':='):
                self.scope.rhs[level] = True
            elif (token is MToken.GROUP and value == ',' and
                  self._get_stack_state(level) == self.scope.stack_state[level]):
                self.scope.rhs[level] = False

            return index, token, value

        elif self.scope.active and token in (MToken.SYMBOL, MToken.BUILTIN):
            # If the code has reached here, the parser is outside the local variables section and in
            # the body of the scoping function.
            if value in self.scope.variables[level]:
                return index, MToken.LOCAL_SCOPE, value
            else:
                return index, token, value

        self.scope.keyword = False
        return index, token, value
