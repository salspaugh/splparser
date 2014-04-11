
from splparser.decorators import *

@splcommandrule
def p_cmdexpr_abstract(p):
    """cmdexpr : ABSTRACT arglist
               | ABSTRACT MACRO"""

@notimplemented
def p_cmdexpr_accum(p):
    """cmdexpr : ACCUM
               | ACCUM arglist
               | ACCUM MACRO"""

@notimplemented
def p_cmdexpr_addcoltotals(p):
    """cmdexpr : ADDCOLTOTALS
               | ADDCOLTOTALS arglist
               | ADDCOLTOTALS MACRO"""

@splcommandrule
def p_cmdexpr_addinfo(p):
    """cmdexpr : ADDINFO"""

@splcommandrule
def p_cmdexpr_addtotals(p):
    """cmdexpr : ADDTOTALS
               | ADDTOTALS arglist
               | ADDTOTALS MACRO"""

@notimplemented
def p_cmdexpr_analyzefields(p):
    """cmdexpr : ANALYZEFIELDS
               | ANALYZEFIELDS arglist
               | ANALYZEFIELDS MACRO"""

@notimplemented
def p_cmdexpr_anomalies(p):
    """cmdexpr : ANOMALIES 
               | ANOMALIES arglist
               | ANOMALIES MACRO"""

@notimplemented
def p_cmdexpr_anomalousvalue(p):
    """cmdexpr : ANOMALOUSVALUE 
               | ANOMALOUSVALUE arglist
               | ANOMALOUSVALUE MACRO"""

@splcommandrule
def p_cmdexpr_append(p):
    """cmdexpr : APPEND
               | APPEND arglist
               | APPEND MACRO"""

@splcommandrule
def p_cmdexpr_appendcols(p):
    """cmdexpr : APPENDCOLS
               | APPENDCOLS arglist
               | APPENDCOLS MACRO"""

@notimplemented
def p_cmdexpr_appendpipe(p):
    """cmdexpr : APPENDPIPE 
               | APPENDPIPE arglist
               | APPENDPIPE MACRO"""

@notimplemented
def p_cmdexpr_associate(p):
    """cmdexpr : ASSOCIATE 
               | ASSOCIATE arglist
               | ASSOCIATE MACRO"""

@splcommandrule
def p_cmdexpr_audit(p):
    """cmdexpr : AUDIT"""

@notimplemented
def p_cmdexpr_autoregress(p):
    """cmdexpr : AUTOREGRESS 
               | AUTOREGRESS arglist
               | AUTOREGRESS MACRO"""

@splcommandrule
def p_cmdexpr_bucket(p):
    """cmdexpr : BUCKET arglist
               | BUCKET MACRO
               | BIN_CMD arglist
               | BIN_CMD MACRO"""

@notimplemented
def p_cmdexpr_bucketdir(p):
    """cmdexpr : BUCKETDIR 
               | BUCKETDIR arglist
               | BUCKETDIR MACRO"""

@splcommandrule
def p_cmdexpr_chart(p):
    """cmdexpr : CHART arglist
               | CHART MACRO
               | SICHART arglist
               | SICHART MACRO"""

@notimplemented
def p_cmdexpr_cluster(p):
    """cmdexpr : CLUSTER 
               | CLUSTER arglist
               | CLUSTER MACRO"""

@splcommandrule
def p_cmdexpr_collect(p):
    """cmdexpr : COLLECT arglist
               | COLLECT MACRO"""

@notimplemented
def p_cmdexpr_concurrency(p):
    """cmdexpr : CONCURRENCY 
               | CONCURRENCY arglist
               | CONCURRENCY MACRO"""

@notimplemented
def p_cmdexpr_contingency(p):
    """cmdexpr : CONTINGENCY 
               | CONTINGENCY arglist
               | CONTINGENCY MACRO"""

@splcommandrule
def p_cmdexpr_convert(p):
    """cmdexpr : CONVERT arglist
               | CONVERT MACRO"""

@notimplemented
def p_cmdexpr_correlate(p):
    """cmdexpr : CORRELATE 
               | CORRELATE arglist
               | CORRELATE MACRO"""

@notimplemented
def p_cmdexpr_crawl(p):
    """cmdexpr : CRAWL
               | CRAWL arglist
               | CRAWL MACRO"""

@notimplemented
def p_cmdexpr_datamodel(p):
    """cmdexpr : DATAMODEL 
               | DATAMODEL arglist
               | DATAMODEL MACRO"""

@notimplemented
def p_cmdexpr_dbinspect(p):
    """cmdexpr : DBINSPECT 
               | DBINSPECT arglist
               | DBINSPECT MACRO"""

@splcommandrule
def p_cmdexpr_dedup(p):
    """cmdexpr : DEDUP arglist
               | DEDUP MACRO"""

@splcommandrule
def p_cmdexpr_delete(p):
    """cmdexpr : DELETE"""

@splcommandrule
def p_cmdexpr_delta(p):
    """cmdexpr : DELTA arglist
               | DELTA MACRO"""

@notimplemented
def p_cmdexpr_diff(p):
    """cmdexpr : DIFF 
               | DIFF arglist
               | DIFF MACRO"""

@notimplemented
def p_cmdexpr_erex(p):
    """cmdexpr : EREX 
               | EREX arglist
               | EREX MACRO"""

@splcommandrule
def p_cmdexpr_eval(p):
    """cmdexpr : EVAL arglist
               | EVAL MACRO"""

@notimplemented
def p_cmdexpr_eventcount(p):
    """cmdexpr : EVENTCOUNT 
               | EVENTCOUNT arglist
               | EVENTCOUNT MACRO"""

@splcommandrule
def p_cmdexpr_eventstats(p):
    """cmdexpr : EVENTSTATS arglist
               | EVENTSTATS MACRO"""

@splcommandrule
def p_cmdexpr_export(p):
    """cmdexpr : EXPORT arglist
               | EXPORT MACRO
               | EXPORT"""

@splcommandrule
def p_cmdexpr_extractkv(p):
    """cmdexpr : EXTRACT arglist
               | KV arglist
               | EXTRACT MACRO
               | KV MACRO"""

@splcommandrule
def p_cmdexpr_fieldformat(p):
    """cmdexpr : FIELDFORMAT arglist
               | FIELDFORMAT MACRO"""

@splcommandrule
def p_cmdexpr_fields(p):
    """cmdexpr : FIELDS
               | FIELDS arglist
               | FIELDS MACRO"""

@notimplemented
def p_cmdexpr_fieldsummary(p):
    """cmdexpr : FIELDSUMMARY 
               | FIELDSUMMARY arglist
               | FIELDSUMMARY MACRO"""

@splcommandrule
def p_cmdexpr_filldown(p):
    """cmdexpr : FILLDOWN
               | FILLDOWN arglist
               | FILLDOWN MACRO"""

@splcommandrule
def p_cmdexpr_fillnull(p):
    """cmdexpr : FILLNULL
	           | FILLNULL arglist
               | FILLNULL MACRO"""

@notimplemented
def p_cmdexpr_findtypes(p):
    """cmdexpr : FINDTYPES 
               | FINDTYPES arglist
               | FINDTYPES MACRO"""

@notimplemented
def p_cmdexpr_folderize(p):
    """cmdexpr : FOLDERIZE 
               | FOLDERIZE arglist
               | FOLDERIZE MACRO"""

@notimplemented
def p_cmdexpr_format(p):
    """cmdexpr : FORMAT 
               | FORMAT arglist
               | FORMAT MACRO"""

@splcommandrule
def p_cmdexpr_gauge(p):
    """cmdexpr : GAUGE arglist
               | GAUGE MACRO"""

@notimplemented
def p_cmdexpr_gentimes(p):
    """cmdexpr : GENTIMES
               | GENTIMES arglist
               | GENTIMES MACRO"""

@splcommandrule
def p_cmdexpr_head(p):
    """cmdexpr : HEAD arglist
               | HEAD MACRO"""

@notimplemented
def p_cmdexpr_highlight(p):
    """cmdexpr : HIGHLIGHT 
               | HIGHLIGHT arglist
               | HIGHLIGHT MACRO"""

@splcommandrule
def p_cmdexpr_history(p):
    """cmdexpr : HISTORY
               | HISTORY arglist
               | HISTORY MACRO"""

@notimplemented
def p_cmdexpr_iconify(p):
    """cmdexpr : ICONIFY 
               | ICONIFY arglist
               | ICONIFY MACRO"""

@notimplemented
def p_cmdexpr_input(p):
    """cmdexpr : INPUT 
               | INPUT arglist
               | INPUT MACRO"""

@splcommandrule
def p_cmdexpr_inputcsv(p):
    """cmdexpr : INPUTCSV arglist
               | INPUTCSV MACRO"""

@splcommandrule
def p_cmdexpr_inputlookup(p):
    """cmdexpr : INPUTLOOKUP arglist
               | INPUTLOOKUP MACRO"""

@notimplemented
def p_cmdexpr_iplocation(p):
    """cmdexpr : IPLOCATION 
               | IPLOCATION arglist
               | IPLOCATION MACRO"""

@splcommandrule
def p_cmdexpr_join(p):
    """cmdexpr : JOIN
               | JOIN arglist
               | JOIN MACRO"""

@notimplemented
def p_cmdexpr_kmeans(p):
    """cmdexpr : KMEANS 
               | KMEANS arglist
               | KMEANS MACRO"""

@notimplemented
def p_cmdexpr_kvform(p):
    """cmdexpr : KVFORM 
               | KVFORM arglist
               | KVFORM MACRO"""

@splcommandrule
def p_cmdexpr_loadjob(p):
    """cmdexpr : LOADJOB arglist
               | LOADJOB MACRO"""

@notimplemented
def p_cmdexpr_localize(p):
    """cmdexpr : LOCALIZE 
               | LOCALIZE arglist
               | LOCALIZE MACRO"""

@splcommandrule
def p_cmdexpr_localop(p):
    """cmdexpr : LOCALOP"""

@splcommandrule
def p_cmdexpr_lookup(p):
    """cmdexpr : LOOKUP
               | LOOKUP arglist
               | LOOKUP MACRO"""

@notimplemented
def p_cmdexpr_makecontinuous(p):
    """cmdexpr : MAKECONTINUOUS 
               | MAKECONTINUOUS arglist
               | MAKECONTINUOUS MACRO"""

@splcommandrule
def p_cmdexpr_makemv(p):
    """cmdexpr : MAKEMV arglist
               | MAKEMV MACRO"""

@notimplemented
def p_cmdexpr_map(p):
    """cmdexpr : MAP 
               | MAP arglist
               | MAP MACRO"""

@splcommandrule
def p_cmdexpr_metadata(p):
    """cmdexpr : METADATA arglist
               | METADATA MACRO"""

@notimplemented
def p_cmdexpr_metasearch(p):
    """cmdexpr : METASEARCH 
               | METASEARCH arglist
               | METASEARCH MACRO"""

@splcommandrule
def p_cmdexpr_multikv(p):
    """cmdexpr : MULTIKV 
               | MULTIKV arglist
               | MULTIKV MACRO"""

@notimplemented
def p_cmdexpr_multisearch(p):
    """cmdexpr : MULTISEARCH 
               | MULTISEARCH arglist
               | MULTISEARCH MACRO"""

@splcommandrule
def p_cmdexpr_mvcombine(p):
    """cmdexpr : MVCOMBINE arglist
               | MVCOMBINE MACRO"""

@splcommandrule
def p_cmdexpr_mvexpand(p):
    """cmdexpr : MVEXPAND arglist
               | MVEXPAND MACRO"""

@splcommandrule
def p_cmdexpr_nomv(p):
    """cmdexpr : NOMV arglist
               | NOMV MACRO"""

@splcommandrule
def p_cmdexpr_outlier(p):
    """cmdexpr : OUTLIER
               | OUTLIER arglist
               | OUTLIER MACRO"""

@splcommandrule
def p_cmdexpr_outputcsv(p):
    """cmdexpr : OUTPUTCSV arglist
               | OUTPUTCSV MACRO"""

@splcommandrule
def p_cmdexpr_outputlookup(p):
    """cmdexpr : OUTPUTLOOKUP arglist
               | OUTPUTLOOKUP MACRO"""

@notimplemented
def p_cmdexpr_outputtext(p):
    """cmdexpr : OUTPUTTEXT 
               | OUTPUTTEXT arglist
               | OUTPUTTEXT MACRO"""

@splcommandrule
def p_cmdexpr_overlap(p):
    """cmdexpr : OVERLAP"""

@notimplemented
def p_cmdexpr_predict(p):
    """cmdexpr : PREDICT 
               | PREDICT arglist
               | PREDICT MACRO"""

@notimplemented
def p_cmdexpr_rangemap(p):
    """cmdexpr : RANGEMAP 
               | RANGEMAP arglist
               | RANGEMAP MACRO"""

@splcommandrule
def p_cmdexpr_rare(p):
    """cmdexpr : RARE arglist
               | RARE MACRO
               | SIRARE arglist
               | SIRARE MACRO"""

@splcommandrule
def p_cmdexpr_regex(p):
    """cmdexpr : REGEX
               | REGEX arglist
               | REGEX MACRO"""

@splcommandrule
def p_cmdexpr_relevancy(p):
    """cmdexpr : RELEVANCY"""

@notimplemented
def p_cmdexpr_reltime(p):
    """cmdexpr : RELTIME 
               | RELTIME arglist
               | RELTIME MACRO"""

@splcommandrule
def p_cmdexpr_rename(p):
    """cmdexpr : RENAME arglist
               | RENAME MACRO"""

@splcommandrule
def p_cmdexpr_replace(p):
    """cmdexpr : REPLACE arglist
               | REPLACE MACRO"""

@notimplemented
def p_cmdexpr_rest(p):
    """cmdexpr : REST 
               | REST arglist
               | REST MACRO"""

@notimplemented
def p_cmdexpr_return(p):
    """cmdexpr : RETURN 
               | RETURN arglist
               | RETURN MACRO"""

@splcommandrule
def p_cmdexpr_reverse(p):
    """cmdexpr : REVERSE"""

@splcommandrule
def p_cmdexpr_rex(p):
    """cmdexpr : REX arglist
               | REX MACRO"""

@notimplemented
def p_cmdexpr_rtorder(p):
    """cmdexpr : RTORDER 
               | RTORDER arglist
               | RTORDER MACRO"""

@notimplemented
def p_cmdexpr_run(p):
    """cmdexpr : RUN 
               | RUN arglist
               | RUN MACRO"""

@notimplemented
def p_cmdexpr_savedsearch(p):
    """cmdexpr : SAVEDSEARCH 
               | SAVEDSEARCH arglist
               | SAVEDSEARCH MACRO"""

@notimplemented
def p_cmdexpr_script(p):
    """cmdexpr : SCRIPT 
               | SCRIPT arglist
               | SCRIPT MACRO"""

@notimplemented
def p_cmdexpr_scrub(p):
    """cmdexpr : SCRUB 
               | SCRUB arglist
               | SCRUB MACRO"""

@splcommandrule
def p_cmdexpr_search(p):
   """cmdexpr : SEARCH arglist
              | SEARCH MACRO"""

@notimplemented
def p_cmdexpr_searchtxn(p):
    """cmdexpr : SEARCHTXN 
               | SEARCHTXN arglist
               | SEARCHTXN MACRO"""

@notimplemented
def p_cmdexpr_selfjoin(p):
    """cmdexpr : SELFJOIN 
               | SELFJOIN arglist
               | SELFJOIN MACRO"""

@notimplemented
def p_cmdexpr_set(p):
    """cmdexpr : SET 
               | SET arglist
               | SET MACRO"""

@notimplemented
def p_cmdexpr_setfields(p):
    """cmdexpr : SETFIELDS 
               | SETFIELDS arglist
               | SETFIELDS MACRO"""

@notimplemented
def p_cmdexpr_sendemail(p):
    """cmdexpr : SENDEMAIL 
               | SENDEMAIL arglist
               | SENDEMAIL MACRO"""

@splcommandrule
def p_cmdexpr_sort(p):
    """cmdexpr : SORT arglist
               | SORT MACRO"""

@splcommandrule
def p_cmdexpr_spath(p):
    """cmdexpr : SPATH
               | SPATH arglist 
               | SPATH MACRO"""

@splcommandrule
def p_cmdexpr_stats(p):
    """cmdexpr : STATS arglist
               | STATS MACRO
               | SISTATS arglist
               | SISTATS MACRO"""

@splcommandrule
def p_cmdexpr_strcat(p):
    """cmdexpr : STRCAT arglist
               | STRCAT MACRO"""

@splcommandrule
def p_cmdexpr_streamstats(p):
    """cmdexpr : STREAMSTATS arglist
               | STREAMSTATS MACRO"""

@splcommandrule
def p_cmdexpr_table(p):
    """cmdexpr : TABLE arglist
               | TABLE MACRO"""

@splcommandrule
def p_cmdexpr_tags(p):
    """cmdexpr : TAGS arglist
               | TAGS MACRO"""

@splcommandrule
def p_cmdexpr_tail(p):
    """cmdexpr : TAIL arglist
               | TAIL MACRO"""

@splcommandrule
def p_cmdexpr_timechart(p):
    """cmdexpr : TIMECHART arglist
               | TIMECHART MACRO
               | SITIMECHART arglist
               | SITIMECHART MACRO"""

@splcommandrule
def p_cmdexpr_top(p):
    """cmdexpr : TOP arglist
               | TOP MACRO
               | SITOP arglist
               | SITOP MACRO"""

@notimplemented
def p_cmdexpr_tscollect(p):
    """cmdexpr : TSCOLLECT 
               | TSCOLLECT arglist
               | TSCOLLECT MACRO"""

@splcommandrule
def p_cmdexpr_transaction(p):
    """cmdexpr : TRANSACTION arglist
               | TRANSACTION MACRO"""

@splcommandrule
def p_cmdexpr_transpose(p):
    """cmdexpr : TRANSPOSE
               | TRANSPOSE arglist
               | TRANSPOSE MACRO"""

@notimplemented
def p_cmdexpr_trendline(p):
    """cmdexpr : TRENDLINE 
               | TRENDLINE arglist
               | TRENDLINE MACRO"""

@splcommandrule
def p_cmdexpr_tstats(p):
    """cmdexpr : TSTATS arglist
               | TSTATS MACRO"""

@splcommandrule
def p_cmdexpr_typeahead(p):
    """cmdexpr : TYPEAHEAD arglist
               | TYPEAHEAD MACRO"""

@notimplemented
def p_cmdexpr_typelearner(p):
    """cmdexpr : TYPELEARNER 
               | TYPELEARNER arglist
               | TYPELEARNER MACRO"""

@notimplemented
def p_cmdexpr_typer(p):
    """cmdexpr : TYPER 
               | TYPER arglist
               | TYPER MACRO"""

@splcommandrule
def p_cmdexpr_uniq(p):
    """cmdexpr : UNIQ"""

@notimplemented
def p_cmdexpr_untable(p):
    """cmdexpr : UNTABLE 
               | UNTABLE arglist
               | UNTABLE MACRO"""

@splcommandrule
def p_cmdexpr_where(p):
    """cmdexpr : WHERE arglist
               | WHERE MACRO"""

@notimplemented
def p_cmdexpr_x11(p):
    """cmdexpr : X11 
               | X11 arglist
               | X11 MACRO"""

@splcommandrule
def p_cmdexpr_xmlkv(p):
    """cmdexpr : XMLKV
               | XMLKV arglist
               | XMLKV MACRO"""

@notimplemented
def p_cmdexpr_xmlunescape(p):
    """cmdexpr : XMLUNESCAPE 
               | XMLUNESCAPE arglist
               | XMLUNESCAPE MACRO"""

@splcommandrule
def p_cmdexpr_xpath(p):
    """cmdexpr : XPATH arglist
               | XPATH MACRO"""

@notimplemented
def p_cmdexpr_xyseries(p):
    """cmdexpr : XYSERIES 
               | XYSERIES arglist
               | XYSERIES MACRO"""
