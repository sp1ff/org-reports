import os
import shutil
import tempfile
import unittest


from orgreports.contexts import find_contexts


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

    def setUp(self):
        self.d = tempfile.mkdtemp();
        with open(os.path.join(self.d, 'a.org'), 'w') as fh:
            fh.write(self.__ORG_FILE_A)

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_find_contexts(self):
        D = find_contexts([os.path.join(self.d, 'a.org')], 'ctx', ['TODO', 'IN-PROGRESS'])
        assert len(D.keys()) == 4


if __name__ == '__main__':
    unittest.main()
