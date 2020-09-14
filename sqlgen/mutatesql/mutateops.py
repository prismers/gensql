import pyparsing
from moz_sql_parser import parse, format

from sqlgen.dbtype.typeenum import BiOpSwap, BiOperatorType, BiOpReverse, LogicOperatorType, LogicOperatorReverse, \
    NumericOpTypeMutator, NumericOpType, BiOpSimilar
from sqlgen.utilities.utility import prettyprint


def swap(tokens, key, item, oldtype=BiOperatorType, newtype=BiOpSwap):
    try:
        # find the new operator
        changed = newtype[key.upper()].describe()
        # print(changed)
        # find the operator name for the parser
        name = oldtype(changed).name.lower()
        # print(name)
        if newtype == BiOpSwap:
            item.reverse()
            # print(item)
        tokens.pop(key)
        tokens[name] = item
        return tokens
    except AttributeError:
        pass
    except KeyError:
        pass
    except ValueError:
        pass

    return None


def doSwap(tokens, func, oldtype=BiOperatorType, newtype=BiOpSwap):
    if isinstance(tokens, dict):
        for key, item in tokens.items():
            newtokens = func(tokens, key, item, oldtype=oldtype, newtype=newtype)
            if newtokens is not None:
                return newtokens
            else:
                newitem = doSwap(item, func, oldtype=oldtype, newtype=newtype)
                if newitem is not None:
                    tokens.pop(key)
                    tokens[key] = newitem
                    return tokens
        else:
            return None
    elif isinstance(tokens, list):
        flag = 0
        for i, it in enumerate(tokens):
            newtokens = doSwap(it, func, oldtype=oldtype, newtype=newtype)
            if newtokens is not None:
                tokens[i] = newtokens
                flag = 1
        if flag:
            return tokens
        else:
            return None


# wrapper to pass the function
def swapLRhs(sqls):
    return doit(sqls, swap)


def doit(sqls, func, oldtype=BiOperatorType, newtype=BiOpSwap):
    num = len(sqls)
    if num > 1:
        prettyprint('%', 'Total #{} SQLs'.format(str(num), ))
    eqpair = list()

    for i, sql in enumerate(sqls):
        newsql = ''
        sql = sql.strip().replace('\n', '')

        err = 0
        try:
            # print("Parsing: ", sql)
            tokens = parse(sql)
        except pyparsing.ParseException as e:
            err = 1
            print('\nparse error')
            # print(e)
        except RecursionError as e:
            err = 1

        if err:
            continue
            # exit(1)

        for key, item in tokens.items():
            # if key == 'where' or key == 'select' or key == 'on':
            # if process when it is a sub-expression
            res = doSwap(item, func, oldtype=oldtype, newtype=newtype)
            if res is not None:
                tokens[key] = res
                try:
                    # FIXME: this will wrongly quote literals as `myword`
                    newsql = format(json=tokens, ansi_quotes=False)
                except Exception as e:
                    print('Reverse Operator Keyerror', type(e))
                    return [(sql, '')]

        if newsql != '':
            eqpair.append((sql, newsql + ';'))
            # print(newsql)
    return eqpair


def reverseBiOP(sqls):
    return doit(sqls, swap, newtype=BiOpReverse)


def similarBiOP(sqls, null=True):
    return doit(sqls, swap, newtype=BiOpSimilar)


def mutateLOP(sqls):
    eqpair = []
    new = ''
    for sql in sqls:
        parsed = sql.strip(';').split()
        for i, token in enumerate(parsed):
            try:
                op = LogicOperatorType(token)
                # reverse the operator
                parsed[i] = LogicOperatorReverse[str(op)].describe()
                if parsed[i + 1] == '0' or parsed[i + 1] == '' or parsed[i + 1] == '-0':
                    parsed[i + 1] = '1'
                new = ' '.join(parsed) + ';'
                break
            except KeyError:
                pass
            except ValueError:
                pass
        eqpair.append((sql, new))
    return eqpair


def mutateNOP(sqls):
    eqpair = []
    new = ''
    for sql in sqls:
        parsed = sql[:-1].split()
        for i, token in enumerate(parsed):
            try:
                op = NumericOpType(token)
                # print(op)
                # reverse the operator
                parsed[i] = NumericOpTypeMutator[op.name].describe()
                new = ' '.join(parsed) + ';'
                break
            except KeyError:
                pass
            except ValueError:
                pass
        eqpair.append((sql, new))
    return eqpair
