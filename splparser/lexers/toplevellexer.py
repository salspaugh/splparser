from string import whitespace as WHITESPACE

QUOTES = ['"', "'", "`"]
ESCAPE = "\\"
SPECIAL = "|[]"

tokens = [
    'PIPE',
    'LBRACKET',
    'RBRACKET',
    'MACRO',
    'ARGS',
    'USER_DEFINED_COMMAND'
    ]

reserved = {
    'abstract': 'ABSTRACT',
    'accum': 'ACCUM',
    'addcoltotals': 'ADDCOLTOTALS',
    'addinfo': 'ADDINFO',
    'addtotals': 'ADDTOTALS',
    'analyzefields': 'ANALYZEFIELDS',
    'anomalies': 'ANOMALIES',
    'anomalousvalue': 'ANOMALOUSVALUE',
    'append': 'APPEND',
    'appendcols': 'APPENDCOLS',
    'appendpipe': 'APPENDPIPE',
    'associate': 'ASSOCIATE',
    'audit': 'AUDIT',
    'autoregress': 'AUTOREGRESS',
    'bucket': 'BUCKET',
    'bin': 'BIN_CMD', # TODO: Change binary token so this can be "BIN"
    'bucketdir': 'BUCKETDIR',
    'chart': 'CHART',
    'cluster': 'CLUSTER',
    'collect': 'COLLECT',
    'concurrency': 'CONCURRENCY',
    'contingency': 'CONTINGENCY',
    'convert': 'CONVERT',
    'correlate': 'CORRELATE',
    'crawl': 'CRAWL',
    'datamodel': 'DATAMODEL',
    'dbinspect': 'DBINSPECT',
    'dedup': 'DEDUP',
    'delete': 'DELETE',
    'delta': 'DELTA',
    'diff': 'DIFF',
    'erex': 'EREX',
    'eval': 'EVAL',
    'eventcount': 'EVENTCOUNT',
    'eventstats': 'EVENTSTATS',
    'export' : 'EXPORT',
    'extract': 'EXTRACT',
    'kv': 'KV',
    'fieldformat': 'FIELDFORMAT',
    'fields': 'FIELDS',
    'fieldsummary': 'FIELDSUMMARY',
    'filldown': 'FILLDOWN',
    'fillnull': 'FILLNULL',
    'findtypes': 'FINDTYPES',
    'folderize': 'FOLDERIZE',
    'format': 'FORMAT',
    'gauge': 'GAUGE',
    'gentimes': 'GENTIMES',
    'head': 'HEAD',
    'highlight': 'HIGHLIGHT',
    'history': 'HISTORY',
    'iconify': 'ICONIFY',
    'input': 'INPUT',
    'inputcsv': 'INPUTCSV',
    'inputlookup': 'INPUTLOOKUP',
    'iplocation': 'IPLOCATION',
    'join': 'JOIN',
    'kmeans': 'KMEANS',
    'kvform': 'KVFORM',
    'loadjob': 'LOADJOB',
    'localize': 'LOCALIZE',
    'localop': 'LOCALOP',
    'lookup': 'LOOKUP',
    'makecontinuous': 'MAKECONTINUOUS',
    'makemv': 'MAKEMV',
    'map': 'MAP',
    'metadata': 'METADATA',
    'metasearch': 'METASEARCH',
    'multikv': 'MULTIKV',
    'multisearch': 'MULTISEARCH',
    'mvcombine': 'MVCOMBINE',
    'mvexpand': 'MVEXPAND',
    'nomv': 'NOMV',
    'outlier': 'OUTLIER',
    'outputcsv': 'OUTPUTCSV',
    'outputlookup': 'OUTPUTLOOKUP',
    'outputtext': 'OUTPUTTEXT',
    'overlap': 'OVERLAP',
    'predict': 'PREDICT',
    'rangemap': 'RANGEMAP',
    'rare': 'RARE',
    'regex': 'REGEX',
    'relevancy': 'RELEVANCY',
    'reltime': 'RELTIME',
    'rename': 'RENAME',
    'replace': 'REPLACE',
    'rest': 'REST',
    'return': 'RETURN',
    'reverse': 'REVERSE',
    'rex': 'REX',
    'rtorder': 'RTORDER',
    'run': 'RUN',
    'savedsearch': 'SAVEDSEARCH',
    'script': 'SCRIPT',
    'scrub': 'SCRUB',
    'search': 'SEARCH',
    'searchtxn': 'SEARCHTXN',
    'selfjoin': 'SELFJOIN',
    'set': 'SET',
    'setfields': 'SETFIELDS',
    'sendemail': 'SENDEMAIL',
    'sichart': 'SICHART',
    'sirare': 'SIRARE',
    'sistats': 'SISTATS',
    'sitimechart': 'SITIMECHART',
    'sitop': 'SITOP',
    'sort': 'SORT',
    'spath': 'SPATH',
    'stats': 'STATS',
    'strcat': 'STRCAT',
    'streamstats': 'STREAMSTATS',
    'table': 'TABLE',
    'tags': 'TAGS',
    'tail': 'TAIL',
    'timechart': 'TIMECHART',
    'top': 'TOP',
    'transaction': 'TRANSACTION',
    'transpose': 'TRANSPOSE',
    'trendline': 'TRENDLINE',
    'tscollect': 'TSCOLLECT',
    'tstats': 'TSTATS',
    'typeahead': 'TYPEAHEAD',
    'typelearner': 'TYPELEARNER',
    'typer': 'TYPER',
    'uniq': 'UNIQ',
    'untable': 'UNTABLE',
    'where': 'WHERE',
    'x11': 'X11',
    'xmlkv': 'XMLKV',
    'xmlunescape': 'XMLUNESCAPE',
    'xpath': 'XPATH',
    'xyseries': 'XYSERIES'
}

tokens = tokens + list(reserved.values())


class SPLToken(object):

    
    def __init__(self, type, value):
        self.type = type
        self.value = value

    
    def __repr__(self):
        return "LexToken(" + str(self.type) + ", '" + str(self.value) + "')"

    
    def __str__(self):
        return self.__repr__()



class SPLLexer(object):
    

    def __init__(self):
        self.data = None
        self.lexpos = -1
        self.first = True

    def input(self, data):
        self.data = data
        self.lexpos = 0
        
        tokens = []
        stack = []
        escaped = False
        quoted = False
        quotechar = ""

        for char in data:

            if not quoted:

                if char in SPECIAL:
                    if escaped:
                        escaped = False
                        stack.append(char)
                        continue
                    else:
                        if stack: tokens.append("".join(stack))
                        tokens.append(char)
                        stack = []
                        escaped = False
                        continue

                if char in QUOTES:
                    if escaped:
                        escaped = False
                        stack.append(char)
                        continue
                    else:
                        escaped = False
                        quoted = True
                        quotechar = char
                        stack.append(char)
                        continue

                if char in WHITESPACE:
                    if stack:
                        tokens.append("".join(stack))
                        stack = []
                    escaped = False
                    continue

                if char == ESCAPE:
                    if not escaped:
                        escaped = True
                        stack.append(char)
                        continue
                    else: # the last character escaped this one
                        escaped = False
                        stack.append(char)
                        continue

                # not special, whitespace, quotechar, or escape
                if escaped: escaped = False
                stack.append(char)
                continue

            if quoted:

                if char in QUOTES:
                    if escaped:
                        escaped = False
                        stack.append(char)
                        continue
                    else:
                        if char == quotechar:
                            escaped = False
                            quoted = False
                            quotechar = ""
                            stack.append(char)
                            tokens.append("".join(stack))
                            stack = []
                            continue
                        else:
                            escaped = False
                            stack.append(char)
                            continue

                if char == ESCAPE:
                    if not escaped:
                        escaped = True
                        stack.append(char)
                        continue
                    else: # the last character escaped this one
                        escaped = False
                        stack.append(char)
                        continue

                # not a quote or an escape character
                if escaped: escaped = False
                stack.append(char)
                continue

        if stack: tokens.append("".join(stack))
    
        self.tokens = tokens


    def is_macro(self, token):
        return token[0] == "`" and len(token) > 1 and token[-1] == "`"
    

    def is_single_quoted(self, token):
        return token[0] == "'" and len(token) > 1 and token[-1] == "'"
    

    def is_double_quoted(self, token):
        return token[0] == '"' and len(token) > 1 and token[-1] == '"'


    def token(self):
        if not self.tokens: return
        tok = self.tokens.pop(0)
        self.lexpos += len(tok)
        if self.is_macro(tok):     
            self.first = False
            return SPLToken("MACRO", tok)
        if self.is_single_quoted(tok) or self.is_double_quoted(tok):
            self.first = False
            return SPLToken("ARGS", tok)
        if tok in reserved:
            if self.first:
                self.first = False
                return SPLToken(reserved[tok], tok)
            else:
                self.first = False
                return SPLToken("ARGS", tok)
        if tok == "[":
            self.first = True
            return SPLToken("LBRACKET", tok)
        if tok == "]":
            self.first = False
            return SPLToken("RBRACKET", tok)
        if tok == "|":
            self.first = True
            return SPLToken("PIPE", tok)
        if self.first:
            self.first = False
            return SPLToken("USER_DEFINED_COMMAND", tok)
        return SPLToken("ARGS", tok)


def lex():
    return SPLLexer()


def tokenize(data, debug=False, debuglog=None):
    lexer = SPLLexer()
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens


if __name__ == '__main__':
    import sys
    print tokenize(' '.join(sys.argv[1:])) 
