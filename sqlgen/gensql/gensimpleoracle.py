from sqlgen.utilities.utility import getSelectWithColAndTable, getAddWhereToSelect, getWhereWithColAndValue, \
    extractValue
from sqlgen.utilities.utility import prettyformat


def verifyEveryRow(values, types, db='mysql'):
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataType
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataType
    sqls = []
    # in a table
    for tid, (ttype, value) in enumerate(zip(types, values)):
        # for a column 'select colx from tx where colx = foo;'
        for _, line in enumerate(value):
            for i, col in enumerate(line):
                t = ttype[i]
                if db == 'mysql':
                    if t is DataType.FLOAT or t is DataType.DOUBLE:
                        continue

                selectcol = getSelectWithColAndTable([i], [tid])

                v = extractValue(col)
                v = prettyformat(t, v, db)

                v = getWhereWithColAndValue(i, v)
                if db == 'mysql':
                    if t is DataType.BINARY or t is DataType.VARBINARY:
                        v = 'binary {}'.format(v)

                sql = getAddWhereToSelect(selectcol, v)
                sqls.append(sql)
    return sqls
