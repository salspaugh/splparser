
from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
from splparser.parser import SPLParser

#def splcommandrule(f):
#    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
#    cmdparser = 'splparser.cmdparsers.' + cmd + 'parser'
#    def helper(p):
#        cmdparse = __import__(cmdparser, fromlist=['__import__ is dumb']).parse
#        try:
#            p[0]  = cmdparse(' '.join(p[1:]))
#        except Exception as e:
#            raise TerminatingSPLSyntaxError(e.message) 
#    helper.__doc__ = f.__doc__
#    return helper

def splcommandrule(f):
    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
    cmdlexer = 'splparser.lexers.' + cmd + 'lexer'
    cmdlexer = __import__(cmdlexer, fromlist=['__import__ is dumb'])
    cmdparsetab = cmd + '_parsetab'
    cmdparsetab_dir = 'parsetabs'
    cmdrules = 'splparser.rules.' + cmd + 'rules'
    cmdrules = __import__(cmdrules, fromlist=['fromlist does nothing'])
    parser = SPLParser(cmdlexer, cmdparsetab, cmdparsetab_dir, cmdrules)
    def helper(p):
        try:
            p[0]  = parser.parse(' '.join(p[1:]))
        except Exception as e:
            raise TerminatingSPLSyntaxError(e.message) 
    helper.__doc__ = f.__doc__
    return helper

def notimplemented(f):
    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
    def helper(p):
        raise NotImplementedError(cmd + " is not yet implemented.")
    helper.__doc__ = f.__doc__
    return helper


