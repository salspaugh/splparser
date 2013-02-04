#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
from splparser.exceptions import SPLSyntaxError

tokens = [
    'PIPE',
#    'LBRACKET', TODO: Add support for subsearches anad macros.
#    'RBRACKET',
#    'TIC',
    'ARGS'
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
    'bucketdir': 'BUCKETDIR',
    'chart': 'CHART',
    'cluster': 'CLUSTER',
    'collect': 'COLLECT',
    'concurrency': 'CONCURRENCY',
    'contingency': 'CONTINGENCY',
    'convert': 'CONVERT',
    'correlate': 'CORRELATE',
    'crawl': 'CRAWL',
    'dbinspect': 'DBINSPECT',
    'dedup': 'DEDUP',
    'delete': 'DELETE',
    'delta': 'DELTA',
    'diff': 'DIFF',
    'erex': 'EREX',
    'eval': 'EVAL',
    'eventcount': 'EVENTCOUNT',
    'eventstats': 'EVENTSTATS',
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

t_ignore = ' '

t_PIPE = r'\|'
#t_LBRACKET = r'\['
#t_RBRACKET = r'\]'
#t_TIC = r'`'

def t_ARGS(t):
    r"""(\'[^\']*\')|("[^"]*")|([^|\[\]`\s]+)"""
    t.type = reserved.get(t.value, 'ARGS')
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character '%s'" % badchar)

lexer = ply.lex.lex()

def tokenize(data, debug = False, debuglog = None):
    lexer = ply.lex.lex()
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
