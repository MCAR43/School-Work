#ifndef GAMES_CHESS_BBOARD_H
#define GAMES_CHESS_BBOARD_H
#include <bitset>
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <random>
#include "constants.h"
typedef std::bitset<64> U64;

struct Move {
  int _origPos, _endPos, _bbLookup, _eval;
  char _repr;
  std::string _capture;
  std::string promotion;
  Move() : _origPos(-1), _endPos(-1) {}
  Move(const int oPos = -1, const int ePos = -1, const char pRepr = 'p', const bool capture = false) {
    int dir = 1;
    promotion = "";
    _origPos = oPos;
    _endPos = ePos; 
    _repr = pRepr;
    _capture = capture ? "x" : "";
    switch(_repr) {
      case 'P': _bbLookup = w_pawn; 
                dir = -1;
                if(_endPos - 56 >= 0) {
                  promotion="Q";
                  _bbLookup = w_queen;
                }
                break;
      case 'R': _bbLookup = w_rook; break;
      case 'N': _bbLookup = w_knight; break;
      case 'B': _bbLookup = w_bishop; break;
      case 'Q': _bbLookup = w_queen; break;
      case 'K': _bbLookup = w_king; break;
      case 'p': _bbLookup = b_pawn; 
                dir = 1;
                if(_endPos - 8 <= 0) {
                  promotion ='q';
                  _bbLookup = b_queen;
                }
                break;
      case 'r': _bbLookup = b_rook; break;
      case 'n': _bbLookup = b_knight; break;
      case 'b': _bbLookup = b_bishop; break;
      case 'q': _bbLookup = b_queen; break;
      case 'k': _bbLookup = b_king; break;
    };
  
    //This avoids the need to serialize bulk generateed pawn pushes in exchange
    //for a small calculation, much faster just harder to read
    if(_origPos == -1) {
      _origPos = _endPos + (8 * dir);
    } else if(_origPos == -2) {
      _origPos = _endPos + (16 * dir);
    }

    //Determine Pawn promotion

  }

  std::string SAN() const {
    return (_repr + INDEX_REPR[_origPos] + _capture + INDEX_REPR[_endPos] + promotion);
    
  }
  bool operator==(Move const& m) {
    return (m._origPos == _origPos && m._endPos == _endPos && m._repr == _repr);
  }

  friend std::ostream& operator<<(std::ostream & out, const Move &rhs) {
    out << rhs.SAN();
    return out;
  }
};

class Bitboard {
  private:
    U64 _pBB[N_BOARDS];
    U64 _empty;
    U64 _all;
    int _enpIdx;
  public:
    int _color;
    int _eval;
    U64 _attMap;
    std::vector<Move> _moveList;
    
    //Constructors
    Bitboard();
    Bitboard(const std::vector<std::string> FEN, const std::string castling, const std::string enpSquare, const std::string pColor); 
    Bitboard operator=(const Bitboard & copy_board);
    friend bool operator==(const Bitboard lhs, const Bitboard rhs);
    //General Bitboard functions for updating and checking the bitboard
    void update(std::vector<std::string> FEN);
    void print(const U64 board);
    void printAll();

    //Setters
    void setAll(const U64 newAll) {_all = newAll;}
    void setColor(const int color) {_color = color;} 

    //Getters
    U64 getPiece(const int index) const {return _pBB[index];}
    int getColor() const {return _color;}
    //Move Generation
    
    //Pawns
    void singlePush();
    void doublePush();
    void pawnAttacks(const bool attMap);
		
    //Knight Generatio
		void knightMoves(const bool attMap);
    
    //Bishop Generation
    void bishopMoves(const bool attMap);
    
    //Rook
    void rookMoves(const bool attMap);
    
    //Queen
    void queenMoves(const bool attMap);
    
    //King Generation
    void kingMoves(const bool attMap);
   
    U64 makeMove(const Move m);
    void undoMove(const Move m);
    friend Bitboard legal(const Bitboard board);
    U64 allMoves(const bool attMap);
    void generateMoves(const int oPos, const U64 b, const char piece, const bool cap);

    int evalBoard();
    void filterLegal();
};


#endif /*BBOARD_H*/


