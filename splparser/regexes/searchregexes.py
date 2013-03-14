
end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|$)'


# ---------------- Command specific options: ----------------

common_opt = r'(?:limit)' + end_of_token

top_opt = r'(?:countfield|limit|otherstr|percentfield|showcount|showperc|useother)' + end_of_token

search_key = r'(?:source|sourcetype|hosttag|eventtype|eventttypetag|savedsearch|savedsplunk|timeformat|starttime|endtime|earliest|latest|startsminutesago|starthoursago|startsdaysago|startmonthsago|endminutesago|endhoursago|enddaysago|endmonthsago|searchtimespanhours|searchtimespanminutes|searchtimespandays|searchtimespanmonths|minutesago|hoursago|daysago|monthsago)' + end_of_token

multikv_list_opt = r'(?:filter|FIELDS|fields)' + end_of_token

multikv_single_opt = r'(?:copyattrs|fields|filter|maxnewresults|forceheader|multitable|noheader|rmorig)' + end_of_token

rex_opt = r'(?:field|mode)' + end_of_token

plus = r'\+' + end_of_token

minus = r'-' + end_of_token

# ---------------- General argument types: ------------------

wildcard = r'\*' + end_of_token

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

tld = r'[a-zA-Z]{1,255}'
hostname_no_end = r'(?:(?:[a-zA-Z0-9\-*]+(?:\.[a-zA-Z0-9\-*]+)+)+\.?){1,255}(?::' + port + r')?'
hostname = r'(?:' + hostname_no_end + end_of_token + r')|(?:"\s*' + hostname_no_end + r'\s*"' + end_of_token + r')' 

valid_email_char = r"[a-zA-Z0-9!$%&*+\-/?^_`{|}~#']"
email_local_simple = r'(?:(?:' + valid_email_char + r'\.' + valid_email_char + r')|' + valid_email_char + r'){1,64}'
email_local_quoted = r'''"(?:[a-zA-Z0-9!#$%&\'*+\-/=?^_`{|}~. (),:;<>@\\\[\]]|\"){0,64}"'''
email_domain_simple = r'(?:' + hostname_no_end + r'|' + tld + r')'
email_domain_ip = r'(?:\[' + ipv4_addr_no_end + r'\]|\[' + ipv6_addr_no_end + '\])' 
email_no_end = r'(?:(?:' + email_local_simple + r'@' + email_domain_simple + r')|' + \
               r'(?:' + email_local_simple + r'@' + email_domain_ip + r')|' + \
               r'(?:' + email_local_quoted + r'@' + email_domain_simple + r')|' + \
               r'(?:' + email_local_quoted + r'@' + email_domain_ip + r'))'
email = r'(?:' + email_no_end + end_of_token + r')|(?:"\s*' + email_no_end + r'\s*"' + end_of_token + r')' 

us_phone_no_end = r'(?:(?:(?:1-)?\d{3}-\d{3}-\d{4})|(?:\(\d{3}\)\s*\d{3}-\d{4}))'
us_phone = r'(?:' + us_phone_no_end + end_of_token + r')|(?:"\s*' + us_phone_no_end + r'\s*"' + end_of_token + r')' 

# TODO: Enforce path restrictions. Had to remove length  restrictions because
#       path was being matched instead of query string ...
path_char_set = r"[a-zA-Z0-9_\-~!*'();:@&+$,?%#\[\].]"
unix_abs_path = r'/' + path_char_set + r'*(?:/' + path_char_set + r'+)*/?'
unix_rel_path = r'/?' + path_char_set + r'+(?:/' + path_char_set + r'+)+/?'
windows_abs_path = r'[a-zA-Z]:\\' + path_char_set + r'*(?:\\' + path_char_set + r'+)*\\?'
windows_rel_path = r'(?:(?:[a-zA-Z]:)?\\)?' + path_char_set + r'*(?:\\' + path_char_set + r'+)+\\?'
path_no_end = r'(?:(?:' + unix_abs_path + r')|' + \
              r'(?:' + unix_rel_path + r')|' + \
              r'(?:' + windows_rel_path + r')|' + \
              r'(?:' + windows_rel_path + r'))'
path = r'(?:' + path_no_end + end_of_token + r')|(?:"\s*' + path_no_end + r'\s*"' + end_of_token + r')' 

# TODO: Enforce query string and fragment ID restrictions.
query_string = r'\?[a-zA-Z0-9_=&]+'
fragment_id = r'\#[a-zA-Z0-9_]+'
url_opt_scheme = r'(?:[a-zA-Z]+://)?(?:(?:' + hostname_no_end + r')|(?:' + ipaddr_no_end + r'))(?:' + path + r')?(?:' + query_string + r')?(?:' + fragment_id + r')?'
url_req_scheme = r'[a-zA-Z]+://(?:(?:' + hostname_no_end + r')|[a-zA-Z0-9\-*]+|(?:' + ipaddr_no_end + r'))(?:' + path_no_end + r')?(?:' + query_string + r')?(?:' + fragment_id + r')?'
url_no_end = r'(?:(?:' + url_opt_scheme + r')|(?:' + url_req_scheme + r'))'
url = r'(?:' + url_no_end + end_of_token + r')|(?:"\s*' + url_no_end + r'\s*"' + end_of_token + r')' 

#word_no_end = r'(?:[*]*[a-zA-Z]+[*]*)'
word_no_end = r'(?:[a-zA-Z]+)'
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

id = r'([a-zA-Z0-9_"*:-]+)' + end_of_token

nbstr = r'"((?<=\\)"|[^"])*"|[^,|()=!<>\[\]\s-]+' + end_of_token

nbstr_sans_at = r'[^,|@()=!<>\[\]\s]+'
email = nbstr_sans_at + r'@' + nbstr_sans_at + end_of_token

regular_expression = r'".*"' + end_of_token
