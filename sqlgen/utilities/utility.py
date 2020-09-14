import random

from sqlgen.dbtype.typeenum import NumericFunctionType
from sqlgen.dbtype.typeenum import BiOperatorType, LogicOperatorType, JoinType, NaturalJoinType

import moz_sql_parser as parser

def castValueWithType(t, v, db):
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import NumericType,StringType, DateType
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import NumericType, StringType, DateType

    value = extractValue(v)
    null = False
    if value == 'NULL':
        null = True

    try:
        # FIXME: cannot handle NULL value
        ntype = NumericType[t.name]

        if isinstance(ntype, NumericType):
            if null:
                return int, '1',
            else:
                return int, int(value),
        flag = 0
        if db == 'mysql':
            if ntype == NumericType.FLOAT or ntype == NumericType.DOUBLE:
                flag = 1
        if db == 'postgres':
            if ntype == NumericType.REAL or ntype == NumericType.FLOAT8:
                flag = 1
        if flag:
            if null:
                return float, '1.0',
            else:
                return float, float(value),
    except KeyError:
        pass

    try:
        ntype = StringType[t.name]
        return str, str(value),
    except KeyError:
        pass

    # it must be date type
    ntype = DateType[t.name]
    return str, str(value), 1


def getTableNameFromId(tid):
    return 't{}'.format(str(tid))


def getColNameFromId(cid):
    return 'col{}'.format(str(cid))


def getSelectedCol(cols):
    return ', '.join([getColNameFromId(cid) for cid in cols])


def getSelectTableNames(tables):
    return [getTableNameFromId(tid) for tid in tables]


def getSelectedTables(tables):
    return ', '.join(getSelectTableNames(tables))


def getWhereWithColAndValue(cid, value):
    if value == 'NULL':
        return getColNameFromId(cid) + ' IS NULL'
    else:
        return getColNameFromId(cid) + ' = ' + str(value)


def getSelectWithColAndTable(cols, tables):
    select = 'select {} from {};'
    return select.format(getSelectedCol(cols), getSelectedTables(tables))


def getAddWhereToSelect(select, where, pred='where'):
    if 'order by' in select:
        parsed = select.split('order by')
        head = parsed[0]
        body = parsed[1][:-1]
        return head + " {} ".format(pred) + where + ' order by ' + body + ';'
    return select[:-1] + " {} ".format(pred) + where.strip() + ' ;'


# adapt for more complex substitutions
def getPredIsNULL(sql, note='IS NULL'):
    # sql = sql.strip().replace('`', '').lower()
    # sql = sql.strip().lower()
    sql = sql.strip()

    if 'WHERE' in sql and 'HAVING' in sql:
        return ''

    if 'WHERE' not in sql and 'HAVING' not in sql and 'ON' not in sql:
        return sql

    subsql = sql
    subquery = False

    # parsing error now
    tokens = parser.parse(sql)

    for key, value in tokens.items():
        if key == 'from' and 'value' in value:
            subsql = parser.format(value['value'], ansi_quotes=False) + ';'
            subquery = True
            break

    if subquery:
        newsubsql = getPredIsNULL(subsql, note)
        # fix comparison and optimize
        if newsubsql.strip().lower() != subsql.strip().lower():
            newsubsql = ' (' + getPredIsNULL(subsql, note).replace(';', '').strip() + ') AS t'
            # print('newsub: ', newsubsql)
            import re
            newsql = re.sub('\s*\(SELECT .*\) AS [a-zA-Z_`]*', newsubsql, sql, re.X)
            # print('sql: ', sql)
            # print('new: ', newsql)
            newsql = newsql.replace('= TRUE', 'IS TRUE'.lower()).replace('= FALSE', 'IS FALSE'.lower())
            return newsql
        else:
            subsql = sql



    # fix, drop limit, not effective
    select = subsql.replace(';', '').split('LIMIT')[0]

    if 'HAVING' in select:
        parsed = select.split('HAVING')
        pred = 'HAVING'
    elif 'WHERE' in select:
        parsed = select.split('WHERE')
        pred = 'WHERE'
    elif 'ON' in select:
        parsed = select.split('ON', 1)
        pred = 'ON'
    else:
        return subsql

    head = parsed[0].strip() + ';'

    if 'ORDER BY' in select:
        where = parsed[1].split('ORDER BY')[0][:-1].strip()
    else:
        where = parsed[1].strip()


    # if not where.strip().startswith('(') or not where.strip().endswith(')'):
    #     where = '({})'.format(where)

    concated = getAddWhereToSelect(head, '( {} ) {}'.format(where, note), pred)
    # print(concated)
    concated = concated.replace('= TRUE', 'IS TRUE'.lower()).replace('= FALSE', 'IS FALSE'.lower())
    # print(concated)
    return concated



def replaceJoinOn(select, where):
    s = select.split('on')[0]
    tables = select.split('from')[1].split('on')[0].split('join')
    tables = [t.strip() for t in tables]
    table = [where.split(' ')[0].split('.')[0]]

    if table is not [] and table != [''] and len(set.intersection(set(tables), set(table))) == 0:
        where = where.replace(table[0], tables[0])

    s = getAddWhereToSelect(s, where)
    return s


def formatJoin(johnkw):
    return ' {} '.format(johnkw)


def genJoinType(db):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import JoinType
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import JoinType
    random.seed()
    return random.choice(list(JoinType)).describe()


def genNaturalJoinType():
    random.seed()
    return random.choice(list(NaturalJoinType)).describe()


def genLimit():
    max = 18446744073709551615
    random.seed()
    return random.randrange(1, 100), max


def genBiOp(db):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import BiOperatorType
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import BiOperatorType
    random.seed()
    return random.choice(list(BiOperatorType))


def genLogicOp():
    random.seed()
    return random.choice(list(LogicOperatorType))


def genCol(types, maxnum=3):
    cols = []
    for tabletype in types:
        columns = len(tabletype)
        if maxnum > columns:
            maxnum = columns
        # random.seed()
        # num = random.randint(1, maxnum)
        random.seed()
        mycol = random.sample(list(enumerate(tabletype)), maxnum)
        cols.append(mycol)
    return cols


def extractValue(v):
    if len(v) > 1:
        return v[1]
    else:
        return v[0]


def getAliasColName(tablename, colname):
    return ' as {}{} '.format(tablename, colname)


def prettyformat(t, v, db='mysql'):
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataType, StringType, DateType
        if t is DataType.BINARY or t is DataType.VARBINARY:
            if v == '':
                v = "''"

    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataType, StringType, DateType
        # if t is DataType.BYTEA:
        #     if v == '':
        #         v = "''"

    if isinstance(t, StringType) or isinstance(t, DataType) or isinstance(t, DateType):
        if v != 'NULL':
            v = "'{}'".format(v)

    return v


def genNumericRandFunc():
    random.seed()
    return random.choice(list(NumericFunctionType)).name


def prettyprint(boxchar, line):
    num = len(line) + 4
    print('\n' + boxchar * num)
    print(boxchar + ' ' + line + ' ' + boxchar)
    print(boxchar * num)


# without ';'
def removePart(sql, key):
    try:
        tmp = sql.split(key)
        head = tmp[0]
        tail = tmp[1]
    except IndexError:
        tail = ''
    return head, tail


def dropPart(sql, key):
    head, tail = removePart(sql, key)
    return head + ';', tail


# fixme
def dropWhereAndGet(sql):
    return sql.spit('where')


def changeToSelectAll(sql):
    return 'select * from {}'.format(sql.split('from')[1])
