from enum import Enum, auto
from zeftoken import ZefToken, ZefTokenType, zeframKeywordStrings

def is_alpha(c):
	return c.isalpha() or c == '_'

def is_numeric(c):
	return c.isnumeric()

def is_alphanum(c):
	return is_alpha(c) or c.isnumeric()

class ZeframLexerError(Enum):
	FILE_NOT_FOUND = auto()
	ILLEGAL_CHARACTER = auto()
	MALFORMED_FLOAT = auto()
	MALFORMED_STRING = auto()

class ZefLexer:
	def __init__(self):
		self.src_files = []
		self.current_file = -1
		self.src = None
		self.hadError = False

		self.pos = 0
		self.line = 1
		self.col = 1

	def throw_error(self, errortype, data, line = 0, col = 0):
		self.hadError = True

		print('[Lexer] ', end='')

		match errortype:
			case ZeframLexerError.FILE_NOT_FOUND:
				print(f'File not found "{data}"')
			case ZeframLexerError.ILLEGAL_CHARACTER:
				print(f'Illegal symbol "{data}" on line {line}, col {col}')
			case ZeframLexerError.MALFORMED_FLOAT:
				print(f'Malformed float "{data}" on line {line}, col {col}')
			case ZeframLexerError.MALFORMED_STRING:
				print(f'Malformed float "{data}" on line {line}, col {col}')

	def load_source(self, src_file):
		try:
			with open(src_file, 'r') as f:
				self.src = f.read()
			self.current_file += 1
			self.src_files.append(src_file)
		except FileNotFoundError:
			self.throw_error(ZeframLexerError.FILE_NOT_FOUND, src_file)

	def is_eof(self):
		return self.pos == len(self.src)

	def advance(self):
		c = self.src[self.pos]
		self.pos += 1
		self.col += 1

		if c == '\n':
			self.line += 1
			self.col = 1

		return c

	def make_token(self, token_type, value = None):
		return ZefToken(token_type, value, self.line, self.col, self.current_file)

	def peek(self):
		if self.is_eof():
			return None
		return self.src[self.pos]

	def peek_next(self):
		if self.pos + 1 >= len(self.src):
			return None
		return self.src[self.pos + 1]

	def skip_whitespace(self):
		while True:
			c = self.peek()

			if c == ' ' or c == '\t' or c == '\r':
				self.advance()
				continue
			if c == '/' and self.peek_next() == '/':
				while not self.is_eof() and self.peek() != '\n':
					self.advance()
				continue

			break

	def make_number(self):
		start = self.pos - 1

		is_float = self.src[start] == '.'

		while not self.is_eof():
			c = self.peek()

			if c == '.':
				if is_float:
					self.throw_error(ZeframLexerError.MALFORMED_FLOAT, '.', self.line, self.col)
					return None
				is_float = True
			elif not is_numeric(c):
				break

			self.advance()

		num = self.src[start:self.pos]

		if is_float:
			return self.make_token(ZefTokenType.FLOAT, float(num))
		else:
			return self.make_token(ZefTokenType.INT, int(num))


	def make_string(self):
		found_end = False
		start = self.pos
		end = self.pos - 1
		while not self.is_eof():
			c = self.advance()

			if c == '"':
				found_end = True
				end = self.pos - 1
				break

		new_string = self.src[start:end]

		if not found_end:
			self.throw_error(ZeframLexerError.MALFORMED_STRING, new_string)
			return None

		return self.make_token(ZefTokenType.STRING, new_string)

	def make_identifier_or_keyword(self):
		start = self.pos - 1

		while not self.is_eof() and is_alphanum(self.peek()):
			self.advance()

		end = self.pos

		identifier = self.src[start:end]

		if identifier in zeframKeywordStrings:
			return self.make_token(ZefTokenType.KEYWORD, zeframKeywordStrings[identifier])
		else:
			return self.make_token(ZefTokenType.IDENTIFIER, identifier)

	def next_token(self):
		while not self.hadError:
			self.skip_whitespace()

			if self.is_eof():
				return self.make_token(ZefTokenType.EOF, 'EOF')

			c = self.advance()

			if c == '\n' or c == ';':
				return self.make_token(ZefTokenType.NEWLINE, '\\n')

			match c:
				case '+':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.PLUS_EQUAL, '+=')
					else:
						return self.make_token(ZefTokenType.PLUS, '+')
				case '-':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.MINUS_EQUAL, '-=')
					else:
						return self.make_token(ZefTokenType.MINUS, '-')
				case '*':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.ASTERISK_EQUAL, '*=')
					else:
						return self.make_token(ZefTokenType.ASTERISK, '*')
				case '/':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.SLASH_EQUAL, '/=')
					else:
						return self.make_token(ZefTokenType.SLASH, '/')
				case ':':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.COLON_EQUAL, ':=')
					else:
						return self.make_token(ZefTokenType.COLON, ':')
				case '>':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.GREATER_EQUAL, '>=')
					elif self.peek() == '>':
						self.advance()
						if self.peek() == '=':
							self.advance()
							return self.make_token(ZefTokenType.SHR_EQUAL, '>>=')
						else:
							return self.make_token(ZefTokenType.SHR, '>>')
					else:
						return self.make_token(ZefTokenType.GREATER, '>')
				case '<':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.LESSER_EQUAL, '<=')
					elif self.peek() == '<':
						self.advance()
						if self.peek() == '=':
							self.advance()
							return self.make_token(ZefTokenType.SHL_EQUAL, '<<=')
						else:
							return self.make_token(ZefTokenType.SHL, '<<')
					else:
						return self.make_token(ZefTokenType.LESSER, '<')
				case '=':
					return self.make_token(ZefTokenType.EQUAL, '=')
				case ',':
					return self.make_token(ZefTokenType.COMMA, ',')
				case '.':
					if self.peek() and is_numeric(self.peek()):
						return self.make_number()
					else:
						return self.make_token(ZefTokenType.PERIOD, '.')
				case '(':
					return self.make_token(ZefTokenType.L_PAREN, '(')
				case ')':
					return self.make_token(ZefTokenType.R_PAREN, ')')
				case '[':
					return self.make_token(ZefTokenType.L_PAREN, '[')
				case ']':
					return self.make_token(ZefTokenType.R_PAREN, ']')
				case '{':
					return self.make_token(ZefTokenType.L_CURLY, '{')
				case '}':
					return self.make_token(ZefTokenType.R_CURLY, '}')
				case '%':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.MODULO_EQUAL, '%=')
					else:
						return self.make_token(ZefTokenType.MODULO, '%')
				case '&':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.AND_EQUAL, '&=')
					else:
						return self.make_token(ZefTokenType.AND, '&')
				case '|':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.OR_EQUAL, '|=')
					else:
						return self.make_token(ZefTokenType.OR, '|')
				case '^':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.XOR_EQUAL, '^=')
					else:
						return self.make_token(ZefTokenType.XOR, '^')
				case '!':
					if self.peek() == '=':
						self.advance()
						return self.make_token(ZefTokenType.NOT_EQUAL, '!=')

			if c == '"':
				return self.make_string()

			if is_alpha(c):
				return self.make_identifier_or_keyword()

			if is_numeric(c):
				return self.make_number()

			self.throw_error(ZeframLexerError.ILLEGAL_CHARACTER, c, self.line, self.col)