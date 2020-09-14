import unittest
from sqlgen.gensql.gensimplesql import genJoin, genSimpleSQL, genSelectWithJoin
from sqlgen.utilities.utility import genCol
from sqlgen.gentable.randtable import randgentable
from sqlgen.dbtype.typeenum import DataType
from sqlgen.gensql.genview import genView


class MyTestCase(unittest.TestCase):

    def testgencol(self):
        types, _, _ = randgentable(3, 3, 3)
        # the maximum number of columns is 3
        cols = genCol(types, 4)

        for col in cols:
            # it cannot be empty
            assert cols is not []
            assert len(col) <= 3
            # correct type
            for i, coln in col:
                assert isinstance(coln, DataType)

    def testgenjoin(self):
        types, _, _ = randgentable(3, 3, 3)
        idcol = genJoin(types, 4)
        # an empty result is meaningless
        assert idcol is not []
        for i in idcol:
            # join table number
            assert len(i) <= 4
            for tableid, colnum in i:
                # correct result
                assert isinstance(tableid, int)
                assert isinstance(colnum, int)

    def testgensimplesql(self):
        types, _, _ = randgentable(2, 5, 1)
        sqls = genSimpleSQL(types, 2)
        for sql in sqls:
            assert isinstance(sql, list)
            for s in sql:
                assert isinstance(s, str)

    def testgensqlwithjoin(self):
        # FIXME: bug when rownum=0
        types, _, _ = randgentable(8, 5, 3)
        sqls = genSelectWithJoin(types, 5, 2)
        # for s in sqls:
        #     print(s)

    def testgenview(self):
        types, _, _ = randgentable(2, 5, 1)
        sql = genSimpleSQL(types, 2)
        views = genView(sql.pop(), 1, joincond=False)

        for v in views:
            assert len(v) == 3
            assert isinstance(v[0], str)
            assert isinstance(v[1], tuple)
            assert isinstance(v[2], str)


if __name__ == '__main__':
    unittest.main()
