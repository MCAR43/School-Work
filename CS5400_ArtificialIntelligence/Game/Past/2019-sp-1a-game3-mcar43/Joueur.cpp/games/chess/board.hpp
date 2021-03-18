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
  //Numbers corresponding to the board location
  int row;
  int col;
  int nRow;
  int nCol;

  //Index into the locations vector from board
  int locInd; 
  int relativeValue;
  
  //Character representation of the Piece
  std::string repr;
  //Is this move a capture (used to add the X inbetween the SAN notation)
  bool capture;

    
  Move(): row(0), col(0), nRow(0), nCol(0), relativeValue(0), repr("-"), capture(false) {}
  Move(const int r, const int c, const int nextRow, const int nextCol, const std::string rep="", const bool cap=false) {
    row = r;
    col = c;
    nRow = nextRow;
    nCol = nextCol;
    repr = rep;
    capture = cap;
    relativeValue = 0;
    switch(repr[0]) {
      //White Pieces
      case 'R':
        locInd = w_rook; break;
      case 'N':
        locInd = w_knight; break;
      case 'B':
        locInd = w_bishop; break;
      case 'Q':
        locInd = w_queen; break;
      case 'K':
        locInd = w_king; break;
      case 'P':
        locInd = w_pawn; break;

      //Black Pieces
      case 'r':
        locInd = b_rook; break;
      case 'n':
        locInd = b_knight; break;
      case 'b':
        locInd = b_bishop; break;
      case 'q':
        locInd = b_queen; break;
      case 'k':
        locInd = b_king; break;
      case 'p':
        locInd = b_pawn; break;
    }
  }
  
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
  
  //Overloaded () operator, this is defined solely for using as a unary predicate for some of the c++ algorithms (std::any_of, std::find_if)
  bool operator()(Move const& pce) {
    return (row == pce.nRow && col == pce.nCol);
  }

  bool operator==(Move const& pce) {
    return(row == pce.row && col == pce.col);
  }

  friend std::ostream& operator << (std::ostream& output, const Move& rhs) {
    output << rhs.moveRepr() << " rV: " << rhs.relativeValue << std::endl;
    return output;
  }
};

class Board {
  public:
    //Character Array representation of the board state
    char m_board[ROWS][COLS];
    //Int representing whether or not hte player is black (7) or white (0)
    int playerRepr;
    //Square that the FENstring says is a valid en passant pawn capture
    std::string enpSquare;
    //Vector of the locations of all the pieces on the board, this is what is used for determining moves and pieces on the board
    Move associatedMove;
    int relativeValue;    
    //m_board is used almost exclusively for debugging purposes
    std::vector<Move> locations[trackedPieces];
    std::vector<Board> _children;
    int depth;
    //Variables
    //Everything public out of laziness - fix later
    
    //Constructors
    Board();
    Board(const Board & copy_board);

    //Gnerating the board at every iteration
    void update(const std::vector<std::string> FEN, const std::string ENP, const std::string castle);
    void addPiece(const int row, const int col, const char repr);
    
    //Move Generation
    friend Board makeMove(Board & orig,const Move _move);
    bool inCheck(std::vector<Move> attVec);
    int boardHeuristic();

    //Utility
    bool operator< (const Board & rhs) const;
    Board operator=(const Board & copy_board);
    bool isSafe(const int row, const int col);
    Move loc_repr(const std::string mapRepr);
    void print();
    void clear();
};
#endif /*GAMES_CHESS_BOARD_HPP*/
