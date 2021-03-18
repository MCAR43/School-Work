CC=g++
CFLAGS=-Wdeprecated
all: parser

parser: andersonWendland.tab.c
	$(CC) andersonWendland.tab.c -o parser

andersonM.tab.c: lex.yy.c
	bison andersonWendland.y

lex.yy.c:
	flex andersonWendland.l

clean:
	rm andersonWendland.tab.c parser lex.yy.c
