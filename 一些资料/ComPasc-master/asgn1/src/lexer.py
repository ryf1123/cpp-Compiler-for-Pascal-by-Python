#!/usr/bin/env python3

# The core lexer program. Uses PLY

import lex
from tokens import *
import sys
from reserved_tokens import *


def build (debug=True):
    '''
    builds and returns the lexer object according to specifications.
    NOTE: We don't require regex for reserved tokens as we first use the regex for identifier and match in the reserved dict
    '''

    # Should we use tokens for +- or literals?

    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_MULTIPLY = r'\*'
    t_DIVIDE = r'\/'
    t_EQUALS = r'\='
    t_NOTEQUALS = r'\<\>'
    t_LANGLE = r'\<' 
    t_RANGLE = r'\>'
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'
    t_DOT = r'\.'
    t_COMMA = r'\,'
    t_INVERTCOMMA = r'\''
    t_INVERTDOUBLECOMMA = r'\"'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_COLON = r'\:'
    t_SEMICOLON = r'\;'
    t_POWER = r'\^'
    t_ATRATE = r'\@'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_AMPERSAND = r'\&'
    t_PERCENT = r'\%'
    t_DOUBLESTAR = r'\*\*'

    t_ASSIGNTO = r'\:\='
    t_LEQ = r'\<\='
    t_GEQ = r'\>\='
    t_DOUBLESLASH = r'\\\\'


    # define identifier
    def t_RANGE(t):
        r'[0-9]*\.\.[0-9]*'
        return t

    def t_ID(t):
        r'[A-Za-z](_?[A-Za-z0-9])*'
        t.type = reserved.get(t.value.lower(), 'ID')
        return t

    # define number
    def t_NUMBER(t):
        r'[-+]?[0-9]*\.?[0-9]+'   
        return t

    # define character
    def t_CHARACTER(t):
        r"(\'([^\\\'])\')|(\"([^\\\"])\")"
        return t

    # define string
    def t_STRING(t): 
        r"(\"([^\\\"]|(\\.))*\")|(\'([^\\\']|(\\.))*\')"
        escaped = 0 
        str = t.value[1:-1] 
        new_str = "" 
        for i in range(0, len(str)): 
            c = str[i] 
            if escaped: 
                if c == "n": 
                    c = "\n" 
                elif c == "t": 
                    c = "\t" 
                new_str += c 
                escaped = 0 
            else: 
                if c == "\\": 
                    escaped = 1 
                else: 
                    new_str += c 
        t.value = new_str
        return t

    # define comment
    def t_COMMENT(t):
        r"{[^}]*} | \/[\/]+.* | (\*+.*\*)" # first is multi-line, then is single-line

    ### Following is borrowed from PLY tutorial

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        # print("Line: [%d] Illegal character '%s'" % t.lineno,t.value[0])
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build and return the lexer
    if debug:
        return lex.lex(debug=1)
    else:
        return lex.lex()


if __name__ == '__main__':
    # Build the lexer
    lexer = build(debug=False)
    
    if len(sys.argv) > 1:
        f = open(sys.argv[1],"r")
        data = f.read()
        f.close()
    else:
        data = ""
        while 1:
            try:
                data += raw_input() + "\n"
            except:
                break
    
    lex.input(data)
    
    tok_count_dict = {}
    tok_lexeme_dict = {}

    # Tokenize
    while 1:
        tok = lex.token()
        if not tok: break      # No more input
        if tok.type not in tok_count_dict:
            tok_count_dict[tok.type] = 1
            tok_lexeme_dict[tok.type] = [tok.value]
        elif (tok.type != 'ID' or (tok.type == 'ID' and tok.value not in tok_lexeme_dict[tok.type])):
            tok_count_dict[tok.type] += 1
            if (tok.type == 'ID' or tok.type == 'STRING' or tok.type == 'CHARACTER' or tok.type == 'NUMBER'):
                tok_lexeme_dict[tok.type].append(tok.value)
            
    print ('     Token \t Occurances\t Lexemes')
    print ('-------------------------------------------')
    for key, count in tok_count_dict.items(): 
        if (key == 'ID' or key == 'STRING' or key == 'CHARACTER' or key == 'NUMBER'):
            print ('%12s  %12s %12s' % (key, count, tok_lexeme_dict[key][0]))
            for i in range (1,len(tok_lexeme_dict[key])):
                print ('\t \t \t   %12s' % (tok_lexeme_dict[key][i]))
        else:
            print ('%12s  %12s %12s' % (key, count, tok_lexeme_dict[key][0]))
