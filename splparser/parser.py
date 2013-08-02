#!/usr/bin/env python

import imp
import logging
import os
import ply.yacc

LOGDIR = 'logs'
logging.getLogger().setLevel(logging.DEBUG)

class SPLParser(object):

    def __init__(self, lexermod, parsetab_name, parsetab_dir, logname, rulesmod, optimize=True):
        self.lexer = lexermod.lex()
        self.parsetab_name = parsetab_name
        self.parsetab_dir = parsetab_dir
        self.parsetab = self.setup_parsetab()
        self.rules = rulesmod
        self.optimize = optimize
        if not optimize:
            self.log = self.setup_log(logname)
            self.parser = ply.yacc.yacc(module=self.rules, 
                                        debug=True,
                                        debuglog=self.log, 
                                        tabmodule=self.parsetab_name, 
                                        outputdir=self.parsetab_dir,
                                        optimize=optimize)
        else:
            self.parser = ply.yacc.yacc(module=self.rules, 
                                        tabmodule=self.parsetab_name, 
                                        outputdir=self.parsetab_dir,
                                        optimize=optimize)

    def setup_parsetab(self):
        
        loaded = False
        try: # check for parsetabs in current installation
            here = os.path.dirname(__file__)
            path_to_parsetab = os.path.join(here, self.parsetab_dir, self.parsetab_name + '.py')
            parsetab = imp.load_source(self.parsetab_name, path_to_parsetab)
            loaded = True
        except IOError:
            parsetab = self.parsetab_name

        if not loaded:
            try: # check for parsetabs in current directory 
                path_to_parsetab = os.path.join(self.parsetab_dir, self.parsetab_name + '.py')
                parsetab = imp.load_source(self.parsetab_name, path_to_parsetab)
            except IOError:
                parsetab = self.parsetab_name

        if not loaded:
            try: # in case the above failed, create dir for PLY to write parsetabs in
                os.stat(self.parsetab_dir)
            except:
                try:
                    os.makedirs(self.parsetab_dir)
                except OSError:
                    sys.stderr.write("ERROR: \
                                      Need permission to write to ./" + self.parsetab_dir + "\n")
                    raise

        return parsetab
    
    def setup_log(self, name):
        try:
            os.stat(LOGDIR)
        except:
            try:
                os.makedirs(LOGDIR)
            except OSError:
                sys.stderr.write("WARNING: Can't write logs to ./" + LOGDIR + "\n")
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        filehandler = logging.FileHandler(LOGDIR + "/" + str(name) + ".log")
        filehandler.setLevel(logging.DEBUG)
        logger.addHandler(filehandler)
        return logger
    
    def parse(self, data):
        parsetree = None
        try:
            if not self.optimize:
                parsetree = self.parser.parse(data, lexer=self.lexer, debug=self.log)
            else:
                parsetree = self.parser.parse(data, lexer=self.lexer)
        except NotImplementedError:
            raise
        except Exception:
            raise
        return parsetree
