class Board:
    """
    Class represents the game board. Class is responsible for initializing an instance
    of itself, and providing the information it knows to the FocusGame class.
    Players and other classes interact with the board indirectly through FocusGame.
    Class will also update itself as needed via valid actions from FocusGame
    (such as updating its state due to Player moves). It does not need to
    interact directly with Player--FocusGame will take care of that.

    Attributes
    ----------
    board : the board, represented by a list of lists
    """

    def __init__(self, p1_color, p2_color):
        """
        Initializes the game board per standard layout rules. Will create the
        pieces in the colors provided by players.
        """
        self._board_layout = []
        for i in range(6):
            if i % 2 == 0:
                self._board_layout.append([[p1_color], [p1_color], [p2_color], [p2_color], [p1_color], [p1_color]])
            else:
                self._board_layout.append([[p2_color], [p2_color], [p1_color], [p1_color], [p2_color], [p2_color]])

    def display_board(self):
        """
        Method prints board with layout of current pieces
        """
        print()
        for row in self._board_layout:
            print(row)

    def modify_tile(self, tile_coord, new_stack):
        """
        Method modifies the value at the indicated coordinates. Essentially it
        changes the pieces in the stack to resolve various game actions.
        :param tile_coord: tuple indicating which tile should be modified
        :param new_stack: list containing stack values (pieces in stack)
        """
        row_coord = tile_coord[0]
        col_coord = tile_coord[1]
        self._board_layout[row_coord][col_coord] = new_stack

    def return_stack(self, tile_coord):
        """
        Method returns stack at a given tile. The bottom piece should be the 0th
        element in a list, with the other pieces in order (rising to top)
        :param tile_coord: the tile for which we want to see the stack of pieces. tuple
        :return: return a list representing the stack of pieces at location
        """
        row_coord = tile_coord[0]
        col_coord = tile_coord[1]

        if 5 < row_coord or row_coord < 0:
            return False
        elif 5 < col_coord or col_coord < 0:
            return False
        else:
            return self._board_layout[row_coord][col_coord]
