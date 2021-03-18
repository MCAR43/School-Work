/*   	example.l
 
 	Specifications of tokens that is to be
      used with bison file example.y
*/

%{

%}

/* Defintions of regular expressions go here */

WSPACE		[ \t\r]+
NEWLINE           \n

DIGIT	            [0-9]
LETTER            [a-zA-Z]

IDENT			{LETTER}({LETTER}|{DIGIT})* 
INTCONST          {DIGIT}+

%%

"foo"         	{
				printTokenInfo("FOO", yytext);
				return T_FOO;
			}
{INTCONST}	     	{
				printTokenInfo("INTCONST", yytext);
				return T_INTCONST;
			}
{IDENT}		{
				printTokenInfo("IDENT", yytext);
				return T_IDENT;
			}
{NEWLINE}		{
                    	numLines++;
                }
{WSPACE}		{ }
.			{
				printTokenInfo("UNKNOWN", yytext);
				return T_UNKNOWN;
			}

%%


