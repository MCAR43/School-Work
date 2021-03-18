
:- dynamic edge/2.

main :-
  g1(X),
  make(X),
  countTriangles(Total),
  print(Total).

g1([[1,2],[2,3],[3,1],[3,4],[4,2],[4,5]]).

g2([[2,1],[2,4],[1,3],[1,4],[3,2],[3,5],[5,6],[6,3],[4,2]]).

make_into_edge(E) :- print(E), nth0(0, E, X), nth0(1, E, Y), assert(edge(X, Y)), nl, print(X), nl, print(Y), nl.

triangle(X, Y, Z) :- 
  edge(X, Y), edge(Y, Z), edge(Z, X).

exist(X, Y, Z) :-
  edge(X, Y), edge(Y, Z), edge(Z, X).

make([]).
make([H|T]) :- 
  make_into_edge(H),
  make(T).

countTriangles(Total) :-aggregate_all(count, exist(_, _, _), Count), Total is Count/3.
