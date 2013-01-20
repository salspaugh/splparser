
#end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|(?=\\)|(?=:)|(?=/)|$)'
#end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|$)'
end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|(?=-)|$)'

wildcard = r'\*' + end_of_token

plus = r'\+' + end_of_token
#plus = r'\+'

minus = r'-' + end_of_token
#minus = r'-'

#times = r'\*' + end_of_token
times = r'\*'

#divides = r'\/' + end_of_token
divides = r'\/'

modulus = r'\%' + end_of_token

stats_fn = r'(?:avg|c|count|dc|distinct_count|earliest|estdc|estdc_error|first|last|latest|list|max|mean|median|min|mode|per_day|per_hour|per_minute|per_second|range|stdev|stdevp|sum|sumsq|values|var|varp)' + end_of_token 

eval_fn = r'(?:abs|case|ceil|ceiling|cidrmatch|coalesce|commands|exact|exp|floor|if|ifnull|isbool|isint|isnotnull|isnull|isnum|isstr|len|like|ln|log|lower|ltrim|match|max|md5|min|mvappend|mvcount|mvindex|mvfilter|mvjoin|mvrange|mvzip|now|null|nullif|pi|pow|random|relative_time|replace|round|rtrim|searchmatch|sigfig|spath|split|sqrt|strftime|strptime|substr|time|tonumber|tostring|trim|typeof|upper|urldecode|validate)' + end_of_token

search_key = r'(?:source|sourcetype|hosttag|eventtype|eventttypetag|savedsearch|savedsplunk|timeformat|starttime|endtime|earliest|latest|startsminutesago|starthoursago|startsdaysago|startmonthsago|endminutesago|endhoursago|enddaysago|endmonthsago|searchtimespanhours|searchtimespanminutes|searchtimespandays|searchtimespanmonths|minutesago|hoursago|daysago|monthsago)' + end_of_token

common_opt = r'(?:limit)' + end_of_token

head_opt = r'(?:null|keeplast)' + end_of_token

top_opt = r'(?:countfield|limit|otherstr|percentfield|showcount|showperc|useother)' + end_of_token

stats_opt = r'(?:allnum|delim)' + end_of_token

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

word_no_end = r'(?:[*]*[a-zA-Z_]+[*]*)'
word = r'(?:' + word_no_end + end_of_token + r')|(?:"\s*' + word_no_end + r'\s*"' + end_of_token + r')' 

int_end_of_token = r'(?:' + end_of_token + r'|%|L|l)' 

wc_int_part = r'[\d*]'
wc_int = r'[1-9*](?:' + wc_int_part + r')*'
comma_int = r'[1-9*](?:' + wc_int_part + r'){0,2}(?:,(?:' + wc_int_part + r'){3})*'
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

#id = r'([a-zA-Z0-9_"*:-]+)+' + end_of_token
id = r'([a-zA-Z0-9_"*:-]+)+' + end_of_token

#nbstr = r'"((?<=\\)"|[^"])*"|[^,|()=!<>\[\]\s]+' + end_of_token
nbstr = r'"((?<=\\)"|[^"])*"|[^,|()=!<>\[\]\s-]+' + end_of_token

nbstr_sans_at = r'[^,|@()=!<>\[\]\s]+'
email = nbstr_sans_at + r'@' + nbstr_sans_at + end_of_token


# TODO: Add parser for money?
# TODO: Add test cases for percents and longs.
