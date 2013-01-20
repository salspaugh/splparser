class SPLSyntaxError(SyntaxError):
    
    def __init__(self, message, *args):
        self.message = message
        SyntaxError.__init__(self, message)

# HACK: The class below is needed because PLY catches SyntaxErrors and attempts
        to continue parsing. Use this when you want to force it to propagate errors. 
class TerminatingSPLSyntaxError(Exception):
    
    def __init__(self, message, *args):
        self.message = message
        Exception.__init__(self, message)
