/*
	example.y

 	Example of a bison specification file.

	Grammar is:
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

				object = [IDENT, IDENT, IDENT]


      To create the syntax analyzer:

        flex example.l
        bison example.y
        g++ example.tab.c -o parser
        parser < inputFileName
 */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include "SymbolTable.h"
#include <stack>

int numLines = 1;
int paramCounter = 0;
std::stack<SYMBOL_TABLE> scopeStack;

void printRule(const char *, const char *);
void printTokenInfo(const char* tokenType, const char* lexeme);
TYPE_INFO findEntryInScope(const std::string entry);
void beginScope();
void endScope();

int yyerror(const char *s)
{
  printf("Line %d: %s\n", numLines, s);
  exit(1);
}

extern "C"
{
    int yyparse(void);
    int yylex(void);
    int yywrap() { return 1; }
}

%}

%union
{
	char* text;
	TYPE_INFO typeInfo;
};

/* Token declarations */
%token  T_IDENT T_INTCONST T_UNKNOWN T_FOO T_NOT T_NE T_EQ T_GE T_LE T_GT T_LT T_AND T_OR T_MULT T_SUB T_DIV T_ADD
			  T_INPUT T_PRINT T_LPAREN T_RPAREN T_LAMBDA T_LETSTAR T_NIL T_T T_STRCONST T_IF

%type <text>T_IDENT
%type <typeInfo> N_CONST N_EXPR N_PARENTHESIZED_EXPR N_IF_EXPR N_ARITHLOGIC_EXPR N_LET_EXPR N_LAMBDA_EXPR N_PRINT_EXPR N_INPUT_EXPR N_EXPR_LIST N_UN_OP N_REL_OP N_ARITH_OP N_BIN_OP
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
	$$.m_type = $1.m_type;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
} | T_IDENT {
	printRule("EXPR", "IDENT");
	TYPE_INFO found = findEntryInScope(std::string($1));
	if (found.m_type == UNDEFINED) {
		yyerror("Undefined identifier");
	}
	$$.m_type = found.m_type;
	$$.m_params = found.m_params;
	$$.m_returnType = found.m_returnType;
} | T_LPAREN N_PARENTHESIZED_EXPR T_RPAREN {
	printRule("EXPR", "( PARENTHESIZED_EXPR )");
	$$.m_type = $2.m_type;
	$$.m_params = $2.m_params;
	$$.m_returnType = $2.m_returnType;

}

N_PARENTHESIZED_EXPR :
N_ARITHLOGIC_EXPR {
	printRule("PARENTHESIZED_EXPR", "ARITHLOGIC_EXPR");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
} | N_IF_EXPR {
	printRule("PARENTHESIZED_EXPR", "IF_EXPR");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
} | N_LET_EXPR {
	printRule("PARENTHESIZED_EXPR", "LET_EXPR");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
} | N_LAMBDA_EXPR {
	printRule("PARENTHESIZED_EXPR", "LAMBDA_EXPR");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
} | N_PRINT_EXPR {
	printRule("PARENTHESIZED_EXPR", "PRINT_EXPR");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
} | N_INPUT_EXPR {
	printRule("PARENTHESIZED_EXPR", "INPUT_EXPR");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
} | N_EXPR_LIST {
	printRule("PARENTHESIZED_EXPR", "EXPR_LIST");
	$$.m_type = $1.m_type;
	$$.m_params = $1.m_params;
	$$.m_returnType = $1.m_returnType;
	//We must set the counting of paramters to 0 since we process this after
	paramCounter = 0;
};

N_ARITHLOGIC_EXPR :
N_UN_OP N_EXPR {
	printRule("ARITHLOGIC_EXPR", "UN_OP EXPR");
	if ($2.m_type == FUNCTION) {
		yyerror("Arg 1 cannot be function");
	}
	$$.m_type = $2.m_type;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;

} | N_BIN_OP N_EXPR N_EXPR {
	printRule("ARITHLOGIC_EXPR", "BIN_OP EXPR EXPR");

	int LHS = $2.m_type;
	int RHS = $3.m_type;
	switch($1.m_type) {
		case REL_OP:
			if (!((LHS & _INT_OR_STR) <= _INT_OR_STR) or LHS == FUNCTION or LHS == _BOOL) {
				yyerror("Arg 1 must be integer or string");
			}
			if (!((RHS & _INT_OR_STR) <= _INT_OR_STR) or RHS == FUNCTION or RHS == _BOOL) {
				yyerror("Arg 2 must be integer or string");
			}
			$$.m_type = _BOOL;
			break;

		case LOG_OP:
			if(LHS == FUNCTION) {
				yyerror("Arg 1 cannot be function");
			}
			if(RHS == FUNCTION) {
				yyerror("Arg 2 cannot be function");
			}
			$$.m_type = _BOOL;
			break;

		default:
			if((LHS & _INT) != _INT) {
				yyerror("Arg 1 must be integer");
			}
			if((RHS & _INT) != _INT) {
				yyerror("Arg 2 must be integer");
			}
			$$.m_type = _INT;
			break;
	}

};

N_IF_EXPR :
T_IF N_EXPR N_EXPR N_EXPR {
	printRule("IF_EXPR", "if EXPR EXPR EXPR");
	if ($2.m_type == FUNCTION) {
		yyerror("Arg 1 cannot be function");
	} else if ($3.m_type == FUNCTION) {
		yyerror("Arg 2 cannot be function");
	} else if ($4.m_type == FUNCTION) {
		yyerror("Arg 3 cannot be function");
	}
	$$.m_type = ($2.m_type | $3.m_type);
};

N_LET_EXPR :
T_LETSTAR T_LPAREN N_ID_EXPR_LIST T_RPAREN N_EXPR {
	printRule("LET_EXPR", "let* ( ID_EXPR_LIST ) EXPR");
	$$.m_type = $5.m_type;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
	endScope();
	if($5.m_type == FUNCTION) {
		yyerror("Arg 2 cannot be function");
	}
};

N_ID_EXPR_LIST :
/* epsilon */ {
	printRule("ID_EXPR_LIST", "epsilon");
} | N_ID_EXPR_LIST T_LPAREN T_IDENT N_EXPR T_RPAREN {
	printRule("ID_EXPR_LIST", "ID_EXPR_LIST ( IDENT EXPR )");
	bool exists = scopeStack.top().addEntry(SYMBOL_TABLE_ENTRY(std::string($3), $4.m_type, $4.m_params, $4.m_returnType));
	if (!exists) {
		yyerror("Multiply defined identifier");
	}



};

N_LAMBDA_EXPR :
T_LAMBDA T_LPAREN N_ID_LIST T_RPAREN N_EXPR {
	printRule("LAMBDA_EXPR", "lambda ( ID_LIST ) EXPR");
	$$.m_type = FUNCTION;
	$$.m_params = scopeStack.top().size(); //Number of parameters is the number of entries in the top symbol table
	$$.m_returnType = $5.m_type; //return type is the type of N_EXPR
	endScope();
	if($5.m_type == FUNCTION) {
		yyerror("Arg 2 cannot be function");
	}
};

N_ID_LIST :
/* epsilon */ {
	printRule("ID_LIST", "epsilon");
} | N_ID_LIST T_IDENT {
	printRule("ID_LIST", "ID_LIST IDENT");
	bool exists = scopeStack.top().addEntry(SYMBOL_TABLE_ENTRY(std::string($2), _INT, NOT_APPLICABLE, NOT_APPLICABLE));
	if (!exists) {
		yyerror("Multiply defined identifier");
	}

};

N_PRINT_EXPR :
T_PRINT N_EXPR {
	printRule("PRINT_EXPR", "print EXPR");
	if($2.m_type == FUNCTION) {
		yyerror("Arg 1 cannot be function");
	}
	$$.m_type = $2.m_type;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
};

N_INPUT_EXPR :
T_INPUT {
	printRule("INPUT_EXPR", "input");
	$$.m_type = _INT_OR_STR;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
};

N_EXPR_LIST :
N_EXPR N_EXPR_LIST {
	//Is this the first N_EXPR in the N_EXPR_LIST?
	printRule("EXPR_LIST", "EXPR EXPR_LIST");
	if($1.m_type == FUNCTION) {
		if($1.m_params != paramCounter){
			//printf("PARAMCOUNTER %d", paramCounter);
			if(paramCounter > $1.m_params) {
				yyerror("Too many parameters in function call");
			}
			else {
				yyerror("Too few parameters in function call");
			}
		}
		if($1.m_returnType == FUNCTION) { //Just beingg safe
			yyerror("CHANGE LATER, N_EXPR_LIST CANNOT BE A FUNCITON, FUNCTION RETURNS FUNCTION");
		}
		$$.m_type = $1.m_returnType;
		$$.m_params = NOT_APPLICABLE;
		$$.m_returnType = NOT_APPLICABLE;

	}
	else {
		paramCounter++;
		$$.m_type = $1.m_type;
		$$.m_params = NOT_APPLICABLE;
		$$.m_returnType = NOT_APPLICABLE;
	}
} | N_EXPR {
	printRule("EXPR_LIST", "EXPR");
	if($1.m_type == FUNCTION) {
		if($1.m_params != paramCounter){
			//printf("PARAMCOUNTER %d", paramCounter);
			if(paramCounter > $1.m_params) {
				yyerror("Too many parameters in function call");
			}
			else {
				yyerror("Too few parameters in function call");
			}
		}
		if($1.m_returnType == FUNCTION) { //Just beingg safe
			yyerror("CHANGE LATER, N_EXPR_LIST CANNOT BE A FUNCITON, FUNCTION RETURNS FUNCTION");
		}
		$$.m_type = $1.m_returnType;
		$$.m_params = NOT_APPLICABLE;
		$$.m_returnType = NOT_APPLICABLE;
	}
	else {
		paramCounter++;
		$$.m_type = $1.m_type;
		$$.m_params = NOT_APPLICABLE;
		$$.m_returnType = NOT_APPLICABLE;
	}
};

N_BIN_OP :
N_ARITH_OP {
	printRule("BIN_OP", "ARITH_OP");
	$$.m_type = _INT;
} | N_LOG_OP {
	printRule("BIN_OP", "LOG_OP");
	$$.m_type = LOG_OP;
} | N_REL_OP {
	printRule("BIN_OP", "REL_OP");
	$$.m_type = REL_OP;
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
	$$.m_type = _INT;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
} | T_STRCONST {
	printRule("CONST", "STRCONST");
	$$.m_type = _STR;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
} | T_T {
	printRule("CONST", "t");
	$$.m_type = _BOOL;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
} | T_NIL {
	printRule("CONST", "nil");
	$$.m_type = _BOOL;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
}
%%

#include "lex.yy.c"
extern FILE *yyin;

void printRule(const char *lhs, const char *rhs)
{
  printf("%s -> %s\n", lhs, rhs);
  return;
}

void printTokenInfo(const char* tokenType, const char* lexeme)
{
  printf("TOKEN: %s  LEXEME: %s\n", tokenType, lexeme);
}

TYPE_INFO findEntryInScope(const std::string entry) {
	TYPE_INFO temp;
	if(scopeStack.empty()) {
		return temp;
	}
	TYPE_INFO found = scopeStack.top().findEntry(entry);
	if(found.m_type != UNDEFINED) {
		return found;
	} else {
		SYMBOL_TABLE symbolTable = scopeStack.top();
		scopeStack.pop();
		found = findEntryInScope(entry);
		scopeStack.push(symbolTable);
		return found;
	}
}


void beginScope() {
	scopeStack.push(SYMBOL_TABLE());
	printf("\n___Entering new scope...\n\n");
}

void endScope() {
	scopeStack.pop();
	printf("\n___Exiting scope...\n\n");
}

int main()
{
  do
  {
	yyparse();
  } while (!feof(yyin));
  return(0);
}
