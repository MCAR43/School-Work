#include "bboard.hpp"
//Begin Utility Functions
//
//
//
namespace utils {
  U64 soutOne(const U64 b) {return (b >> 8);}
  U64 nortOne(const U64 b) {return (b << 8);}
  int bitSerialization(U64 b) {
    for(int i = 0; i < b.size(); ++i) {
      if(b.test(i)) {
        return i;
      }
    }
    return -1;
  }

  int revBitSerialization(U64 b) {
    for(int i = b.size() - 1; i >= 0; --i) {
      if(b.test(i)) {
        return i;
      }
    }
    return -1;
  }

  int findBoard(const U64 _pBB[N_BOARDS], const int idx, const int color) {
    for(int i = color + 2; i < w_king; i+=2) {
      if(_pBB[i].test(idx)) {
        return i;
      }
    }
    return -1;
  }

  int findIdx(const std::string val) {
    for(int i = 0; i < 64; ++i) {
      if(INDEX_REPR[i] == val){
        return i;
      }
    }
  }

}

//End Utility Functions

Bitboard::Bitboard() {
  for(int i = 0; i < N_BOARDS; ++i) {
    _pBB[i].reset();
  }
  _empty.reset();
  _all.reset();
  _children.clear();
  _moveList.clear();
  _eval = 0;
  _enpIdx = -1;
}

Bitboard Bitboard::operator=(const Bitboard copy_board) {
  for(int i = 0; i < N_BOARDS; ++i) {
    _pBB[i] = copy_board._pBB[i];
  }
  _empty = copy_board._empty;
  _all = copy_board._all;
  _color = copy_board._color;
  //_moveList = copy_board._moveList;
  _children.clear();
  assocMove = copy_board.assocMove;
  _enpIdx = copy_board._enpIdx;
  return *this;
}

bool operator==(const Bitboard lhs, const Bitboard rhs) { 
  for(int i = 0; i < N_BOARDS; ++i) {
    if(lhs.getPiece(i) != rhs.getPiece(i)) {
      return false;
    }
  } 
  return true;
}

Bitboard::Bitboard(const std::vector<std::string> FEN, 
    const std::string castling, 
    const std::string enpSquare, 
    const std::string pColor) {
      _color = pColor == "white" ? white : black;
      if(enpSquare != "-") {
        _enpIdx = utils::findIdx(enpSquare);
      } else {
        _enpIdx = -1;
      }
      update(FEN);
}

void Bitboard::update(std::vector<std::string> _FEN) {
  int rankIndex = 0;
  int fileIndex = 0;
  std::string rank;
  std::reverse(_FEN.begin(), _FEN.end());
  for(int i = 0; i < _FEN.size(); ++i) {
    rank = _FEN[i];
    rankIndex = 0;
    for(int k = 0; k < rank.length(); k++) {
      switch(rank[k]) {
        case 'R':
          _pBB[w_rook].set(rankIndex + fileIndex); break;
        case 'N':
          _pBB[w_knight].set(rankIndex + fileIndex); break;
        case 'B':
          _pBB[w_bishop].set(rankIndex + fileIndex); break;
        case 'Q':
          _pBB[w_queen].set(rankIndex + fileIndex); break;
        case 'K':
          _pBB[w_king].set(rankIndex + fileIndex); break;
        case 'P':
          _pBB[w_pawn].set(rankIndex + fileIndex); break;
        
        case 'r':
          _pBB[b_rook].set(rankIndex + fileIndex); break;
        case 'n':
          _pBB[b_knight].set(rankIndex + fileIndex); break;
        case 'b':
          _pBB[b_bishop].set(rankIndex + fileIndex); break;
        case 'q':
          _pBB[b_queen].set(rankIndex + fileIndex); break;
        case 'k':
          _pBB[b_king].set(rankIndex + fileIndex); break;
        case 'p':
          _pBB[b_pawn].set(rankIndex + fileIndex); break;
        default:
          if (isdigit(rank[k])) {
            rankIndex += (static_cast<int>(rank[k]) - '0') - 1;
          }
      }
      rankIndex++;
    }
    fileIndex+=8;
  }
  _pBB[n_white] = (_pBB[w_pawn] | _pBB[w_rook] | _pBB[w_bishop] | _pBB[w_knight] | _pBB[w_queen] | _pBB[w_king]);
  _pBB[n_black] = (_pBB[b_pawn] | _pBB[b_rook] | _pBB[b_bishop] | _pBB[b_knight] | _pBB[b_queen] | _pBB[b_king]);
  _empty = ~(_pBB[n_white] | _pBB[n_black]);
  _all = (_pBB[n_white] | _pBB[n_black]);
}

void Bitboard::print(const U64 board) {
  for(int i = 7; i >= 0; --i) {
    std::cout << i + 1 << "| ";
    for(int k = 0; k < 8; ++k) {
      std::cout << board[(i * 8) + k] << " ";
    }
    std::cout << std::endl;
  }
  std::cout << "   ---------------\n   a b c d e f g h\n";
}

void Bitboard::printAll() {
  for (int piece = 0; piece < N_BOARDS; ++piece) {
    std::cout << "BOARD ASSOCIATED WITH: " << piece << std::endl; 
    for(int i = 7; i >= 0; --i) {
      for(int k = 0; k < 8; ++k) {
        std::cout << _pBB[piece][(i * 8) + k];
      }
      std::cout << std::endl;
    }
  }
}



//Begin Move Generation
//


//Begin Pawn Generation


// <summary>
// Calculates the single push moves of the pawns for the current board
// which pawns are chosen is decided by the variable _color in the board class
// The pawns are calculated by logical ANDing the north/south shift of the pawn bitboard (_pBB[c_pawn])
// with the _empty pieces bitboard calculated from the update function.
//
// The resulting bitboard is called with generateMoves() which will serialize the inputs, and convert
// them to SAN notation
// </summary>
void Bitboard::singlePush() {
  if (_color == white) {
    generateMoves(-1, utils::nortOne(_pBB[w_pawn]) & _empty, 'P', false);
  } else {
    generateMoves(-1, utils::soutOne(_pBB[b_pawn]) & _empty, 'p', false);
  }
}


// <summary>
// Same as the singlePush() function but instead we calculate for double pushes
// First we determine which pawns are capable of double pushing (those that are on their beginning rank)
// which we find by an index into the RANK_MASK[] array in "constants.h".  We logical AND the bitboard of
// pawns with this mask to determine which pawns are on their starting rank.  Then this resulting bitboard is ANDed again with 
// the bitboard of all pawns shifted north/south and the empty bitboard to determine if there are any pieces in between the pawn
// on its starting rank, and the pawns final position.  
// </summary>
void Bitboard::doublePush() {
  if (_color == white) {
    U64 dPushPawns = _pBB[w_pawn] & RANK_MASK[1];
    dPushPawns = utils::nortOne(dPushPawns) & _empty;
    generateMoves(-2, utils::nortOne(dPushPawns) & _empty & RANK_MASK[3], 'P', false);
  } else {
    U64 dPushPawns = _pBB[b_pawn] & RANK_MASK[6];
    dPushPawns = utils::soutOne(dPushPawns) & _empty;
    generateMoves(-2, utils::soutOne(dPushPawns) & _empty & RANK_MASK[4], 'p', false);
  }
}

// <summary>
// This function is used to calculate the attack sets of the pawns.  It utilizes the PAWN_ATTACKS arrays in "constants.h" to 
// index into based on the pawns FILE-RANK position.  For example, a pawn on a2 will index into the PAWN_ATTACKS array based on its
// enumeration of a2 (8).  This returns a bitboard with the possible attack locations of a pawn on that specific tile, which we then
// logical AND with the bitboard of all the opposite color pieces.  This resulting bitboard is then sent to generateMoves() to be
// serialized and converted to SAN notation.
// </summary>
void Bitboard::pawnAttacks(const bool attMap) {
  U64 pawns;
  U64 valid;
  U64 attBoard;
  if (_color == white) {
    pawns = _pBB[w_pawn];
    attBoard = _pBB[n_black];
    if(_enpIdx != -1) {
      attBoard.set(_enpIdx); 
    }
    while(!pawns.none()) {
      int idx = utils::bitSerialization(pawns);
      pawns.flip(idx);
      valid = W_PAWN_ATTACKS[idx - 8];
      if(!attMap) {
        generateMoves(idx, valid & attBoard, 'P', true); 
      } else {
        _attMap |= ((valid & _empty) | (valid & attBoard));
      }
    }
  } else {
    pawns = _pBB[b_pawn];
    attBoard = _pBB[n_white];
    if(_enpIdx != -1) {
      attBoard.set(_enpIdx); 
    }
    while(!pawns.none()) {
      int idx = utils::bitSerialization(pawns);
      pawns.flip(idx);
      valid = B_PAWN_ATTACKS[idx - 8];
      if(!attMap) {
        generateMoves(idx, valid & attBoard, 'p', true); 
      } else {
        _attMap |= ((valid & _empty) | (valid & attBoard));
      }
    }
  }
}
//End Pawn Generation

//Begin Knight Generation

// <summary>
//
// </summary>
void Bitboard::knightMoves(const bool attMap) {
	U64 knights;
  U64 attPieces;
  char piece;
	if(_color == white) {
		knights = _pBB[w_knight];
    attPieces = _pBB[n_black];
    piece = 'N';
	} else {
    knights = _pBB[b_knight];
    attPieces = _pBB[n_white];
    piece = 'n';
  }
  while(!knights.none()) {
    int idx = utils::bitSerialization(knights);
    knights.flip(idx);

    if(!attMap) {
      generateMoves(idx, KNIGHT_ATTACKS[idx] & _empty, piece, false);
      generateMoves(idx, KNIGHT_ATTACKS[idx] & attPieces, piece, true);
    } else {
      _attMap |= ((KNIGHT_ATTACKS[idx]));
    }
  }
}

//End Knight Generation


//Begin King Generation
//
void Bitboard::kingMoves(const bool attMap) {
  U64 king;
  U64 attPieces;
  char piece;
  if(_color == white) {
    king = _pBB[w_king];
    attPieces = _pBB[n_black];
    piece = 'K';
  } else {
    king = _pBB[b_king];
    attPieces = _pBB[n_white];
    piece = 'k';
  }
  int idx = utils::bitSerialization(king);
  king.flip(idx);

  if(!attMap) {
    generateMoves(idx, KING_ATTACKS[idx] & _empty, piece, false);
    generateMoves(idx, KING_ATTACKS[idx] & attPieces, piece, true);
  } else {
    _attMap |= ((KING_ATTACKS[idx] &_empty) | (KING_ATTACKS[idx] & attPieces));
  }
}

//End King Generation
//

//Begin Bishop Gen
void Bitboard::bishopMoves(const bool attMap) {
  U64 valid;
  U64 bishops;
  U64 attPieces;
  U64 ray; 
  int blockerIdx = 0;
  char piece;
  if(_color == white) {
    bishops = _pBB[w_bishop];
    attPieces = _pBB[n_black];
    piece = 'B';
  } else {
    bishops = _pBB[b_bishop];
    attPieces = _pBB[n_white];
    piece = 'b';
  }
  while(!bishops.none()) {
    int idx = utils::bitSerialization(bishops);
    valid.reset();
    bishops.flip(idx);
    for(int i = 0; i < 8; i+=2) {
      ray = RAY_ATTACKS[i][idx];
      valid |= ray; 
      if(!(ray & _all).none()) {
        if(i == SOUTHWEST || i == SOUTHEAST) {
          blockerIdx = utils::revBitSerialization(ray & _all);
        } else {
          blockerIdx = utils::bitSerialization(ray & _all);
        }
        valid &= ~RAY_ATTACKS[i][blockerIdx];
      }
    }
    if(!attMap) {
      generateMoves(idx, valid & _empty, piece, false);
      generateMoves(idx, valid & attPieces, piece, true);
    } else {
      _attMap |= ((valid & _empty) | (valid & attPieces));
    }
  }
}

//Switch to magic bitboards instead of kindergarten eventually
void Bitboard::rookMoves(const bool attMap) {
  U64 valid;
  U64 rooks;
  U64 attPieces;
  U64 ray;
  int blockerIdx = 0;
  char piece;
  if(_color == white) {
    rooks = _pBB[w_rook];
    attPieces = _pBB[n_black];
    piece = 'R';
  } else {
    rooks = _pBB[b_rook];
    attPieces = _pBB[n_white];
    piece = 'r';
  }
  while(!rooks.none()) {
    int idx = utils::bitSerialization(rooks);
    valid.reset();
    rooks.flip(idx);
    for(int i = 1; i < 8; i+=2) {
      ray = RAY_ATTACKS[i][idx];
      valid |= ray; 
      if(!(ray & _all).none()) {
        if(i == SOUTH || i == WEST) {
          blockerIdx = utils::revBitSerialization(ray & _all);
        } else {
          blockerIdx = utils::bitSerialization(ray & _all);
        }
        valid &= ~RAY_ATTACKS[i][blockerIdx];
      }
    }
    if(!attMap) {
      generateMoves(idx, valid & _empty, piece, false);
      generateMoves(idx, valid & attPieces, piece, true);
    } else {
      _attMap |= ((valid & _empty) | (valid & attPieces));
    }
  }
}


void Bitboard::queenMoves(const bool attMap) {
  U64 valid;
  U64 queen;
  U64 attPieces;
  U64 ray;
  int blockerIdx = 0;
  char piece;
  if(_color == white) {
    queen = _pBB[w_queen];
    attPieces = _pBB[n_black];
    piece = 'Q';
  } else {
    queen = _pBB[b_queen];
    attPieces = _pBB[n_white];
    piece = 'q';
  }
  if(!queen.none()) {
    int idx = utils::bitSerialization(queen);
    for(int i = 0; i < 8; ++i) {
      ray = RAY_ATTACKS[i][idx];
      valid |= ray; 
      if(!(ray & _all).none()) {
        if(i == WEST || i == SOUTHWEST || i == SOUTHEAST || i == SOUTH) {
          blockerIdx = utils::revBitSerialization(ray & _all);
        } else {
          blockerIdx = utils::bitSerialization(ray & _all);
        }
        valid &= ~RAY_ATTACKS[i][blockerIdx];
      }
    }
    if(!attMap) {
      generateMoves(idx, valid & _empty, piece, false);
      generateMoves(idx, valid & attPieces, piece, true);
    } else {
      _attMap |= ((valid & _empty) | (valid & attPieces));
    }
  }
}

U64 Bitboard::allMoves(const bool attMap) {
  int orig = _color;
  if(!attMap) {
    singlePush();
    doublePush();
  } else {
    _color = (_color == white) ? black : white;
  }
  pawnAttacks(attMap);
  knightMoves(attMap);
  bishopMoves(attMap);
  rookMoves(attMap);
  queenMoves(attMap);
  kingMoves(attMap);
  _color = orig;
  return _attMap;
}


Bitboard Bitboard::makeMove(Move & m) {
  U64 result;
  int enemyColor = (_color == white) ? black : white;
  int boardIdx = enemyColor;
  //Generalized piece location board
  _all.reset(m._origPos);
  _all.set(m._endPos);
  //Specific piece board
  
  if(m.promotion == "q" || m.promotion == "Q") {
    _pBB[_color + 2].reset(m._origPos);
  } else {
    _pBB[m._bbLookup].reset(m._origPos);
  }
  _pBB[m._bbLookup].set(m._endPos);
  //n_COLOR generalized location board
  _pBB[_color].reset(m._origPos);
  _pBB[_color].set(m._endPos);
  //If there is a captured piece we must also remove it from the enemy board
  //for calculating attack maps

  if(m._capture == "x") {
    boardIdx = utils::findBoard(_pBB, m._endPos, enemyColor);
    _pBB[enemyColor].reset(m._endPos);
    _pBB[boardIdx].reset(m._endPos);
    m._eval = PIECE_VALUES[boardIdx];
  }
  this->_color = enemyColor;
  return *this;
}

void Bitboard::undoMove(const Move m) {
  int enemyColor = (_color == white) ? black : white;
  int boardIdx = enemyColor;
  _color = (_color == white) ? black : white;
  //Generalized piece location board
  _all.set(m._origPos);
  _all.reset(m._endPos);

  if(m.promotion == "q" || m.promotion == "Q") {
    _pBB[_color + 2].set(m._origPos);
  } else {
    _pBB[m._bbLookup].set(m._origPos);
  }
  //Specific piece board
  _pBB[m._bbLookup].reset(m._endPos);

  //Enemyies generalized location board
  _pBB[_color].set(m._origPos);
  _pBB[_color].reset(m._endPos);

  //If there is a captured piece we must also remove it from the enemy board
  //for calculating attack maps
  if(m._capture == "x") {
    boardIdx = utils::findBoard(_pBB, m._endPos, enemyColor);
    _pBB[enemyColor].set(m._endPos);
    _pBB[boardIdx].set(m._endPos);
  }
  this->_color = enemyColor;
}

void Bitboard::filterLegal() {
  int enemyInd, enemyColor, kingInd;
  U64 inCheck;
  Bitboard res;
  U64 attmap;
  std::vector<Move> _filtered;
  std::vector<Bitboard> _newChildren;
  if(_color == white) {
    enemyColor = black;
    enemyInd = n_white;
    kingInd = w_king;
  } else {
    enemyColor = white;
    enemyInd = n_black;
    kingInd = b_king;
  }

  allMoves(false);
  for(std::vector<Move>::iterator it = _moveList.begin(); it != _moveList.end(); ++it) {
    res = (makeMove(*it));
    attmap = res.allMoves(true);
    inCheck = res._pBB[kingInd] & attmap; 
    if(inCheck.none()) {
      res._children.clear();
      res._moveList.clear();
      res.assocMove = *it;
      res._color = enemyColor;
      _newChildren.emplace_back(res);
      _filtered.push_back(*it);
    }
    undoMove(*it);
  }
  _moveList = _filtered;
  _children = _newChildren;
}

void Bitboard::generateMoves(const int oPos, const U64 b, const char piece, const bool cap) {
  U64 board = b;
  while(!board.none()) {
    int idx = utils::bitSerialization(board);
    board.flip(idx);
    _moveList.push_back(Move(oPos, idx, piece, cap));
  }
}

int Bitboard::evalBoard() {
  int pieceCount = 0;
  int pieceValue = 0;
  int mod = (_color == black) ? -1 : 1;
  _eval = 0;
  for(int i = 2; i < 14; ++i) {
    _eval += (PIECE_VALUES[i] * _pBB[i].count()) * mod;
  }
  assocMove._eval = _eval;
  return _eval; 
}

bool Bitboard::isQuiescent() {
  U64 attackPos = allMoves(true);
  U64 kingPos = _pBB[w_king + _color];
  if(!(kingPos & attackPos).none()) {
    return false;
  } 

  for(std::vector<Move>::iterator it = _moveList.begin(); it != _moveList.end(); ++it) {
    if(it->_capture != "") {
      return false;
    }  
  }

  return true;
}


