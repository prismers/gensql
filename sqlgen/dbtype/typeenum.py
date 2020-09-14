import random
import uuid
from enum import unique, Enum, auto


# @unique
# class IsType(Enum):
#     EXISTS = 'IS NOT NULL'
#     MISSING = 'IS NULL'
#
#
# @unique
# class IsTypeReverse(Enum):


@unique
class AggreFunc(Enum):
    COUNT = auto()
    SUM = auto()
    AVG = auto()
    MIN = auto()
    MAX = auto()

    def __str__(self):
        return self.name


@unique
class DataType(Enum):
    INT = 'INT'
    TINYINT = 'TINYINT'
    BIGINT = 'BIGINT'
    SMALLINT = 'SMALLINT'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    TIMESTAMP = 'TIMESTAMP'
    CHAR = 'CHAR'
    VARCHAR = 'VARCHAR'
    BINARY = 'BINARY'
    VARBINARY = 'VARBINARY'
    BLOB = 'BLOB'
    TEXT = 'TEXT'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class NumericType(Enum):
    INT = auto()
    TINYINT = auto()
    BIGINT = auto()
    SMALLINT = auto()
    FLOAT = auto()
    DOUBLE = auto()


@unique
class StringType(Enum):
    CHAR = auto()
    VARCHAR = auto()
    BINARY = auto()
    VARBINARY = auto()
    BLOB = auto()
    TEXT = auto()

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class DateType(Enum):
    DATE = auto()
    DATETIME = auto()
    TIMESTAMP = auto()


class BiOpSimilar(Enum):
    EQ = '>='
    # NEQ = '=!'
    LT = '<='
    GT = '>='

    # LTE = '>='
    # GTE = '<='
    # NSEQ = '<=>'

    def describe(self):
        return self.value

    def __str__(self):
        return self.name


class BiOpSwap(Enum):
    EQ = '='
    NEQ = '<>'
    LT = '>'
    GT = '<'
    LTE = '>='
    GTE = '<='
    NSEQ = '<=>'

    def describe(self):
        return self.value

    def __str__(self):
        return self.name


class BiOpReverse(Enum):
    EQ = '<>'
    NEQ = '='
    LT = '>='
    GT = '<='
    LTE = '>'
    GTE = '<'
    NSEQ = '!='
    IN = 'NOT IN'
    NIN = 'IN'

    def describe(self):
        return self.value

    def __str__(self):
        return self.name


@unique
class BiOperatorType(Enum):
    EQ = '='
    # NEQ = '!='
    NEQ = '<>'
    LT = "<"
    GT = ">"
    LTE = "<="
    GTE = ">="
    NSEQ = '<=>'
    IN = 'IN'
    NIN = 'NOT IN'

    def describe(self):
        return self.value

    def __str__(self):
        return self.name


@unique
class LogicOperatorType(Enum):
    OR = 'OR'
    AND = 'AND'
    XOR = 'XOR'

    # ISNULL = 'is null'
    # ISNNULL = 'is not null'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


class LogicOperatorReverse(Enum):
    OR = 'OR 1 OR'
    AND = 'OR 1 OR'
    XOR = 'XOR 1 OR 1 OR'

    # ISNULL = 'is null'
    # ISNNULL = 'is not null'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class BitOperatorType(Enum):
    AND = '&'
    OR = '|'
    XOR = '^'
    NOT = '~'
    LSHIFT = '<<'
    RSHIFT = '>>'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class NumericOpType(Enum):
    ADD = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


class NumericOpTypeMutator(Enum):
    ADD = '+ 1 +'
    MINUS = '- 1 -'
    MULTIPLY = '+ 1 +'
    # how? x/0
    DIVIDE = '* 1 + 1 +'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class DataValue(Enum):
    INT = ['-2147483648', '-1', '-0', '0', '1', '2147483647']
    TINYINT = ['-128', '-0', '0', '1', '127']
    BIGINT = ['-9223372036854775807', '-1', '-0', '0', '1', '9223372036854775807']
    SMALLINT = ['-32768', '-0', '0', '1', '32767']
    FLOAT = 'float'
    DOUBLE = 'double'
    DATE = ['1000-01-02', '1000-01-03', '1000-01-04']
    DATETIME = ['1000-01-02 00:00:00', '1000-01-03 00:00:00', '1000-01-04 00:00:00']
    TIMESTAMP = ['1970-01-02 00:00:01', '1970-01-03 00:00:01', '1970-01-04 00:00:01']
    CHAR = 'char'
    VARCHAR = 'varchar'
    BINARY = 'binary'
    VARBINARY = 'varbinary'
    BLOB = 'blob'
    TEXT = 'text'

    def __init__(self, *arg):
        Enum.__init__(arg)
        self.char = 0
        self.varchar = 0
        self.binary = 0
        self.varbinary = 0
        self.blob = 0
        self.text = 0
        self.nullRate = 50

    def describe(self):
        return self.value

    # random pick a value for the column
    def randpickvalue(self):
        random.seed()

        # if self == DataValue.BLOB:
        #     # if self.blob == 0:
        #     #     random.seed()
        #     #     self.blob = random.randrange(1, 255)
        #     #     return self.blob, "I am a blob"
        #     return "I am a blob",
        #
        # if self == DataValue.TEXT:
        #     # if self.text == 0:
        #     #     random.seed()
        #     #     self.blob = random.randrange(1, 255)
        #     return "I am a text",

        random.seed()
        choose = random.randrange(0, 99)

        # choose = 0
        if self == DataValue.FLOAT or self == DataValue.DOUBLE:
            if choose >= self.nullRate:
                return 'NULL',
            return random.uniform(-1000.0000, 1000.0000),

        # need size
        if self == DataValue.CHAR:
            if self.char == 0:
                self.char = random.randrange(1, 255)
            if choose >= self.nullRate:
                return self.char, 'NULL'
            value = str(uuid.uuid4())[:self.char]
            return self.char, value

        if self == DataValue.BINARY:
            if self.binary == 0:
                self.binary = random.randrange(1, 255)
            if choose >= self.nullRate:
                return self.binary, 'NULL'
            num = random.randint(1, 255)
            random.seed()
            value = str(bin(abs(num)))[:self.binary][2:]
            return self.binary, value

        # var dbtype
        if self == DataValue.VARCHAR:
            if self.varchar == 0:
                self.varchar = random.randrange(1, 655)
            if choose >= self.nullRate:
                return self.varchar, 'NULL'
            random.seed()
            upper = random.randint(1, self.varchar)
            value = str(uuid.uuid4())[:upper]
            return self.varchar, value

        if self == DataValue.VARBINARY:
            if self.varbinary == 0:
                self.varbinary = random.randrange(1, 655)
            if choose >= self.nullRate:
                return self.varbinary, 'NULL'
            random.seed()
            num = random.randint(1, 655)
            random.seed()
            upper = random.randint(1, self.varbinary)
            value = str(bin(abs(num)))[:upper][2:]
            return self.varbinary, value

        # date and time
        # if self == DataValue.DATE or self == DataValue.DATETIME \
        #         or self == DataValue.TIMESTAMP:
        #     return self.value,
        random.seed()
        return random.choice(self.value),


@unique
class CharsetType(Enum):
    pass

    def __str__(self):
        return self.value


@unique
class EngineType(Enum):
    pass

    def __str__(self):
        return self.value


@unique
class JoinType(Enum):
    IJ = 'INNER JOIN'
    CJ = 'CROSS JOIN'
    LJ = 'LEFT JOIN'
    RJ = 'RIGHT JOIN'
    LOJ = 'LEFT OUTER JOIN'
    ROJ = 'RIGHT OUTER JOIN'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class NaturalJoinType(Enum):
    NLJ = 'NATURAL LEFT JOIN'
    NRJ = 'NATURAL RIGHT JOIN'
    LOJ = 'NATURAL LEFT OUTER JOIN'
    ROJ = 'NATURAL RIGHT OUTER JOIN'

    # mysql 8 feature
    # NIJ = 'NATURAL INNER JOIN'

    def describe(self):
        return self.value

    def __str__(self):
        return self.value


@unique
class NumericFunctionType(Enum):
    ABS = auto()
    SQRT = auto()
    # EXP
    LN = auto()
    CEIL = auto()
    FLOOR = auto()
    SIGN = auto()
