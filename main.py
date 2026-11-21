import sys
import zeflexer
import zefparser

def main():
	lexer = zeflexer.ZefLexer()
	parser = zefparser.ZefParser()

	lexer.load_source('example.zef')

	while not lexer.is_eof() and not lexer.hadError:
		print(lexer.next_token())

	#parser.parse_ast(lexer)


if __name__ == '__main__':
	main()

