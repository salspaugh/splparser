
import inspect
import sys

from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
from splparser.parser import SPLParser

#OPTIMIZE = False
OPTIMIZE = True

def splcommandrule(f):
    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
    cmdlexer = "splparser.lexers." + cmd + "lexer"
    cmdlexer = __import__(cmdlexer, fromlist=["__import__ is dumb"])
    cmdparsetab = cmd + "_parsetab"
    cmdparsetab_dir = "parsetabs"
    cmdlogname = cmd + "rules"
    cmdrules = "splparser.rules." + cmd + "rules"
    cmdrules = __import__(cmdrules, fromlist=["fromlist does nothing"])
    parser = SPLParser(cmdlexer, cmdparsetab, cmdparsetab_dir, cmdlogname, cmdrules, optimize=OPTIMIZE)
    def helper(p):
        try:
            p[0]  = parser.parse(' '.join(p[1:]))
        except Exception as e:
            msg = e.args + (stacktrace(),)
            raise TerminatingSPLSyntaxError(msg) 
    helper.__doc__ = f.__doc__
    return helper

def notimplemented(f):
    cmd = f.__doc__.split(':')[1].split()[0].strip().lower()
    def helper(p):
        raise NotImplementedError(cmd + " is not yet implemented.")
    helper.__doc__ = f.__doc__
    return helper

def stacktrace():
    s = ''
    for frame in inspect.trace():
        s = ''.join([s, ' ', frame[1], ': line ', str(frame[2]), ' in ', frame[3]])
        if frame[4]:
            s = ': '.join([s, frame[4][0].strip()])
        s = ''.join([s, ';'])
    return s


