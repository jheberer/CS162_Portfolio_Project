# Author: Jonathan Heberer
# Date: 11/22/2020
# Desc: File contains classes needed to play Focus Game board game

from Board import Board
from Player import Player


class FocusGame:
    """
    This class represents the game Focus. It is the primary point of interaction
    for the user. It also governs almost all object-to-object interactions within
    the program--for example, FocusGame will interact with both the Player and
    Board classes to perform captures, rather than having these classes interact
    directly.
    Attributes
    ----------
    current_player_turn : indicates which player's turn it is
    game_state : indicates the game state--whether it is a draw, in progress,
                 or a particular player has won
    player1 : tuple representing name and color of first player (player who begins game)
    player2 : tuple representing name and color of second player(player who acts second)
    """

    def __init__(self, player1, player2):
        """
        Initializes the game. Assigns players and play order based on input. Sets
        game state to default value (in progress). Calls Board class to initialize board.
        """
        player1_color = player1[1]
        player2_color = player2[1]
        player1_name = player1[0]
        player2_name = player2[0]

        self._board = Board(player1_color, player2_color)
        self._current_player_turn = player1_name
        self._player1 = Player(player1_name, player1_color)
        self._player2 = Player(player2_name, player2_color)
        self._game_state = 'IN PROGRESS'
        self._players = {player1_name: self._player1, player2_name: self._player2}

    def determine_game_state(self):
        """
        Method determines game_state using rules of game.
        Returns a string with one of the following values:
        -IN PROGRESS
        -PLAYER 1 WINS
        -PLAYER 2 WINS
        :return: the game_state of the game
        """
        if self._player1.get_captured() >= 6:
            return 'PLAYER 1 WINS'
        elif self._player2.get_captured() >= 6:
            return 'PLAYER 2 WINS'
        else:
            return 'IN PROGRESS'

    def show_pieces(self, tile_coord):
        """
        Takes a tuple with board position coordinates and returns a list with the
        value of pieces at the position (as a list)
        :param tile_coord: tuple containing board position coordinates
        :return: list showing number and ownership of pieces at position
        """
        return self._board.return_stack(tile_coord)

    def basic_move_validation(self, player_name, from_coordinates, to_coordinates, number_of_pieces):
        """
        Perform basic validations for attempted move. Following validations are made:
        - It is player's turn
        - Player has move-able piece at source
        - The source and target locations are on the board
        - Player is trying to move an invalid number of pieces
            - is negative
            - is larger than the stack size
            - cannot reach target coordinates with number of pieces
        :param player_name: name of player making move
        :param from_coordinates: tile to move pieces from
        :param to_coordinates: tile to move pieces to
        :param number_of_pieces: number of pieces to move
        :return: True if valid, False if invalid
        """

        # check if the coordinates are on the board. do this before other index manipulations to avoid errors
        all_coords = [from_coordinates[0], from_coordinates[1], to_coordinates[0], to_coordinates[1]]
        for coords in all_coords:
            if coords not in (0, 1, 2, 3, 4, 5):
                return False
        # can't move if the game is over
        if self._game_state != 'IN PROGRESS':
            return False
        # can't move if it's not your turn
        if player_name != self._current_player_turn:
            return False
        # can't perform a one piece move if there is not a piece on the board
        if number_of_pieces == 1 and len(self.show_pieces(from_coordinates)) == 0:
            return False
        # can't move a piece if it's not at the current location on the board
        if len(self.show_pieces(from_coordinates)) == 0:
            return False
        # can't move if the top piece of the stack does not belong to current player
        if self.show_pieces(from_coordinates)[-1] != self._players[player_name].get_color():
            return False
        # must move between 1 and (stack size) of pieces
        if number_of_pieces < 0 or number_of_pieces > len(self.show_pieces(from_coordinates)):
            return False
        # can only move the same number of tiles as number of pieces to be moved
        if abs(to_coordinates[0] - from_coordinates[0]) != number_of_pieces \
                and abs(to_coordinates[1] - from_coordinates[1]) != number_of_pieces:
            return False
        # no diagonal moves
        if to_coordinates[0] != from_coordinates[0] and to_coordinates[1] != to_coordinates[1]:
            return False

        return True

    def resolve_stacks(self, input_stack, player_name):
        """
        Method is used to resolve stacks when the number of pieces exceeds 5.
        :param player_name: the name of the player executing the move
        :param input_stack: the stack to be resolved after move
        :return: new stack to be placed on tile
        """
        pieces_to_resolve_cnt = len(input_stack) - 5
        i = 0

        player = self._players[player_name]

        while i < pieces_to_resolve_cnt:
            current_piece = input_stack[i]
            i += 1

            if current_piece == player.get_color():
                player.add_to_reserve()
            else:
                player.add_to_captured()

        new_stack = input_stack[pieces_to_resolve_cnt:]

        return new_stack

    def single_move(self, player_name, from_coordinates, to_coordinates):
        """
        Method helps move_piece by executing the logic for single moves.
        Move was already validated outside of method.
        Does not return anything--just updates board
        :param player_name: player executing the move
        :param from_coordinates: tuple indicating which piece is to be moved
        :param to_coordinates: tuple indicating which tile piece should move to
        """
        player = self._players[player_name]
        old_stack = self.show_pieces(from_coordinates)
        old_stack = old_stack[0:len(old_stack) - 1]
        new_stack = self.show_pieces(to_coordinates)
        new_stack.append(player.get_color())

        if len(new_stack) > 5:
            new_stack = self.resolve_stacks(new_stack, player_name)

        self._board.modify_tile(from_coordinates, old_stack)
        self._board.modify_tile(to_coordinates, new_stack)

    def multiple_move(self, player_name, from_coordinates, to_coordinates, number_of_pieces):
        """
        Method helps move_piece by executing the logic for multipiece moves.
        Method contains logic ot determine validity of move (for example,
        the piece belongs to the moving player).
        Returns True if move is valid, else return False.
        :param player_name: player executing the move
        :param from_coordinates: tuple indicating which piece is to be moved
        :param to_coordinates: tuple indicating which tile piece should move to
        :param number_of_pieces: int indicating number of pieces to move
        :return: boolean indicating whether move was successful
        """
        new_stack = self.show_pieces(to_coordinates)
        old_stack = self.show_pieces(from_coordinates)
        old_stack = old_stack[0:len(old_stack) - number_of_pieces]
        pieces_to_move = self.show_pieces(from_coordinates)[-number_of_pieces:]
        new_stack.extend(pieces_to_move)

        if len(new_stack) > 5:
            new_stack = self.resolve_stacks(new_stack, player_name)

        self._board.modify_tile(from_coordinates, old_stack)
        self._board.modify_tile(to_coordinates, new_stack)

    def move_piece(self, player_name, from_coordinates, to_coordinates, number_of_pieces):
        """
        Method moves player pieces. It will determine which kind of move is needed
        (for example, single vs multiple) and call the relevant helping method.
        Will resolve the outcome of the move (for example, if pieces are captured).
        Checks game_state at end of move to determine if player won.
        :param player_name: the player making the move
        :param from_coordinates: tuple indicating location on board that contains
                                 moving piece
        :param to_coordinates: tuple indicating location to move stack to
        :param number_of_pieces: int representing the number of pieces to move
        :return: message indicating the outcome of the move (failed, success, player won, etc.)
        """

        if not self.basic_move_validation(player_name, from_coordinates, to_coordinates, number_of_pieces):
            return False

        if number_of_pieces == 1:
            self.single_move(player_name, from_coordinates, to_coordinates)
            result = 'successfully moved'
        else:
            self.multiple_move(player_name, from_coordinates, to_coordinates, number_of_pieces)
            result = 'successfully moved'

        if self._current_player_turn == self._player1.get_name():
            self._current_player_turn = self._player2.get_name()
        else:
            self._current_player_turn = self._player1.get_name()

        self._game_state = self.determine_game_state()

        if self._game_state in ('PLAYER 1 WINS', 'PLAYER 2 WINS'):
            return f'{self._current_player_turn} wins'
        else:
            return result

    def show_reserve(self, player_name):
        """
        Method takes player name and returns the count of pieces player has in reserve
        :param player_name: player name as string
        :return: count (int) of pieces in reserve
        """
        if self._player1.get_name() == player_name:
            return self._player1.get_reserve()
        elif self._player2.get_name() == player_name:
            return self._player2.get_reserve()
        else:
            return False

    def show_captured(self, player_name):
        """
        Method takes player name and returns the count of pieces player has in reserve
        :param player_name: player name as string
        :return: count (int) of pieces captured
        """

        if self._player1.get_name() == player_name:
            return self._player1.get_captured()
        elif self._player2.get_name() == player_name:
            return self._player2.get_captured()
        else:
            return False

    def reserved_move(self, player_name, to_coordinates):
        """
        Method allows player to play piece from reserve to empty tile on board.
        Returns a message if move is not valid. Contains its own validation logic
        :param player_name: string representing player making move
        :param to_coordinates: tuple indicating position on board to play piece from reserve
        :return: message if move fails, else None
        """
        player = self._players[player_name]
        to_stack = self.show_pieces(to_coordinates)

        # validation
        if player.get_reserve() == 0:
            return False

        if player_name != self._current_player_turn:
            return False
        all_coords = [to_coordinates[0], to_coordinates[1]]

        for coords in all_coords:
            if coords not in (0, 1, 2, 3, 4, 5):
                return False

        # execute reserve
        player.play_from_reserve()
        new_stack = to_stack
        new_stack.append(player.get_color())
        if len(new_stack) > 5:
            new_stack = self.resolve_stacks(new_stack, player_name)
        self._board.modify_tile(to_coordinates, new_stack)

        # change turn and set gamestate
        if self._current_player_turn == self._player1.get_name():
            self._current_player_turn = self._player2.get_name()
        else:
            self._current_player_turn = self._player1.get_name()

        self._game_state = self.determine_game_state()

        if self._game_state in ('PLAYER 1 WINS', 'PLAYER 2 WINS'):
            return f'{self._current_player_turn} wins'
        else:
            return True

    def display_board(self):
        """
        Displays the board. Method simply calls display_board from Board class.
        This implementation keeps FocusGame as the interface for user.
        """
        self._board.display_board()