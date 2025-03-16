# -*- coding: utf-8 -*-
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

from nose.tools import assert_equal
from pygments.token import Token

import mathematica.builtins as mma
from mathematica.lexer import MathematicaLexer, MToken


class TestMathematicaLexer:
    def setup(self):
        self.lexer = MathematicaLexer()

    def verify(self, code, expected):
        expected.append((Token.Text.Whitespace, '\n'))
        returned = list(self.lexer.get_tokens(code))
        assert_equal(expected, returned)

    def verify_all(self, code_list, expected_list):
        for code, expected in zip(code_list, expected_list):
            self.verify(code, expected)

    def test_comments(self):
        code = '(* a comment *)'
        expected = [
            (MToken.COMMENT, '(*'),
            (MToken.COMMENT, ' a comment '),
            (MToken.COMMENT, '*)')
        ]
        self.verify(code, expected)

    def test_comments_with_code(self):
        code = '(* Plot[Sin[x], {x, 0, 2 Pi}] *)'
        expected = [
            (MToken.COMMENT, '(*'),
            (MToken.COMMENT, ' Plot[Sin[x], {x, 0, 2 Pi}] '),
            (MToken.COMMENT, '*)')
        ]
        self.verify(code, expected)

    def test_nested_comments(self):
        code = '(* foo (* bar *) baz *)'
        expected = [
            (MToken.COMMENT, '(*'),
            (MToken.COMMENT, ' foo '),
            (MToken.COMMENT, '(*'),
            (MToken.COMMENT, ' bar '),
            (MToken.COMMENT, '*)'),
            (MToken.COMMENT, ' baz '),
            (MToken.COMMENT, '*)'),
        ]
        self.verify(code, expected)

    def test_multiline_comment(self):
        code = '(* a comment\non two lines *)'
        expected = [
            (MToken.COMMENT, '(*'),
            (MToken.COMMENT, ' a comment\non two lines '),
            (MToken.COMMENT, '*)'),
        ]
        self.verify(code, expected)

    def test_strings(self):
        code = [
            '"a string"',
            '"a string \\" with a quote"',
            '"a string with a newline\\n"',
            '"a string with \\ two backslashes"',
        ]
        expected = [
            [
                (MToken.STRING, '"'),
                (MToken.STRING, 'a string'),
                (MToken.STRING, '"'),
            ],
            [
                (MToken.STRING, '"'),
                (MToken.STRING, 'a string \\" with a quote'),
                (MToken.STRING, '"'),
            ],
            [
                (MToken.STRING, '"'),
                (MToken.STRING, 'a string with a newline\\n'),
                (MToken.STRING, '"'),
            ],
            [
                (MToken.STRING, '"'),
                (MToken.STRING, 'a string with \\ two backslashes'),
                (MToken.STRING, '"'),
            ]
        ]
        self.verify_all(code, expected)

    def test_integers(self):
        code = '123'
        expected = [(MToken.NUMBER, '123')]
        self.verify(code, expected)

    def test_floats(self):
        code = ['1.23', '10.1', '.123']
        expected = [[(MToken.NUMBER, num)] for num in code]
        self.verify_all(code, expected)

    def test_precision_numbers(self):
        code = ['1`', '1.2`', '1.23`30', '20`20']
        expected = [[(MToken.NUMBER, num)] for num in code]
        self.verify_all(code, expected)

    def test_base_numbers(self):
        code = ['2^^101', '8 ^^ 17', '10^^ 3.4']
        expected = [[(MToken.NUMBER, num)] for num in code]
        self.verify_all(code, expected)

    def test_scientific_number(self):
        code = ['1*^3', '2 *^23', '1.23*^4']
        expected = [[(MToken.NUMBER, num)] for num in code]
        self.verify_all(code, expected)

    def test_patterns(self):
        code = [
            '_Head', '__Head', '___Head',
            'x_Head', 'x__Head', 'x___Head',
            'Foo`Bar_Head', 'Foo`Bar__Integer', 'Foo`Bar___Baz',
            'Foo`Bar_Ctx`Baz', 'Foo`Bar__Ctx`Baz', 'Foo`Bar___Ctx`Baz`Qux',
        ]
        expected = [[(MToken.PATTERN, pat)] for pat in code]
        self.verify_all(code, expected)

    def test_slots(self):
        code = ['#', '#1', '#234']
        expected = [[(MToken.SLOT, st)] for st in code]
        self.verify_all(code, expected)

    def test_slot_sequences(self):
        code = ['##', '##2', '##23']
        expected = [[(MToken.SLOT, st)] for st in code]
        self.verify_all(code, expected)

    def test_association_slots(self):
        code = ['#foo', '#"foo"', '#foo`bar', '#Foo$1`Bar2$']
        expected = [[(MToken.SLOT, st)] for st in code]
        self.verify_all(code, expected)

    def test_operators(self):
        code = mma.OPERATORS
        expected = [[(MToken.OPERATOR, op)] for op in code]
        self.verify_all(code, expected)

    def test_messages(self):
        code = ['General::foo', 'Foo::bar', 'Foo`Bar::baz']
        expected = [
            [
                (MToken.BUILTIN, 'General'),
                (MToken.OPERATOR, '::'),
                (MToken.MESSAGE, 'foo')
            ],
            [
                (MToken.SYMBOL, 'Foo'),
                (MToken.OPERATOR, '::'),
                (MToken.MESSAGE, 'bar')
            ],
            [
                (MToken.SYMBOL, 'Foo`Bar'),
                (MToken.OPERATOR, '::'),
                (MToken.MESSAGE, 'baz')
            ],
        ]
        self.verify_all(code, expected)

    def test_symbols(self):
        code = ['foo', 'Foo', 'camelCase', 'Context`symbol', '`symbol', '$foo`bar', '$Bar`Baz`Qux']
        expected = [[(MToken.SYMBOL, sym)] for sym in code]
        self.verify_all(code, expected)

    def test_get(self):
        code = ['<<Foo`', '<<Foo`Bar`']
        expected = [
            [
                (MToken.OPERATOR, '<<'),
                (MToken.SYMBOL, 'Foo`'),
            ],
            [
                (MToken.OPERATOR, '<<'),
                (MToken.SYMBOL, 'Foo`Bar`'),
            ]
        ]
        self.verify_all(code, expected)

    def test_builtins(self):
        code = list(mma.SYSTEM_SYMBOLS)
        expected = [[(MToken.BUILTIN, sym)] for sym in code]
        self.verify_all(code, expected)

    def test_unicode_builtins(self):
        code = list(mma.UNICODE_SYSTEM_SYMBOLS)
        expected = [[(MToken.BUILTIN, sym)] for sym in code]
        self.verify_all(code, expected)

    def test_unicode_groupings(self):
        code = list(mma.UNICODE_GROUPINGS)
        expected = [[(MToken.GROUP, grp)] for grp in code]
        self.verify_all(code, expected)

    def test_unicode_operators(self):
        code = list(mma.UNICODE_OPERATORS)
        expected = [[(MToken.OPERATOR, op)] for op in code]
        self.verify_all(code, expected)

    def test_unicode_undefined(self):
        code = list(mma.UNICODE_SYSTEM_UNDEFINED_SYMBOLS)
        expected = [[(MToken.SYMBOL, sym)] for sym in code]
        self.verify_all(code, expected)

    def test_lexical_scope_simple(self):
        code = [
            'Block[{x = 1}, Sin[x]]',
            'Module[{y := Cos[x]}, x + y]',
            'With[{$foo = 1}, f[$foo]]'
        ]
        expected = [
            [
                (MToken.BUILTIN, 'Block'),
                (MToken.GROUP, '['),
                (MToken.GROUP, '{'),
                (MToken.LOCAL_SCOPE, 'x'),
                (MToken.WHITESPACE, ' '),
                (MToken.OPERATOR, '='),
                (MToken.WHITESPACE, ' '),
                (MToken.NUMBER, '1'),
                (MToken.GROUP, '}'),
                (MToken.GROUP, ','),
                (MToken.WHITESPACE, ' '),
                (MToken.BUILTIN, 'Sin'),
                (MToken.GROUP, '['),
                (MToken.LOCAL_SCOPE, 'x'),
                (MToken.GROUP, ']'),
                (MToken.GROUP, ']'),
            ],
            [
                (MToken.BUILTIN, 'Module'),
                (MToken.GROUP, '['),
                (MToken.GROUP, '{'),
                (MToken.LOCAL_SCOPE, 'y'),
                (MToken.WHITESPACE, ' '),
                (MToken.OPERATOR, ':='),
                (MToken.WHITESPACE, ' '),
                (MToken.BUILTIN, 'Cos'),
                (MToken.GROUP, '['),
                (MToken.SYMBOL, 'x'),
                (MToken.GROUP, ']'),
                (MToken.GROUP, '}'),
                (MToken.GROUP, ','),
                (MToken.WHITESPACE, ' '),
                (MToken.SYMBOL, 'x'),
                (MToken.WHITESPACE, ' '),
                (MToken.OPERATOR, '+'),
                (MToken.WHITESPACE, ' '),
                (MToken.LOCAL_SCOPE, 'y'),
                (MToken.GROUP, ']'),
            ],
            [
                (MToken.BUILTIN, 'With'),
                (MToken.GROUP, '['),
                (MToken.GROUP, '{'),
                (MToken.LOCAL_SCOPE, '$foo'),
                (MToken.WHITESPACE, ' '),
                (MToken.OPERATOR, '='),
                (MToken.WHITESPACE, ' '),
                (MToken.NUMBER, '1'),
                (MToken.GROUP, '}'),
                (MToken.GROUP, ','),
                (MToken.WHITESPACE, ' '),
                (MToken.SYMBOL, 'f'),
                (MToken.GROUP, '['),
                (MToken.LOCAL_SCOPE, '$foo'),
                (MToken.GROUP, ']'),
                (MToken.GROUP, ']'),
            ],
        ]
        self.verify_all(code, expected)

    def test_lexical_scope_nested(self):
        code = 'Block[{Plus = Times}, x + With[{y = 1}, 3 * y]]'
        expected = [
            (MToken.BUILTIN, 'Block'),
            (MToken.GROUP, '['),
            (MToken.GROUP, '{'),
            (MToken.LOCAL_SCOPE, 'Plus'),
            (MToken.WHITESPACE, ' '),
            (MToken.OPERATOR, '='),
            (MToken.WHITESPACE, ' '),
            (MToken.BUILTIN, 'Times'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, ','),
            (MToken.WHITESPACE, ' '),
            (MToken.SYMBOL, 'x'),
            (MToken.WHITESPACE, ' '),
            (MToken.OPERATOR, '+'),
            (MToken.WHITESPACE, ' '),
            (MToken.BUILTIN, 'With'),
            (MToken.GROUP, '['),
            (MToken.GROUP, '{'),
            (MToken.LOCAL_SCOPE, 'y'),
            (MToken.WHITESPACE, ' '),
            (MToken.OPERATOR, '='),
            (MToken.WHITESPACE, ' '),
            (MToken.NUMBER, '1'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, ','),
            (MToken.WHITESPACE, ' '),
            (MToken.NUMBER, '3'),
            (MToken.WHITESPACE, ' '),
            (MToken.OPERATOR, '*'),
            (MToken.WHITESPACE, ' '),
            (MToken.LOCAL_SCOPE, 'y'),
            (MToken.GROUP, ']'),
            (MToken.GROUP, ']'),
        ]
        self.verify(code, expected)

    def test_lexical_scope_nasty(self):
        code = 'Block[{x=Module[{y=<|a->1,b->2|>},y],z=With[{k={1,2}},k*3]}, x+y*Block[{k=3},f[k]]]'
        expected = [
            (MToken.BUILTIN, 'Block'),
            (MToken.GROUP, '['),
            (MToken.GROUP, '{'),
            (MToken.LOCAL_SCOPE, 'x'),
            (MToken.OPERATOR, '='),
            (MToken.BUILTIN, 'Module'),
            (MToken.GROUP, '['),
            (MToken.GROUP, '{'),
            (MToken.LOCAL_SCOPE, 'y'),
            (MToken.OPERATOR, '='),
            (MToken.GROUP, '<|'),
            (MToken.SYMBOL, 'a'),
            (MToken.OPERATOR, '->'),
            (MToken.NUMBER, '1'),
            (MToken.GROUP, ','),
            (MToken.SYMBOL, 'b'),
            (MToken.OPERATOR, '->'),
            (MToken.NUMBER, '2'),
            (MToken.GROUP, '|>'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, ','),
            (MToken.LOCAL_SCOPE, 'y'),
            (MToken.GROUP, ']'),
            (MToken.GROUP, ','),
            (MToken.LOCAL_SCOPE, 'z'),
            (MToken.OPERATOR, '='),
            (MToken.BUILTIN, 'With'),
            (MToken.GROUP, '['),
            (MToken.GROUP, '{'),
            (MToken.LOCAL_SCOPE, 'k'),
            (MToken.OPERATOR, '='),
            (MToken.GROUP, '{'),
            (MToken.NUMBER, '1'),
            (MToken.GROUP, ','),
            (MToken.NUMBER, '2'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, ','),
            (MToken.LOCAL_SCOPE, 'k'),
            (MToken.OPERATOR, '*'),
            (MToken.NUMBER, '3'),
            (MToken.GROUP, ']'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, ','),
            (MToken.WHITESPACE, ' '),
            (MToken.LOCAL_SCOPE, 'x'),
            (MToken.OPERATOR, '+'),
            (MToken.SYMBOL, 'y'),
            (MToken.OPERATOR, '*'),
            (MToken.BUILTIN, 'Block'),
            (MToken.GROUP, '['),
            (MToken.GROUP, '{'),
            (MToken.LOCAL_SCOPE, 'k'),
            (MToken.OPERATOR, '='),
            (MToken.NUMBER, '3'),
            (MToken.GROUP, '}'),
            (MToken.GROUP, ','),
            (MToken.SYMBOL, 'f'),
            (MToken.GROUP, '['),
            (MToken.LOCAL_SCOPE, 'k'),
            (MToken.GROUP, ']'),
            (MToken.GROUP, ']'),
            (MToken.GROUP, ']'),
        ]
        self.verify(code, expected)

    def test_string_closing_quote_on_newline(self):
        code = '"test string\n"abc'
        expected = [
            (MToken.STRING, '"'),
            (MToken.STRING, 'test string\n'),
            (MToken.STRING, '"'),
            (MToken.SYMBOL, 'abc'),
        ]
        self.verify(code, expected)

    def test_unicode_greek(self):
        code = [
            'varλ1a',
            'Δ',
            'f[Δx_List] := Δx',
            'a∂_',
        ]
        expected = [
            [(MToken.SYMBOL, 'varλ1a')],
            [(MToken.SYMBOL, 'Δ')],
            [
                (MToken.SYMBOL, 'f'),
                (MToken.GROUP, '['),
                (MToken.PATTERN, 'Δx_List'),
                (MToken.GROUP, ']'),
                (MToken.WHITESPACE, ' '),
                (MToken.OPERATOR, ':='),
                (MToken.WHITESPACE, ' '),
                (MToken.SYMBOL, 'Δx'),
            ],
            [(MToken.PATTERN, 'a∂_')],
        ]
        self.verify_all(code, expected)