// AI
// This is where you build your AI

#include "ai.hpp"
#include <vector>
#include <sstream>
#include <chrono>
using namespace std::chrono;
/// <summary>
/// std::string split implementation by using delimiter as a character.
/// </summary>
std::vector<std::string> string_split(std::string str_to_split, char delimeter)
{
    std::stringstream ss(str_to_split);
    std::string item;
    std::vector<std::string> split_strings;
    while (std::getline(ss, item, delimeter))
    {
        split_strings.push_back(item);
    }

    return split_strings;
}

/// <summary>
/// Pretty formats an FEN string to a human readable string.
///
/// For more information on FEN (Forsyth-Edwards Notation) strings see:
/// https://wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
/// </summary>
std::string prettyFEN(std::string fen, std::string us)
{
    // split the FEN string up to help parse it
    auto split = string_split(fen, ' ');
    auto first = split[0]; // the first part is always the board locations

    auto sideToMove = split[1].at(0); // always the second part for side to move
    auto usOrThem = sideToMove == us.at(0) ? "us" : "them";

    auto fullmove = split[5]; // always the sixth part for the full move

    auto lines = string_split(first, '/');
    std::stringstream strings;
    strings << "Move: " << fullmove << "\n"
            << "Side to move: " << sideToMove << " (" << usOrThem << ")\n"
            << "   +-----------------+";

    int i = 9;
    for (auto line : lines)
    {
        i--;
        strings << "\n " << (i) << " |";
        for (char &character : line)
        {
            int asInt = (int)character - 48; // test for char '1' -> int 1
            if (asInt > -1 && asInt < 9)
            {
                // blank tiles n times, so repeat the . that many times
                for (int j = 0; j < asInt; j++)
                {
                    strings << " .";
                }
            }
            else
            {
                // it was a regular character for a piece
                strings << ' ' << character;
            }
        }
        strings << " |";
    }
    strings << "\n   +-----------------+\n     a b c d e f g h\n";

    return strings.str();
}

void printMoves(std::vector<Move> moveList) {
  std::vector<Move>::iterator it;
  std::cout << "Valid Moves: ";
  for(it = moveList.begin(); it != moveList.end(); ++it) {
    std::cout << ", " << it->moveRepr();
  }
  std::cout << std::endl;
}

namespace cpp_client
{

namespace chess
{

/// <summary>
/// This returns your AI's name to the game server.
/// Replace the string name.
/// </summary>
/// <returns>The name of your AI.</returns>
std::string AI::get_name() const
{
    // REPLACE WITH YOUR TEAM NAME!
    return "Swampletics";
}

/// <summary>
/// This is automatically called when the game first starts, once the game objects are created
/// </summary>
void AI::start()
{
  if(this->player->color == "white") {
    board.playerRepr = w_pawn;
  } else {
    board.playerRepr = b_pawn;
  }
}

/// <summary>
/// This is automatically called the game (or anything in it) updates
/// </summary>
void AI::game_updated()
{
  // If a function you call triggers an update this will be called before it returns.
}

/// <summary>
/// This is automatically called when the game ends.
/// </summary>
/// <param name="won">true if you won, false otherwise</param>
/// <param name="reason">An explanation for why you either won or lost</param>
void AI::ended(bool won, const std::string &reason)
{
    // You can do any cleanup of your AI here.  The program ends when this function returns.
}

/// <summary>
/// This is called every time it is this AI.player's turn to make a move.
/// </summary>
/// <returns>A string in Standard Algebriac Notation (SAN) for the move you want to make. If the move is invalid or not properly formatted you will lose the game.</returns>
std::string AI::make_move()
{
    /*******************************************************************************************************
     * IMPORTANT SERVER VARIABLES TO KNOW:
     *******************************************************************************************************
     * 
     * * Game.History
     *      - The list of moves that have occurred in the game so far in SAN.
     *
     * * Game.Fen
     *      - The FEN string representing the current board state. Updated every turn
     *      - For more info about FEN strings: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
     *
     * * Player
     *      - Your player object.
     *      - Important properties:
     *          * Player.Color
     *              - Your client's color ("white" or "black")
     *          * Player.Opponent
     *              - Your opponent's player object.
     *
     * NOTE THAT ALL OBJECT INFORMATION IS CONTAINED IN Joueur.cpp/games/chess/
     * HOWEVER, DO NOT CHANGE ANY OF THESE FILES EXCEPT FOR ai.cpp, ai.hpp, AND ANY OTHER FILES YOU MAY ADD YOURSELF
     * 
     *******************************************************************************************************
     * STANDARD ALGEBRAIC NOTATION
     *******************************************************************************************************
     * 
     * * When returning your move in Standard Algebraic Notation (SAN), the way I recommend is to first
     *   indicate the piece type if the piece is not a pawn, then the starting square's file and rank, then
     *   an x if there is a capture, then the ending square's file and rank.
     *   
     * * Pieces are indicated as R for Rook, N for Knight, B for Bishop, Q for Queen, and K for King. Pawns
     *   are not denoted by any letter.
     * 
     * * For castling in SAN, king-side castling is indicated by "O-O", while queen-side castling is
     *   indicated by "O-O-O".
     * 
     * * To promote a pawn when it reaches the other side of the board, add the type of piece to promote to
     *   at the end of the string.
     *   
     * * All SAN is case sensitive.
     * 
     * * Some examples:
     *      - Move a pawn from a2 to a4: a2a4
     *      - Capture a piece with a pawn from c6 to d5: c6xd5
     *      - Move a knight from b1 to c3: Nb1c3
     *      - Capture a piece with a queen from h3 to e6: Qh3xe6
     *      - King-side castle: O-O
     *      
     * * For more info about SAN: https://en.wikipedia.org/wiki/Algebraic_notation_(chess)
     * 
     *******************************************************************************************************/
    //Printing out details of the board
    
    std::cout << prettyFEN(this->game->fen, this->player->color);
    std::vector<std::string> _FEN = string_split(this->game->fen, ' ');
    std::cout << "FEN: " << this->game->fen << std::endl;  
 
    //the move that will be chosen after the minimax
    Move chosenMove;
    chosenMove.relativeValue = -9999;
    //Update the board with the new FENstrings
    board.update(string_split(_FEN.front(), '/'), _FEN[3], _FEN[2]);
    //Iteratively call minimax with increasing depth limits
    /*
    if(this->player->color == "white") {
      high_resolution_clock::time_point t1 = high_resolution_clock::now();
      for(int i = 0; i < MAX_DEPTH + 1; ++i) {
        mmax(chosenMove,board, i, true, -100000, 100000, t1, this->player->time_remaining / ESTIMATED_NUM_MOVES);
      }
    } else {
      generateMoves(board);
      chosenMove = _validVec[std::rand() % _validVec.size()];
    }
    */
    generateMoves(board);
    chosenMove = makeMove(board, _validVec[std::rand() % _validVec.size()]).associatedMove;
    return chosenMove.moveRepr(); 
}


// You can add additional methods here for your AI to call
Move AI::pushGen(Move & potMove, const int rowMod, const int colMod, const bool isSlider, const bool attFlag) {
  bool valid = !board.isSafe(potMove.nRow, potMove.nCol) && board.m_board[potMove.nRow][potMove.nCol] == '-';
  //We start in a while loop just in case the piece is a slider (bishop, rook, etc.)
  while(valid) {
    //If we are generating the attack vector add the valid move to the attack vector, else add to the valid moves vector
    if(attFlag) {
      _attVec.push_back(potMove); 
    } else {
      _validVec.push_back(potMove);
    }

    //Increment the move and determine if it is valid, if it is valid, loop again, else return the move 
    if(!isSlider) {
      return potMove;
    } else {
      potMove.nRow += rowMod;
      potMove.nCol += colMod;
      valid = !board.isSafe(potMove.nRow, potMove.nCol) && board.m_board[potMove.nRow][potMove.nCol] == '-';
    }
  };
  return potMove;
}

void AI::attGen(Move potMove, const bool attFlag, const int playerID) {
  //We are just checking against the in bounds array, ebcause we are looking to take a piece
  bool valid = !board.isSafe(potMove.nRow, potMove.nCol);
  std::vector<Move>::iterator it;
  //The pieces that we are looking to take (w_pieces, or b_pieces in the location vector)
  std::vector<Move> attPieces = board.locations[b_pieces - playerID];
  if(valid) {
    for(it = attPieces.begin(); it != attPieces.end(); ++it) {
      if(it->row == potMove.nRow && it->col == potMove.nCol) {
        potMove.capture = true;
        if(attFlag) {
          _attVec.push_back(potMove);
        } else {
          _validVec.push_back(potMove);
        }
      }
    }
  }
}

void AI::moveGen(const int pieceRepr, const bool attFlag) {
  int playerID = (attFlag ? (board.playerRepr > w_pawn ? w_pawn : b_pawn) : board.playerRepr);
  int posMoves, colMod, rowMod;
  bool slidingPiece = false;

  Move potLoc, initLoc;
  std::vector<Move> piece = board.locations[pieceRepr + playerID];
  std::vector<Move>::iterator it;
  
  //Determine the amount of places a certain piece can go to, rooks and bishops can move in 4 directions, kings 8, etc.
  //Also determine if the piece is a sliding piece (rook, bishop, etc.)
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

  //Loop through all of the selected pieces (all pawns, all rooks, etc.)
  for(it = piece.begin(); it != piece.end(); ++it) {
    //Loop through all possible moves that thus piece could have, regardless of if its valid
    for(int i = 0; i < posMoves; ++i) {
      //Get the direction and modifier that this piece will use from constants.h and mulitply it by dir
      //dir represents the direction the pieces move
      colMod = colDir[pieceRepr][i];
      rowMod = rowDir[pieceRepr][i];
      potLoc = Move(it->row, it->col, it->row + rowMod, it->col + colMod, pieceCharacters[pieceRepr + playerID]);

      initLoc = potLoc;
      //Call pushGen to determine push locations for the specified piece and move
      potLoc = pushGen(potLoc, rowMod, colMod, slidingPiece, attFlag);
      if(pieceRepr == w_knight || pieceRepr == b_knight || pieceRepr == b_king || pieceRepr == w_king) {
        potLoc = initLoc;
      }
      //Call attgen for the spicified piece and move
      attGen(potLoc, attFlag, playerID);
    }
  }
}

void AI::pawnGen(const bool attFlag) {
  int dir, startingRow, playerID, rowMod, colMod;
  bool twoPush, valid;
  Move potMove;
  std::vector<Move>::iterator it;
  playerID = (attFlag ? (board.playerRepr > w_pawn ? w_pawn : b_pawn) : board.playerRepr);
  std::vector<Move> attPieces = board.locations[b_pieces - playerID];
  std::vector<Move> piece = board.locations[w_pawn + playerID];
  dir = 1;
  twoPush = valid = false;

  if(playerID > 0) {
    dir = 1;
    startingRow = 1;
  } else {
    dir = -1;
    startingRow = 6;
  }
  rowMod = rowDir[w_pawn][0] * dir;
  colMod = colDir[w_pawn][0] * dir;
  for(it = piece.begin(); it != piece.end(); ++it) {
    if(!attFlag) {    
      twoPush = (it->row == startingRow) ? true : false;
      potMove = Move(it->row, it->col, it->row + rowMod, it->col + colMod, pieceCharacters[w_pawn + playerID]);
      valid = !board.isSafe(potMove.nRow, potMove.nCol) && board.m_board[potMove.nRow][potMove.nCol] == '-';
      if(valid) {
        _validVec.push_back(potMove);
        if(twoPush) {
          potMove.nRow += rowMod;
          potMove.nCol += colMod;
          if(board.m_board[potMove.nRow][potMove.nCol] == '-') {
            _validVec.push_back(potMove);
          }
        }
      }
    }

    for(int k = -1; k < 2; k+=2) {
      potMove = Move(it->row, it->col, it->row + dir, it->col + k, pieceCharacters[w_pawn + playerID]);
      if(!board.isSafe(potMove.nRow, potMove.nCol)) {
        if(attFlag) {
          _attVec.push_back(potMove);
        } else {
          attGen(potMove, attFlag, playerID);
        }
      }
    }
  }
}

void AI::wrapperGen(const bool attFlag) {
  pawnGen(attFlag);
  for(int i = w_rook; i < w_pieces; ++i) {
    moveGen(i, attFlag);
  }
}

std::vector<Move> AI::generateMoves(const Board b) {
  std::vector<Move> filteredMoves;
  std::vector<Move>::iterator it;
  Move kingLoc = b.locations[w_king + b.playerRepr].front();
  _validVec.clear();
  board = b;
  wrapperGen(false);
  for(it = _validVec.begin(); it != _validVec.end(); ++it) {
    board = b;
    //Locates the matching piece in the correct location vector and changes its location
    board = makeMove(board, *it);
    //Remove the king from the b to check for pinned pieces
    board.m_board[kingLoc.row][kingLoc.col] = '-';
    wrapperGen(true);
    board.m_board[kingLoc.row][kingLoc.col] = kingLoc.repr[0];
    if(!board.inCheck(_attVec)) {
      board.boardHeuristic();
      it->relativeValue = board.relativeValue;
      filteredMoves.push_back(*it);
    }
  }
  _validVec = filteredMoves;
  return filteredMoves;
}

int AI::mmax(Move & bestMove, Board node, int depth, bool maximizer, int alpha, int beta, std::chrono::high_resolution_clock::time_point t1, const double maxTime) { 
  if(duration_cast<duration<double> >(high_resolution_clock::now() - t1).count() > maxTime) {
    return 0;
  }
  if(depth == 0) {
    return node.boardHeuristic(); 
  }
  if(maximizer) {
    int max = -9999;
    //Generate moves for current Node
    node.playerRepr = (this->player->color == "white") ? w_pawn : b_pawn;
    generateMoves(node);
    for(std::vector<Move>::iterator it = _validVec.begin(); it != _validVec.end(); ++it) {
      makeMove(node, *it);
    }
    for(std::vector<Board>::iterator _child = node._children.begin(); _child != node._children.end(); ++_child) {
      int val = mmax(bestMove, *_child, depth - 1, false, alpha, beta, t1, maxTime);
      max = std::max(max, val);
      if (bestMove.relativeValue > max) {
        bestMove = node.associatedMove;
      }
      alpha = std::max(alpha, max);
      if (beta <= alpha) {
        break;
      }
    }
    return node.boardHeuristic(); 
  } else {
    int min = 9999;
    //Generate Moves for current node after switching player sides
    node.playerRepr = (this->player->color == "white") ? b_pawn : w_pawn;
    generateMoves(node);
    for(std::vector<Move>::iterator it = _validVec.begin(); it != _validVec.end(); ++it) {
      makeMove(node, *it);
    }
    for(std::vector<Board>::iterator _child = node._children.begin(); _child != node._children.end(); ++_child) {
      int val = mmax(bestMove, *_child, depth - 1, true, alpha, beta, t1, maxTime); 
      min = std::min(min, val);
      if (bestMove.relativeValue < min) {
        bestMove = node.associatedMove;
      }
      beta = std::min(beta, min);
      if (beta <= alpha) {
        break;
      }
    }
    return node.boardHeuristic(); 
  }
}

} // namespace chess

} // namespace cpp_client





