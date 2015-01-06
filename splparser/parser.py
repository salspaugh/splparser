#!/usr/bin/env python

import imp
import logging
import os
import ply.yacc

LOGDIR = 'logs'
logging.getLogger().setLevel(logging.DEBUG)

class SPLParser(object):
    """Represents a parser object that can parse SPL queries.

    You should not need to create one of these. Simply import
    parse from the splparser module.
    """

    def __init__(self, lexermod, parsetab_name, parsetab_dir, logname, rulesmod, optimize=True):
        """Creates an SPLParser object.

        :param self: The object being created
        :type self: SPLParser
        :param lexermod: The corresponding lexer module
        :type lexermod: module
        :param parsetab_name: The name of the toplevel parse table file
        :type parsetab_name: str
        :param parsetab_dir: The directory in which to store parse tables
        :type parsetab_dir: str
        :param logname: The name of the log
        :type logname: str
        :param rulesmod: The module containing the top-level rules
        :type rulesmod: module
        :param optimize: Whether or not to write a log (it slows performance and can cause the parser to sometimes fail due to too many open file handles -- one for each command parsed as they have separate log files)
        :type optimize: dir
        :rtype: SPLParser
        """
        self.lexer = lexermod.lex()
        modname, dirname = self.setup_parsetab(parsetab_name, parsetab_dir)
        self.parsetab_name = modname
        self.parsetab_dir = dirname
        self.rules = rulesmod
        self.optimize = optimize
        if not optimize: # TODO: Why is this conditional necessary?
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

    def setup_parsetab(self, parsetab_name, parsetab_dir):

        loaded = False
        try: # check for parsetabs in current installation
            install_location = os.path.dirname(__file__)
            path_to_parsetab = os.path.join(install_location, parsetab_dir, parsetab_name + '.py')
            parsetab = imp.load_source(parsetab_name, path_to_parsetab)
            loaded = True
            install_parsetab_dir = os.path.join(install_location, parsetab_dir)
            return parsetab_name, install_parsetab_dir
        except IOError: # parsetab module does not exist in install location
            pass

        if not loaded:
            try: # check for parsetabs in current directory 
                path_to_parsetab = os.path.join(parsetab_dir, parsetab_name + '.py')
                parsetab = imp.load_source(parsetab_name, path_to_parsetab)
                loaded = True
                return parsetab_name, parsetab_dir
            except IOError: # parsetab module does not exist in current directory
                pass

        if not loaded:
            try: # in case the above failed, create dir for PLY to write parsetabs in
                os.stat(parsetab_dir)
            except:
                try:
                    os.makedirs(parsetab_dir)
                except OSError:
                    msg = "ERROR: Need permission to write to ./%s\n" % parsetab_dir
                    sys.stderr.write(msg)
                    raise

        return parsetab_name, parsetab_dir
    
    def setup_log(self, name):
        """Set up the log so that parsing info can be written out.
        
        :param self: The current SPLParser object
        :type self: SPLParser
        :param name: The name of the log file
        :type name: str
        :rtype: logging.Logger
        """
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
        """Parse the given string.
        
        :param self: The current SPLParser object
        :type self: SPLParser
        :param data: The string to parse
        :type data: str
        :rtype: ParseTreeNode
        """
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
