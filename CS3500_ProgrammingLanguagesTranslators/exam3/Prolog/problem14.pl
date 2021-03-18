g1([[1,2],[2,3],[3,1],[3,4],[4,2],[4,5]]).
g2([[2,1],[2,4],[1,3],[1,4],[3,2],[3,5],[5,6],[6,3],[4,2]]).
firstRun :-
  retractall(path(_,_)),
  g1(A),
  createPaths(A),
  countTriangles(NumTriangles),
  Answer is NumTriangles / 3,
  print(Answer),
  Answer is 0,
  NumTriangles is 0.

secondRun :-
  retractall(path(_,_)),
  g2(A),
  createPaths(A),
  countTriangles(NumTriangles),
  Answer is NumTriangles / 3,
  print(Answer),
  Answer is 0,
  NumTriangles is 0.


createPaths([]).
createPaths([H|L]) :-
  nth0(0, H, A),
  nth0(1, H, B),
  assert(path(A,B)),
  createPaths(L).


exist(E1, E2, E3) :-
  path(E1, E2), path(E2,E3), path(E3, E1).


countTriangles(Num) :- 
  aggregate_all(count, exist(_, _, _), Num).
 
