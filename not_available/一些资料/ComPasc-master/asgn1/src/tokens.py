#List of tokens used by Lexer, for tokenization
#taken from https://www.freepascal.org/docs-html/ref/refch1.html

# One thing I fail to understand is the use of literals as given in doc of PLY vs token. Eg: +

from reserved_tokens import *

tokens = [
    #Symbols and operators
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQUALS',
    'NOTEQUALS',
    'LANGLE',                                           #LEFT ANGLE BRACKET '<'
    'RANGLE',
    'LSQUARE',                                          #LEFT SQUARE BRACKET '['
    'RSQUARE',
    'DOT',
    'COMMA',
    'INVERTCOMMA',                                      # '\''     
    'INVERTDOUBLECOMMA',                                # '\"'
    'LPAREN',                                           #LEFT PARENTHESES '('
    'RPAREN',
    'COLON',
    'SEMICOLON',                                        # ';'
    'POWER',                                            # '^'
    'ATRATE',                                           # '@'
    'LCURLY',                                           # '{'
    'RCURLY',
    #'DOLLAR',                                          # will have to check whether to remove or keep these (DOLLAR and HASH)
    #'HASH',
    'AMPERSAND',
    'PERCENT',
    'DOUBLESTAR',                                       # used for calculating powers '**'
    #'CINPUT',                                          # '<<' used for input in C
    #'COUTPUT',                                         # '>>' probably this and the upper symbol are not to tbe used in pascal
    #'LRANGLE',                                         # '<>' again probably not used in our grammar
    'ASSIGNTO',                                         # ':=' (used in assignment statements)
    'LEQ',                                    # '<='
    'GEQ',                                 # '>='
    'DOUBLESLASH',                                      # '//'  
    #Identifiers and constants
    'RANGE',
    'NUMBER',
    'CHARACTER',                                      
    'UNDERSCORE',
    'ID',
    'STRING',
    'COMMENT',
    #Bases of numbers
    #'HEX',
    #'BINARY',
    #'DECIMAL'
] + list(reserved.values())
