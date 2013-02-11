end_of_token = r'(?:(?=\s)|(?==)|(?=,)|(?=\()|(?=\))|(?=])|(?=\|)|(?=!)|(?=<)|(?=>)|(?=-)|$)'

word_no_end = r'(?:[*]*[a-zA-Z_]+[*]*)'
word = r'(?:' + word_no_end + end_of_token + r')|(?:"\s*' + word_no_end + r'\s*"' + end_of_token + r')' 
