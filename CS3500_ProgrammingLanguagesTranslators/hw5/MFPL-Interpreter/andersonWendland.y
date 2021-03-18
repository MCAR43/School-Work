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
#include <string.h>
#include "SymbolTable.h"
#include <stack>
#include <iostream>

std::stack<char> operationStack;
TYPE_INFO setMe;
int numLines = 1;
int paramCounter = 0;
std::stack<SYMBOL_TABLE> scopeStack;
void printRule(const char *, const char *);
void printTokenInfo(const char* tokenType, const char* lexeme);
TYPE_INFO findEntryInScope(const char* entry);
void beginScope();
void endScope();
void copyType(TYPE_INFO& dest, const TYPE_INFO source);
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
	int val;
	TYPE_INFO typeInfo;
};

/* Token declarations */
%token  T_IDENT T_INTCONST T_UNKNOWN T_FOO T_NOT T_NE T_EQ T_GE T_LE T_GT T_LT T_AND T_OR T_MULT T_SUB T_DIV T_ADD
			  T_INPUT T_PRINT T_LPAREN T_RPAREN T_LAMBDA T_LETSTAR T_NIL T_T T_STRCONST T_IF

%type <val>T_INTCONST
%type <text>T_IDENT T_STRCONST
%type <typeInfo> N_CONST N_EXPR N_PARENTHESIZED_EXPR N_IF_EXPR N_ARITHLOGIC_EXPR N_LET_EXPR N_PRINT_EXPR N_INPUT_EXPR N_EXPR_LIST N_UN_OP N_REL_OP N_ARITH_OP N_BIN_OP N_LOG_OP
/* Starting point */
%start		N_START

/* Translation rules */
%%
N_START		: N_EXPR {
	printRule("START", "EXPR");
  printf("\n---- Completed parsing ----\n\n");
  int sw = $1.m_type;
  switch(sw){
    case _INT: printf("\nValue of the expression is: %d\n", $1.m_intVal); break;
    case _BOOL: printf("\nValue of the expression is: %s\n", $1.m_boolVal ? "t" : "nil"); break;
    case _STR: printf("\nValue of the expression is: %s\n", $1.m_strVal); break;
	}
  

	return 0;
};

N_EXPR :
N_CONST {
	printRule("EXPR", "CONST");
  copyType($$,$1);
} | T_IDENT {
	printRule("EXPR", "IDENT");
	TYPE_INFO found = findEntryInScope($1);
	if (found.m_type == UNDEFINED) {
		yyerror("Undefined identifier");
	}
	copyType($$,found);
} | T_LPAREN N_PARENTHESIZED_EXPR T_RPAREN {
	printRule("EXPR", "( PARENTHESIZED_EXPR )");
	copyType($$,$2);
}

N_PARENTHESIZED_EXPR :
N_ARITHLOGIC_EXPR {
	printRule("PARENTHESIZED_EXPR", "ARITHLOGIC_EXPR");
  copyType($$,$1);
} | N_IF_EXPR {
	printRule("PARENTHESIZED_EXPR", "IF_EXPR");
	copyType($$,$1);
} | N_LET_EXPR {
	printRule("PARENTHESIZED_EXPR", "LET_EXPR");
  copyType($$,$1);
} | N_PRINT_EXPR {
	printRule("PARENTHESIZED_EXPR", "PRINT_EXPR");
  	copyType($$,$1);
} | N_INPUT_EXPR {
	printRule("PARENTHESIZED_EXPR", "INPUT_EXPR");
  copyType($$,$1);
} | N_EXPR_LIST {
	printRule("PARENTHESIZED_EXPR", "EXPR_LIST");
	copyType($$,setMe);
	copyType($1, setMe);
  //We must set the counting of paramters to 0 since we process this after
	paramCounter = 0;
};

N_ARITHLOGIC_EXPR :
N_UN_OP N_EXPR {
	printRule("ARITHLOGIC_EXPR", "UN_OP EXPR");
	if ($2.m_type == FUNCTION) {
		yyerror("Arg 1 cannot be function");
	}
  $$.m_type = _BOOL;
  $$.m_boolVal = !$2.m_boolVal;
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
      if (RHS == LHS){
        if(RHS == _INT) {
          switch(operationStack.top()) {
            case LT: $$.m_boolVal = $2.m_intVal < $3.m_intVal; break;
            case GT: $$.m_boolVal = $2.m_intVal > $3.m_intVal; break;
            case NE: $$.m_boolVal = $2.m_intVal != $3.m_intVal; break;
            case GE: $$.m_boolVal = $2.m_intVal >= $3.m_intVal; break;
            case LE: $$.m_boolVal = $2.m_intVal <= $3.m_intVal; break;
            case EQ: $$.m_boolVal = $2.m_intVal == $3.m_intVal; break;
          }
          operationStack.pop();
        }
        if(RHS == _STR) {
          switch(operationStack.top()) { 
            case EQ: $$.m_boolVal = !(strcmp($2.m_strVal, $3.m_strVal)); break;
          }
        }
      } else {
        yyerror("not thes ame type");
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
      if(operationStack.top() == AND) {
        $$.m_boolVal = $2.m_boolVal && $3.m_boolVal;
      } else {
        $$.m_boolVal = $2.m_boolVal || $3.m_boolVal;
      }
			$$.m_type = _BOOL;
			break;

		default:
			if($2.m_type != _INT) {
				yyerror("Arg 1 must be integer");
			}
			if($3.m_type != _INT) {
				yyerror("Arg 2 must be integer");	
      }
      switch(operationStack.top()) {
        case '+': $$.m_intVal = $2.m_intVal + $3.m_intVal; break;
        case '/': 
          if ($3.m_intVal == 0) {
            yyerror("Attempted division by zero");
          }
          $$.m_intVal = $2.m_intVal / $3.m_intVal; break;
        case '-': $$.m_intVal = $2.m_intVal - $3.m_intVal; break;
        case '*': $$.m_intVal = $2.m_intVal * $3.m_intVal; break;
      }
      operationStack.pop();
      			$$.m_boolVal = true;
			$$.m_type = _INT;
			break;
	}

};

N_IF_EXPR :
T_IF N_EXPR N_EXPR N_EXPR {
  printRule("IF_EXPR", "if EXPR EXPR EXPR");
  if ($2.m_boolVal) {
    copyType($$,$3);
  } else {
    copyType($$,$4);
  }
};

N_LET_EXPR :
T_LETSTAR T_LPAREN N_ID_EXPR_LIST T_RPAREN N_EXPR {
	printRule("LET_EXPR", "let* ( ID_EXPR_LIST ) EXPR");
	copyType($$, $5);
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
  bool exists = false;

  switch ($4.m_type) {
    case _INT:
      exists = scopeStack.top().addEntry(SYMBOL_TABLE_ENTRY($3, $4.m_type, $4.m_params, $4.m_returnType, $4.m_intVal));
      break;
    case _STR:
      exists = scopeStack.top().addEntry(SYMBOL_TABLE_ENTRY($3, $4.m_type, $4.m_params, $4.m_returnType, $4.m_strVal));
      break;
    case _BOOL:
      exists = scopeStack.top().addEntry(SYMBOL_TABLE_ENTRY($3, $4.m_type, $4.m_params, $4.m_returnType, $4.m_boolVal));
      break;
  }
	if (!exists) {
		yyerror("Multiply defined identifier");
	}
};



N_PRINT_EXPR :
T_PRINT N_EXPR {
	printRule("PRINT_EXPR", "print EXPR");
  switch($2.m_type) {
    case _INT:
      printf("%d\n", $2.m_intVal);
      break;
    case _BOOL:
      printf("%s\n", $2.m_boolVal ? "t" : "nil");
      break;
    case _STR:
      printf("%s\n", $2.m_strVal);
      break;
  }
	copyType($$,$2);
};

N_INPUT_EXPR :
T_INPUT {
	printRule("INPUT_EXPR", "input");
	std::string text = "";
	getline(cin, text);
	if (text[0] == '+' || text[0] == '-') {
	  $$.m_type = _INT;
	  $$.m_intVal = atoi(text.c_str());
	  $$.m_boolVal = true;
	  strcpy($$.m_strVal, "");
	} else {
	  $$.m_type = _STR;
	  strcpy($$.m_strVal, text.c_str());
	  $$.m_intVal = 0;
	  $$.m_boolVal = true;
	}
};

N_EXPR_LIST :
N_EXPR N_EXPR_LIST {
	//Is this the first N_EXPR in the N_EXPR_LIST?	
	printRule("EXPR_LIST", "EXPR EXPR_LIST");
} | N_EXPR {
	printRule("EXPR_LIST", "EXPR");
	setMe = $1;
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
  operationStack.push('*');
} | T_SUB {
	printRule("ARITH_OP" , "-");
  operationStack.push('-');
} | T_DIV {
	printRule("ARITH_OP" , "/");
  operationStack.push('/');
} | T_ADD {
	printRule("ARITH_OP" , "+");
  operationStack.push('+');
};

N_LOG_OP :
T_AND {
	printRule("LOG_OP" , "and");
  operationStack.push(AND);
} | T_OR {
	printRule("LOG_OP" , "or");
  operationStack.push(OR);
};

N_REL_OP :
T_LT {
	printRule("REL_OP" , "<");
  operationStack.push(LT);
} | T_GT {
	printRule("REL_OP" , ">");
  operationStack.push(GT);
} | T_LE {
	printRule("REL_OP" , "<=");
  operationStack.push(LE);
} | T_GE {
	printRule("REL_OP" , ">=");
  operationStack.push(GE);
} | T_EQ {
  printRule("REL_OP" , "=");
  operationStack.push(EQ);
} | T_NE {
  printRule("REL_OP" , "/=");
  operationStack.push(NE);
};

N_UN_OP :
T_NOT {
	printRule("UN_OP", "not");
  operationStack.push(NOT);
};

N_CONST :
T_INTCONST {
	printRule("CONST", "INTCONST");
  $$.m_boolVal = true;
  $$.m_intVal = $1;
  strcpy($$.m_strVal,"");
	$$.m_type = _INT;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
} | T_STRCONST {
	printRule("CONST", "STRCONST");
  	$$.m_intVal = 0;
  $$.m_boolVal = true;
  strcpy($$.m_strVal,strdup($1));
	$$.m_type = _STR;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
} | T_T {
	printRule("CONST", "t");
  $$.m_boolVal = true;
	$$.m_type = _BOOL;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
	$$.m_intVal = 0;
  strcpy($$.m_strVal,"");
} | T_NIL {
	printRule("CONST", "nil");
  $$.m_boolVal = false;
	$$.m_type = _BOOL;
	$$.m_params = NOT_APPLICABLE;
	$$.m_returnType = NOT_APPLICABLE;
	$$.m_intVal = 0;
  strcpy($$.m_strVal,"");
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

TYPE_INFO findEntryInScope(const char* entry) {
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



void copyType(TYPE_INFO& dest, const TYPE_INFO source) {
    dest.m_intVal = source.m_intVal;
    dest.m_boolVal = source.m_boolVal;
    dest.m_type = source.m_type;
    dest.m_params = source.m_params;
    dest.m_returnType = source.m_returnType;
    //dest.m_strVal = static_cast<char*>(malloc((strlen(source.m_strVal) + 1) * sizeof(char)));
    strcpy(dest.m_strVal, source.m_strVal);
}


int main(int argc, char** argv)
{
  if (argc < 2) {
    printf("You must specify a file in the command line!\n");
    exit(1);
  }
  yyin = fopen(argv[1], "r");
  do
  {
    yyparse();
  } while (!feof(yyin));
  fclose(yyin);
  return(0);
}
