from enum import Enum, auto
from zeftoken import ZefTokenType, ZefReservedKeywords
from zeflexer import ZefLexer

class ZefLexerError(Enum):
	UNEXPECTED_EOF = auto()

class ZefAST:
	def __init__(self):
		pass

class ZefSymbolTable:
	def __init__(self):
		pass

class ZefParser:
	def __init__(self):
		self.hadError = False
		self.lexer = None
		self.current = None
		self.next = None

	def parse_ast(self, lexer : ZefLexer):
		self.lexer = lexer
		self.hadError = False

		ast = ZefAST()

		self.current = self.lexer.advance()
		self.next = self.lexer.advance()

		return ast