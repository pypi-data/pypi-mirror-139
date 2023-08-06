
***
ryd
***

.. image:: https://sourceforge.net/p/ryd/code/ci/default/tree/_doc/_static/license.svg?format=raw
   :target: https://opensource.org/licenses/MIT

.. image:: https://sourceforge.net/p/ryd/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
   :target: https://pypi.org/project/ryd/

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
   :target: https://pypi.org/project/oitnb/

.. image:: https://sourceforge.net/p/ryd/code/ci/default/tree/_doc/_static/ryd.svg?format=raw
   :target: https://pypi.org/project/ryd/


``ryd`` ( /rɑɪt/, pronounced like the verb "write" ) is a preprocessor for text
based documents, that builds upon the multi-document capabilities of YAML
files/streams.

The use of multi-document in ``ryd`` allows for clear separation between
document text and any programs referenced in those text. Thereby making it
possible to run (c.q. compile) the program parts of a document, e.g. to check
whether they are syntactically correct. It can also capture the *actual* output
of those programs to be included in the document.

This allows for easier maintenance of (correct) program sources, in document
source texts like reStructuredText, LaTeX, etc.

Example
=======

A "normal" ``.ryd`` file consists of multiple YAML 1.2 documents in one file.

The first of these documents has, at the root-level, a mapping. This
mapping is the **ryd configuration data** for this stream of
documents, and is used to define ``ryd`` document version used, output
and other configuration informationis. The first document doesn't
normally have any directives, that the document is YAML 1.2 is
implicit, so no ``%YAML 1.2`` directive is needed and without
directive and no preceding document, you should not have a
directives-end marker line (``---``)

The documents following the first document are usually block
style literal scalars with an optional tag. The tag influences how the scalar
string is processed within the selected output system::

  version: 0.1
  output: rst
  fix_inline_single_backquotes: true
  --- |
  Example Python program
  ++++++++++++++++++++++

  This is an example of a python program
  --- !python |
  n = 7
  print(n**2 - n)
  --- !stdout |
  The answer is::

this will generate (using: ``ryd convert test.ryd``) the following ``test.rst``::

  Example Python program
  ++++++++++++++++++++++

  This is an example of a Python program
  ::

    n = 7
    print(n**2 - n)

  The answer is::

    42

which can then be converted to PDF using ``rst2pdf`` or HTML using ``rst2html``.

Command-line options
++++++++++++++++++++

The command-line of ``ryd`` consists of multiple components::

   ryd [--global-option] command [--options] [arguments]

Although not indicated most global options can occur after the command as well.

commands
^^^^^^^^

::

    convert             generate output as per first YAML document
    clean               clean output files for .ryd files
    roundtrip           roundtrip .ryd file, updating sections
    from-rst (fromrst)  convert .rst to .ryd

You'll most often use ``convert`` it takes one or more filenames as argument
and generates output as specified in the ryd configuration data. Some options allow you to override settings there (e.g. ``--pdf`` and ``-no-pdf``)

The command ``from-rst`` converts a ``.rst`` file into ``.ryd`` doing some section underline checking and adding the ryd configuration data document.

The ``roundtrip`` command has an option ``--oitnb`` running in place
code-formatting on the ``!Python)-pre)`` sections of the ``.ryd`` file. You need to
have `oitnb <https://pypi.org/project/oitnb/>`__ in your path for this.

Doing ``ryd command --help`` might indicate extra options that have not yet made it into
the documentation.

Documents and document tags
+++++++++++++++++++++++++++

Each YAML document is separated from other documents in the stream by the
document start marker ``---``. Apart from the first document, most documents
contain a single, multi-line, non-indented, scalar. The document start marker is
therefor followed by the pipe (``|``) symbol, which is the YAML indication for a
multi-line scalar.

That scalar can be "typed" in the normal way of YAML by inserting a
tag before the ``|``. E.g. a document that is a type of Python program
has a tag ``!python``.

What a document tag exactly does, depends on the tag, but, potentially, also, on
the output file format selected, on previously processed tagged documents, other
``.ryd`` files processed previously and the environment.
The following are short descriptions for all tags, independent of the selected
output format:


!code
  Include program in text. Do not mark as executable, doesn't influence    ``!stdout``.

!comment
  The whole document will be discarded, i.e. not included in the output.

!inc
  Include the content of the listed files (indented), without other processing,     into the output. Preceed with ``::`` if necessary.

!incraw
  Include the listed files raw (i.e. without processing, or indenting) into the output.

!last-compile
  Include output from last compilation as code.

!nim
  Include Nim program in text. Prefix and mark as executable.

!nim-pre
  Prefix all following ``!nim`` documents with this document (e.g. used for imports)

!python
  Include Python program in text. Prefix and mark as executable.

!python-hidden
  Do  not include Python program in text. Prefix and mark as executable.

!python-pre
  Prefix all following ``!python`` documents with this document (e.g. used for imports)

!stdout
  Include output from last executable document (e.g. ``!python``) as code.

!stdout-raw
  Include output from the last program, as source for the output format.

!unpy
  Include Nim program in text. Do not mark as executable. Set output to result of unpy.

RST
===

The output to ``.rst`` expects non-code YAML documents to be valid
reStructuredText. Any non-tagged documents, i.e. those starting with::

  --- |

are assumed to be text input.

Section underlining
+++++++++++++++++++

Because of the special meaning of ``---`` (and ``...``) at the beginning of a line,
followed by newline or space, the section under/over-line characters used in
``.ryd`` files that are source for ``.rst`` should not use ``-`` or ``.``
sequences if a any of those section names consist of three letters (e.g. a section
named API or RST). It is recommended to use the following scheme::

   Sections, subsections, etc. in .ryd files
    # with over-line, for parts
    * with over-line, for chapters
    =, for sections
    +, for subsections
    ^, for sub-subsections
    ", for paragraphs

Single backquotes
+++++++++++++++++

The ``fix_inline_single_backquotes: true`` tells ``ryd`` to indicate lines that have
single backquotes, that need fixing (by replacing them with double backquotes)::

  README.ryd
  47: this will generate (`ryd convert test.ryd`) the following
                        --^
                                             --^

(If you are used to other inline code markup editing e.g. on Stack Overflow, that uses single
backquotes, you'll come to appreciate this.)

Python
++++++

Python code is indicated by::

  --- !python |

The document is inserted into the ``.rst`` with a two space indent. If
the previous block does not end in ``::`` this double colon, and a
newline, are explicitly inserted before the program. The difference
being that a text block ending in ``::`` will have a single ``:`` rendered, a
``::`` on a line of its own will not. An empty line between the
preceding text and the code is inserted when needed.

If your program relies on specific packages, those packages, need to
be available in the environment in which ``ryd`` is started (which can e.g. be a
specifically set up ``virtualenv``)


It is possible to have "partial programs" by preceding a python document with
e.g.::

  --- !python-pre |
  from __future__ import print_function
  import sys
  import ruamel.yaml
  from ruamel.std.pathlib import Path, pushd, popd, PathLibConversionHelper
  pl = PathLibConversionHelper()

Such a block is pre-pended to all following ``--- !python |`` documents (until
superseded by another ``--- !python-pre |`` block)


Captured output
+++++++++++++++

The output from the last program that was run (``--- !python |``) is stored and
can be post-pended to a reStructuredText document by tagging it with ``!stdout``
(i.e. ``--- !stdout |``)

non-running code
++++++++++++++++

A document tagged ``!code`` will be represented as one tagged ``!python``, but
the code will not be run (and hence the output used for ``!stdout`` not changed).

Nim
+++

Nim code is indicated by::

  --- !nim |

The document is inserted as with Python, there can be a ``!nim-pre`` document,
and output is captured and displayed with ``--- !stdout |``)::

  let a = 123
  let x = 0b0010_1010
  echo(fmt"The answer to the question: {x}")

which outputs::

  The answer to the question: 42


Make sure you append ``::`` at the end of your text, this is currently not
automatically inserted.

The compilation is done with options ``--verbosity:0 --hint[Processing]:off`` .

compiler output
^^^^^^^^^^^^^^^

If you are interested in the textual output of the compiler you can use
``--- !last-compile |``

For which the text should also end with ``::`` ::

  /tmp/ryd-of-anthon/ryd-29/tmp_1.nim(4, 5) Hint: 'a' is declared but not used [XDeclaredButNotUsed]


Comments
========

Block style literal scalars do not allow YAML comments. To insert comments in a
text, either use the format acceptable by the output, e.g. when generating ``.rst`` use::

   ..
      this will show up in the resulting .rst file, but will
      not render

..
  this will show up in the resulting .rst file, but will
  not render

Alternatively you can create a comment YAML document (``--- !comment |``), for
which the text will not be represented in the output file format **at all**.


History
=======

``ryd`` grew out of a in-house solution where sections of reStructuredText files were
updated, in-place, by running Python programs specified in separate files. Also
allowing the inclusion of the (error) output.

An example of this can be seen in `this
<https://bitbucket.org/ruamel/yaml/raw/0be7d3cb8449b15d9ac9b097322f09e52b92f868/_doc/example.rst>`_
old version of the ``example.rst`` file of the ``ruamel.yaml`` package::

  Basic round trip of parsing YAML to Python objects, modifying
  and generating YAML::

    import sys
    from ruamel.yaml import YAML

    inp = """\
    # example
    name:
      # details
      family: Smith   # very common
      given: Alice    # one of the siblings
    """

    yaml = YAML()
    code = yaml.load(inp)
    code['name']['given'] = 'Bob'

    yaml.dump(code, sys.stdout)

  .. example code small.py

  Resulting in ::

    # example
    name:
      # details
      family: Smith   # very common
      given: Bob      # one of the siblings


  .. example output small.py


The program was inserted before the ``.. example code`` line and its output before
``.. example output``, replacing all the text starting after the previous ``::``

The ``small.py`` referenced a separate file for this piece of code.
This resulted in multiple source files that were associated with a single
``.rst`` file. There was no mechanism to have partial programs that could be
tested by execution, which precluded getting output from such program as well.

Although the code could have been edited in place, and used to get the
output, this would force one to use the extra indentation required for
lines following reST's ``::``.

Once this system came under review, the solution with a structured YAML header, as used
with various file formats, combined with multiple document consisting of
(tagged) top level, non-indented, block style literal scalars, was chosen instead.
