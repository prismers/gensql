import random
from sqlgen.utilities.utility import getTableNameFromId, getColNameFromId, extractValue, prettyformat, castValueWithType, genNumericRandFunc
from sqlgen.dbtype.typeenum import LogicOperatorType, NumericOpType


# random predicate with col, logic op, any values

# print(alleps)


def genRandBiOp(db='mysql'):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataValue, BiOperatorType, BitOperatorType
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataValue, BiOperatorType, BitOperatorType
    random.seed()
    return random.choice(list(BiOperatorType) + list(LogicOperatorType)).describe()


def genRandNumericBiOp(db='mysql'):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataValue, BiOperatorType, BitOperatorType
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataValue, BiOperatorType, BitOperatorType
    random.seed()
    return random.choice(list(BiOperatorType) + list(LogicOperatorType) + list(NumericOpType)).describe()


def getRandExp(length, db='mysql'):
    alleps = list()
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataValue, BiOperatorType, BitOperatorType
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataValue, BiOperatorType, BitOperatorType

    # for i in list(LogicOperatorType):
    #     alleps.append(i.describe())
    for i in list(BitOperatorType):
        alleps.append(i.describe())
    for i in list(BiOperatorType):
        alleps.append(i.describe())

    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataValue
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataValue

    for i in list(DataValue):
        if i is DataValue.TEXT or i is DataValue.BLOB or i is DataValue.CHAR or i is DataValue.VARCHAR:
            continue
        v = i.randpickvalue()
        alleps.append(str(extractValue(v)))
    random.seed()
    return random.sample(alleps, length)


def getRandValue(db='mysql'):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataValue
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataValue

    random.seed()
    return random.choice(list(DataValue))


def getRandValueFromType(randt, db='mysql'):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataValue
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataValue
    random.seed()
    return DataValue[randt.describe()].randpickvalue()


def getRandType(db='mysql'):
    if db == 'postgres':
        from sqlgen.dbtype.typeenumpsql import DataType
    if db == 'mysql':
        from sqlgen.dbtype.typeenum import DataType
    random.seed()
    return random.choice(list(DataType))


def genRanExpFromTaE(tid, colid, e, db):
    return getTableNameFromId(tid) + '.' + getColNameFromId(colid) + ' ' + \
           genRandNumericBiOp(db) + ' ' + e


def getRanExpFromTaV(tid, colid, t, v, db):
    return getTableNameFromId(tid) + '.' + getColNameFromId(colid) + ' ' + \
           genRandBiOp(db) + ' ' + prettyformat(t, str(extractValue(v)))


def getTotalRandExp(length):
    explist = getRandExp(length)
    return ' ' + ''.join(["'{}'".format(x) for x in explist])


def genwherepred(types, valuess, length, db='mysql'):
    predss = []
    for i, (ttype, values) in enumerate(zip(types, valuess)):
        pred = list()
        for value in values:
            # type with concrete value
            for colid, (t, v) in enumerate(zip(ttype, value)):
                if extractValue(v) == '0' or extractValue(v) == '-0':
                    continue
                if db == 'mysql':
                    from sqlgen.dbtype.typeenum import DataType
                    if t is DataType.CHAR or t is DataType.VARCHAR \
                            or t is DataType.BLOB or t is DataType.TEXT:
                            # or t is DataType.TIMESTAMP \
                            # or t is DataType.DATE or t is DataType.DATETIME:
                        continue
                # rand `col op v`
                randv = getRandValueFromType(t, db)
                colandv = getRanExpFromTaV(i, colid, t, randv, db)
                randpreds = getTotalRandExp(length)
                # print(randpreds)
                pred.append(colandv)
                pred.append(randpreds)
        predss.append(pred)
    return predss


# select function based on the type
def genFunWithType(t, v, db):
    res = castValueWithType(t, v, db)
    rt = res[0]
    rv = res[1]
    # print(rt)
    # print(rv)
    if rt is int or rt is float:
        return genNumericRandFunc(), rv
    if rt is str:
        if len(res) > 2:
            return 'HEX', rv
        return 'CONCAT', rv


# generate predicate with column operation
def genPredWithCol(types, valuess, db):
    predss = []
    for i, (ttype, values) in enumerate(zip(types, valuess)):
        pred = list()
        for value in values:
            for colid, (t, v) in enumerate(zip(ttype, value)):
                func = genFunWithType(t, v, db)
                # print('myfunction: ' + str(func) + '\n')
                # print(func)
                if func is not None:
                    if isinstance(func[1], int) or isinstance(func[1], float):
                        e = '{}({})'.format(func[0], abs(func[1]))
                    else:
                        e = '{}({})'.format(func[0], func[1])
                    expr = genRanExpFromTaE(i, colid, e, db)
                    pred.append(expr)
        predss.append(pred)
    return predss
