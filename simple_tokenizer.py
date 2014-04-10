from string import whitespace

def tokenize(query):

    tokens = []
    stack = []
    escaped = False
    escape = "\\"
    quoted = False
    quotechars = ['"', "'", "`"]
    quote = ""
    pipe = "|"

    for char in query:

        if not quoted:

            if char == pipe:
                if escaped:
                    escaped = False
                    stack.append(char)
                    continue
                else:
                    if stack: tokens.append("".join(stack))
                    tokens.append(char)
                    stack = []
                    escaped = False
                    continue

            if char in quotechars:
                if escaped:
                    escaped = False
                    stack.append(char)
                    continue
                else:
                    escaped = False
                    quoted = True
                    quote = char
                    stack.append(char)
                    continue

            if char in whitespace:
                if stack:
                    tokens.append("".join(stack))
                    stack = []
                escaped = False
                continue

            if char == escape:
                if not escaped:
                    escaped = True
                    stack.append(char)
                    continue
                else: # the last character escaped this one
                    escaped = False
                    stack.append(char)
                    continue

            # not pipe, whitespace, quote, or escape
            if escaped: escaped = False
            stack.append(char)
            continue

        if quoted:

            if char in quotechars:
                if escaped:
                    escaped = False
                    stack.append(char)
                    continue
                else:
                    if char == quote:
                        escaped = False
                        quoted = False
                        quote = ""
                        stack.append(char)
                        tokens.append("".join(stack))
                        stack = []
                        continue
                    else:
                        escaped = False
                        stack.append(char)
                        continue

            if char == escape:
                if not escaped:
                    escaped = True
                    stack.append(char)
                    continue
                else: # the last character escaped this one
                    escaped = False
                    stack.append(char)
                    continue

            # not a quote or an escape character
            if escaped: escaped = False
            stack.append(char)
            continue

    if stack: tokens.append("".join(stack))
    return tokens        


print r"search hi"
print tokenize(r"search hi")

print r"search 'hi'"
print tokenize(r"search 'hi'")

print r"search ' this is some stuff '"
print tokenize(r"search ' this is some stuff '")

print r"search ' this is\' a trick'"
print tokenize(r"search ' this is\' a trick'")

print r" `macro` bo backro"
print tokenize(r" `macro` bo backro")

print r"'unclosed quote!"
print tokenize(r"'unclosed quote!")

print r"this had | better split 'not | here though'"
print tokenize(r"this had | better split 'not | here though'")

print r"here '|' is a '`tricky` quote' situation"
print tokenize(r"here '|' is a '`tricky` quote' situation")

print r"\n"
print tokenize(r"\n")
