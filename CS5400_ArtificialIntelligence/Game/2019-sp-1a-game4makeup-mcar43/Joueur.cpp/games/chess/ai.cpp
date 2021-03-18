// AI
// This is where you build your AI

#include "ai.hpp"
#include <vector>
#include <sstream>
#include "bboard.hpp"

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

    int i = -1;
    for (auto line : lines)
    {
        i++;
        strings << "\n " << (8 - i) << " |";
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
    return "Chess C++ Player";
}

/// <summary>
/// This is automatically called when the game first starts, once the game objects are created
/// </summary>
void AI::start()
{
  for(int i = 0; i < 64; ++i) {
    for(int k = 0; k < 64; ++k) {
      hist_table[i][k] = 0;
    }
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
    Move bestMove;
    bestMove._eval = MAX_VALUE; 
    std::string SAN_RETURN;
    std::cout << prettyFEN(this->game->fen, this->player->color);
    std::vector<std::string> fenString = string_split(this->game->fen, ' ');
    std::cout << "Fen: " << fenString[0] << std::endl;
    Bitboard currentState(string_split(fenString[0], '/'), fenString[2], fenString[3], this->player->color);
    std::cout << "Current State:\n";
    srand(time(NULL));
    if(this->player->color == "white") {
      for(int i = 0; i < 4; ++i) {
        std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
        max(bestMove, i, 2, currentState, MAX_VALUE, MIN_VALUE, t1, this->player->time_remaining / 100);
      }
    } else {
      currentState.filterLegal();
      bestMove = currentState._moveList[std::rand() % currentState._moveList.size()];
    }
      
    SAN_RETURN = bestMove.SAN();
    std::cout << "Move: " << SAN_RETURN << std::endl;
    return SAN_RETURN; 
    
    // This will only work if we are black move the pawn at b2 to b3.
    // Otherwise we will lose.
    // Your job is to code SOMETHING to parse the FEN string in some way to determine a valid move, in SAN format.
     
}

// You can add additional methods here for your AI to call
int AI::max(Move & best, int depth, int qui_depth, Bitboard & state, int alpha, int beta,
            std::chrono::high_resolution_clock::time_point t1, const double maxTime) {
  
  
  high_resolution_clock::time_point t2 = high_resolution_clock::now();
  duration<double> time_span = duration_cast<duration<double> >(t2 - t1);
  if(time_span.count() > (maxTime / 1e9)) { 
    return 0;
  }
  
  if(depth == 0) {
    if(state.isQuiescent() || qui_depth <= 0) {
      int result = state.evalBoard();
      return result; 
    } else {
      qui_depth--;
    }
  } else {
    depth--;
  }

  int max = MAX_VALUE;
  state.filterLegal();
  if(state._moveList.empty()) {
    return 0;
  }
  for(std::vector<Bitboard>::iterator it = state._children.begin(); it != state._children.end(); ++it) {
    //std::cout << "(" << state._color << "|" << depth <<") : Maximizing-child--> " << it->assocMove.SAN() << " -- ";
    int eval = min(best, depth, qui_depth, (*it), alpha, beta, t1, maxTime) + hist_table[it->assocMove._origPos][it->assocMove._endPos];
    if(eval > max) {
      max = eval;
      best = it->assocMove;
    }
    alpha = std::max(alpha, eval);
    if(beta <= alpha) {
      break;
    }
  }
  hist_table[best._origPos][best._endPos] += (depth * depth);
  return max;
}

int AI::min(Move & best, int depth, int qui_depth, Bitboard & state, int alpha, int beta,
            std::chrono::high_resolution_clock::time_point t1, const double maxTime) {

  high_resolution_clock::time_point t2 = high_resolution_clock::now();
  duration<double> time_span = duration_cast<duration<double> >(t2 - t1);
  if(time_span.count() > maxTime / 1e9) { 
    return 0;
  }
  if(depth == 0) {
    if(state.isQuiescent() || qui_depth == 0) {
      int result = state.evalBoard();
      return result;
    } else {
      qui_depth--;
    }
  } else {
    depth--;
  }
  int min = MIN_VALUE;
  state.filterLegal();
  if(state._moveList.empty()) {
    return 0;
  }
  for(std::vector<Bitboard>::iterator it = state._children.begin(); it != state._children.end(); ++it) {
    //std::cout << "(" << state._color << "|" << depth <<") : Minimizing-child--> " << it->assocMove.SAN() << " -- ";
    int eval = max(best, depth, qui_depth, (*it), alpha, beta, t1, maxTime) + hist_table[it->assocMove._origPos][it->assocMove._endPos];
    if(eval < min) {
      min = eval;
      best = state.assocMove;
    }
    beta = std::min(beta, eval);
    if(beta <= alpha) {
      break;
    }
  }
  hist_table[best._origPos][best._endPos] += (depth * depth);
  return min;
}
} // namespace chess

} // namespace cpp_client
