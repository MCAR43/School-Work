% Declarationt for animal classes and subclasses
animal(X) :- mammal(X).
animal(X) :- bird(X).
animal(X) :- fish(X).

% What is each subclass of animal covered in
covering(X, fur) :- mammal(X).
covering(X, scales) :- fish(X).
covering(X, feathers) :- bird(X).

% How many legs does each subclass of animal have
legs(X, 4) :- mammal(X); not(primate(X).
legs(X, 2) :- primate(X); bird(X). 
legs(X, 0) :- fish(X).


% What is each subclass of mammal and bird
mammal(X) :- primate(X).
mammal(X) :- cat(X).
mammal(X) :- dog(X).
bird(X) :- hawk(X).


% determining the sound a subclass of animal makes
sound(X, bark) :- dog(X).
sound(X, purr) :- cat(X).


% Atoms
cat(sylvester).
cat(felix).

dog(spike).
dog(fido).

primate(george).
primate(king kong).

bird(tweety).
hawk(tony).
fish(nemo).
