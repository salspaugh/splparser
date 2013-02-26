import splparser.lexer
import splparser.toplevelrules

from splparser.parser import SPLParser

PARSETAB = 'parsetab'
PARSETAB_DIR = '.'

def parse(data):
    parser = SPLParser(splparser.lexer, PARSETAB, PARSETAB_DIR, splparser.toplevelrules)
    return parser.parse(data)

if __name__ == "__main__":
    import sys
    print parse(sys.argv[1:])
