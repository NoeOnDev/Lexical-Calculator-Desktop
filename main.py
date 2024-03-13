import re

TOKENS = [
    ('NUMBER', r'\d+(\.\d*)?'),
    ('ADD', r'\+'),
    ('SUB', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LPAR', r'\('),
    ('RPAR', r'\)'),
    ('WS', r'\s+'),
]

def lexer(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, regex in TOKENS:
            regex = re.compile(regex)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_type != 'WS':
                    tokens.append((token_type, text))
                pos = match.end()
                break
        if not match:
            raise SyntaxError(f'Unexpected character: {code[pos]}')
    return tokens