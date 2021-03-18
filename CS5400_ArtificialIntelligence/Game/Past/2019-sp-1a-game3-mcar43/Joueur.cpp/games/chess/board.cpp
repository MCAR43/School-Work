#include "board.hpp"
//Determines if a Given move is inside the bounds of the array, so we don't loop to the otherside and produce invalid moes

bool Board::isSafe(const int row, const int col) {
  bool inbounds;
  inbounds = ( (row < 0) || (row >= ROWS) ) ;
  inbounds |= ( (col < 0) || (col >= COLS) );
  return inbounds;
}

Move Board::loc_repr(const std::string mapRepr) {
  for(int i = 0; i < ROWS; ++i) {
    for(int k = 0; k < COLS; ++k) {
      if(mapping[i][k] == mapRepr) {
        return(Move(i, k, 0, 0));
      }
    }
  }
  return(Move());
}


Board::Board() {
  _children.clear();
  depth = 0;
  relativeValue = 0;
  clear();
}

//Copy Constructor for the board class
Board::Board(const Board & copy_board) {
  for(int i = 0; i < ROWS; ++i) {
    for(int k = 0; k < ROWS; ++k) {
      m_board[i][k] = copy_board.m_board[i][k];
    }
  }
  for(int i = 0; i < trackedPieces; ++i) {
    locations[i] = copy_board.locations[i];
  }
  playerRepr = playerRepr = copy_board.playerRepr;
  enpSquare = copy_board.enpSquare;
  associatedMove = copy_board.associatedMove;
  relativeValue = copy_board.relativeValue;
  depth = copy_board.depth;
}

bool Board::operator<(const Board &rhs) const {
  return (depth < rhs.depth);
}

//Assignment operator for the board
Board Board::operator=(const Board & copy_board) {
  for(int i = 0; i < ROWS; ++i) {
    for(int k = 0; k < ROWS; ++k) {
      m_board[i][k] = copy_board.m_board[i][k];
    }
  }
  for(int i = 0; i < trackedPieces; ++i) {
    locations[i] = copy_board.locations[i];
  }
  playerRepr = copy_board.playerRepr;
  enpSquare = copy_board.enpSquare;
  associatedMove = copy_board.associatedMove;
  relativeValue = copy_board.relativeValue;
  depth = copy_board.depth;
  return *this;
}

//Clears the move queue, board state, and piece locations on the current board
//i represents the current Row  when indexing into the chess board array
//k represents the current col when indexing into the chess board array
void Board::clear() {
  for(int i = 0; i < ROWS; i++) {
    for(int k = 0; k < COLS; k++) {
      m_board[i][k] = '-';
    }
  }

  // Clearing the tracked pieces so we can generate new ones based on the given FEN string
  // i represents the array index that we're delting in the tracked pieces
  for(int i = 0; i < trackedPieces; i++) {
    locations[i].clear();
  }
  relativeValue = 0;
  depth = 0;
  associatedMove = Move();
}


//Scans through the FEN-string and assigns the pieces to a location on the board, and tracks each individual piece in a vector of pieces
void Board::update(const std::vector<std::string> FEN, const std::string ENP, const std::string castle) {
  clear();
  int rInd = 0;
  std::string rank;
  enpSquare = ENP;
  relativeValue = 0;

  for(int i = 0; i < FEN.size(); i++) {
    rank = FEN[i];
    rInd = 0;
    for(int k = 0; k < rank.length(); k++) {
      //If the scanned piece is a digit instead of a character, we add that digit to the rank index, so we can assign it to the board properly
      if (isdigit(rank[k])) {
        rInd += static_cast<int>(rank[k]) - '0' - 1;
      } else {
        addPiece(i, k + rInd, rank[k]);
      }
    }
  }
  //Copy all of the white pieces into the w_pieces index, same for black
  for(int i = w_pawn; i <= w_king; ++i) {
    locations[w_pieces].insert(locations[w_pieces].end(),locations[i].begin(), locations[i].end());
  }
  for(int i = b_pawn; i <= b_king; ++i) {
    locations[b_pieces].insert(locations[b_pieces].end(),locations[i].begin(), locations[i].end());
  }
}

//Adds a piece to the board, and its corresponding piece vector
void Board::addPiece(const int row, const int col, const char repr) { 
  std::string stringRepr = "";
  stringRepr += repr;
  //Create a new Move object based on the row, col, and the character
  Move pce(row, col, 0, 0, stringRepr);
  //Add it to the chess board representation
  m_board[row][col] = repr;
  
  //Add the piece to the location vector
  locations[pce.locInd].push_back(pce);
}

void Board::print() {
  std::cout << "Depth: " << depth << std::endl;
  for(int i = 0; i < 8; ++i) {
    for(int k = 0; k < 8; ++k) {
      std::cout << m_board[i][k] << " ";
    }
    std::cout << std::endl;
  }
}

//This function is used for determing the locations that pieces are able to 'push to'
//It first determines that the arrived at location is within the bounds of the board array, and then uses the 'attFlag'
//variable to determine if we are finding the attack locations of the other player, this is used for determining where
//the other player is able to take pieces, instead of just where we can move
//
//The sliding piece variable is used for sliding pieces, and will loop until it encounters an out of bounds error, or until it encounters
//another piece
//This function returns a Move variable of the last valid move it was able to complete, so that the attackLocations function, can pick up where it
//last left off, to avoid rechecking valid spaces.


bool Board::inCheck(std::vector<Move> attVec) {
  Move kingLoc = locations[w_king + playerRepr].front();
  std::vector<Move>::iterator it;
  for(it = attVec.begin(); it != attVec.end(); ++it) {
    if (it->nRow == kingLoc.row && it->nCol == kingLoc.col) {
      return true;    
    }
  }
  return false;
}

int Board::boardHeuristic() {
  std::vector<Move>::iterator it;
  int index = 0;
  relativeValue = 0;
  for(int cPiece = (w_pawn + playerRepr); cPiece < (w_pieces + playerRepr); ++cPiece) {
    for(it = locations[cPiece].begin(); it != locations[cPiece].end(); ++it) {
      relativeValue += PIECE_VALUES[index];  
    }
    index++;
  }
   
  index=0;
  for(int cPiece = (b_pawn - playerRepr); cPiece < (b_pieces - playerRepr); ++cPiece) {
    for(it = locations[cPiece].begin(); it != locations[cPiece].end(); ++it) {
      relativeValue -= PIECE_VALUES[index];
    } 
    index++;
  }
  
  return relativeValue;
}

Board makeMove(Board & orig, const Move _move) {
  std::vector<Move>::iterator piece;
  int enemyPieces = (orig.playerRepr > w_pawn) ? b_pieces : w_pieces;
  Board temp = orig;
  Move tempMove;
  temp.associatedMove = _move;
  //Find the Corresponding move in the temp.locations vector for is specified piece
  piece = std::find(temp.locations[temp.associatedMove.locInd].begin(), temp.locations[temp.associatedMove.locInd].end(), temp.associatedMove);
  piece->row = temp.associatedMove.nRow;
  piece->col = temp.associatedMove.nCol;
  temp.m_board[_move.nRow][_move.nCol] = _move.repr[0];
  temp.m_board[_move.row][_move.col] = '-';
  //Same thing but for the generalized piece location vector
  piece = std::find(temp.locations[w_pieces + temp.playerRepr].begin(), temp.locations[w_pieces + temp.playerRepr].end(), temp.associatedMove);
  piece->row = temp.associatedMove.nRow;
  piece->col = temp.associatedMove.nCol;
 
  if(temp.associatedMove.capture) {
    //Find the corresponding move in the locations vector for the captured piece to remove it.
    for(std::vector<Move>::iterator it = temp.locations[enemyPieces].begin(); it != temp.locations[enemyPieces].end(); ++it) {
      if(it->row == _move.nRow && it->col == _move.nCol) {
        piece = it;
      }
    }
    temp.locations[enemyPieces].erase(piece);
  }
  temp.depth += 1;
  orig._children.push_back(temp);
  return temp;
}

