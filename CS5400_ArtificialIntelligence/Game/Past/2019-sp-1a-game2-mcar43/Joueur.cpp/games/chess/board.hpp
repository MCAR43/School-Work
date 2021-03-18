#ifndef GAMES_CHESS_BOARD_HPP
#define GAMES_CHESS_BOARD_HPP
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>
#include <random>
#include <ctime>
#include "constants.h"

struct Move {
  int row;
  int col;
  int nRow;
  int nCol;
  std::string repr;
  bool capture;


  Move(): row(0), col(0), nRow(0), nCol(0), repr("-"), capture(false) {}
  Move(int const &nr, int const &nc): row(nr), col(nc) {}
  Move(int const &r, int const &c, int const &nr, int const& nc): row(r), col(c), nRow(nr), nCol(nc), capture(false) {}
  Move(int const &r, int const &c, int const &nr, int const& nc, std::string const& rep, bool const& cap): row(r), col(c), nRow(nr), nCol(nc), repr(rep), capture(cap) {}
  Move(int const &r, int const &c, int const &nr, int const& nc, std::string const &rep): row(r), col(c), nRow(nr), nCol(nc), repr(rep), capture(false) {}
  
  std::string moveRepr() const {
    if(repr == "KC") {
      return("O-O");
    } else if(repr == "QC") {
      return("O-O-O");
    }
    if(capture) {
      return(repr + mapping[row][col] + "x" + mapping[nRow][nCol]);
    } else {
      return(repr + mapping[row][col] + mapping[nRow][nCol]);
    }
  }
  
  bool operator()(Move const& pce) {
    return (row == pce.nRow && col == pce.nCol);
  }

  friend std::ostream& operator << (std::ostream& output, const Move& rhs) {
    output << "row: " << rhs.row << " col: " << rhs.col << " nRow: " << rhs.nRow << " nCol: " << rhs.nCol;
    return output;
  }
};

class Board {
  public:
    char m_board[ROWS][COLS];
    char m_attBoard[ROWS][COLS];
    bool whitePlayer = false;
    bool castleQueen, castleKing;
    int playerRepr;
    std::string enpSquare;
    std::vector<Move> locations[trackedPieces];
    std::vector<Move> validMoves;
    std::vector<Move> attackVector;
    enum Piece {
      w_pawn, //    0
      w_rook, //    1
      w_knight, //  2
      w_bishop, //  3
      w_queen, //   4
      w_king, //    5 
      w_pieces, //  6
      b_pawn, //    7
      b_rook, //    8
      b_knight, //  9
      b_bishop, //  10
      b_queen, //   11
      b_king, //    12
      b_pieces //   13
    };
    //Variables
    //Everything public out of laziness - fix later
    
    //Constructors
    Board();
    Board(const Board & copy_board);

    //Gnerating the board at every iteration
    void update(const std::vector<std::string> FEN, const std::string ENP, const std::string castle);
    void addPiece(const int row, const int col, const char repr);
    
    //Move Generation
    std::string makeMove();
    void genMove(const int pieceRepr, const bool attFlag);
    Move pushLocations(Move & potMove, const int rowMod, const int colMod, const bool isSlider, const bool attFlag);

    void attackLocations(Move potMove, std::vector<Move> attPieces, const bool attFlag);
    void genPawn(const bool attVectorFlag); 
    void genAll(const bool attFlag);
    bool inCheck();
    bool checkMove(const Move m);
    
    //Utility
    Board operator=(const Board & copy_board);
    void print();
    void clear();
};


#endif /*GAMES_CHESS_BOARD_HPP*/
