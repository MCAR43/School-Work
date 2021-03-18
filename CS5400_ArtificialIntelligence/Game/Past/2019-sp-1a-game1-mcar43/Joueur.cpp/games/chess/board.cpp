#include "board.hpp"
//Determines if a Given move is inside the bounds of the array, so we don't loop to the otherside and produce invalid moes
bool isSafe(const int row, const int col) {
  bool inbounds;
  inbounds = ( (row < 0) || (row >= ROWS) ) ;
  inbounds |= ( (col < 0) || (col >= COLS) );
  return inbounds;
}

Move loc_repr(const std::string mapRepr) {
  for(int i = 0; i < ROWS; ++i) {
    for(int k = 0; k < COLS; ++k) {
      if(mapping[i][k] == mapRepr) {
        return(Move(i, k));
      }
    }
  }
  return(Move(0,0));
}

Board::Board() {
  clear();
}

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
  validMoves = copy_board.validMoves;
  attackVector = copy_board.attackVector;
}

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
  validMoves = copy_board.validMoves;
  attackVector = copy_board.attackVector;
  return *this;
}

//Clears the move queue, board state, and piece locations on the current board
//i represents the current Row  when indexing into the chess board array
//k represents the current col when indexing into the chess board array
void Board::clear() {
  for(int i = 0; i < ROWS; i++) {
    for(int k = 0; k < COLS; k++) {
      m_board[i][k] = '-';
      m_attBoard[i][k] = '-';
    }
  }

  // Clearing the tracked pieces so we can generate new ones based on the given FEN string
  // i represents the array index that we're delting in the tracked pieces
  for(int i = 0; i < trackedPieces; i++) {
    locations[i].clear();
  }
  validMoves.clear();
  attackVector.clear();
}


//Scans through the FEN-string and assigns the pieces to a location on the board, and tracks each individual piece in a vector of pieces
void Board::update(const std::vector<std::string> FEN, const std::string ENP, const std::string castle) {
  clear();
  int rInd = 0;
  std::string rank;
  enpSquare = ENP;

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
  //Based on the input character, add it to its corresponding piece location vector
  switch(repr) {
    case 'R':
      locations[w_rook].push_back(pce); break;
    case 'N':
      locations[w_knight].push_back(pce); break;
    case 'B':
      locations[w_bishop].push_back(pce); break;
    case 'Q':
      locations[w_queen].push_back(pce); break;
    case 'K':
      locations[w_king].push_back(pce); break;
    case 'P':
      locations[w_pawn].push_back(pce); break;

    case 'r':
      locations[b_rook].push_back(pce); break;
    case 'n':
      locations[b_knight].push_back(pce); break;
    case 'b':
      locations[b_bishop].push_back(pce); break;
    case 'q':
      locations[b_queen].push_back(pce); break;
    case 'k':
      locations[b_king].push_back(pce); break;
    case 'p':
      locations[b_pawn].push_back(pce); break;
  }
}

void Board::print() {
  std::cout << "Board Represented By:\n";
  for(int i = 0; i < ROWS; i++) {
    for(int k = 0; k < COLS; k++) {
      std::cout << m_board[i][k] << " ";
    }
    std::cout << std::endl;
  }
  
  std::cout << "\nAttack Vector: \n";
  for(int i = 0; i < ROWS; ++i) {
    for(int k = 0; k < COLS; ++k) {
      std::cout << m_attBoard[i][k] << " ";
    }
    std::cout << std::endl;
  }

  std::cout << std::endl;
}

Move Board::pushLocations(Move & potMove, const int rowMod, const int colMod, const bool isSlider, const bool attFlag) {
  bool valid = !isSafe(potMove.nRow, potMove.nCol) && m_board[potMove.nRow][potMove.nCol] == '-';
  while (valid) {
    if(attFlag) {
      attackVector.push_back(potMove);
    } else {
      validMoves.push_back(potMove);
    }
    potMove.nRow += rowMod;
    potMove.nCol += colMod;
    if(!isSlider) {
      return potMove;
    } else {
      valid = !isSafe(potMove.nRow, potMove.nCol) && m_board[potMove.nRow][potMove.nCol] == '-';
    }
  }; 
  return potMove;
}

void Board::attackLocations(Move potMove, std::vector<Move> attPieces, const bool attFlag) {
  bool valid = !isSafe(potMove.nRow, potMove.nCol);
  std::vector<Move>::iterator it;
  if(valid) {
    for(it = attPieces.begin(); it != attPieces.end(); ++it) {
      if(it->row == potMove.nRow && it->col == potMove.nCol) {
        potMove.capture = true;
        if(attFlag) {
          attackVector.push_back(potMove);
        } else {
          validMoves.push_back(potMove);
        }
      }
    }
  }
}
  
void Board::genMove(const int pieceRepr, const bool attFlag) {
  //Piece is a list of the pieces we wish to move, its indexed into the location vector by the piece enum representation, and the player color constant
  //This function is always called with the enum of white pieces, and determining color is done with the player color constant
  // If the player is black and wishes to move a pawn it would index into
  // w_pawn = 0, playerRepr = 7 = 7
  // locations[7] = all black pawns
  int prev = playerRepr;
  if (attFlag) {
    playerRepr = (playerRepr > w_pawn) ? w_pawn : b_pawn;
  }
  std::vector<Move> piece = locations[pieceRepr + playerRepr];
  //Same logic but for finding the location of all pieces of a certain color
  //If we're wanting to gen moves for black pawns as in above
  //playerRepr = 8; b_pieces = 14, 14 -  6 = 8
  //locations[8] == all  white pieces
  std::vector<Move> attackPieces = locations[b_pieces - playerRepr];
  std::vector<Move>::iterator it;
  //Boolean to determine if move is within the bounds for the array
  bool inbounds = false;
  bool slidingPiece = false;
  //number of possible directions for the piece, pawns have 1, rooks have 4, bishops have 8...
  int posMoves;
  int colMod, rowMod;
  //representing direction on the board, if the player is black we're incrementing up the board, white we increment down the board
  int dir = (playerRepr > 0) ? 1 : -1;
  Move potentialLoc, initialLoc;

  //Determining the number of directions based on the piece representation constant passed
  switch(pieceRepr) {
    case w_rook:
    case w_bishop:
      posMoves = 4;
      slidingPiece = true;
      break;
    case w_queen:
      slidingPiece = true;
      posMoves = 8;
      break;
    case w_knight:
    case w_king:
      slidingPiece = false;
      posMoves = 8;
      break;
  };

  //Loop through all of the pieces that we wish to be moved (all the black pawns, all the black rooks, etc.)
  for(it = piece.begin(); it != piece.end(); ++it) {
    //Loop through the possible directions the piece can move
    for(int i = 0; i < posMoves; ++i) {
      //Create a new move based on the direction indexed into colDir/rowDir from constants.h this gives us our cardinal directions based on the piece given
      colMod = colDir[pieceRepr][i] * dir;
      rowMod = rowDir[pieceRepr][i] * dir;
      potentialLoc = Move(it->row, it->col, it->row + rowMod, it->col + colMod, pieceCharacters[pieceRepr]);
      initialLoc = potentialLoc;
      potentialLoc = pushLocations(potentialLoc, rowMod, colMod, slidingPiece, attFlag);
      if (pieceRepr == w_knight || pieceRepr == b_knight) {
        potentialLoc = initialLoc;
      }
      attackLocations(potentialLoc, attackPieces, attFlag); 
    }
  }
  playerRepr = prev;
}

//We gen pawn seperately because of the various rules, en passant, promotion, 2 square moves etc...
void Board::genPawn(const bool attVectorFlag) {
  int dir, startingRow, prev;
  std::vector<Move> attackPieces = locations[b_pieces - playerRepr];
  std::vector<Move>::iterator it;
  std::vector<Move>::iterator attackIt;
  bool inbounds = false;
  Move potLoc;
  bool twoPush = false;
  bool valid = false;
  prev = playerRepr;
  
  //Check for the enpassant square generated from the FENstring, and we can add that as a 'piece' to eb taken
  //in the attack pieces vector
  if (enpSquare != "-") {
    attackPieces.push_back(loc_repr(enpSquare));
  }
  //Determines the direction the pawns move,  as well as determining if they are eligible for a 2 square movement
  if (playerRepr > 0) {
    dir = 1;
    startingRow = 1;
  } else {
    dir = -1;
    startingRow = 7;
  }

  if(attVectorFlag) {
    playerRepr = (playerRepr > w_pawn) ? w_pawn : b_pawn;
    dir *= -1;
  }
  std::vector<Move> piece = locations[w_pawn + playerRepr];
  //Check for empty squares and non attacking moves
  for(it = piece.begin(); it != piece.end(); ++it) {
    //If the row the pawn is currently on the starting row for its respective color, the number of possible pushes is 2, 1 space forward and 2 spaces forawrd
    if(!attVectorFlag) {
      twoPush = (it->row == startingRow) ? true : false;
      potLoc = Move(it->row, it->col, it->row + rowDir[w_pawn][0] * dir, it->col + colDir[w_pawn][0] * dir, pieceCharacters[w_pawn]);
      valid = !isSafe(potLoc.nRow, potLoc.nCol) && m_board[potLoc.nRow][potLoc.nCol] == '-';
      if(valid) {
        validMoves.push_back(potLoc);
        if(twoPush) {
          potLoc.nRow += rowDir[w_pawn][0] * dir;
          potLoc.nCol += colDir[w_pawn][0] * dir;
          if(m_board[potLoc.nRow][potLoc.nCol] == '-') {
            validMoves.push_back(potLoc);
          }
        }
      }
    }
    for(int k = -1; k < 2; k+=2) {
      if(!isSafe(it->row + dir, it->col + k)) {
        if(attVectorFlag) {
          attackVector.push_back(Move(it->row, it->col, it->row + dir, it->col + k, pieceCharacters[w_pawn]));
        } else {
          for(attackIt = attackPieces.begin(); attackIt != attackPieces.end(); ++attackIt) {
            potLoc = Move(it->row, it->col, it->row + dir, it->col + k, pieceCharacters[w_pawn]);
            if(attackIt->row == potLoc.nRow && attackIt->col == potLoc.nCol) {
              potLoc.capture = true;
              if(attVectorFlag) {
                attackVector.push_back(potLoc);
              } else {
                validMoves.push_back(potLoc);
              }
            }
          }
        }
      }
    }
  }
  playerRepr = prev;
}

void Board::genAll(const bool attFlag) {
  std::vector<Move>::iterator it;
  genPawn(attFlag);
  for(int i = w_rook; i < w_pieces; ++i) {
    genMove(i, attFlag);
  }

  if(attFlag) {
    for(it = attackVector.begin(); it != attackVector.end(); ++it) {
      m_attBoard[it->nRow][it->nCol] = 'X';
    }
  }
}

bool Board::inCheck() {
  Move kingLoc = locations[w_king + playerRepr].front();
  genAll(true);

  /*
  if(std::any_of(attackVector.begin(), attackVector.end(), Move(kingLoc))) {
    return true;
  } else {
    return false;
  }*/

  if(m_attBoard[kingLoc.row][kingLoc.col] != '-') {
    return true;
  } else {
    return false;
  }
}

std::string Board::makeMove() {
  std::vector<Move>::iterator it;
  std::vector<Move> pieceLocations;
  std::vector<Move>::iterator mLoc;
  Board temp;
  Move sel;
  int locInd;


  for(it = validMoves.begin(); it != validMoves.end(); ++it) {
    temp = *this;
    temp.m_board[it->row][it->col] = '-';
    temp.m_board[it->nRow][it->nCol] = it->repr[0];
    /*locInd = playerRepr;
    switch (it->repr[0]) {
      case 'P':
        break;
      case 'R':
        locInd += w_rook;
        break;
      case 'N':
        locInd += w_knight;
        break;
      case 'B':
        locInd += w_bishop;
        break;
      case 'Q':
        locInd += w_queen;
        break;
      case 'K':
        locInd += w_king;
        break;
      default:
        std::cout << "YOU SHOULD NEVER BE HERE\n\n";
        break;
    };
    pieceLocations = temp.locations[locInd];
    for(mLoc = pieceLocations.begin(); mLoc != pieceLocations.end(); ++mLoc) {
      if(mLoc->row == it->row && mLoc->col == it->col) {
        mLoc->nRow = it->nRow;
        mLoc->nCol = it->nCol;
      }
    }
    */

    if(temp.inCheck()) {
      validMoves.erase(it);
    }
  }
  return (validMoves.at(std::rand() % validMoves.size()).moveRepr());

}

void Board::heuristic() {
  
}




