import random

from sqlgen.utilities.utility import extractValue
from .genindex import genOneIndex


class TableGenerator:

    def __init__(self, num=1, col=5, rownum=10, db='mysql'):
        self.num = num
        self.col = col
        self.rownum = rownum
        self.key = 0
        self.db = db

    def getcreatesql(self, num, mytype, value):
        if self.db == 'postgres':
            from sqlgen.dbtype.typeenumpsql import DataType
            drop = 'drop table if exists t{} CASCADE;'
        if self.db == 'mysql':
            from sqlgen.dbtype.typeenum import DataType
            drop = 'drop table if exists t{};'
        # line = 'create table t{} ({}) charset=latin1, engine=MyISAM;'
        line = 'create table t{} ({});'
        # random.seed()
        # iftmp = random.randrange(0, 9)
        # if iftmp > 4:
        #     line = 'create table t{} ({});'
        # else:
        #     line = 'create temporary table t{} ({});'
        declares = []
        for i, (tp, v) in enumerate(zip(mytype, value)):
            t = tp[0]
            key = ''
            if len(tp) > 1:
                key = tp[1]
            col = 'col{}'.format(str(i))

            if self.db == 'postgres':
                if t is DataType.CHAR or t is DataType.VARCHAR:
                    # or t is DataType.BLOB or t is DataType.TEXT:
                    col += ' {}({})'.format(t.describe(), str(v[0]))
                else:
                    col += ' {}'.format(t.describe())

            if self.db == 'mysql':
                if t is DataType.CHAR or t is DataType.VARCHAR or t is \
                        DataType.BINARY or t is DataType.VARBINARY:
                    col += ' {}({})'.format(t.describe(), str(v[0]))
                else:
                    col += ' {}'.format(t.describe())

            if key != '':
                col += ' ' + key

            declares.append(col)
        return [drop.format(str(num)), line.format(str(num), ', '.join(declares))]

    def getinsertsql(self, num, value):
        line = 'insert into t{} values ({});'
        vlist = []
        for v in value:
            if len(v) > 1:
                _, n = v
            else:
                n = v[0]
            if n == 'NULL':
                vlist.append('NULL')
            else:
                vlist.append('\'{}\''.format(str(n)))
        return line.format(str(num), ', '.join(vlist))

    def getinsertsqls(self, num, values):
        return [self.getinsertsql(num, v) for v in values]

    def getddl(self, types, values):
        ddl = []
        for i, (t, v) in enumerate(zip(types, values)):
            index = ''
            if random.randrange(0, 10) > 4:
                index = genOneIndex(t, i)
            if index == '':
                ddl.append(self.getcreatesql(i, t, v[0]) + self.getinsertsqls(i, v))
            else:
                ddl.append(self.getcreatesql(i, t, v[0]) + self.getinsertsqls(i, v) + [index])

        return ddl

    def genvalue(self, mytype):
        if self.db == 'postgres':
            from sqlgen.dbtype.typeenumpsql import DataValue
        else:
            from sqlgen.dbtype.typeenum import DataValue
        values = []
        for i in range(0, self.rownum):
            value = list()
            for j, t in enumerate(mytype):  # each column
                while True:
                    flag = 0
                    v = DataValue[t[0].describe()].randpickvalue()
                    vv = extractValue(v)
                    #  fix for constraint violation
                    if t[1] == 'NOT NULL':
                        if vv == 'NULL':
                            continue
                        break
                    if t[1] == 'PRIMARY KEY' or t[1] == 'UNIQUE':
                        if vv == 'NULL':
                            continue
                        for vs in values:  # :check for the constraint
                            vvs = extractValue(vs[j])

                            # 0 = -0
                            try:
                                if int(vv) == int(vvs):
                                    flag = 1
                                    break
                            except TypeError:
                                pass
                            except ValueError:
                                pass
                            # print(vvs, vv)
                            if vv == vvs:
                                flag = 1
                                break

                    if flag == 0:
                        break

                value.append(v)
            values.append(value)
        return values

    def genvalues(self, types):
        return [self.genvalue(t) for t in types]

    def gendatatype(self):
        if self.db == 'postgres':
            from sqlgen.dbtype.typeenumpsql import DataType, StringType
        if self.db == 'mysql':
            from sqlgen.dbtype.typeenum import DataType, StringType
        random.seed()
        datatype = random.sample(list(DataType), self.col)
        types = []
        for t in datatype:
            try:
                if StringType[str(t)]:
                    types.append((t, ''))
                    # print(t)
            except KeyError:
                random.seed()
                seed = random.randrange(0, 10)
                if seed <= 2 and self.key == 0:
                    self.key = 1
                    types.append((t, 'PRIMARY KEY'))
                elif seed <= 5:
                    types.append((t, 'UNIQUE'))
                elif seed <= 8:
                    types.append((t, 'NOT NULL'))
                else:
                    types.append((t, ''))
        return types

    def gendatatypes(self):
        datatypes = []
        for i in range(0, self.num):
            datatypes.append(self.gendatatype())
        return datatypes


def randgentable(num=5, col=5, rownum=3, db='mysql'):
    tableGenerator = TableGenerator(num, col, rownum, db)
    types = tableGenerator.gendatatypes()
    values = tableGenerator.genvalues(types)
    sql = tableGenerator.getddl(types, values)

    onlytypes = []
    for ttype in types:
        ttypeonly = [t[0] for t in ttype]
        onlytypes.append(ttypeonly)
    return onlytypes, values, sql
