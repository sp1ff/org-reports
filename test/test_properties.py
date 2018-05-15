import click
import os
import shutil
import tempfile
import unittest


from click.testing import CliRunner
from orgreports.properties import main


class Fixture(unittest.TestCase):
    """Simple fixture for testing properties."""

    __ORG_FILE_A = """#+TITLE: A
* 1
** TODO [#B] 1.1 foo
      :PROPERTIES:
      :Foo: A
      :Bar: X
      :END:
** IN-PROGRESS 1.2 bar
      :PROPERTIES:
      :Foo: A
      :Bar: Y
      :END:
* 2
** DONE 2.1 splat
      :PROPERTIES:
      :Foo: A
      :Bar: X
      :END:
** TODO 2.1 baz
      :PROPERTIES:
      :Foo: A
      :END:
"""

    __REPORT_ON_FOO = """
| Foo                              | # Tasks |
|----------------------------------+---------|
| A                                |       2 |
|----------------------------------+---------|
"""
    __REPORT_ON_BAR = """
| Bar                              | # Tasks |
|----------------------------------+---------|
| X                                |       1 |
| Y                                |       1 |
| nil                              |       1 |
|----------------------------------+---------|
"""

    __REPORT_ON_FOO_BAR = """
| Foo,Bar                          | # Tasks |
|----------------------------------+---------|
| A,X                              |       1 |
| A,Y                              |       1 |
| A,nil                            |       1 |
|----------------------------------+---------|
"""

    def setUp(self):
        self.d = tempfile.mkdtemp();
        with open(os.path.join(self.d, 'a.org'), 'w') as fh:
            fh.write(self.__ORG_FILE_A)

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_sub_command(self):
        """Test the 'properties' sub-command."""

        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code == 2
        assert result.output == 'Usage: main [OPTIONS] FILES...\n\nError: Missing argument "files".\n'

        f = os.path.join(self.d, 'a.org')

        result = runner.invoke(main, ['-p', 'Foo', f])
        assert result.exit_code == 0
        assert self.__REPORT_ON_FOO == result.output

        result = runner.invoke(main, ['--sort', 'alpha', '-p', 'Bar', '-s', 'TODO', '-s', 'IN-PROGRESS', f])
        assert result.exit_code == 0
        assert self.__REPORT_ON_BAR == result.output

        result = runner.invoke(main, ['--sort', 'alpha', '-p', 'Foo', '-p', 'Bar', '-s', 'TODO', '-s', 'IN-PROGRESS', f])
        assert result.exit_code == 0
        assert self.__REPORT_ON_FOO_BAR == result.output

    def test_find(self):
        """Test find_by_property."""

        from orgreports.properties import find_by_property

        f = os.path.join(self.d, 'a.org')
        D = find_by_property([f], 'Bar', ['TODO', 'IN-PROGRESS'])
        assert len(D.keys()) == 4
        assert D[0] == [('2.1 baz', f)]
        assert D[1] == [ ]
        assert D['X'] == [('1.1 foo', f)]
        assert D['Y'] == [('1.2 bar', f)]

    def test_product(self):
        """Test form_product."""

        from orgreports.properties import form_product

        f = os.path.join(self.d, 'a.org')
        X = form_product([f], ['Foo', 'Bar'], ['TODO', 'IN-PROGRESS'])
        assert X['A,nil'] == 1
        assert X['A,X'] == 1
        assert X['A,Y'] == 1
