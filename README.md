# Mathematica lexer and highlighter for Pygments

The most up-to-date lexer and highlighter for [_Mathematica_](http://wolfram.com/mathematica)/Wolfram Language
 source code using the [pygments](http://pygments.org) engine.

![](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![](https://img.shields.io/badge/version-0.3.4-yellow.svg?style=flat-square)
![](https://img.shields.io/travis/rsmenon/pygments-mathematica/master.svg?style=flat-square)
![](https://img.shields.io/badge/python-2.7%7C3.3%2B-lightgrey.svg?style=flat-square)
![](https://img.shields.io/pypi/v/pygments-mathematica.svg?style=flat-square)
## Features

It can currently lex and highlight:

  - All builtin functions in the ``System` `` context including unicode symbols like `π` except those
  that use characters from the private unicode space (e.g. `\[FormalA]`).
  - User defined symbols, including those in a context.
  - All operators including unicode operators like `∈` and `⊕`.
  - Comments, including multi line and nested.
  - Strings, including multi line and escaped quotes.
  - Patterns, slots (including named slots `#name` introduced in version 10) and slot sequences.
  - Message names (e.g. the `ivar` in `General::ivar`)
  - Numbers including base notation (e.g. `8 ^^ 23 == 19`) and scientific notation (e.g. `1 *^ 3 == 1000`).
  - Local variables in `Block`, `With` and `Module`.

### Example:
```
(* An example highlighting the features of
   this Pygments plugin for Mathematica *)
lissajous::usage = "An example Lissajous curve.\n" <>
                   "Definition: f(t) = (sin(3t + π/2), sin(t))"
lissajous = {Sin[2^^11 # + 0.005`10 * 1*^2 * Pi], Sin[#]} &;

With[{max = 2 Pi, min = 0},
    ParametricPlot[lissajous[t], {t, min, max}] /. x_Line :> {Dashed, x}
]
```
<img width="700" src="https://cloud.githubusercontent.com/assets/2389211/13201234/e974332e-d81c-11e5-986d-a8afbc4d8fff.png">

## Installation

### Using `pip`

Run `pip install pygments-mathematica` from the command line. That's it!

### From source code

If you'd like to make modifications to the color scheme for personal use or if you'd like to try the
most recent release that might not yet be available in PyPi, download and unzip the source code
from the [latest release](https://github.com/rsmenon/pygments-mathematica/releases/latest). After
you've [installed Pygments](http://pygments.org/download/) (`pip install Pygments` works well
if you already have python setup on your system), run the following from the repo's root directory:

```bash
python setup.py install
```

## Usage

### Server-side syntax highlighting in Jekyll, Octopress and other static websites

To highlight _Mathematica_ code using this lexer, enclose the code between these liquid tags:

```
{% highlight wl %}
<your code here>
{% endhighlight %}
```

You can also use `wolfram` and `wolfram-language` as the language hint. (See the note at the end of the section.)

If you are using Jekyll, depending on your setup, you might need to add the following in your `_plugins/ext.rb`:

```ruby
require 'pygments'
Pygments.start('<path to your python env>/site-packages/pygments/')
```

> **NOTE:** Although this lexer is registered with the names `mathematica` and `mma` for use as language hints, the
default lexer that ships with Pygments overrides this. Hence until this is incorporated into the main Pygments repository
please use `wl` or `wolfram` or `wolfram-language` as the language hint.

### Highlighting in LaTeX documents

_Mathematica_ code can be highlighted in LaTeX documents using the [minted](http://mirrors.rit.edu/CTAN/macros/latex/contrib/minted/minted.pdf) (PDF) package.
The following minimal example shows how:

```latex
\documentclass{article}
\usepackage[english]{babel}
\usepackage{fontspec}
\setmonofont{Menlo}

\usepackage{minted}
\usemintedstyle{mathematica}

\begin{document}
\begin{minted}[linenos=true]{wolfram}
(* An example highlighting the features of
   this Pygments plugin for Mathematica *)
lissajous::usage = "An example Lissajous curve.\n" <>
                   "Definition: f(t) = (sin(3t + Pi/2), sin(t))"
lissajous = {Sin[2^^11 # + 0.005`10 * 1*^2 * π], Sin[#]} &;

ParametricPlot[lissajous[t], {t, 0, 2 π}] /. x_Line :> {Dashed, x}
\end{minted}
\end{document}
```

Saving the above as `mma.tex` and running `xelatex --shell-escape mma.tex` should produce a PDF with highlighted code.

> *NOTE:* If your LaTeX colors don't show up properly, try deleting your `*.aux`, `*.log` files and any `_minted-mma/` directory before running XeLaTeX again.

### Pelican static page generator

The [Pelican static generator](http://blog.getpelican.com/) is written in Python and uses Pygments by default. To use it there, you mark code blocks with the usual 4 spaces indent and you prepend it with `:::wl` if you are using Markdown

```
    :::wl
    FileNames["CodeGenerator.m", {$InstallationDirectory}, 4]
    (*
      {"/Applications/Development/Mathematica.app/SystemFiles/Links/GPUTools/CodeGenerator.m"}
    *)
```

If you are using ReStructuredText, please mark your *Mathematica* code with

```
.. code-block:: wl

   <indented code block goes here>
```

### Command line usage

The `pygmentize` command can be used to invoke this lexer and convert any _Mathematica_ file to an appropriately
highlighted file in a different format. For example, to convert a file `package.m` to a HTML file, run

```bash
pygmentize -O full,style=mathematica -f html -l wl -o package.html package.m
```

## Styles

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

If you fancy the default style that ships with the _Mathematica_ notebook, use the `mathematica-notebook` scheme.

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

