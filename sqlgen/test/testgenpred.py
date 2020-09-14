import unittest
from sqlgen.gensql.gensimpleoracle import verifyEveryRow
from sqlgen.gentable.randtable import randgentable
from sqlgen.gensql.genpredicate import genwherepred, genPredWithCol


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.types, self. values, _ = randgentable(2, 5, 3)

    def test_something(self):
        sqls = verifyEveryRow(self.values, self.types)
        # for s in sqls:
        #  print(s)

    def test_genwhere(self):
        preds = genwherepred(self.types, self.values, 5)
        # for p in preds:
        #     print(p)

    def test_colpred(self):
        pred = genPredWithCol(self.types, self.values, db='mysql')
        for p in pred:
            for line in p:
                assert '(' in line and ')' in line


if __name__ == '__main__':
    unittest.main()
