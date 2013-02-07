
from splparser.decorators import *

@splcommandrule
def p_cmdexpr_eval(p):
    """cmdexpr : EVAL arglist"""

@splcommandrule
def p_cmdexpr_fields(p):
    """cmdexpr : FIELDS
               | FIELDS arglist"""

@splcommandrule
def p_cmdexpr_head(p):
    """cmdexpr : HEAD arglist"""

@splcommandrule
def p_cmdexpr_rename(p):
    """cmdexpr : RENAME arglist"""

@splcommandrule
def p_cmdexpr_reverse(p):
    """cmdexpr : REVERSE"""

@splcommandrule
def p_cmdexpr_search(p):
    """cmdexpr : SEARCH arglist"""

@splcommandrule
def p_cmdexpr_stats(p):
    """cmdexpr : STATS arglist"""

@splcommandrule
def p_cmdexpr_table(p):
    """cmdexpr : TABLE arglist"""

@splcommandrule
def p_cmdexpr_tail(p):
    """cmdexpr : TAIL arglist"""

@splcommandrule
def p_cmdexpr_top(p):
    """cmdexpr : TOP arglist"""

@notimplemented
def p_cmdexpr_abstract(p):
    """cmdexpr : ABSTRACT arglist"""

@notimplemented
def p_cmdexpr_accum(p):
    """cmdexpr : ACCUM arglist"""

@notimplemented
def p_cmdexpr_addcoltotals(p):
    """cmdexpr : ADDCOLTOTALS arglist"""

@notimplemented
def p_cmdexpr_addinfo(p):
    """cmdexpr : ADDINFO arglist"""

@notimplemented
def p_cmdexpr_addtotals(p):
    """cmdexpr : ADDTOTALS arglist"""

@notimplemented
def p_cmdexpr_analyzefields(p):
    """cmdexpr : ANALYZEFIELDS arglist"""

@notimplemented
def p_cmdexpr_anomalies(p):
    """cmdexpr : ANOMALIES arglist"""

@notimplemented
def p_cmdexpr_anomalousvalue(p):
    """cmdexpr : ANOMALOUSVALUE arglist"""

@notimplemented
def p_cmdexpr_append(p):
    """cmdexpr : APPEND arglist"""

@notimplemented
def p_cmdexpr_appendcols(p):
    """cmdexpr : APPENDCOLS arglist"""

@notimplemented
def p_cmdexpr_appendpipe(p):
    """cmdexpr : APPENDPIPE arglist"""

@notimplemented
def p_cmdexpr_associate(p):
    """cmdexpr : ASSOCIATE arglist"""

@notimplemented
def p_cmdexpr_audit(p):
    """cmdexpr : AUDIT arglist"""

@notimplemented
def p_cmdexpr_autoregress(p):
    """cmdexpr : AUTOREGRESS arglist"""

@notimplemented
def p_cmdexpr_bucket(p):
    """cmdexpr : BUCKET arglist"""

@notimplemented
def p_cmdexpr_bucketdir(p):
    """cmdexpr : BUCKETDIR arglist"""

@notimplemented
def p_cmdexpr_chart(p):
    """cmdexpr : CHART arglist"""

@notimplemented
def p_cmdexpr_cluster(p):
    """cmdexpr : CLUSTER arglist"""

@notimplemented
def p_cmdexpr_collect(p):
    """cmdexpr : COLLECT arglist"""

@notimplemented
def p_cmdexpr_concurrency(p):
    """cmdexpr : CONCURRENCY arglist"""

@notimplemented
def p_cmdexpr_contingency(p):
    """cmdexpr : CONTINGENCY arglist"""

@notimplemented
def p_cmdexpr_convert(p):
    """cmdexpr : CONVERT arglist"""

@notimplemented
def p_cmdexpr_correlate(p):
    """cmdexpr : CORRELATE arglist"""

@notimplemented
def p_cmdexpr_crawl(p):
    """cmdexpr : CRAWL arglist"""

@notimplemented
def p_cmdexpr_dbinspect(p):
    """cmdexpr : DBINSPECT arglist"""

@notimplemented
def p_cmdexpr_dedup(p):
    """cmdexpr : DEDUP arglist"""

@notimplemented
def p_cmdexpr_delete(p):
    """cmdexpr : DELETE arglist"""

@notimplemented
def p_cmdexpr_delta(p):
    """cmdexpr : DELTA arglist"""

@notimplemented
def p_cmdexpr_diff(p):
    """cmdexpr : DIFF arglist"""

@notimplemented
def p_cmdexpr_erex(p):
    """cmdexpr : EREX arglist"""

@notimplemented
def p_cmdexpr_eventcount(p):
    """cmdexpr : EVENTCOUNT arglist"""

@notimplemented
def p_cmdexpr_eventstats(p):
    """cmdexpr : EVENTSTATS arglist"""

@notimplemented
def p_cmdexpr_extractkv(p):
    """cmdexpr : EXTRACT arglist
               | KV arglist"""

@notimplemented
def p_cmdexpr_fieldformat(p):
    """cmdexpr : FIELDFORMAT arglist"""

@notimplemented
def p_cmdexpr_fieldsummary(p):
    """cmdexpr : FIELDSUMMARY arglist"""

@notimplemented
def p_cmdexpr_filldown(p):
    """cmdexpr : FILLDOWN arglist"""

@notimplemented
def p_cmdexpr_fillnull(p):
    """cmdexpr : FILLNULL arglist"""

@notimplemented
def p_cmdexpr_findtypes(p):
    """cmdexpr : FINDTYPES arglist"""

@notimplemented
def p_cmdexpr_folderize(p):
    """cmdexpr : FOLDERIZE arglist"""

@notimplemented
def p_cmdexpr_format(p):
    """cmdexpr : FORMAT arglist"""

@notimplemented
def p_cmdexpr_gauge(p):
    """cmdexpr : GAUGE arglist"""

@notimplemented
def p_cmdexpr_gentimes(p):
    """cmdexpr : GENTIMES arglist"""

@notimplemented
def p_cmdexpr_highlight(p):
    """cmdexpr : HIGHLIGHT arglist"""

@notimplemented
def p_cmdexpr_history(p):
    """cmdexpr : HISTORY arglist"""

@notimplemented
def p_cmdexpr_iconify(p):
    """cmdexpr : ICONIFY arglist"""

@notimplemented
def p_cmdexpr_input(p):
    """cmdexpr : INPUT arglist"""

@notimplemented
def p_cmdexpr_inputcsv(p):
    """cmdexpr : INPUTCSV arglist"""

@notimplemented
def p_cmdexpr_inputlookup(p):
    """cmdexpr : INPUTLOOKUP arglist"""

@notimplemented
def p_cmdexpr_iplocation(p):
    """cmdexpr : IPLOCATION arglist"""

@notimplemented
def p_cmdexpr_join(p):
    """cmdexpr : JOIN arglist"""

@notimplemented
def p_cmdexpr_kmeans(p):
    """cmdexpr : KMEANS arglist"""

@notimplemented
def p_cmdexpr_kvform(p):
    """cmdexpr : KVFORM arglist"""

@notimplemented
def p_cmdexpr_loadjob(p):
    """cmdexpr : LOADJOB arglist"""

@notimplemented
def p_cmdexpr_localize(p):
    """cmdexpr : LOCALIZE arglist"""

@notimplemented
def p_cmdexpr_localop(p):
    """cmdexpr : LOCALOP arglist"""

@splcommandrule
def p_cmdexpr_lookup(p):
    """cmdexpr : LOOKUP
               | LOOKUP arglist"""

@notimplemented
def p_cmdexpr_makecontinuous(p):
    """cmdexpr : MAKECONTINUOUS arglist"""

@notimplemented
def p_cmdexpr_makemv(p):
    """cmdexpr : MAKEMV arglist"""

@notimplemented
def p_cmdexpr_map(p):
    """cmdexpr : MAP arglist"""

@notimplemented
def p_cmdexpr_metadata(p):
    """cmdexpr : METADATA arglist"""

@notimplemented
def p_cmdexpr_metasearch(p):
    """cmdexpr : METASEARCH arglist"""

@notimplemented
def p_cmdexpr_multikv(p):
    """cmdexpr : MULTIKV arglist"""

@notimplemented
def p_cmdexpr_multisearch(p):
    """cmdexpr : MULTISEARCH arglist"""

@notimplemented
def p_cmdexpr_mvcombine(p):
    """cmdexpr : MVCOMBINE arglist"""

@notimplemented
def p_cmdexpr_mvexpand(p):
    """cmdexpr : MVEXPAND arglist"""

@notimplemented
def p_cmdexpr_nomv(p):
    """cmdexpr : NOMV arglist"""

@notimplemented
def p_cmdexpr_outlier(p):
    """cmdexpr : OUTLIER arglist"""

@notimplemented
def p_cmdexpr_outputcsv(p):
    """cmdexpr : OUTPUTCSV arglist"""

@notimplemented
def p_cmdexpr_outputlookup(p):
    """cmdexpr : OUTPUTLOOKUP arglist"""

@notimplemented
def p_cmdexpr_outputtext(p):
    """cmdexpr : OUTPUTTEXT arglist"""

@notimplemented
def p_cmdexpr_overlap(p):
    """cmdexpr : OVERLAP arglist"""

@notimplemented
def p_cmdexpr_predict(p):
    """cmdexpr : PREDICT arglist"""

@notimplemented
def p_cmdexpr_rangemap(p):
    """cmdexpr : RANGEMAP arglist"""

@notimplemented
def p_cmdexpr_rare(p):
    """cmdexpr : RARE arglist"""

@notimplemented
def p_cmdexpr_regex(p):
    """cmdexpr : REGEX arglist"""

@notimplemented
def p_cmdexpr_relevancy(p):
    """cmdexpr : RELEVANCY arglist"""

@notimplemented
def p_cmdexpr_reltime(p):
    """cmdexpr : RELTIME arglist"""

@notimplemented
def p_cmdexpr_replace(p):
    """cmdexpr : REPLACE arglist"""

@notimplemented
def p_cmdexpr_rest(p):
    """cmdexpr : REST arglist"""

@notimplemented
def p_cmdexpr_return(p):
    """cmdexpr : RETURN arglist"""

@notimplemented
def p_cmdexpr_rex(p):
    """cmdexpr : REX arglist"""

@notimplemented
def p_cmdexpr_rtorder(p):
    """cmdexpr : RTORDER arglist"""

@notimplemented
def p_cmdexpr_run(p):
    """cmdexpr : RUN arglist"""

@notimplemented
def p_cmdexpr_savedsearch(p):
    """cmdexpr : SAVEDSEARCH arglist"""

@notimplemented
def p_cmdexpr_script(p):
    """cmdexpr : SCRIPT arglist"""

@notimplemented
def p_cmdexpr_scrub(p):
    """cmdexpr : SCRUB arglist"""

@notimplemented
def p_cmdexpr_searchtxn(p):
    """cmdexpr : SEARCHTXN arglist"""

@notimplemented
def p_cmdexpr_selfjoin(p):
    """cmdexpr : SELFJOIN arglist"""

@notimplemented
def p_cmdexpr_set(p):
    """cmdexpr : SET arglist"""

@notimplemented
def p_cmdexpr_setfields(p):
    """cmdexpr : SETFIELDS arglist"""

@notimplemented
def p_cmdexpr_sendemail(p):
    """cmdexpr : SENDEMAIL arglist"""

@notimplemented
def p_cmdexpr_sichart(p):
    """cmdexpr : SICHART arglist"""

@notimplemented
def p_cmdexpr_sirare(p):
    """cmdexpr : SIRARE arglist"""

@notimplemented
def p_cmdexpr_sistats(p):
    """cmdexpr : SISTATS arglist"""

@notimplemented
def p_cmdexpr_sitimechart(p):
    """cmdexpr : SITIMECHART arglist"""

@notimplemented
def p_cmdexpr_sitop(p):
    """cmdexpr : SITOP arglist"""

@notimplemented
def p_cmdexpr_sort(p):
    """cmdexpr : SORT arglist"""

@notimplemented
def p_cmdexpr_spath(p):
    """cmdexpr : SPATH arglist"""

@notimplemented
def p_cmdexpr_strcat(p):
    """cmdexpr : STRCAT arglist"""

@notimplemented
def p_cmdexpr_streamstats(p):
    """cmdexpr : STREAMSTATS arglist"""

@notimplemented
def p_cmdexpr_tags(p):
    """cmdexpr : TAGS arglist"""

@notimplemented
def p_cmdexpr_timechart(p):
    """cmdexpr : TIMECHART arglist"""

@notimplemented
def p_cmdexpr_transaction(p):
    """cmdexpr : TRANSACTION arglist"""

@notimplemented
def p_cmdexpr_transpose(p):
    """cmdexpr : TRANSPOSE arglist"""

@notimplemented
def p_cmdexpr_trendline(p):
    """cmdexpr : TRENDLINE arglist"""

@notimplemented
def p_cmdexpr_typeahead(p):
    """cmdexpr : TYPEAHEAD arglist"""

@notimplemented
def p_cmdexpr_typelearner(p):
    """cmdexpr : TYPELEARNER arglist"""

@notimplemented
def p_cmdexpr_typer(p):
    """cmdexpr : TYPER arglist"""

@notimplemented
def p_cmdexpr_uniq(p):
    """cmdexpr : UNIQ arglist"""

@notimplemented
def p_cmdexpr_untable(p):
    """cmdexpr : UNTABLE arglist"""

@notimplemented
def p_cmdexpr_where(p):
    """cmdexpr : WHERE arglist"""

@notimplemented
def p_cmdexpr_x11(p):
    """cmdexpr : X11 arglist"""

@notimplemented
def p_cmdexpr_xmlkv(p):
    """cmdexpr : XMLKV arglist"""

@notimplemented
def p_cmdexpr_xmlunescape(p):
    """cmdexpr : XMLUNESCAPE arglist"""

@notimplemented
def p_cmdexpr_xpath(p):
    """cmdexpr : XPATH arglist"""

@notimplemented
def p_cmdexpr_xyseries(p):
    """cmdexpr : XYSERIES arglist"""
