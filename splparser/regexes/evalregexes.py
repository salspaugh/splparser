
end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|(?=\\)|(?=:)|(?=/)|(?=\.)|(?=-)|(?=\+)|(?=\*)|$)'

internal_field = r'(?:_raw|_time|_indextime|_cd)' + end_of_token

default_field = r'(?:host|index|linecount|punct|source|sourcetype|splunk_server|timestamp)' + end_of_token

default_datetime_field = r'(?:date_hour|date_mday|date_minute|date_month|date_second|date_wday|date_year|date_zone)' + end_of_token

# ---------------- Command specific options: ----------------

sort_fn = r'(auto|str|ip|num)' + end_of_token

chart_opt = r'(?:sep|partial|cont|agg|bins|minspan|span|start|end|fixedrange|usenull|useother|nullstr|otherstr)' + end_of_token

stats_fn = r'(?:avg|c|count|dc|distinct_count|earliest|estdc|estdc_error|first|last|latest|list|max|mean|median|min|mode|per_day|per_hour|per_minute|per_second|range|stdev|stdevp|sumsq|values|var|varp|p1|p2|p3|p4|p5|p6|p7|p8|p9|p10|p11|p12|p13|p14|p15|p16|p17|p18|p19|p20|p21|p22|p23|p24|p25|p26|p27|p28|p29|p30|p31|p32|p33|p34|p35|p36|p37|p38|p39|p40|p41|p42|p43|p44|p45|p46|p47|p48|p49|p50|p51|p52|p53|p54|p55|p56|p57|p58|p59|p60|p61|p62|p63|p64|p65|p66|p67|p68|p69|p70|p71|p72|p73|p74|p75|p76|p77|p78|p79|p80|p81|p82|p83|p84|p85|p86|p87|p88|p89|p90|p91|p92|p93|p94|p95|p96|p97|p98|p99|p100|perc1|perc2|perc3|perc4|perc5|perc6|perc7|perc8|perc9|perc10|perc11|perc12|perc13|perc14|perc15|perc16|perc17|perc18|perc19|perc20|perc21|perc22|perc23|perc24|perc25|perc26|perc27|perc28|perc29|perc30|perc31|perc32|perc33|perc34|perc35|perc36|perc37|perc38|perc39|perc40|perc41|perc42|perc43|perc44|perc45|perc46|perc47|perc48|perc49|perc50|perc51|perc52|perc53|perc54|perc55|perc56|perc57|perc58|perc59|perc60|perc61|perc62|perc63|perc64|perc65|perc66|perc67|perc68|perc69|perc70|perc71|perc72|perc73|perc74|perc75|perc76|perc77|perc78|perc79|perc80|perc81|perc82|perc83|perc84|perc85|perc86|perc87|perc88|perc89|perc90|perc91|perc92|perc93|perc94|perc95|perc96|perc97|perc98|perc99|perc100)' + end_of_token 

stats_opt = r'(?:allnum|delim)' + end_of_token

eventstats_opt = r'(?:allnum)' + end_of_token

streamstats_opt = r'(?:current|window|global|allnum)' + end_of_token

tstats_opt = r'(?:prestats|local|append|summariesonly|sid|datamodel|span)' + end_of_token

eval_fn = r'(?:abs|case|ceil|ceiling|cidrmatch|coalesce|commands|exact|exp|floor|if|ifnull|isbool|isint|isnotnull|isnull|isnum|isstr|len|like|ln|log|lower|ltrim|match|md5|mvappend|mvcount|mvindex|mvfilter|mvjoin|mvrange|mvzip|now|null|nullif|pi|pow|random|relative_time|replace|round|rtrim|searchmatch|sigfig|spath|split|sqrt|strftime|strptime|substr|time|tonumber|tostring|trim|typeof|upper|urldecode|validate)' + end_of_token

common_fn = r'(?:max|min|sum)' + end_of_token

common_opt = r'(?:limit)' + end_of_token

head_opt = r'(?:null|keeplast)' + end_of_token

inn = r'(?:in)' + end_of_token
notin = r'(?:notin)' + end_of_token
top = r'(?:top)' + end_of_token
bottom = r'(?:bottom)' + end_of_token


# ---------------- General argument types: ------------------

plus = r'\+'

minus = r'-'

times = r'\*'

divides = r'\/'

modulus = r'\%' + end_of_token

port = r'\d{1,5}'
slash = r'/\d\d?\d?'

ipv4_part = r'[\d*]{1,3}'
ipv4_addr_no_end = r'(?:(?:' + ipv4_part + r'\.){3}' + ipv4_part + r')(?:(?:' + slash + ')|:' + port + r')?'
ipv4_addr = r'(?:' + ipv4_addr_no_end + end_of_token + r')|(?:"\s*' + ipv4_addr_no_end + r'\s*"' + end_of_token + r')' 

ipv6_part = r'[a-fA-F0-9*]{0,4}'
ipv6_addr_no_end = r'(?:(?:(?:' + ipv6_part + r':){2,7}' + ipv6_part + r')|(?:(?:' + ipv6_part + r':){2,6}' + ipv4_addr_no_end + r'))(?:(?:' + slash + ')|:' + port + r')?'
ipv6_addr = r'(?:' + ipv6_addr_no_end + end_of_token + r')|(?:"\s*' + ipv6_addr_no_end + r'\s*"' + end_of_token + r')' 

ipaddr_no_end = r'(?:(?:' + ipv4_addr_no_end + r')|(?:' + ipv6_addr_no_end + r'))'
ipaddr = r'(?:' + ipv4_addr + r')|(?:' + ipv6_addr + r')'

word_no_end = r'(?:[a-zA-Z]+)'
word = word_no_end + end_of_token 

int_end_of_token = r'(?:' + end_of_token + r'|%|L|l)' 

wc_int_part = r'[\d]'
wc_int = r'[1-9](?:' + wc_int_part + r')*|0'
comma_int = r'[1-9](?:' + wc_int_part + r'){0,2}(?:,(?:' + wc_int_part + r'){3})*'
int_no_end = r'-?(?:(?:' + wc_int + r')|(?:' + comma_int + r'))'
int = r'(?:' + int_no_end + int_end_of_token + r')|(?:"\s*' + int_no_end + r'\s*"' + int_end_of_token + r')' 

float_end_of_token = r'(?:' + end_of_token + r'|%)'
float_no_end = r'-?(?:(?:' + wc_int + r')|(?:' + comma_int + r')|0)\.(?:\d)+'
float = r'(?:' + float_no_end + float_end_of_token + r')|(?:"\s*' + float_no_end + r'\s*"' + float_end_of_token + r')' 

bin_no_end = r'-?0b[0-1*]+(?:\.[0-1*]+)?'
bin = r'(?:' + bin_no_end + int_end_of_token + r')|(?:"\s*' + bin_no_end + r'\s*"' + int_end_of_token + r')' 

oct_no_end = r'-?0[0-7*]+(?:\.[0-7*]+)?'
oct = r'(?:' + oct_no_end + int_end_of_token + r')|(?:"\s*' + oct_no_end + r'\s*"' + int_end_of_token + r')' 

hex_no_end = r'-?0(?:x|X)[0-9a-fA-F*]+(?:\.[0-9a-fA-F*]+)?'
hex = r'(?:' + hex_no_end + int_end_of_token + r')|(?:"\s*' + hex_no_end + r'\s*"' + int_end_of_token + r')' 

id_no_end = r'([a-zA-Z0-9_:]+)+'
id = id_no_end + end_of_token

nbstr = r'"((?<=\\)"|[^"])*"|[^,|()=!<>\[\]\s-]+' + end_of_token

literal = r'(?:"\s*' + word_no_end + r'\s*"' + end_of_token + r')|(?:"\s*' + id_no_end + r'\s*"' + end_of_token + r')'

#literal = r'"(?:[^"]+(?:(\s|-|\(|\)|_|=)+[^"]+)+\s*)"|"[=;|]+[^"]*"|"[^"]*[;=|]+"' + "|'(?:[^']+(?:(\s|-|\(|\)|_|=)+[^']+)+\s*)'|'[=;|]+[^']*'|'[^']*[;=|]+'" + '|"[^"]"' + end_of_token + "|'[^']'" + end_of_token
