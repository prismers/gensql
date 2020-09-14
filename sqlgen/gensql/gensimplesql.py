import random
import itertools

from sqlgen.utilities.utility import genBiOp, genCol, genJoinType, formatJoin, genNaturalJoinType, getSelectTableNames, \
    getColNameFromId, getAliasColName


# find same type of
def genJoin(types, maxnum=3):
    random.seed()
    if maxnum > len(types):
        maxnum = len(types)

    selected = random.sample(list(enumerate(types)), maxnum)

    ids = []
    tables = []
    # id in the original list
    for i, t in selected:
        ids.append(i)
        tables.append(t)

    joinidcol = []
    # product of the types
    for cols in itertools.product(*tables):
        # print(tables)
        # print(cols)
        # ignore different table
        if len(set(cols)) == len(cols):
            continue
        # the same cols
        joincol = [(i, x) for i, x in enumerate(cols) if cols.count(x) > 1]
        # find the col in table
        for col in list(set(joincol)):
            # print(col)
            idcol = []
            # the product
            for i, x in enumerate(cols):
                if x == col[1]:
                    # fix: wrong order of tableid and colid.  2020.07.04
                    idcol.append((ids[i], types[ids[i]].index(x)))
            joinidcol.append(idcol)
    return joinidcol


def genSimpleSQL(types, colnum, orderby=False):
    cols = genCol(types, colnum)
    sqlss = []
    sql = 'SELECT {} from t{};'
    sqlorder = 'SELECT {} from t{} order by {};'

    for tableid, col in enumerate(cols):
        sqls = []
        cols = ', '.join(['col{}'.format(str(i)) for i, _ in col])
        sqlfort = sql.format(cols, str(tableid))
        sqls.append(sqlfort)
        if orderby:
            random.seed()
            for i, _ in col:
                sqlx = sqlorder.format(cols, str(tableid), getColNameFromId(i))
                sqls.append(sqlx)
        sqlss.append(sqls)
    return sqlss


def genSelectWithJoin(types, colnum, joinnum, db='mysql'):
    cols = genCol(types, colnum)
    joins = genJoin(types, joinnum)

    tableidss = []
    joincolss = []
    for join in joins:
        tableids = []
        joincols = []
        for tableid, colid in join:
            tableids.append(tableid)
            joincols.append(colid)
        tableidss.append(tableids)
        joincolss.append(joincols)

    sql = "select {} from {};"
    sqljohn = 'select {} from {} on {};'


    sqls = []
    n = 10
    while n > 0:
        random.seed()
        tables = random.sample(list(enumerate(cols)), joinnum)
        ids, colss = getTablenameColname(tables)

        froms = getSelectTableNames(ids)
        colnames = []
        for i, colsx in zip(ids, colss):  # fix 2020.06.29
            tname = getTableNames([i])
            for c in colsx:
                colnames.append(tname + '.' + str(c) + getAliasColName(tname, c))
        colnames = ', '.join(colnames)

        johnkw = formatJoin(genJoinType(db))

        # natural join
        sqls.append(sql.format(colnames, ', '.join(froms)))

        if db == 'mysql':
            njoinkw = formatJoin(genNaturalJoinType())
            # explicit natural join
            sqls.append(sql.format(colnames, njoinkw.join(froms)))

        # theta join
        for tableids, joincols in zip(tableidss, joincolss):
            froms, johncols = getJoinTableCol(tableids, joincols)
            selectcol = [cols[i] for i in tableids]
            _, selectcols = getJoinTableCol(tableids, colTupleToList(selectcol))
            # where = '( ( {} ) xor NULL ) is NULL'.format(' {} '.format(genBiOp().describe()).join(johncols))
            where = ' {} '.format(genBiOp(db).describe()).join(johncols)
            # default order
            sqls.append(sqljohn.format(', '.join(selectcols), johnkw.join(froms), where))
            # reverse order
            # list.reverse(tableids)  # fix 2020.06.27
            # froms = getSelectTableNames(tableids)
            # sqls.append(sqljohn.format(', '.join(selectcols), johnkw.join(froms), where))
            # # random order
            # random.seed()
            # random.shuffle(tableids)  # fix 2020.06.27
            # froms = getSelectTableNames(tableids)
            # sqls.append(sqljohn.format(', '.join(selectcols), johnkw.join(froms), where))
        n -= 1

    return sqls


def colTupleToList(colss):
    collist = []
    for cols in colss:
        col = [c for c, _ in cols]
        collist.append(col)
    return collist


def getJoinTableCol(tables, joincols):
    tablenames = []
    tablecols = []

    for tid, col in zip(tables, joincols):
        tablename = getTableNames([tid])
        tablenames.append(tablename)
        if isinstance(col, list):
            colnames = list()
            for c in col:
                cname = getAliasColName(tablename, c)
                colnames.append(tablename + '.col' + str(c) + cname)
            colnamestr = ','.join(colnames)
        else:
            col = getColNames([col])
            colnamestr = tablename + '.' + col
        tablecols.append(colnamestr)
    # print(tablenames)
    # print(tablecols)
    return tablenames, tablecols


def getTableNames(ids):
    return ','.join(['t{}'.format(x) for x in ids])


def getColNames(cols, form=''):
    if form != '':
        return ', '.join([form.format(x) for x in cols])
    else:
        return ', '.join(['col{}'.format(x) for x in cols])


def getTablenameColname(tables):
    ids = []
    cols = []
    tn = 't{}'

    for id, col in tables:
        ids.append(str(id))
        # colfort = ', '.join([tn.format('{}.col{}'.format(id, c)) for c, _ in col])
        colfort = ['col{}'.format(c) for c, _ in col]
        cols.append(colfort)

    assert len(ids) == len(cols)
    return ids, cols

