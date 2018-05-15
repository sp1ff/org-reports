import os
import shutil
import tempfile
import unittest


from click.testing import CliRunner
from orgreports.contexts import main


class Fixture(unittest.TestCase):
    """Simple fixture for testing contexts."""

    __ORG_FILE_A = """#+TITLE: A
* 1

** TODO [#B] 1.1 foo
      :PROPERTIES:
      :ctx:  @online
      :END:
** IN-PROGRESS 1.2 bar
      :PROPERTIES:
      :ctx:  @home
      :END:

* 2

** DONE 2.1 X
      :PROPERTIES:
      :ctx:  @work
      :END:

* 3

** TODO [#C] 3.1 splat
      :PROPERTIES:
      :ctx:  @online
      :END:
"""

    __OUTPUT = """
2 tasks in -1 ctxs:

| ctx                              | # Tasks |        |
|----------------------------------+---------+--------|
| @online                          |       2 | 100.0% |
|----------------------------------+---------+--------|
"""


    def setUp(self):
        self.d = tempfile.mkdtemp();
        with open(os.path.join(self.d, 'a.org'), 'w') as fh:
            fh.write(self.__ORG_FILE_A)

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_sub_command(self):

        f = os.path.join(self.d, 'a.org')
        runner = CliRunner()
        result = runner.invoke(main, ['-p', 'ctx', f])
        assert result.exit_code == 0
        assert result.output == self.__OUTPUT
        print(result)


if __name__ == '__main__':
    unittest.main()
