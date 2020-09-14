import random
import string


def genOneIndex(types, tid=0, num=2, db='mysql'):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataType
    else:
        from sqlgen.dbtype.typeenum import DataType
    ci = "create index {} on t{} ({});"
    # index column
    random.seed()
    index = random.sample(list(enumerate(types)), num)
    # index name
    random.seed()
    iname = random.sample(string.ascii_lowercase, 5)
    if db == 'mysql':
        for i, mytype in index:
            # cannot be used as index
            try:
                if len(mytype) > 1:
                    if mytype[0] is DataType.BLOB or mytype[0] is DataType.TEXT:
                        return ''
            except TypeError:
                if mytype is DataType.BLOB or mytype is DataType.TEXT:
                    return ''
    return ci.format(''.join(iname), str(tid), ', '.join(['col{}'.format(str(i)) for i, _ in index]))
