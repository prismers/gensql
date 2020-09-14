import unittest
import sqlgen.gentable.randtable as randgen
from sqlgen.gentable import genindex
import random


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.types, self.values, self.sql = randgen.randgentable()

    def testrandgen(self):
        # write to `test.sq`
        # and returns a triple
        n = 100
        while n > 0:
            assert len(self.types) == len(self.values) == len(self.sql)
            # check for default parameters,
            for mytype, value, s in zip(self.types, self.values, self.sql):
                assert len(mytype) == 5
                assert len(value) == 3
            n -= 1

    def testviewgen(self):
        random.seed()
        table = random.choice(list(enumerate(self.types)))
        ifort = genindex.genOneIndex(table[1], table[0], 2)
        assert isinstance(ifort, str)


if __name__ == '__main__':
    unittest.main()
