#include "bitboard.h"
Bitboard::Bitboard() {
  for(int i = 0; i < numBitBoards; i++) {
    m_piecesBoard[i].reset();
  }
  m_clearBoard.reset();
  m_occupiedBoard.reset();
}

void Bitboard::update(const std::vector<std::string> FEN) {
  int rankIndex = 0;
  int fileIndex = 56;
  std::string rank;
  }

  for(int i = 0; i < FEN.size(); i++) {
    rank = FEN[i];
    rankIndex = 7;
    for(int k = 0; k < rank.length(); k++) {
      switch(rank[k]) {
        case 'R':
          m_piecesBoard[whiteRook].set(rankIndex + fileIndex); break;
        case 'N':
          m_piecesBoard[whiteKnight].set(rankIndex + fileIndex); break;
        case 'B':
          m_piecesBoard[whiteBishop].set(rankIndex + fileIndex); break;
        case 'Q':
          m_piecesBoard[whiteQueen].set(rankIndex + fileIndex); break;
        case 'K':
          m_piecesBoard[whiteKing].set(rankIndex + fileIndex); break;
        case 'P':
          m_piecesBoard[whitePawn].set(rankIndex + fileIndex); break;
        
        case 'r':
          m_piecesBoard[blackRook].set(rankIndex + fileIndex); break;
        case 'n':
          m_piecesBoard[blackKnight].set(rankIndex + fileIndex); break;
        case 'b':
          m_piecesBoard[blackBishop].set(rankIndex + fileIndex); break;
        case 'q':
          m_piecesBoard[blackQueen].set(rankIndex + fileIndex); break;
        case 'k':
          m_piecesBoard[blackKing].set(rankIndex + fileIndex); break;
        case 'p':
          m_piecesBoard[blackPawn].set(rankIndex + fileIndex); break;
        
        default:
          if (isdigit(rank[k])) {
            rankIndex -= (static_cast<int>(rank[k]) - '0') - 1;
          }
      }
      rankIndex--;
    }
    fileIndex-=8;
  }
  m_piecesBoard[white] = (m_piecesBoard[whitePawn] | m_piecesBoard[whiteRook] | m_piecesBoard[whiteKnight] | m_piecesBoard[whiteBishop] | m_piecesBoard[whiteQueen] | m_piecesBoard[whiteKing]);
  m_piecesBoard[black] = (m_piecesBoard[blackPawn] | m_piecesBoard[blackRook] | m_piecesBoard[blackKnight] | m_piecesBoard[blackBishop] | m_piecesBoard[blackQueen] | m_piecesBoard[blackKing]);
  m_piecesBoard[all] = m_piecesBoard[white] | m_piecesBoard[black];
}


void Bitboard::print(const std::string board) {
  for(int k = 0; k < board.length(); k++) {
    std::cout << board[k];
    if ((k + 1) % 8 == 0) {
      std::cout << std::endl;
    }
  }
  std::cout << std::endl;
}

std::vector<std::string> Bitboard::genPawn(const std::string color) {
  std::vector<std::string> validMoves;
  std::bitset<64> moves;
  validMoves.clear();
  moves.reset();
  if (color == "white") {
    moves = ((m_piecesBoard[whitePawn] << 8) & (~(m_piecesBoard[all])));
  } else {
    moves = ((m_piecesBoard[blackPawn] >> 8) & (~(m_piecesBoard[all]))); 
  }
  for(int i = 0; i < moves.size(); i++) {
    if (moves.test(i)) {
      validMoves.push_back(rev_mapping[i]);
    }
  }
  return validMoves;
}

std::vector<std::string> Bitboard::genPawnAttack(const std::string color) {
  std::bitset<64> pawnMask;
  std::bitset<64> attackMask;
  std::vector<std::string> valid;
  if (color == "white") {
    pawnMask = m_piecesBoard[whitePawn];
    for(int i = 0; i < pawnMask.size(); i++) {
      if (pawnMask.test(i)) {
        if ((i + 1) % 8 == 0) {
           
        }
      }
    }
  } else {
    pawnMask = m_piecesBoard[blackPawn];
  }
}





