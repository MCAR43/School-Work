:- dynamic passenger/1.
passenger(w).
goat :- passenger(g), retract(passenger(g)), assert(passenger(c)).
wolf :- passenger(w), retract(passenger(w)), assert(passenger(g)).
cabbage :- passenger(c), retract(passenger(c)), assert(passenger(w)).

