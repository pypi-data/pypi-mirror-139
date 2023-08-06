# coding: utf-8

from typing import Dict, Any

_package_data: Dict[str, Any] = dict(
    full_package_name='ryd',
    version_info=(0, 5, 1),
    __version__='0.5.1',
    version_timestamp='2022-02-19 10:30:11',
    author='Anthon van der Neut',
    author_email='a.van.der.neut@ruamel.eu',
    description='Ruamel Yaml Doc preprocessor',
    keywords='restructuredtext markup preprocessing',
    entry_points='ryd=ryd.__main__:main',
    # entry_points=None,
    license='MIT',
    since=2017,
    # status="α|β|stable",  # the package status on PyPI
    # data_files="",
    universal=True,
    install_requires=[
        'ruamel.std.pathlib',
        'ruamel.yaml',
    ],
    tox=dict(
        env='3',
    ),
    oitnb=dict(
        multi_line_unwrap=True,
    ),
    print_allowed=True,
    python_requires='>=3',
)  # NOQA


version_info = _package_data['version_info']
__version__ = _package_data['__version__']

_cligen_data = """\
# all tags start with an uppercase char and can often be shortened to three and/or one
# characters. If a tag has multiple uppercase letter, only using the uppercase letters is a
# valid shortening
# Tags used:
# !Commandlineinterface, !Cli,
# !Option, !Opt, !O
# !PreSubparserOption, !PSO
# !Help, !H
# !Argument, !Arg
# !Module   # make subparser function calls imported from module
# !Instance # module.Class: assume subparser method calls on instance of Class imported from module
# !Action # either one of the actions in subdir _action (by stem of the file) or e.g. "store_action"
# !NQS used on arguments, makes sure the scalar is non-quoted e.g for instance/method/function
#      call arguments, when cligen knows about what argument a keyword takes, this is not needed
!Cli 0:
- formatter_class: !NQS argparse.RawTextHelpFormatter
- !Epilog |
    Sections, subsections, etc. in .ryd files
      # with over-line, for parts
      * with over-line, for chapters
      =, for sections
      +, for subsections
      ^, for subsubsections
      ", for paragraphs
- !Opt [verbose, v, !Help increase verbosity level, !Action count, const: 1, nargs: 0, default: 0]
- !Opt [force, !Help 'force action, even on normally skipped files', !Action count, const: 1, nargs: 0, default: 0]
- !Instance ryd.ryd.RYD
- convert:
  - !DefaultSubparser
  - !Opt [pdf, !Action store_true, default: null]
  - !Opt [no-pdf, !Action store_false, dest: pdf]
  - !Opt [stdout, !Action store_true, default: null]
  - !Opt [keep, !Action store_true, default: null, !Help preserve partial .rst on execution error]
  - !Arg [file, nargs: +, !Help files to process]
  - !Help generate output as per first YAML document
- clean:
  - !Arg [file, nargs: +, !Help files to process]
  - !Help clean output files for .ryd files
- roundtrip:
  - !Opt [oitnb, !Action store_true, !Help apply oitnb to !Python(-pre) documents]
  - !Arg [file, nargs: +, !Help files to process]
  - !Help roundtrip .ryd file, updating sections
- from-rst:
  - !Help convert .rst to .ryd
"""  # NOQA
