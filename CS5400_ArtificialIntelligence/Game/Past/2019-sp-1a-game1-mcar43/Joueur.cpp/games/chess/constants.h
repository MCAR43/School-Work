#ifndef GAMES_CHESS_CONSTANTS_H
#define GAMES_CHESS_CONSTANTS_H
const int numBitBoards = 15;
const short ROWS = 8;
const short COLS = 8;
const short trackedPieces = 14;

const std::string mapping[8][8] = {
  {"a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"},
  {"a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"},
  {"a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"},
  {"a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"},
  {"a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"},
  {"a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"},
  {"a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"},
  {"a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"}
};

const std::string pieceCharacters[6] = {"P", "R", "N", "B", "Q", "K"};

const int rowDir[6][8] = {
  {1, 2}, //Pawn / Rook
  {1, -1, 0, 0},
  {-2, -2, -1, -1, 1, 1, 2, 2},
  {1, 1, -1, -1},
  {1, -1, 0, 0, 1, 1, -1, -1},
  {1, -1, 0, 0, 1, 1, -1, -1}
};

const int colDir[6][8] = {
  {0, 0},
  {0, 0, 1, -1},
  {1, -1, 2, -2, 2, -2, 1, -1},
  {1, -1, 1, -1},
  {0, 0, 1, -1, 1, -1, 1, -1},
  {0, 0, 1, -1, 1, -1, 1, -1}
};


#endif /*GAMES_CHESS_CONSTANTS_H*/
