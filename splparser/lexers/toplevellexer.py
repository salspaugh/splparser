import re

from splparser.exceptions import SPLSyntaxError

tokens = [
    'PIPE',
#    'LBRACKET', TODO: Add support for subsearches anad macros.
#    'RBRACKET',
    'MACRO',
    'ARGS'
    ]

reserved = {
##    'abstract': 'ABSTRACT',
##    'accum': 'ACCUM',
##    'addcoltotals': 'ADDCOLTOTALS',
##    'addinfo': 'ADDINFO',
##    'addtotals': 'ADDTOTALS',
##    'analyzefields': 'ANALYZEFIELDS',
##    'anomalies': 'ANOMALIES',
##    'anomalousvalue': 'ANOMALOUSVALUE',
##    'append': 'APPEND',
##    'appendcols': 'APPENDCOLS',
##    'appendpipe': 'APPENDPIPE',
##    'associate': 'ASSOCIATE',
##    'audit': 'AUDIT',
##    'autoregress': 'AUTOREGRESS',
##    'bucket': 'BUCKET',
##    'bucketdir': 'BUCKETDIR',
##    'chart': 'CHART',
##    'cluster': 'CLUSTER',
##    'collect': 'COLLECT',
##    'concurrency': 'CONCURRENCY',
##    'contingency': 'CONTINGENCY',
##    'convert': 'CONVERT',
##    'correlate': 'CORRELATE',
##    'crawl': 'CRAWL',
##    'dbinspect': 'DBINSPECT',
##    'dedup': 'DEDUP',
##    'delete': 'DELETE',
##    'delta': 'DELTA',
##    'diff': 'DIFF',
##    'erex': 'EREX',
#    'eval': 'EVAL',
##    'eventcount': 'EVENTCOUNT',
##    'eventstats': 'EVENTSTATS',
##    'extract': 'EXTRACT',
##    'kv': 'KV',
##    'fieldformat': 'FIELDFORMAT',
    'fields': 'FIELDS',
##    'fieldsummary': 'FIELDSUMMARY',
##    'filldown': 'FILLDOWN',
##    'fillnull': 'FILLNULL',
##    'findtypes': 'FINDTYPES',
##    'folderize': 'FOLDERIZE',
##    'format': 'FORMAT',
##    'gauge': 'GAUGE',
##    'gentimes': 'GENTIMES',
#    'head': 'HEAD',
##    'highlight': 'HIGHLIGHT',
##    'history': 'HISTORY',
##    'iconify': 'ICONIFY',
##    'input': 'INPUT',
##    'inputcsv': 'INPUTCSV',
##    'inputlookup': 'INPUTLOOKUP',
##    'iplocation': 'IPLOCATION',
##    'join': 'JOIN',
##    'kmeans': 'KMEANS',
##    'kvform': 'KVFORM',
##    'loadjob': 'LOADJOB',
##    'localize': 'LOCALIZE',
##    'localop': 'LOCALOP',
#    'lookup': 'LOOKUP',
##    'makecontinuous': 'MAKECONTINUOUS',
##    'makemv': 'MAKEMV',
##    'map': 'MAP',
##    'metadata': 'METADATA',
##    'metasearch': 'METASEARCH',
#    'multikv': 'MULTIKV',
##    'multisearch': 'MULTISEARCH',
##    'mvcombine': 'MVCOMBINE',
##    'mvexpand': 'MVEXPAND',
##    'nomv': 'NOMV',
##    'outlier': 'OUTLIER',
##    'outputcsv': 'OUTPUTCSV',
##    'outputlookup': 'OUTPUTLOOKUP',
##    'outputtext': 'OUTPUTTEXT',
##    'overlap': 'OVERLAP',
##    'predict': 'PREDICT',
##    'rangemap': 'RANGEMAP',
##    'rare': 'RARE',
##    'regex': 'REGEX',
##    'relevancy': 'RELEVANCY',
##    'reltime': 'RELTIME',
##    'rename': 'RENAME',
##    'replace': 'REPLACE',
##    'rest': 'REST',
##    'return': 'RETURN',
##    'reverse': 'REVERSE',
##    'rex': 'REX',
##    'rtorder': 'RTORDER',
##    'run': 'RUN',
##    'savedsearch': 'SAVEDSEARCH',
##    'script': 'SCRIPT',
##    'scrub': 'SCRUB',
    'search': 'SEARCH',
##    'searchtxn': 'SEARCHTXN',
##    'selfjoin': 'SELFJOIN',
##    'set': 'SET',
##    'setfields': 'SETFIELDS',
##    'sendemail': 'SENDEMAIL',
##    'sichart': 'SICHART',
##    'sirare': 'SIRARE',
##    'sistats': 'SISTATS',
##    'sitimechart': 'SITIMECHART',
##    'sitop': 'SITOP',
##    'sort': 'SORT',
##    'spath': 'SPATH',
##    'stats': 'STATS',
##    'strcat': 'STRCAT',
##    'streamstats': 'STREAMSTATS',
##    'table': 'TABLE',
##    'tags': 'TAGS',
##    'tail': 'TAIL',
##    'timechart': 'TIMECHART',
##    'top': 'TOP',
##    'transaction': 'TRANSACTION',
##    'transpose': 'TRANSPOSE',
##    'trendline': 'TRENDLINE',
##    'typeahead': 'TYPEAHEAD',
##    'typelearner': 'TYPELEARNER',
##    'typer': 'TYPER',
##    'uniq': 'UNIQ',
##    'untable': 'UNTABLE',
##    'where': 'WHERE',
##    'x11': 'X11',
##    'xmlkv': 'XMLKV',
##    'xmlunescape': 'XMLUNESCAPE',
##    'xpath': 'XPATH',
##    'xyseries': 'XYSERIES'
}

tokens = tokens + list(reserved.values())

whitespace = ' \t\n\r\f\v'

def nonbreaking_char(c):
    return c not in whitespace and c != '|' and c != '`' and c != '"' and c != "'"

class SPLToken(object):

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return "LexToken(" + str(self.type) + ", '" + str(self.value) + "')"

    def __str__(self):
        return self.__repr__()

def extract_quote(data):
    escaped_slash_holder = "~#888$*$333#~"
    escaped_quote_holder = "~#777$*$222#~"
    quote_char = data[0]
    escaped_quote = r'\"'
    if quote_char == "'":
        escaped_quote = r"\'"
    tmp_data = data.replace('\\', escaped_slash_holder)
    tmp_data = tmp_data.replace(escaped_quote, escaped_quote_holder)
    next_quote_pos = tmp_data[1:].find(quote_char) + 1
    if next_quote_pos == -1:
        raise SPLSyntaxError("Unclosed quote.")
    return data[:next_quote_pos+1] 

class SPLLexer(object):
    
    def __init__(self):
        self.data = None
        self.lexpos = -1

    def input(self, data):
        self.data = data
        self.lexpos = 0

    def token(self):

        if not self.data: return
        if len(self.data) == 0: return
        
        while self.data[0] in whitespace:
            self.data = self.data[1:]
            if len(self.data) == 0: return
            self.lexpos += 1 
        
        if self.data[0] == '|':
            self.data = self.data[1:]
            self.lexpos += 1 
            return SPLToken('PIPE', '|')
        
        for k in reserved.iterkeys():
            if self.data.find(k + ' ') == 0 or self.data == k:
                self.data = self.data[len(k)+1:]
                self.lexpos += len(k) + 1 
                return SPLToken(reserved[k], k)
        
        if self.data[0] == '`':
            end = self.data[1:].find('`') + 1
            macro = self.data[:end+1]
            self.data = self.data[len(macro):]
            self.lexpos += len(macro)
            return SPLToken('MACRO', macro)
        
        args = ''
        while nonbreaking_char(self.data[0]):
            args = ''.join([args, self.data[0]])
            self.data = self.data[1:]
            if len(self.data) == 0: break
            self.lexpos += 1 
        if args:
            return SPLToken('ARGS', args)
        if len(self.data) == 0: return
        
        quotes = ''
        if self.data[0] == '"' or self.data[0] == "'":
            quotes = extract_quote(self.data)
            self.data = self.data[len(quotes):]
            self.lexpos += len(quotes) 
            return SPLToken('ARGS', quotes)

        return None

def lex():
    return SPLLexer()

def tokenize(data, debug = False, debuglog = None):
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
