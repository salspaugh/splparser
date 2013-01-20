precedence = (
    ('nonassoc', 'NE' ,'LT', 'LE', 'GE', 'GT'),
    ('left', 'OR'),
    ('left', 'AND', 'COMMA'),
    ('right', 'EQ', 'DCOLON'),
    ('left', 'PLUS', 'MINUS'), 
#    ('left', 'PLUS'), 
#    ('right', 'MINUS'), 
    ('left', 'TIMES', 'DIVIDES'), 
    ('right', 'NOT'),
    ('right', 'UMINUS'),
#    ('left', 'UMINUS'),
#    ('right', 'LPAREN'),
#    ('left', 'RPAREN'),
)

