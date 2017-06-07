import ply.lex as lex
import ply.yacc as yacc

states = (
    ('dquoted', 'exclusive'),
    ('squoted', 'exclusive'),
)
tokens = 'STRING'.split()
literals = ['"', "'", ':']

def t_empty_quotes(t):
    r"''|\"\""
    t.type = 'STRING'
    t.value = ''
    return t

def t_single_quote(t):
    r"'"
    t.lexer.push_state('squoted')

t_squoted_STRING = r"(?:.(?!(?<![\\])'))+."

def t_squoted_end(t):
    r"'"
    t.lexer.pop_state()

def t_double_quote(t):
    r'"'
    t.lexer.push_state('dquoted')

t_dquoted_STRING = r'(?:.(?!(?<![\\])"))+.'

def t_dquoted_end(t):
    r'"'
    t.lexer.pop_state()

def t_STRING(t):
    r"[^ :'\"]+"
    return t

t_ignore = ' \t'
t_squoted_ignore = ''
t_dquoted_ignore = ''

def t_ANY_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def p_result_add_bare(p):
    "result : result bare"
    bares, pairs = p[1]
    bares.append(p[2])
    p[0] = (bares, pairs)

def p_result_add_pair(p):
    "result : result pair"
    bares, pairs = p[1]
    if p[2]:
        pairs.update(p[2])
    p[0] = (bares, pairs)

def p_result_bare(p):
    "result : bare"
    p[0] = ([p[1]], {})

def p_result_pair(p):
    "result : pair"
    if p[1]:
        p[0] = ([], p[1])
    else:
        p[0] = ([], {})

def p_bare(p):
    "bare : STRING"
    p[0] = p[1]

def p_pair(p):
    "pair : STRING ':' STRING"
    p[0] = {p[1]: p[3]}

def p_empty_pair(p):
    "pair : STRING ':'"

parser = yacc.yacc()
