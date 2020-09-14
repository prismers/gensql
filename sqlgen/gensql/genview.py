import random
import uuid
from sqlgen.utilities.utility import dropPart, changeToSelectAll


# select num of views to create
def genView(ori, all=True, num=1, where=True, orderby=True, joincond=True):
    sqls = ori
    random.seed()
    cv = "create view v{} as {}"
    dcv = "drop view if exists v{};"

    # if not where:
    #     sqls = [dropPart(s, 'where') for _, s in enumerate(sqls)]
    # if not orderby:
    #     sqls = [dropPart(s, 'order by') for _, s in enumerate(sqls)]
    if not joincond:
        # print(sqls[0])
        sqls = [dropPart(s, 'on') for _, s in enumerate(sqls)]
        for i, (s, on) in enumerate(sqls):
            if 'NATURAL' in s:
                continue
            sql = '{} on 1 union all {} on 0;'
            s = s.strip(';')
            if 'OUTER' in s:
                sqls[i] = (sql.format(s, s), on)
                continue
            if 'JOIN' in s and on != '':
                sqls[i] = (sql.format(s, s), on)
                continue

    sqls = [(cv.format(str(i), s[:-1]), on) for i, (s, on) in enumerate(sqls)]
    dcvs = [dcv.format(str(i)) for i in range(len(sqls))]

    if all:
        return list(zip(dcvs, sqls, ori))
    return random.sample(list(zip(dcvs, sqls, ori)), num)

