import ply.yacc as yacc 
from lp_lex import tokens, literals 

def p_Program(p):
    "Program : Declarations Statements"
    p[0] = "start\n" + p[2] + "stop\n"

def p_Declarations_list(p):
    "Declarations : Declarations Declaration"

def p_Declarations_empty(p):
    "Declarations : "

def p_Declaration(p):
    'Declaration : Type IdList'

def p_Type_int(p):
    'Type : INT'

def p_Type_str(p):
    'Type : STR'  

def p_IdList_list(p):
    "IdList : IdList ',' id"

def p_IdList_single(p):
    "IdList : id"

def p_Statements_list(p):
    "Statements : Statements Statement"
    p[0] = p[1] + p[2]

def p_Statements_single(p):
    "Statements : Statement"
    p[0] = p[1]

def p_Statement_atrib(p):
    "Statement : id '=' Exp"
    p[0] = p[3]


def p_Statement_print(p):
    "Statement : PRINT '(' PrintArgs ')'"
    p[0] = p[3]

def p_PrintArgs_list(p):
    "PrintArgs : PrintArgs ',' PrintArg"
    p[0] = p[1] + p[3]

def p_PrintArgs_single(p):
    "PrintArgs : PrintArg"
    p[0] = p[1]

def p_PrintArg_str(p):
    "PrintArg : str"
    p[0] = "\t pushs "+p[1]+"\n\t writes\n"

def p_PrintArg_exp(p):
    "PrintArg : Exp"
    p[0] = p[1] + "\twritei\n"

def p_Exp_ad(p):
    "Exp : Exp '+' Term" 
    p[0] = p[1] + p[3] + "add\n"

def p_Exp_sub(p):
    "Exp : Exp '-' Term" 
    p[0] = p[1] + p[3] + "\tsub\n"

def p_Exp_term(p):
    "Exp : Term" 
    p[0] = p[1]

def p_Term_mul(p):
    "Term : Term '*' Factor" 
    p[0] = p[1] + p[3] + "\tmul\n"

def p_Term_div(p):
    "Term : Term '/' Factor" 
    p[0] = p[1] + p[3] + "\tdiv\n"

def p_Term_factor(p):
    "Term : Factor" 
    p[0] = p[1]

def p_Factor_int(p):
    "Factor : INT '(' Exp ')'" 
    

def p_Factor_input(p):
    "Factor : INPUT '(' str ')'" 

def p_Factor_id(p):
    "Factor : id"

def p_Factor_num(p):
    "Factor : num"
    p[0] = "\tpushi "+ p[1]+"\n" 

def p_Statement_while(p):
    "Statement : WHILE '(' Cond ')' CondStatements "

def p_Statement_if(p):
    "Statement : IF '(' Cond ')' CondStatements Else"

def p_Else_empty(p):
    "Else : "

def p_Else(p):
    "Else : ELSE CondStatements"

def p_CondStatements_simple(p):
    "CondStatements : Statement"

def p_CondStatements_compound(p):
    "CondStatements : '{' Statements '}'"

def p_Cond_or(p):
    "Cond : Cond OR Cond2"

def p_Cond(p):
    "Cond : Cond2"

def p_Cond2_and(p):
    "Cond2 : Cond2 AND Cond3"

def p_Cond2(p):
    "Cond2 : Cond3"

def p_Cond3_not(p):
    "Cond3 : NOT ExpRel"

def p_Cond3(p):
    "Cond3 : ExpRel"

def p_Cond3_True(p):
    "Cond3 : TRUE"

def p_Cond3_False(p):
    "Cond3 : FALSE"

def p_ExpRel_gt(p):
    "ExpRel : Exp '>' Exp"

def p_ExpRel_lt(p):
    "ExpRel : Exp '<' Exp"

def p_ExpRel_ge(p):
    "ExpRel : Exp GE Exp"

def p_ExpRel_le(p):
    "ExpRel : Exp LE Exp"

def p_ExpRel_eq(p):
    "ExpRel : Exp EQ Exp"

def p_ExpRel_neq(p):
    "ExpRel : Exp NEQ Exp"

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()
parser.ts = {}

# Read line from input and parse it
import sys
parser.success = True

program = sys.stdin.read()
codigo = parser.parse(program)
if parser.success:
    print("Programa estruturalmente correto!")
    print(codigo)
else:
    print("Programa com erros... Corrija e tente novamente!")
#"""