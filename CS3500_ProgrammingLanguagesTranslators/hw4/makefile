CC=g++
CFLAGS=-Wall
all: parser

parser: andersonM.tab.c
	$(CC) andersonM.tab.c -o parser

andersonM.tab.c: lex.yy.c
	bison andersonM.y

lex.yy.c:
	flex andersonM.l

clean:
	rm andersonM.tab.c parser lex.yy.c
