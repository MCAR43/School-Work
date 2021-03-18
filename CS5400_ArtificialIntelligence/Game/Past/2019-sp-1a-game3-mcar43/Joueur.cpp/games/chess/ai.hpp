#ifndef GAMES_CHESS_AI_HPP
#define GAMES_CHESS_AI_HPP

#include "impl/chess.hpp"
#include "game.hpp"
#include "game_object.hpp"
#include "player.hpp"

#include "../../joueur/src/base_ai.hpp"
#include "../../joueur/src/attr_wrapper.hpp"

// You can add additional #includes here
#include <set>
#include "board.hpp"
namespace cpp_client
{

namespace chess
{
/// <summary>
/// This is the header file for building your Chess AI
/// </summary>
class AI : public Base_ai
{
public:
    /// <summary>
    /// This is a reference to the Game object itself, it contains all the information about the current game
    /// </summary>
    Game game;

    /// <summary>
    /// This is a pointer to your AI's player. This AI class is not a player, but it should command this Player.
    /// </summary>
    Player player;

    // You can add additional class variables here.
    //Bitboard bitboard;
    Board board;
    std::vector<Move> _attVec;
    std::vector<Move> _validVec;
    std::set<Board> _tree;
    /// This returns your AI's name to the game server.
    /// Replace the string name.
    /// </summary>
    /// <returns>The name of your AI.</returns>
    virtual std::string get_name() const override;

    /// <summary>
    /// This is automatically called when the game first starts, once the game objects are created
    /// </summary>
    virtual void start() override;

    /// <summary>
    /// This is automatically called when the game ends.
    /// </summary>
    /// <param name="won">true if you won, false otherwise</param>
    /// <param name="reason">An explanation for why you either won or lost</param>
    virtual void ended(bool won, const std::string& reason) override;

    /// <summary>
    /// This is automatically called the game (or anything in it) updates
    /// </summary>
    virtual void game_updated() override;

    /// <summary>
    /// This is called every time it is this AI.player's turn to make a move.
    /// </summary>
    /// <returns>A string in Standard Algebriac Notation (SAN) for the move you want to make. If the move is invalid or not properly formatted you will lose the game.</returns>
    std::string make_move();
    

    // You can add additional methods here.
    
    // <summary>
    //
    // </summary>
    // <returns>
    //
    // </returns>
    Move pushGen(Move & potMove, const int rowMod, const int colMod, const bool isSlider, const bool attFlag);
    
    // <summary>
    //
    // </summary>
    // <returns>
    //
    // </returns>
    void attGen(Move potMove, const bool attFlag, const int playerID);


    // <summary>
    //
    // </summary>
    // <returns>
    //
    // </returns>
    void moveGen(const int pieceRepr, const bool attFlag);

    // <summary>
    //
    // </summary>
    // <returns>
    //
    // </returns>
    void pawnGen(const bool attFlag);
 
    // <summary>
    //
    // </summary>
    // <returns>
    //
    // </returns>
    void wrapperGen(const bool attFlag);

    // <summary>
    //
    // </summary>
    // <returns>
    //
    // </returns>
    std::vector<Move> generateMoves(const Board b);
    Board genToDepth(const int depth, std::vector<Board> _list, Board & gen);
    int mmax(Move & bestMove, Board node, int depth, bool maximizer, int alpha, int beta, std::chrono::high_resolution_clock::time_point t1, const double maxTime);
    Move minimizer(Move & bestMove, Board _curr, int depth);
    Move maximizer(Move & bestMove, Board _curr, int depth);
    Move whileMMAX(Move & bestMove, Board _curr, int depth, int repr);

    // ####################
    // Don't edit these!
    // ####################
    /// \cond FALSE
    virtual std::string invoke_by_name(const std::string& name,
                                       const std::unordered_map<std::string, Any>& args) override;
    virtual void set_game(Base_game* ptr) override;
    virtual void set_player(std::shared_ptr<Base_object> obj) override;
    virtual void print_win_loss_info() override;
    /// \endcond
    // ####################
    // Don't edit these!
    // ####################

};

} // CHESS

} // cpp_client

#endif // GAMES_CHESS_AI_HPP
