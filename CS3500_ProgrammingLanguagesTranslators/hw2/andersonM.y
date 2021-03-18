/*
	example.y

 	Example of a bison specification file.

	Grammar is:

        <expr> -> intconst | ident | foo <identList> 
                  <intconstList>
        <identList> -> lambda | <identList> ident
        <intconstList> -> intconst | <intconstList> intconst

				<N_EXPR> -> N_CONST | T_IDENT | T_LPAREN N_PARENTHESIZED_EXPR T_RPAREN
				<N_CONST> T_INTCONST | T_STRCONST | T_T | T_NIL
				<N_PARENTHESIZED_EXPR> -> N_ARITHLOGIC_EXPR | N_IF_EXPR | N_LET_EXPR | N_LAMBDA_EXPR | N_PRINT_EXPR
																										| N_INPUT_EXPR | N_EXPR_LIST
				<N_ARITHLOGIC_EXPR> -> N_UN_OP N_EXPR | N_BIN_OP N_EXPR N_EXPR
				<N_IF_EXPR> -> T_IF N_EXPR N_EXPR N_EXPR
				<N_LET_EXPR> -> T_LETSTAR T_LPAREN N_ID_EXPR_LIST T_RPAREN N_EXPR
				<N_ID_EXPR_LIST> -> e | N_ID_EXPR_LIST T_LPAREN T_IDENT N_EXPR T_RPAREN
				<N_LAMBDA_EXPR> -> T_LAMBDA T_LPAREN N_ID_LIST T_RPAREN N_EXPR
				<N_ID_LIST> -> e | N_ID_LIST T_IDENT
				<N_PRINT_EXPR> -> T_PRINT N_EXPR
				<N_INPUT_EXPR> -> T_INPUT
				<N_EXPR_LIST> -> N_EXPR N_EXPR_LIST | N_EXPR
				<N_BIN_OP> -> N_ARITH_OP | N_LOG_OP | N_REL_OP
				<N_ARITH_OP> -> T_MULT | T_SUB | T_DIV | T_ADD
				<N_LOG_OP> -> T_AND | T_OR
				<N_REL_OP> -> T_LT | T_GT | T_LE | T_GE | T_EQ | T_NE
				<N_UN_OP> -> T_NOT
				


      To create the syntax analyzer:

        flex example.l
        bison example.y
        g++ example.tab.c -o parser
        parser < inputFileName
 */

%{
#include <stdio.h>

int numLines = 1; 

void printRule(const char *, const char *);
int yyerror(const char *s);
void printTokenInfo(const char* tokenType, const char* lexeme);

extern "C" 
{
    int yyparse(void);
    int yylex(void);
    int yywrap() { return 1; }
}

%}

/* Token declarations */
%token  T_IDENT T_INTCONST T_UNKNOWN T_FOO T_NOT T_NE T_EQ T_GE T_LE T_GT T_LT T_AND T_OR T_MULT T_SUB T_DIV T_ADD
			  T_INPUT T_PRINT T_LPAREN T_RPAREN T_LAMBDA T_LETSTAR T_NIL T_T T_STRCONST T_IF
/* Starting point */
%start		N_START

/* Translation rules */
%%
N_START		: N_EXPR {
	printRule("START", "EXPR");
	printf("\n---- Completed parsing ----\n\n");
	return 0;
};

N_EXPR :
N_CONST {
	printRule("EXPR", "CONST");
} | T_IDENT {
	printRule("EXPR", "IDENT");
} | T_LPAREN N_PARENTHESIZED_EXPR T_RPAREN {
	printRule("EXPR", "( PARENTHESIZED_EXPR )");
}

N_PARENTHESIZED_EXPR :
N_ARITHLOGIC_EXPR {
	printRule("PARENTHESIZED_EXPR", "ARITHLOGIC_EXPR");
} | N_IF_EXPR {
	printRule("PARENTHESIZED_EXPR", "IF_EXPR");
} | N_LET_EXPR {
	printRule("PARENTHESIZED_EXPR", "LET_EXPR");
} | N_LAMBDA_EXPR {
	printRule("PARENTHESIZED_EXPR", "LAMBDA_EXPR");
} | N_PRINT_EXPR {
	printRule("PARENTHESIZED_EXPR", "PRINT_EXPR");
} | N_INPUT_EXPR {
	printRule("PARENTHESIZED_EXPR", "INPUT_EXPR");
} | N_EXPR_LIST {
	printRule("PARENTHESIZED_EXPR", "EXPR_LIST");
};

N_ARITHLOGIC_EXPR :
N_UN_OP N_EXPR {
	printRule("ARITHLOGIC_EXPR", "UN_OP EXPR");
} | N_BIN_OP N_EXPR N_EXPR {
	printRule("ARITHLOGIC_EXPR", "BIN_OP EXPR EXPR");
};

N_IF_EXPR :
T_IF N_EXPR N_EXPR N_EXPR {
	printRule("IF_EXPR", "if EXPR EXPR EXPR");
};

N_LET_EXPR :
T_LETSTAR T_LPAREN N_ID_EXPR_LIST T_RPAREN N_EXPR {
	printRule("LET_EXPR", "let* ( ID_EXPR_LIST ) EXPR");
};

N_ID_EXPR_LIST :
/* epsilon */ {
	printRule("ID_EXPR_LIST", "epsilon");
} | N_ID_EXPR_LIST T_LPAREN T_IDENT N_EXPR T_RPAREN {
	printRule("ID_EXPR_LIST", "( IDENT EXPR )");
};

N_LAMBDA_EXPR :
T_LAMBDA T_LPAREN N_ID_LIST T_RPAREN N_EXPR {
	printRule("LAMBDA_EXPR", "lambda ( ID_LIST ) EXPR");
};

N_ID_LIST :
/* epsilon */ {
	printRule("ID_LIST", "epsilon");
} | N_ID_LIST T_IDENT {
	printRule("ID_LIST", "IDENT");
};

N_PRINT_EXPR :
T_PRINT N_EXPR {
	printRule("PRINT_EXPR", "print EXPR");
};

N_INPUT_EXPR :
T_INPUT {
	printRule("INPUT_EXPR", "input");
};

N_EXPR_LIST :
N_EXPR N_EXPR_LIST {	
	printRule("EXPR_LIST", "EXPR EXPR_LIST");
} | N_EXPR {
	printRule("EXPR_LIST", "EXPR")
};

N_BIN_OP :
N_ARITH_OP {
	printRule("BIN_OP", "ARITH_OP");
} | N_LOG_OP {
	printRule("BIN_OP", "LOG_OP");
} | N_REL_OP {
	printRule("BIN_OP", "REL_OP");
};

N_ARITH_OP :
T_MULT {
	printRule("ARITH_OP" , "*");
} | T_SUB {
	printRule("ARITH_OP" , "-");
} | T_DIV {
	printRule("ARITH_OP" , "/");
} | T_ADD {
	printRule("ARITH_OP" , "+");
};

N_LOG_OP :
T_AND {
	printRule("LOG_OP" , "and");
} | T_OR {
	printRule("LOG_OP" , "or");
};

N_REL_OP :
T_LT {
	printRule("REL_OP" , "<");
} | T_GT {
	printRule("REL_OP" , ">");
} | T_LE {
	printRule("REL_OP" , "<=");
} | T_GE {
	printRule("REL_OP" , ">=");
} | T_EQ {
  printRule("REL_OP" , "=");
} | T_NE {
  printRule("REL_OP" , "/=");
};

N_UN_OP :
T_NOT {
	printRule("UN_OP", "not");
};

N_CONST :
T_INTCONST {
	printRule("CONST", "INTCONST");
} | T_STRCONST {
	printRule("CONST", "STRCONST");
} | T_T {
	printRule("CONST", "t");
} | T_NIL {
	printRule("CONST", "nil");
}
%%

#include "lex.yy.c"
extern FILE *yyin;

void printRule(const char *lhs, const char *rhs) 
{
  printf("%s -> %s\n", lhs, rhs);
  return;
}

int yyerror(const char *s) 
{
  printf("Line %d: %s\n", numLines, s);
  return(1);
}

void printTokenInfo(const char* tokenType, const char* lexeme) 
{
  printf("TOKEN: %s  LEXEME: %s\n", tokenType, lexeme);
}

int main() 
{
  do 
  {
	yyparse();
  } while (!feof(yyin));
  return(0);
}
