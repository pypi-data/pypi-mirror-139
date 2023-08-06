# coding: utf-8

import glob
import os
import sys
import inspect
import subprocess
import argparse
import datetime
from textwrap import dedent
from ruamel.std.pathlib import Path
from ruamel.std.pathlib.tempdir import TempDir
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

from typing import Optional, Any, Union, Dict, Set, List, TextIO

from .stdout import StdOut

Bugs = """\
- check empty documents. E.g. !python that only has code in !pre, and !stdout
  without any introductory text
"""

ToDo = """\
- some mechanism to show the name, leave option for 'skipping'/'converting'
  comment and push out newline later. Test incombination with verbosity
- specify Python interpreter, or create virtualenv + package installs, in a better
  way than using RYD_PYTHON env var.
- formalize temporary directory
- store (prefixed) program, only execute when !stdout is requested.
- parse messages like:
  README.rst:72: (ERROR/3) Inconsistent literal block quoting.
  and show output context
- zoom in on errors that have no line number: `some name <>`__
- document handling of :: in RST, and need for |+ in stdraw
- describe yaml comments after `|+ # `
- support code-block directive  http://rst2pdf.ralsina.me/handbook.html#syntax-highlighting
- list structure of the .ryd file
- process documents using xyz:prog  matching the document tag xyz by rt piping through prog
- why do toplevel LiteralScalarString dumps have |2, it is not even correct!
= consider moving to plugin system
"""


class RydExecError(Exception):
    pass


class RYD(object):
    def __init__(self, args: argparse.Namespace, config: Optional[Any] = None) -> None:
        self._args = args
        self._config = config
        self._name_printed = False
        self._current_path: Union[Path, None] = None

    def convert(self) -> None:
        for file_name in self._args.file:
            self._name_printed = False
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    self.convert_one(Path(exp_file_name), verbose=self._args.verbose)
                continue
            self.convert_one(Path(file_name), verbose=self._args.verbose)

    def clean(self) -> None:
        for file_name in self._todo():
            self.convert_one(file_name, clean=True)

    def _todo(self) -> list[Path]:
        todo = []
        for file_name in self._args.file:
            self._name_printed = False
            if file_name[0] == '*':
                for exp_file_name in sorted(Path('.').glob(file_name)):
                    todo.append(exp_file_name)
                    continue
            if '*' in file_name or '?' in file_name:
                for exp_file_name in sorted(glob.glob(file_name)):
                    todo.append(Path(exp_file_name))
                continue
            todo.append(Path(file_name))
        # print('todo', todo)
        return todo

    def name(self) -> None:
        """print name of file only once (either verbose or on error)"""
        if self._name_printed:
            return
        self._name_printed = True
        print(self._current_path)

    def convert_one(self, path: Path, clean: bool = False, verbose: int = 0) -> None:
        from .stackoverflow import StackOverflowConvertor
        from .markdown import MarkdownConvertor

        if self._current_path is None and not path.exists():
            print('unknown command, or file:', path)
            sys.exit(1)
        self._current_path = path
        if verbose > 0:
            self.name()
        yaml = YAML()
        convertor: Optional[Convertor] = None
        for x in yaml.load_all(path):
            if convertor is None:
                assert 0.099 < float(x['version']) < 0.201
                if x['output'] == 'rst':
                    convertor = RSTConvertor(self, yaml, x, path)
                elif x['output'] == 'md':
                    convertor = MarkdownConvertor(self, yaml, x, path)
                elif x['output'] == 'so':
                    convertor = StackOverflowConvertor(self, yaml, x, path)
                else:
                    raise NotImplementedError
                continue
            if clean:
                convertor.clean()
                return
            if not convertor(x):  # already up-to-date
                sys.stdout.flush()
                # ToDo you cannot return here, the PDF might not be generated because
                # of some rst2pdf issue
                return
        assert convertor is not None
        if convertor.updated:
            if verbose > 0:
                print('updated')
        convertor.write()
        # convertor.dump()
        sys.stdout.flush()

    def from_rst(self) -> None:
        for file_name in (Path(f) for f in self._args.file):
            ryd_name = file_name.with_suffix('.ryd')
            if ryd_name.exists() and not self._args.force:
                print('skipping', ryd_name)
                continue
            print('writing', ryd_name)
            rst = reStructuredText(file_name)
            rst.analyse_sections()
            with ryd_name.open('w') as fp:
                fp.write(
                    dedent("""\
                ---
                version: 0.1
                output: rst
                fix_inline_single_backquotes: true
                # pdf: true
                --- |
                """)
                )
                fp.write(rst.update_sections())

    def roundtrip(self) -> None:
        for file_name in self._todo():
            self.round_trip_one(file_name)

    def round_trip_one(self, path: Path) -> None:
        self._current_path = path
        if self._args.verbose > 0:
            self.name()
        yaml = YAML()
        convertor = None
        for x in yaml.load_all(path):
            if convertor is None:
                convertor = RoundTripConvertor(self, yaml, x, path)
                continue
            convertor(x)
        assert convertor is not None
        if convertor.updated:
            convertor.write()


class reStructuredText(object):
    def __init__(self, path: Path) -> None:
        self._path = path
        self._lines: Union[List[str], None] = None
        self._blank = set([-1])  # in case you have a divider on the first line
        self._section_lines: Dict[int, str] = {}
        self._divider_lines: Set[Any] = set()
        self._double_section = ""  # above and below
        self._double_section_lines: Dict[Any, Any] = {}
        self._single_section = ""  # only below
        self._single_section_lines: Dict[Any, Any] = {}

    @property
    def lines(self) -> list[str]:
        if self._lines is None:
            self._lines = self._path.read_text().splitlines()
        assert isinstance(self._lines, list)
        return self._lines

    def analyse_sections(self) -> None:
        non_alpha = '\'"#*=-^+'
        non_alpha = '=-`:\'"~^_*+#<>.'

        def char_repeats(line: str) -> bool:
            """assume a stripped line, check if the first character is repeated"""
            idx = len(line)
            while idx > 1:
                idx -= 1
                if line[idx] != line[0]:
                    return False
            return True

        # for x in ['===', '==', '=', 'x=']:
        #    print(x, char_repeats(x))
        current_level = 0  # NOQA
        previous_blank = False  # NOQA
        for line_number, line in enumerate(self.lines):
            s_line = line.strip()
            if not s_line:
                self._blank.add(line_number)
                previous_blank = True
                continue  # empty line
            fc = line[0]  # first character
            if fc not in non_alpha or not char_repeats(s_line):
                previous_blank = False  # NOQA
                continue
            self._section_lines[line_number] = s_line
        # print(self._blank)
        for line_number in self._section_lines:
            if (line_number - 1) in self._blank and (line_number + 1) in self._blank:
                self._divider_lines.add(line_number)
        for line_number in self._divider_lines:
            del self._section_lines[line_number]
        # cleaned up, now analyse
        line_numbers = sorted(self._section_lines.keys())
        idx = -1
        single_level = 0
        while idx < len(line_numbers) - 1:
            idx += 1
            line_number = line_numbers[idx]
            line = self._section_lines[line_number]
            # print(line_number, self._section_lines[line_number])
            if line_number + 2 in self._section_lines:
                if line[0] == self._section_lines[line_number + 2][0]:
                    pass
                    # print('double', line_number)
                else:
                    print('non-matching over-under-line', line_number)
                    sys.exit(1)
                idx += 1  # skip the matching underline
                if not self._double_section and self._single_section:
                    print("don't know how to handle over-under-line after under-line")
                    sys.exit(1)
                if line[0] not in self._double_section:
                    self._double_section += line[0]
                self._double_section_lines.setdefault(line[0], []).extend(
                    [line_number, line_number + 2]
                )
                single_level = 0
                continue
            if line[0] not in self._single_section:
                if single_level != len(self._single_section):
                    print('unexpected underline level', line_number, single_level)
                    sys.exit(1)
                self._single_section += line[0]
                single_level += 1
            else:
                single_level = self._single_section.index(line[0]) + 1
            self._single_section_lines.setdefault(line[0], []).append(line_number)

        print('double:', self._double_section)
        print('       ', self._double_section_lines)
        print('single:', self._single_section)
        print('       ', self._single_section_lines)

    def update_sections(self) -> str:
        # almost the Python recomendation, but not using '-' for sections
        double = '#*'
        single = '=+^"'
        assert len(double) >= len(self._double_section)
        assert len(single) >= len(self._single_section)
        for level, ch in enumerate(self._double_section):
            new_ch = double[level]
            for line_number in self._double_section_lines[ch]:
                self.lines[line_number] = new_ch * len(self.lines[line_number])
        for level, ch in enumerate(self._single_section):
            new_ch = single[level]
            for line_number in self._single_section_lines[ch]:
                self.lines[line_number] = new_ch * len(self.lines[line_number])
        return '\n'.join(self.lines)


##############################################################################


class RydDoc(LiteralScalarString):

    needs_double_colon = True

    @classmethod
    def from_yaml(cls, constructor: Any, node: Any) -> Any:
        return cls(node.value)

    @classmethod
    def to_yaml(cls, representer: Any, node: Any) -> Any:
        return representer.represent_literal_scalarstring(cls.yaml_tag, node.value)  # type: ignore # NOQA


# class BashRaw(RydDoc):
#     """Invoke bash on the document as script.
#     """
#     yaml_tag = '!bash-raw'


class Code(RydDoc):
    """Include program in text. Do not mark as executable, doesn't influence \
   ``!stdout``.
    """

    yaml_tag = '!code'


class Comment(RydDoc):
    """The whole document will be discarded, i.e. not included in the output.

    This allows commenting out complete sections in an output independent way.
    """

    yaml_tag = '!comment'


class Inc(RydDoc):
    """Include the content of the listed files (indented), without other processing, \
    into the output. Preceed with ``::`` if necessary.

    If a file name doesn't start with ``/``, it is considered to be relative to the
    directory of the output path.
    """

    yaml_tag = '!inc'


class IncRaw(RydDoc):
    """Include the listed files raw (i.e. without processing, or indenting) into the output.

    If a file name doesn't start with ``/``, it is considered to be relative to the
    directory of the output path.
    """

    yaml_tag = '!incraw'


class LastCompile(RydDoc):
    """Include output from last compilation as code.

    """

    yaml_tag = '!last-compile'


class Python(RydDoc):
    """Include Python program in text. Prefix and mark as executable.
    """

    yaml_tag = '!python'


class PythonHidden(RydDoc):
    '''Do  not include Python program in text. Prefix and mark as executable.

    This can be used to write files to the output directory, using:
    import pathlib; pathlib.Path("file_name").writetext("""contents of file""")
    '''

    yaml_tag = '!python-hidden'


class PythonPre(RydDoc):
    """Prefix all following ``!python`` documents with this document (e.g. used for imports)

    This part will not be be shown. The content should be a python snippet, that
    will be used as prefix for following programs which can be incomplete.
    This is useful for  suppressing repetetive import statements.
    """

    yaml_tag = '!python-pre'


class Stdout(RydDoc):
    """Include output from last executable document (e.g. ``!python``) as code.

    """

    yaml_tag = '!stdout'


class StdoutRaw(RydDoc):
    """
    Include output from the last program, as source for the output format.

    This can be used to e.g. have a program generate an definition list programmatically.
    """

    yaml_tag = '!stdout-raw'


class RydProgram(RydDoc):
    needs_double_colon = True

    def dump(self, fp: TextIO, convertor: 'Convertor') -> None:
        """generic include of code with indentation unless empty"""
        for line in self.strip().splitlines():
            if line.strip():
                print('  ', line, sep="", file=fp)
            else:
                print('', line, sep="", file=fp)
        print(file=fp)
        # convertor.last_code = True
        # not using nim prefix when unpy-ing
        self.last_output = self.check_output(convertor)

    def check_output(self, convertor: 'Convertor') -> Union[str, None]:
        raise NotImplementedError


#########
# Nim
#########
class Nim(RydProgram):
    """Include Nim program in text. Prefix and mark as executable.
    """

    yaml_tag = '!nim'

    def check_output(self, convertor: 'Convertor') -> Union[str, None]:
        # None is replaced by the filename
        cmd = ['nim', 'compile', '--verbosity:0', '--hint[Processing]:off', None]
        convertor.last_compile = convertor.check_output(
            convertor.nim_pre + self,  # type: ignore
            exe=cmd,
            ext='.nim',
        )
        # print('convertor.last_compile', convertor.last_compile)
        exe = convertor.last_source.with_suffix("")
        if exe.exists():
            return subprocess.check_output([exe]).decode('utf-8')
        return convertor.last_compile


class NimPre(RydDoc):
    """Prefix all following ``!nim`` documents with this document (e.g. used for imports)

    This part will not be be shown. The content should be a nim snippet, that
    will be used as prefix for following programs which can be incomplete.
    This is useful for  suppressing repetetive import statements.
    """

    yaml_tag = '!nim-pre'

    def dump(self, fp: Any, convertor: 'Convertor') -> None:
        convertor.nim_pre = self  # type: ignore


class UnPy(RydProgram):
    """Include Nim program in text. Do not mark as executable. Set output to result of unpy.
    """

    yaml_tag = '!unpy'

    def check_output(self, convertor: 'Convertor') -> Union[str, None]:
        # None is replaced by the filename
        return convertor.check_output(
            self, exe=['unpy', 'update', '--output:-', None], ext='.nim'
        )


##############################################################################


class Convertor(object):
    def __init__(self, ryd: RYD) -> None:
        self._ryd = ryd
        self._tempdir: Optional[TempDir] = None
        self._tmpfile_nr = 0
        self._tag_obj: Dict[str, Any] = {}
        self._tag_doc = self.gather_tag_documentation()
        self.last_compile: Any = None
        self._path: Path
        self.updated = False
        self._out_path: Union[Path, StdOut]

    def gather_tag_documentation(self) -> Dict[str, List[Any]]:
        tag_doc = {}
        for _name, obj in inspect.getmembers(sys.modules[__name__]):
            if (
                inspect.isclass(obj)
                and obj is not RydDoc
                and issubclass(obj, RydDoc)
                and hasattr(obj, 'yaml_tag')
            ):
                self._tag_obj[obj.yaml_tag] = obj  # type: ignore
                d = obj.__doc__ if obj.__doc__ is not None else 'N/A\n  N/A'
                d1, d2 = d.lstrip().split('\n', 1)
                d1 = d1.strip()
                d2 = dedent(d2).lstrip()
                tag_doc[obj.yaml_tag] = [d1, d2]  # type: ignore
        # for k in sorted(self.tags):
        #     print(k, '->', self.tags[k])
        return tag_doc

    @property
    def tempdir(self) -> TempDir:
        if self._tempdir is None:
            self._tempdir = TempDir(prefix='ryd', keep=3)
        return self._tempdir

    def get_tags(self) -> Dict[str, List[Any]]:
        return self._tag_doc

    def update(self, s: Any) -> Any:
        return s

    def clean(self) -> None:
        assert self._path.exists()
        if self._out_path.exists():
            self._out_path.unlink()

    python_exe = os.environ.get('RYD_PYTHON', sys.executable)
    # print('python_exe', python_exe, sys.executable)

    def check_output(
        self, s: str, exe: Optional[list[Any]] = None, ext: Optional[str] = None
    ) -> Union[str, None]:
        if exe is None:
            exe = [self.python_exe, None]
            ext = '.py'
        if ext is None:
            raise NotImplementedError
        p = self.tempdir.directory / 'tmp_{}{}'.format(self._tmpfile_nr, ext)
        self.last_source = p
        self._tmpfile_nr += 1
        p.write_text(s)
        try:
            return subprocess.check_output(
                [x if x is not None else str(p) for x in exe], stderr=subprocess.STDOUT
            ).decode('utf-8')
        except subprocess.CalledProcessError as e:  # NOQA
            res = e.output.decode('utf-8')
            sys.stdout.write(res)
            if 'ImportError: No module named ryd.ryd' in res:
                print(
                    '\nWhen generating ryd documentation use:\n'
                    '  RYD_PYTHON=/opt/util/ryd/bin/python ryd ...'
                )
            return None

    def __call__(self, s: Any) -> bool:
        raise NotImplementedError

    def write(self) -> None:
        raise NotImplementedError


class RSTConvertor(Convertor):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd)
        self._yaml = yaml
        for v in self._tag_obj.values():
            yaml.register_class(v)
        self._md = md
        self._path = path
        self._out_path = self._path.with_suffix('.rst')
        self.data: List[Any] = []
        ####
        self.last_output: Union[str, None] = ""
        self.updated = False
        self.python_pre = ""
        # register all defined classes and store tag + comment

    def __call__(self, s: Any) -> bool:
        # the read is at the end
        if (
            not self._ryd._args.force
            and self._out_path.exists()
            and self._path.stat().st_mtime < self._out_path.stat().st_mtime  # type: ignore
        ):
            if self._ryd._args.verbose > 0:
                print('skipping', end=' ')
                self._ryd.name()
            return False
        try:
            self._line = self._yaml.reader.line - s.count('\n') + 1
        except AttributeError:
            print('error getting s.count', s)
            raise
        sx = self.update(s)
        if sx:
            self.updated = True
            self.data.append(sx)
        else:
            self.data.append(s)
        return True

    def update(self, s: Any) -> bool:
        # if isinstance(s, RydDoc) and not isinstance(s, Python):
        #     print(type(s))
        if isinstance(s, Python):
            return False
        # find all backquotes in document
        bqs = []
        # character index in file to beginning of each line
        lines: List[Union[int, None]] = [0]
        line = 0
        col = 0
        for idx, ch in enumerate(s):
            if ch == '`':
                bqs.append((idx, line, col))
            elif ch == '\n':
                lines.append(idx + 1)
                line += 1
                col = 0
                continue
            col += 1
        lines.append(None)  # for last line
        bqidx = 0
        last_line_displayed = -1
        while bqidx < len(bqs):
            lnr = bqs[bqidx][1]
            # ``pair of double backquotes`` -> code
            try:
                assert isinstance(lines[lnr], int)
                tlnr: int = lines[lnr]  # type: ignore
                if s[tlnr] == ' ' and s[tlnr + 1] == ' ':
                    # first characters on line are spaces -> code/ryd example
                    bqidx += 1
                    continue
            except IndexError:
                print('error')
                pass
            if (
                bqidx + 3 <= len(bqs)
                and bqs[bqidx][0] + 1 == bqs[bqidx + 1][0]
                and bqs[bqidx + 2][0] + 1 == bqs[bqidx + 3][0]
            ):
                bqidx += 4
                continue
            # unmatched double backquotes
            # if bqidx + 1 <= len(bqs) and \
            #    bqs[bqidx][0] + 1 ==  bqs[bqidx+1][0]:

            # :cmd:`some string`
            if bqidx > 0 and s[bqs[bqidx][0] - 1] == ':':
                bqidx += 2
                continue
            # `some <url>`_
            try:
                if bqidx + 1 < len(bqs) and s[bqs[bqidx + 1][0] + 1] == '_':
                    bqidx += 2
                    continue
            except IndexError:
                pass  # probably end of file
            self._ryd.name()
            if lnr != last_line_displayed:
                print(
                    '{}: {}'.format(lnr + self._line, s[lines[lnr] : lines[lnr + 1]]), end=""
                )

                last_line_displayed = lnr
            print(' ' * (-1 + len(str(lnr + self._line)) + bqs[bqidx][2]), '--^')
            bqidx += 1
        return False

    def rst2pdf(self, file_path: Union[Path, StdOut]) -> str:
        if self._ryd._args.verbose > 0:
            print('generating PDF')
        fn = str(file_path)
        return subprocess.check_output(
            ['rst2pdf', fn, '-s', 'freetype-sans,eightpoint'], encoding='utf-8'
        )

    def write(self) -> None:
        with self._out_path.open('w') as fp:
            try:
                self.dump(fp, base_dir=self._out_path.parent)
                rst_ok = True
            except RydExecError:
                rst_ok = False
        if not rst_ok:
            if self._ryd._args.keep:
                print('not removing partial', self._out_path)
            else:
                print('removing', self._out_path, 'add --keep to preserve partial result')
                self._out_path.unlink()
            sys.exit(1)

        if self._ryd._args.pdf is False:  # can be None
            return
        if self._ryd._args.pdf or self._md.get('pdf'):
            self.rst2pdf(self._out_path)
            if self._md.get('encrypt'):
                pw = self._md['encrypt']['passwd']
                # print('pw', pw, file=sys.stderr)
                assert isinstance(self._out_path, Path)
                pdf_file = self._out_path.with_suffix('.pdf')
                enc_file = self._out_path.with_suffix(
                    '.{:%Y%m%d}.pdf'.format(datetime.date.today())
                )
                # self._out_path.rename(tmp_file)
                subprocess.check_output(
                    ['pdftk', str(pdf_file), 'output', str(enc_file), 'user_pw', pw]
                )

    def dump(self, fp: Any = sys.stdout, base_dir: Optional[Path] = None) -> None:
        last_ended_in_double_colon = False
        last_code = False
        for d in self.data:
            sys.stdout.flush()

            if hasattr(d, 'dump'):
                if not last_ended_in_double_colon and d.needs_double_colon:
                    print('\n::\n', file=fp)
                d.dump(fp, self)
                if hasattr(d, 'last_output'):
                    self.last_output = d.last_output
            elif isinstance(d, IncRaw):
                if last_code:
                    last_code = False
                    print('', file=fp)
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        p = Path(line)
                    print(p.read_text(), file=fp, end="")
            elif isinstance(d, Inc):
                if last_code:
                    last_code = False
                    print('', file=fp)
                for line in d.strip().splitlines():
                    if not line:
                        continue
                    if '{tempdir}' in line and line[0] != '/':
                        p = Path(line.format(tempdir=self.tempdir.directory))
                    elif base_dir is not None and line[0] != '/':
                        p = base_dir / line
                    else:
                        Path(line)
                    for line in p.open():
                        if line.strip():
                            print('  ', line, sep="", end="", file=fp)
                        else:
                            print('', line, sep="", end="", file=fp)
            # elif isinstance(d, PythonHidden):
            #    self.last_output = self.check_output(self.python_pre + d)
            #    if self.last_output is None:
            #        raise RydExecError("error executing Python")
            elif isinstance(d, (Python, Code, PythonHidden)):
                if d and not isinstance(d, PythonHidden):
                    if not last_ended_in_double_colon:
                        print('\n::\n', file=fp)
                    for line in d.strip().splitlines():
                        # print(' ', line, file=fp)
                        if line.strip():
                            print('  ', line, sep="", file=fp)
                        else:
                            print('', line, sep="", file=fp)
                    last_code = True
                else:
                    pass  # empty segment, might have pre-
                if isinstance(d, (Python, PythonHidden)):
                    self.last_output = self.check_output(self.python_pre + d)
                    if self._ryd._args.verbose > 1:
                        print('=========== output =========')
                        print(self.last_output, end="")
                        print('============================')
                    if self.last_output is None:
                        raise RydExecError('error executing Python')
            elif isinstance(d, PythonPre):
                self.python_pre = d
            elif isinstance(d, Comment):
                pass
            else:
                drs = d.rstrip()
                if drs.endswith('::'):
                    last_ended_in_double_colon = True
                    d = type(d)(drs + '\n\n')
                else:
                    last_ended_in_double_colon = False
                if last_code:
                    last_code = False
                    print('', file=fp)
                print(d, file=fp, end="")
                if isinstance(d, (Stdout, LastCompile, StdoutRaw)):
                    prefix = "" if isinstance(d, StdoutRaw) else '  '
                    op = self.last_compile if isinstance(d, LastCompile) else self.last_output
                    if op is None:
                        print(
                            '{}>>>>>>>>>  NO OUTPUT GENERATED <<<<<<<<<'.format(prefix),
                            file=fp,
                        )
                    else:
                        for line in op.rstrip().splitlines():
                            print('{}{}'.format(prefix, line), file=fp)
                    last_code = True
                elif type(d) != LiteralScalarString:
                    print('found unknown document type:', d.yaml_tag)
                    sys.exit(1)
                # print(file=fp)


class RoundTripConvertor(Convertor):
    def __init__(self, ryd: RYD, yaml: YAML, md: Dict[str, Any], path: Path) -> None:
        super().__init__(ryd)
        self._yaml = yaml
        # for v in self._tag_obj.values():
        #     yaml.register_class(v)
        self._md = md
        self._path = path
        self._out_path = self._path  # .with_suffix('.ryd.new')
        self.data = [md]
        self.last_output = ""
        self.updated = False

    def __call__(self, x: Any) -> bool:
        if not self._ryd._args.oitnb:
            self.data.append(x)
            return True
        try:
            v = x.tag.value
        except AttributeError:
            self.data.append(x)
            return True
        if not v.startswith('!python') or not x.value.strip():
            self.data.append(x)
            return True
        # only python with a real body
        y = subprocess.check_output(
            ['oitnb', '-q', '-'], input=bytes(x.value, 'utf-8')
        ).decode('utf-8')
        if x.value != y:
            print(x.value, y)
            self.updated = True
            x.value = y + '\n'
        self.data.append(x)
        return True

    def write(self) -> None:
        print('writing')
        self._yaml.explicit_start = True
        self._yaml.dump_all(self.data, self._out_path)
        # self._yaml.dump_all(self.data, sys.stdout)
