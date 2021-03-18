example.tab.c: example.y
	bison example.y

lex.yy.c: flex.lex
	flex flex.l

parser: example.tab.c
	g++ -o parser example.tab.c

clean:
	rm parser example.tab.c lex.yy.c
