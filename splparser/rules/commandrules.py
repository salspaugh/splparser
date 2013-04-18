
from splparser.decorators import *

@splcommandrule
def p_cmdexpr_abstract(p):
    """cmdexpr : ABSTRACT arglist
               | ABSTRACT MACRO"""

@notimplemented
def p_cmdexpr_accum(p):
    """cmdexpr : ACCUM arglist
               | ACCUM MACRO"""

@notimplemented
def p_cmdexpr_addcoltotals(p):
    """cmdexpr : ADDCOLTOTALS arglist
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
    """cmdexpr : ANALYZEFIELDS arglist
               | ANALYZEFIELDS MACRO"""

@notimplemented
def p_cmdexpr_anomalies(p):
    """cmdexpr : ANOMALIES arglist
               | ANOMALIES MACRO"""

@notimplemented
def p_cmdexpr_anomalousvalue(p):
    """cmdexpr : ANOMALOUSVALUE arglist
               | ANOMALOUSVALUE MACRO"""

@notimplemented
def p_cmdexpr_append(p):
    """cmdexpr : APPEND arglist
               | APPEND MACRO"""

@notimplemented
def p_cmdexpr_appendcols(p):
    """cmdexpr : APPENDCOLS arglist
               | APPENDCOLS MACRO"""

@notimplemented
def p_cmdexpr_appendpipe(p):
    """cmdexpr : APPENDPIPE arglist
               | APPENDPIPE MACRO"""

@notimplemented
def p_cmdexpr_associate(p):
    """cmdexpr : ASSOCIATE arglist
               | ASSOCIATE MACRO"""

@splcommandrule
def p_cmdexpr_audit(p):
    """cmdexpr : AUDIT"""

@notimplemented
def p_cmdexpr_autoregress(p):
    """cmdexpr : AUTOREGRESS arglist
               | AUTOREGRESS MACRO"""

@splcommandrule
def p_cmdexpr_bucket(p):
    """cmdexpr : BUCKET arglist
               | BUCKET MACRO"""

@notimplemented
def p_cmdexpr_bucketdir(p):
    """cmdexpr : BUCKETDIR arglist
               | BUCKETDIR MACRO"""

@splcommandrule
def p_cmdexpr_chart(p):
    """cmdexpr : CHART arglist
               | CHART MACRO
               | SICHART arglist
               | SICHART MACRO"""

@notimplemented
def p_cmdexpr_cluster(p):
    """cmdexpr : CLUSTER arglist
               | CLUSTER MACRO"""

@splcommandrule
def p_cmdexpr_collect(p):
    """cmdexpr : COLLECT arglist
               | COLLECT MACRO"""

@notimplemented
def p_cmdexpr_concurrency(p):
    """cmdexpr : CONCURRENCY arglist
               | CONCURRENCY MACRO"""

@notimplemented
def p_cmdexpr_contingency(p):
    """cmdexpr : CONTINGENCY arglist
               | CONTINGENCY MACRO"""

@splcommandrule
def p_cmdexpr_convert(p):
    """cmdexpr : CONVERT arglist
               | CONVERT MACRO"""

@notimplemented
def p_cmdexpr_correlate(p):
    """cmdexpr : CORRELATE arglist
               | CORRELATE MACRO"""

@notimplemented
def p_cmdexpr_crawl(p):
    """cmdexpr : CRAWL arglist
               | CRAWL MACRO"""

@notimplemented
def p_cmdexpr_dbinspect(p):
    """cmdexpr : DBINSPECT arglist
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
    """cmdexpr : DIFF arglist
               | DIFF MACRO"""

@notimplemented
def p_cmdexpr_erex(p):
    """cmdexpr : EREX arglist
               | EREX MACRO"""

@splcommandrule
def p_cmdexpr_eval(p):
    """cmdexpr : EVAL arglist
               | EVAL MACRO"""

@notimplemented
def p_cmdexpr_eventcount(p):
    """cmdexpr : EVENTCOUNT arglist
               | EVENTCOUNT MACRO"""

@notimplemented
def p_cmdexpr_eventstats(p):
    """cmdexpr : EVENTSTATS arglist
               | EVENTSTATS MACRO"""

@splcommandrule
def p_cmdexpr_export(p):
    """cmdexpr : EXPORT arglist
               | EXPORT MACRO
               | EXPORT"""

@notimplemented
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
    """cmdexpr : FIELDSUMMARY arglist
               | FIELDSUMMARY MACRO"""

@notimplemented
def p_cmdexpr_filldown(p):
    """cmdexpr : FILLDOWN arglist
               | FILLDOWN MACRO"""

@splcommandrule
def p_cmdexpr_fillnull(p):
    """cmdexpr : FILLNULL
	       | FILLNULL arglist
               | FILLNULL MACRO"""

@notimplemented
def p_cmdexpr_findtypes(p):
    """cmdexpr : FINDTYPES arglist
               | FINDTYPES MACRO"""

@notimplemented
def p_cmdexpr_folderize(p):
    """cmdexpr : FOLDERIZE arglist
               | FOLDERIZE MACRO"""

@notimplemented
def p_cmdexpr_format(p):
    """cmdexpr : FORMAT arglist
               | FORMAT MACRO"""

@notimplemented
def p_cmdexpr_gauge(p):
    """cmdexpr : GAUGE arglist
               | GAUGE MACRO"""

@notimplemented
def p_cmdexpr_gentimes(p):
    """cmdexpr : GENTIMES arglist
               | GENTIMES MACRO"""

@splcommandrule
def p_cmdexpr_head(p):
    """cmdexpr : HEAD arglist
               | HEAD MACRO"""

@notimplemented
def p_cmdexpr_highlight(p):
    """cmdexpr : HIGHLIGHT arglist
               | HIGHLIGHT MACRO"""

@notimplemented
def p_cmdexpr_history(p):
    """cmdexpr : HISTORY arglist
               | HISTORY MACRO"""

@notimplemented
def p_cmdexpr_iconify(p):
    """cmdexpr : ICONIFY arglist
               | ICONIFY MACRO"""

@notimplemented
def p_cmdexpr_input(p):
    """cmdexpr : INPUT arglist
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
    """cmdexpr : IPLOCATION arglist
               | IPLOCATION MACRO"""

@notimplemented
def p_cmdexpr_join(p):
    """cmdexpr : JOIN arglist
               | JOIN MACRO"""

@notimplemented
def p_cmdexpr_kmeans(p):
    """cmdexpr : KMEANS arglist
               | KMEANS MACRO"""

@notimplemented
def p_cmdexpr_kvform(p):
    """cmdexpr : KVFORM arglist
               | KVFORM MACRO"""

@notimplemented
def p_cmdexpr_loadjob(p):
    """cmdexpr : LOADJOB arglist
               | LOADJOB MACRO"""

@notimplemented
def p_cmdexpr_localize(p):
    """cmdexpr : LOCALIZE arglist
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
    """cmdexpr : MAKECONTINUOUS arglist
               | MAKECONTINUOUS MACRO"""

@splcommandrule
def p_cmdexpr_makemv(p):
    """cmdexpr : MAKEMV arglist
               | MAKEMV MACRO"""

@notimplemented
def p_cmdexpr_map(p):
    """cmdexpr : MAP arglist
               | MAP MACRO"""

@notimplemented
def p_cmdexpr_metadata(p):
    """cmdexpr : METADATA arglist
               | METADATA MACRO"""

@notimplemented
def p_cmdexpr_metasearch(p):
    """cmdexpr : METASEARCH arglist
               | METASEARCH MACRO"""

@splcommandrule
def p_cmdexpr_multikv(p):
    """cmdexpr : MULTIKV 
               | MULTIKV arglist
               | MULTIKV MACRO"""

@notimplemented
def p_cmdexpr_multisearch(p):
    """cmdexpr : MULTISEARCH arglist
               | MULTISEARCH MACRO"""

@splcommandrule
def p_cmdexpr_mvcombine(p):
    """cmdexpr : MVCOMBINE arglist
               | MVCOMBINE MACRO"""

@splcommandrule
def p_cmdexpr_mvexpand(p):
    """cmdexpr : MVEXPAND arglist
               | MVEXPAND MACRO"""

@notimplemented
def p_cmdexpr_nomv(p):
    """cmdexpr : NOMV arglist
               | NOMV MACRO"""

@notimplemented
def p_cmdexpr_outlier(p):
    """cmdexpr : OUTLIER arglist
               | OUTLIER MACRO"""

@notimplemented
def p_cmdexpr_outputcsv(p):
    """cmdexpr : OUTPUTCSV arglist
               | OUTPUTCSV MACRO"""

@splcommandrule
def p_cmdexpr_outputlookup(p):
    """cmdexpr : OUTPUTLOOKUP arglist
               | OUTPUTLOOKUP MACRO"""

@notimplemented
def p_cmdexpr_outputtext(p):
    """cmdexpr : OUTPUTTEXT arglist
               | OUTPUTTEXT MACRO"""

@splcommandrule
def p_cmdexpr_overlap(p):
    """cmdexpr : OVERLAP"""

@notimplemented
def p_cmdexpr_predict(p):
    """cmdexpr : PREDICT arglist
               | PREDICT MACRO"""

@notimplemented
def p_cmdexpr_rangemap(p):
    """cmdexpr : RANGEMAP arglist
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
    """cmdexpr : RELTIME arglist
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
    """cmdexpr : REST arglist
               | REST MACRO"""

@notimplemented
def p_cmdexpr_return(p):
    """cmdexpr : RETURN arglist
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
    """cmdexpr : RTORDER arglist
               | RTORDER MACRO"""

@notimplemented
def p_cmdexpr_run(p):
    """cmdexpr : RUN arglist
               | RUN MACRO"""

@notimplemented
def p_cmdexpr_savedsearch(p):
    """cmdexpr : SAVEDSEARCH arglist
               | SAVEDSEARCH MACRO"""

@notimplemented
def p_cmdexpr_script(p):
    """cmdexpr : SCRIPT arglist
               | SCRIPT MACRO"""

@notimplemented
def p_cmdexpr_scrub(p):
    """cmdexpr : SCRUB arglist
               | SCRUB MACRO"""

@splcommandrule
def p_cmdexpr_search(p):
   """cmdexpr : SEARCH arglist
              | SEARCH MACRO"""

@notimplemented
def p_cmdexpr_searchtxn(p):
    """cmdexpr : SEARCHTXN arglist
               | SEARCHTXN MACRO"""

@notimplemented
def p_cmdexpr_selfjoin(p):
    """cmdexpr : SELFJOIN arglist
               | SELFJOIN MACRO"""

@notimplemented
def p_cmdexpr_set(p):
    """cmdexpr : SET arglist
               | SET MACRO"""

@notimplemented
def p_cmdexpr_setfields(p):
    """cmdexpr : SETFIELDS arglist
               | SETFIELDS MACRO"""

@notimplemented
def p_cmdexpr_sendemail(p):
    """cmdexpr : SENDEMAIL arglist
               | SENDEMAIL MACRO"""

@splcommandrule
def p_cmdexpr_sort(p):
    """cmdexpr : SORT arglist
               | SORT MACRO"""

@notimplemented
def p_cmdexpr_spath(p):
    """cmdexpr : SPATH arglist
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

@notimplemented
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
    """cmdexpr : TRENDLINE arglist
               | TRENDLINE MACRO"""

@notimplemented
def p_cmdexpr_typeahead(p):
    """cmdexpr : TYPEAHEAD arglist
               | TYPEAHEAD MACRO"""

@notimplemented
def p_cmdexpr_typelearner(p):
    """cmdexpr : TYPELEARNER arglist
               | TYPELEARNER MACRO"""

@notimplemented
def p_cmdexpr_typer(p):
    """cmdexpr : TYPER arglist
               | TYPER MACRO"""

@splcommandrule
def p_cmdexpr_uniq(p):
    """cmdexpr : UNIQ"""

@notimplemented
def p_cmdexpr_untable(p):
    """cmdexpr : UNTABLE arglist
               | UNTABLE MACRO"""

@splcommandrule
def p_cmdexpr_where(p):
    """cmdexpr : WHERE arglist
               | WHERE MACRO"""

@notimplemented
def p_cmdexpr_x11(p):
    """cmdexpr : X11 arglist
               | X11 MACRO"""

@splcommandrule
def p_cmdexpr_xmlkv(p):
    """cmdexpr : XMLKV
               | XMLKV arglist
               | XMLKV MACRO"""

@notimplemented
def p_cmdexpr_xmlunescape(p):
    """cmdexpr : XMLUNESCAPE arglist
               | XMLUNESCAPE MACRO"""

@notimplemented
def p_cmdexpr_xpath(p):
    """cmdexpr : XPATH arglist
               | XPATH MACRO"""

@notimplemented
def p_cmdexpr_xyseries(p):
    """cmdexpr : XYSERIES arglist
               | XYSERIES MACRO"""
