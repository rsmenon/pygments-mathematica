# Mathematica lexer and highlighter for Pygments

The most up-to-date lexer and highlighter for [_Mathematica_](http://wolfram.com/mathematica)/Wolfram Language
 source code using the [pygments](http://pygments.org) engine.

![](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![](https://img.shields.io/badge/version-0.1.0-yellow.svg?style=flat-square)
![](https://img.shields.io/travis/rsmenon/pygments-mathematica/master.svg?style=flat-square)
![](https://img.shields.io/badge/python-2.7%7C3.3%2B-lightgrey.svg?style=flat-square)
## Features

It can currently lex and highlight:

  - All builtin functions in the ``System` `` context except those that use characters from the private
  unicode space (e.g. `\[FormalA]`)
  - User defined symbols, including those in a context.
  - Comments, including multi line and nested.
  - Strings, including multi line and escaped quotes.
  - Patterns, slots (including named slots `#name` introduced in version 10) and slot sequences.
  - Message names (e.g. the `ivar` in `General::ivar`)
  - Numbers including base notation (e.g. `8 ^^ 23 == 19`) and scientific notation (e.g. `1 *^ 3 == 1000`).

### Example:
```
(* An example highlighting the features of
   this Pygments plugin for Mathematica *)
lissajous::usage = "An example Lissajous curve.\n" <>
                   "Definition: f(t) = (sin(3t + π/2), sin(t))"
lissajous = {Sin[2^^11 # + 0.005`10 * 1*^2 * Pi], Sin[#]} &;

ParametricPlot[lissajous[t], {t, 0, 2 Pi}] /. x_Line :> {Dashed, x}
```
<img width="700" src="https://cloud.githubusercontent.com/assets/2389211/13039847/6b3a44f2-d359-11e5-877c-72477a550913.png">

## Installation

After you've [installed Pygments](http://pygments.org/download/) (`pip install Pygments` works well
if you already have python setup on your system), download this repository and from within the repo's
root directory, run

```bash
python setup.py install
```

That's it!

## Usage

### Server-side highlighting in Jekyll, Octopress and other static websites

To highlight _Mathematica_ code using this lexer, enclose the code between these liquid tags:

```
{% highlight wl %}
<your code here>
{% endhighlight %}
```

You can also use `wolfram` and `wolfram-language` as the language hint. (See the note in the next section.)

If you are using Jekyll, depending on your setup, you might need to add the following in your `_plugins/ext.rb`:

```ruby
require 'pygments'
Pygments.start('<path to your python env>/site-packages/pygments/')
```

### Command line usage

The `pygmentize` command can be used to invoke this lexer and convert any _Mathematica_ file to an appropriately
highlighted file in a different format. For example, to convert a file `package.m` to a HTML file, run

```bash
pygmentize -O full,style=mathematica -f html -l wl -o package.html package.m
```

> **NOTE:** Although this lexer is registered with the names `mathematica` and `mma` for use as language hints, the
default lexer that ships with Pygments overrides this. Hence until this is incorporated into the main Pygments repository
please use `wl` or `wolfram` or `wolfram-language` as the language hint.

### Styles

The default styles that come with Pygments do not go well with _Mathematica_ code. If you're using this lexer
for highlighting source code on a website, use the `mma.scss` [Sass](http://sass-lang.com) file in this repository to obtain good default colors (as shown in the
screenshot). You can, if you choose, modify the colors in the SCSS file and then convert it to CSS
using the `scss` compiler as:

```
scss mma.scss > mma.css
```

For other applications including command line usage, the lexer ships with a style named `mathematica`.
(See the arguments to the `pygmentize` command in the section above.) To use different colors, modify
the style in `mathematica/style.py` and run `python setup.py install` again.

## Limitations

It cannot highlight lexically and dynamically scoped variables (e.g. the `x` in `With[{x = 1}, x + 1]` or
the `Plus` in `Block[{Plus = Times}, 2 + 3]`, etc.) consistently throughout their scope. This would require a
parser that further processes the stream of tokens and builds an AST that captures the semantics of the language.

This is currently not a high priority since it is non-trivial to implement it within the framework
by Pygments, but I am interested in supporting this eventually, so collaborations/pull requests are welcome :)

## Acknowledgments

The lexing rules for _Mathematica_ syntax are largely based on two prior projects:

 - My [vim-mathematica](https://github.com/rsmenon/vim-mathematica) syntax highlighting plugin.
 - Patrick Scheibe's [Mathematica plugin for IntelliJ IDEA](https://github.com/halirutan/Mathematica-IntelliJ-Plugin) (if you develop in _Mathematica_ and
 haven't seen this yet, please do try it out. It's wonderful!).

