end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|(?=-)|$)'

plus = r'\+'
minus = r'-'

word_no_end = r'(?:[*]*[a-zA-Z0-9]+[*]*)'
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
id = r'([a-zA-Z0-9_"*:]+)+' + end_of_token

#nbstr = r'"((?<=\\)"|[^"])*"|[^,|()=!<>\[\]\s]+' + end_of_token
nbstr = r'"((?<=\\)"|[^"])*"|[^,|()=!<>\[\]\s-]+' + end_of_token

nbstr_sans_at = r'[^,|@()=!<>\[\]\s]+'
email = nbstr_sans_at + r'@' + nbstr_sans_at + end_of_token
