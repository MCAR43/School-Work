/*#ifndef GAMES_CHESS_BITBOARD_H
#define GAMES_CHESS_BITBOARD_H
#include <vector>
#include <iostream>
#include <cstdlib>
#include <cctype>
#include "constants.h"
class Bitboard {
  public:
    std::bitset<64> m_piecesBoard[numBitBoards];
    std::bitset<64> m_clearBoard;
    std::bitset<64> m_occupiedBoard;
    
    enum Piece {
      all,
      white,
      black,
      whitePawn,
      blackPawn,
      whiteRook,
      blackRook,
      whiteKnight,
      blackKnight,
      whiteBishop,
      blackBishop,
      whiteQueen,
      blackQueen,
      whiteKing,
      blackKing
    };

    Bitboard();
    void update(const std::vector<std::string> FEN);
    void print(const std::string board);
    std::vector<std::string> genPawn(const std::string color);
    std::vector<std::string> genPawnAttack(const std::string color);
};


#endif // GAMES_CHESS_BITBOARD_HPP
*/
