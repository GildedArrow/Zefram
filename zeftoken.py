from enum import Enum, auto

class ZefTokenType(Enum):
	KEYWORD = auto()
	IDENTIFIER = auto()
	FLOAT = auto()
	INT = auto()
	STRING = auto()

	PLUS = auto() # +
	MINUS = auto() # -
	ASTERISK = auto() # *
	SLASH = auto() # /
	COLON = auto() # :
	LESSER = auto() # <
	GREATER = auto() # >
	MODULO = auto() # %
	AND = auto() # &
	OR = auto() # |
	XOR = auto() # ^
	NOT = auto() # ~

	EQUAL = auto() # =
	PERIOD = auto() # .
	COMMA = auto() # ,
	NEWLINE = auto() # \n

	L_PAREN = auto() # (
	R_PAREN = auto() # )
	L_BRACKET = auto() # [
	R_BRACKET = auto() # ]
	L_CURLY = auto() # {
	R_CURLY = auto() # }

	SHL = auto() # <<
	SHR = auto() # >>

	PLUS_EQUAL = auto() # +=
	MINUS_EQUAL = auto() # -=
	ASTERISK_EQUAL = auto() # *=
	SLASH_EQUAL = auto() # /=
	GREATER_EQUAL = auto() # >=
	LESSER_EQUAL = auto() # <=
	COLON_EQUAL = auto() # :=
	MODULO_EQUAL = auto() # %=
	AND_EQUAL = auto() # &=
	OR_EQUAL = auto() # |=
	XOR_EQUAL = auto() # ^=
	SHL_EQUAL = auto() # <<=
	SHR_EQUAL = auto() # >>=
	NOT_EQUAL = auto() # !=

	EOF = auto()

class ZefReservedKeywords(Enum):
	IF = auto()
	THEN = auto()
	ELSE = auto()
	TRY = auto()
	EXCEPT = auto()
	END = auto()
	SWITCH = auto()
	CASE = auto()
	DEFAULT = auto()

	FOR = auto()
	WHILE = auto()
	CONTINUE = auto()
	BREAK = auto()

	BYTE = auto()
	SHORT = auto()
	INT = auto()
	FLOAT = auto()
	LONG = auto()
	DOUBLE = auto()
	CONST = auto()
	UNSIGNED = auto()
	NULL = auto()

	NEW = auto()
	DELETE = auto()

	NOT = auto()
	AND = auto()
	OR = auto()
	XOR = auto()

	TRUE = auto()
	FALSE = auto()

	DEFINE = auto()
	RETURN = auto()
	TYPE = auto()

	IMPORT = auto()

zeframKeywordStrings = {
	'if' : ZefReservedKeywords.IF,
	'then': ZefReservedKeywords.THEN,
	'else': ZefReservedKeywords.ELSE,
	'try': ZefReservedKeywords.TRY,
	'except': ZefReservedKeywords.EXCEPT,
	'end': ZefReservedKeywords.END,
	'switch': ZefReservedKeywords.SWITCH,
	'case': ZefReservedKeywords.CASE,
	'default': ZefReservedKeywords.DEFAULT,
	'for': ZefReservedKeywords.FOR,
	'while': ZefReservedKeywords.WHILE,
	'continue': ZefReservedKeywords.CONTINUE,
	'break': ZefReservedKeywords.BREAK,
	'byte': ZefReservedKeywords.BYTE,
	'short': ZefReservedKeywords.SHORT,
	'int': ZefReservedKeywords.INT,
	'float': ZefReservedKeywords.FLOAT,
	'long': ZefReservedKeywords.LONG,
	'double': ZefReservedKeywords.DOUBLE,
	'const': ZefReservedKeywords.CONST,
	'unsigned': ZefReservedKeywords.UNSIGNED,
	'null': ZefReservedKeywords.NULL,
	'not': ZefReservedKeywords.NOT,
	'and': ZefReservedKeywords.AND,
	'or': ZefReservedKeywords.OR,
	'xor': ZefReservedKeywords.XOR,
	'true': ZefReservedKeywords.TRUE,
	'false': ZefReservedKeywords.FALSE,
	'define': ZefReservedKeywords.DEFINE,
	'return': ZefReservedKeywords.RETURN,
	'type': ZefReservedKeywords.TYPE,
	'import': ZefReservedKeywords.IMPORT,
}

class ZefToken:
	def __init__(self, token_type, value, line, col, src_file_index):
		self.type = token_type
		self.value = value
		self.line = line
		self.col = col
		self.src_file_index = src_file_index

	def __repr__(self):
		return f'[{self.line},{self.col}] [{self.type} \'{self.value}\']'