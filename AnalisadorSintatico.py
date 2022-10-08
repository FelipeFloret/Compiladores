from ply.yacc import yacc
from lexico import lexer, tokens


VERBOSE = 1

def p_program(p):
    'program : list_class'

def p_list_class(p):
    '''list_class : list_class class PONTOVIRGULA
        | class PONTOVIRGULA '''
    pass

def p_class(p):
    ''' class : CLASS ID INHERITS ID ABRECHAVES list_feature FECHACHAVES
        | CLASS ID ABRECHAVES list_feature FECHACHAVES
        | CLASS ID ABRECHAVES FECHACHAVES '''
    pass

def p_list_feature(p):
    ''' list_feature : list_feature feature PONTOVIRGULA
    | feature PONTOVIRGULA
    | empty'''
    pass

def p_feature(p):
    ''' feature : ID ABREPARENTESES list_formal FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
    | ID ABREPARENTESES FECHAPARENTESES DOISPONTOS ID ABRECHAVES expr FECHACHAVES
    | ID DOISPONTOS ID ATRIB expr
    | ID DOISPONTOS ID '''
    pass

def p_list_formal(p):
    ''' list_formal : list_formal VIRGULA formal
    | formal
    | empty '''
    pass

def p_formal(p):
    '''formal : ID DOISPONTOS ID '''
    pass

def p_expr(p):
    ''' expr : expr SOMA expr
    | expr SUB expr
    | expr MULTIPLICACAO expr
    | expr DIVISAO expr
    | COMPLE expr
    | expr MENOR expr
    | expr MENORIGUAL expr
    | expr IGUAL expr
    | NOT expr
    | ABREPARENTESES expr FECHAPARENTESES
    | ID
    | NUMERO
    | STRING
    | TRUE
    | FALSE
    | ISVOID expr
    | NEW ID
    | IF expr THEN expr ELSE expr FI
    | WHILE expr LOOP expr POOL
    | ID ATRIB expr
    '''
    pass


def p_ID_expr(p):
    ''' expr : ID ABREPARENTESES list_expr FECHAPARENTESES '''
    pass

def p_list_expr(p):
    '''list_expr : list_expr VIRGULA expr
    | expr
    | empty'''
    pass

def p_arroba_expr(p):
    ''' expr : expr ARROBA ID PONTO ID ABREPARENTESES list_expr FECHAPARENTESES
    | expr PONTO ID ABREPARENTESES list_expr FECHAPARENTESES '''
    pass

def p_expr2(p):
    ''' expr : ABRECHAVES list_expr2 FECHACHAVES '''
    pass

def p_list_expr2(p):
    '''list_expr2 : list_expr2 expr PONTOVIRGULA
        | expr PONTOVIRGULA '''
    pass

def p_let_expr(p):
    '''expr : LET ID DOISPONTOS ID ATRIB expr list_id IN expr
    | LET ID DOISPONTOS ID list_id IN expr
    '''
    pass

def p_list_id(p):
    ''' list_id : VIRGULA ID DOISPONTOS ID ATRIB expr
    | VIRGULA ID DOISPONTOS ID
    | empty'''
    pass

def p_case(p):
    ''' expr : CASE expr OF list_case ESAC
    '''
    pass

def p_list_case(p):
    ''' list_case : ID DOISPONTOS ID SETA expr PONTOVIRGULA '''
    pass

def p_empty(p):
    '''empty : '''
    pass

def p_error(p):
    #print str(dir(p))
    #print str(dir(c_lexer))
    if VERBOSE:
        if p is not None:
            print ("Sintatic error in line:" + str(lexer.lineno)+"  Context error " + str(p.value))
        else:
            print ("Lexico error in line: " + str(lexer.lexer.lineno))
    else:
        raise Exception('Syntax', 'error')

parser = yacc()

arq_open = 'palindrome.cl'
arq = open(arq_open,'r')
leit = arq.read()
aux = parser.parse(leit, lexer = lexer)
print(aux)

