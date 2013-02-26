import splparser.lexers.toplevellexer
import splparser.rules.toplevelrules

from splparser.parser import SPLParser

PARSETAB = 'toplevel_parsetab'
PARSETAB_DIR = 'parsetabs'

def parse(data):
    parser = SPLParser(splparser.lexers.toplevellexer, PARSETAB, PARSETAB_DIR, splparser.rules.toplevelrules)
    return parser.parse(data)

if __name__ == "__main__":
    import sys
    print parse(sys.argv[1:])
