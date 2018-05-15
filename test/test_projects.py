import click
import os
import shutil
import tempfile
import unittest


from click.testing import CliRunner
from orgreports.projects import main


class Fixture(unittest.TestCase):
    """Simple fixture for testing projects."""

    __ORG_FILE_A = """#+FILETAGS: PROJECT
* A
** Foo
** Bar
* B
** Splat
"""

    __VERBOSE = """2 A:
    Foo
    Bar
1 B:
    Splat
"""

    __BRIEF = """2 A
1 B
"""

    def setUp(self):
        self.d = tempfile.mkdtemp();
        with open(os.path.join(self.d, 'a.org'), 'w') as fh:
            fh.write(self.__ORG_FILE_A)

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_sub_command(self):
        """Test the 'projects' sub-command."""

        runner = CliRunner()
        result = runner.invoke(main, [])
        assert result.exit_code == 2
        assert result.output == 'Usage: main [OPTIONS] FILES...\n\nError: Missing argument "files".\n'

        f = os.path.join(self.d, 'a.org')

        result = runner.invoke(main, [f])
        assert result.exit_code == 0
        assert result.output == self.__VERBOSE

        result = runner.invoke(main, ['-b', f])
        assert result.exit_code == 0
        assert result.output == self.__BRIEF
