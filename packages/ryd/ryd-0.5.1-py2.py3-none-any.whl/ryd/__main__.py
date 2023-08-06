# coding: utf-8
# flake8: noqa
# cligen: 0.2.0, dd: 2022-02-17


import argparse
import importlib
import sys
import typing

from . import __version__


class DefaultVal(str):
    def __init__(self, val: typing.Any):
        self.val = val

    def __str__(self) -> str:
        return str(self.val)


class CountAction(argparse.Action):
    """argparse action for counting up and down

    standard argparse action='count', only increments with +1, this action uses
    the value of self.const if provided, and +1 if not provided

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action=CountAction, const=1,
            nargs=0)
    parser.add_argument('--quiet', '-q', action=CountAction, dest='verbose',
            const=-1, nargs=0)
    """

    def __call__(
        self,
        parser: typing.Any,
        namespace: argparse.Namespace,
        values: typing.Union[str, typing.Sequence[str], None],
        option_string: typing.Optional[str] = None,
    ) -> None:
        if self.const is None:
            self.const = 1
        try:
            val = getattr(namespace, self.dest) + self.const
        except TypeError:  # probably None
            val = self.const
        setattr(namespace, self.dest, val)


def main(cmdarg: typing.Optional[list[str]]=None) -> int:
    cmdarg = sys.argv if cmdarg is None else cmdarg
    parsers = []
    parsers.append(argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog='Sections, subsections, etc. in .ryd files\n  # with over-line, for parts\n  * with over-line, for chapters\n  =, for sections\n  +, for subsections\n  ^, for subsubsections\n  ", for paragraphs\n'))
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), dest='_gl_verbose', metavar='VERBOSE', nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(0), dest='_gl_force', metavar='FORCE', nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    parsers[-1].add_argument('--version', action='store_true', help='show program\'s version number and exit')
    subp = parsers[-1].add_subparsers()
    px = subp.add_parser('convert', help='generate output as per first YAML document')
    px.set_defaults(subparser_func='convert')
    parsers.append(px)
    parsers[-1].add_argument('--pdf', action='store_true')
    parsers[-1].add_argument('--no-pdf', action='store_false', dest='pdf')
    parsers[-1].add_argument('--stdout', action='store_true')
    parsers[-1].add_argument('--keep', action='store_true', help='preserve partial .rst on execution error')
    parsers[-1].add_argument('file', nargs='+', help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(0), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('clean', help='clean output files for .ryd files')
    px.set_defaults(subparser_func='clean')
    parsers.append(px)
    parsers[-1].add_argument('file', nargs='+', help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(0), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('roundtrip', help='roundtrip .ryd file, updating sections')
    px.set_defaults(subparser_func='roundtrip')
    parsers.append(px)
    parsers[-1].add_argument('--oitnb', action='store_true', help='apply oitnb to !Python(-pre) documents')
    parsers[-1].add_argument('file', nargs='+', help='files to process')
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(0), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    px = subp.add_parser('from-rst', help='convert .rst to .ryd')
    px.set_defaults(subparser_func='from-rst')
    parsers.append(px)
    parsers[-1].add_argument('--verbose', '-v', default=DefaultVal(0), nargs=0, help='increase verbosity level', action=CountAction, const=1)
    parsers[-1].add_argument('--force', default=DefaultVal(0), nargs=0, help='force action, even on normally skipped files', action=CountAction, const=1)
    parsers.pop()
    # sp: convert
    _subparser_found = False
    for arg in cmdarg[1:]:
        if arg in ['-h', '--help', '--version']:  # global help if no subparser
            break
    else:
        for sp_name in ['convert', 'clean', 'roundtrip', 'from-rst']:
            if sp_name in cmdarg[1:]:
                break
        else:
            # insert default in first position, this implies no
            # global options without a sub_parsers specified
            cmdarg.insert(1, 'convert')
    if '--version' in cmdarg[1:]:
        if '-v' in cmdarg[1:] or '--verbose' in cmdarg[1:]:
            return list_versions(pkg_name='ryd', version=None, pkgs=['ruamel.std.pathlib', 'ruamel.yaml'])
        print(__version__)
        return 0
    if '--help-all' in cmdarg[1:]:
        try:
            parsers[0].parse_args(['--help'])
        except SystemExit:
            pass
        for sc in parsers[1:]:
            print('-' * 72)
            try:
                parsers[0].parse_args([sc.prog.split()[1], '--help'])
            except SystemExit:
                pass
        sys.exit(0)
    args = parsers[0].parse_args(args=cmdarg[1:])
    for gl in ['verbose', 'force']:
        glv = getattr(args, '_gl_' + gl, None)
        if isinstance(getattr(args, gl, None), (DefaultVal, type(None))) and glv is not None:
            setattr(args, gl, glv)
        delattr(args, '_gl_' + gl)
        if isinstance(getattr(args, gl), DefaultVal):
            setattr(args, gl, getattr(args, gl).val)
    cls = getattr(importlib.import_module('ryd.ryd'), 'RYD')
    obj = cls(args)
    funcname = getattr(args, 'subparser_func', None)
    if funcname is None:
        parsers[0].parse_args('--help')
    fun = getattr(obj, args.subparser_func)
    ret_val = fun()
    if ret_val is None:
        return 0
    if isinstance(ret_val, int):
        return ret_val
    return -1

def list_versions(pkg_name: str, version: typing.Union[str, None], pkgs: typing.Sequence[str]) -> int:
    version_data = [
        ('Python', '{v.major}.{v.minor}.{v.micro}'.format(v=sys.version_info)),
        (pkg_name, __version__ if version is None else version),
    ]
    for pkg in pkgs:
        try:
            version_data.append(
                (pkg,  getattr(importlib.import_module(pkg), '__version__', '--'))
            )
        except ModuleNotFoundError:
            version_data.append((pkg, 'NA'))
        except KeyError:
            pass
    longest = max([len(x[0]) for x in version_data]) + 1
    for pkg, ver in version_data:
        print('{:{}s} {}'.format(pkg + ':', longest, ver))
    return 0


if __name__ == '__main__':
    sys.exit(main())
