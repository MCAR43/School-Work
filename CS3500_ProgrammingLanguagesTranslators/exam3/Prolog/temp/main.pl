g1([[1,2],[2,3],[3,1],[3,4],[4,2],[4,5]]).
g2([[2,1],[2,4],[1,3],[1,4],[3,2],[3,5],[5,6],[6,3],[4,2]]).
temp([0,0]).


main :-
  g1(PAIR),
  loop1(PAIR).

loop1([]).
loop1([H|L]) :-
  loop2(L, H),
  loop1(L).

loop2([], []).
loop2([H|T], P) :-
  print(P),
  print(H),
  assert(temp([0,0])),
  print(temp([0,0])),
  nl,
  loop2(T, P).





