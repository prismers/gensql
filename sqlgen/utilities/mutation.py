from time import sleep

from sqlgen.mutatesql.mutateops import reverseBiOP
from sqlgen.dbtype.typeenum import AggreFunc
from .utility import getPredIsNULL
import mysql.connector


def doMutate(cu, func, sql, orin, row, debug=False):
    default = orin
    sql = sql.replace('\r', '').replace('\n', '')
    res = func([sql])
    if len(res) < 1 or res is None:
        new = ''
    else:
        # print(res)
        _, new = res.pop()
        new = new.replace('NEG', '-')
        print("\nnew:", new)
        print(' cannot reverse the operator') if new == '' else None

    null = getPredIsNULL(sql).replace('neg', '-')
    if null == '':
        print('>>>> Cannot handle, verify manually\n') if debug else None
        return 1

    true = getPredIsNULL(sql, 'IS TRUE').replace('neg', '-')
    false = getPredIsNULL(sql, 'IS FALSE').replace('neg', '-')

    nullnum = 0

    try:
        print("\nVerify queries...")
        # runnable
        print(repr(new))
        cu.execute(new)
        print(repr(true))
        cu.execute(true)
        print(repr(false))
        cu.execute(false)
        # save rownum
        cu.execute(null)
        nullnum = len(cu.fetchall())
    except mysql.connector.errors.DatabaseError as e:
        if 'out of range' in str(e):
            return 0

        sleep(1)
        print('\nMutation error!')
        print(false)
        print(null)

        with open('syntaxerr.txt', 'a+') as f:
            f.write(new)
            f.flush()
            f.close()

        # exit(1)

    for s in [null, true, false]:
        # there is no predicate but cannot return all rows
        # a bug
        if s.lower() == sql.lower():
            return 1

    bug = 0
    if new != '':
        cu.execute(new)
        newnum = len(cu.fetchall())
        print("#row={} Reverse condition: {}".format(newnum, new)) if debug else None


        # if origin == newnum, the reverse may have no effect
        # if orin != newnum:
        orin += newnum

        if orin != row:
            print("#row={} NULL condition: {}\n".format(nullnum, null)) if debug else None

            orin += nullnum
            if orin != row:
                print('Mutation: correct rows should be #' + str(row) + ', get #' + str(orin), end='\n\n') if debug \
                        else None
                bug = 1

    # eliminate possible false-positives
    if (new != '' and bug == 1) or new == '':
        # if 'where' in sql and '%' in sql.split('where')[1]:
        #     return 0
        # if 'having' in sql and '%' in sql.split('having')[1]:
        #     return 0
        print("\nThree-value conditions: ")
        print(null)
        print('row#={}'.format(str(nullnum)))
        # print(sql)
        # cu.execute(sql)
        print(true)
        cu.execute(true)
        truenum = len(cu.fetchall())
        print('row#={}'.format(str(truenum)))
        nullnum += truenum

        print(false)
        cu.execute(false)
        falsenum = len(cu.fetchall())
        print('row#={}'.format(str(falsenum)))
        nullnum += falsenum
        print('\n\n')

        if nullnum != row:
            if default == truenum:
                print('Expected #row = {}'.format(row))
                print('\n\n!!! A bug is reported!\n\n\n')
                return 1

        # if truenum != default:
        #     print('!!! Implicit conversion error, will report as a bug !!!')
        #     return 1

        if (nullnum - falsenum) != (row - falsenum):
            print('!!! Not true is not handled correctly,  will report as a bug !!!')
            return 1

        # handle false-negatives
        if not debug:
            if bug == 1 and new != '':
                return 1

        return 0

    return 0


aggfunc = [str(f) for f in list(AggreFunc)]


def haveAggFunc(sql):
    for f in aggfunc:
        # aggregation in target list
        if f.lower() in sql.lower().split('from')[0]:
            return True
    else:
        return False


def controlMutation(c, orin, row, sql, debug=False):
    mutations = [reverseBiOP]
    # mutations = [reverseBiOP, mutateNOP, mutateLOP]
    print('Mutating the following sql:')
    print('#row=' + str(orin) + ': ' + sql, end='') if debug else None

    bug = 0
    for m in mutations:
        res = doMutate(c, m, sql, orin, row, debug)
        bug += res
    return bug


def mutateAndTry(c, sql, err, row, debug=False):
    if haveAggFunc(sql):
        row = 3

    if sql == '':
        return 0

    c.execute(sql)
    # c.fetchall()
    orin = len(c.fetchall())

    agg = haveAggFunc(sql)
    # the origin predicate forms a partition
    if ('where' not in sql.lower()) and ('having' not in sql.lower()):
        if orin == row or (agg and orin == 1):
            # print("...mutation not needed") if debug else None
            print("...mutation not needed")
            return 0
    elif agg:
        if 'having' in sql.lower():
            row = 1
        elif 'where' in sql.lower():
            row = 3

    res = controlMutation(c, orin, row, sql, debug)
    # if res >= 1:
    #     if '<=>' in sql:
    #         print('...changed <=> to = in: ' + sql) if debug else None
    #         sql = sql.replace('<=>', '=')
    #         c.execute(sql)
    #         orin = c.rowcount
    #         bug = controlMutation(c, orin, row, sql, debug)
    #         if bug >= 1:
    #             logging.info('I captured a potential bug, please check the last query: ' + sql)
    #     else:
    #         bug = res
    #     logging.info('I captured a potential bug, please check the last query: ' + sql)

    print('Finished mutation for the current sql.') if debug else None
    # fix bug, the return value must be 1
    if res >= 1:
        err.write('partition error >>>>>>\n')
        err.write(sql + '\n')
        err.write('<<<<<< end of the error\n')
        err.flush()

        return 1
    return 0



