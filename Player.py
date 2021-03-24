class Player:
    """
    Class represents a player of the FocusGame. Contains attributes and methods for
    interacting with the FocusGame class. The FocusGame class will retrieve information
    about the pieces the player has in reserve and captured, so that it can determine
    whether a player can play from reserve and the game state, respectively.
    Player does not need to interact with Board--FocusGame will take care of that.

    Attributes
    ------------
    name : name of the player
    color : color of the player's pieces
    reserved : pieces of player's own color they hold in reserve
    captured : pieces of player's opponents color they have captured
    """

    def __init__(self, name, color):
        """
        Initializes instance of player. Name and color are taken as parameters;
        reserved and captured are initialized to zero as consistent with the rules of
        the game.
        """
        self._name = name
        self._color = color
        self._reserved = 0
        self._captured = 0

    def add_to_reserve(self):
        """
        Increase number of reserved pieces by one. A player can play these reserve
        pieces to empty spots on the board.
        """
        self._reserved += 1

    def add_to_captured(self):
        """
        Increase number of captured pieces by one. First player to capture six
        pieces of the opponent wins the game.
        """
        self._captured += 1

    def play_from_reserve(self):
        """
        Decrements the reserve value by 1, if possible, so player can play a piece
        from reserve onto the board.
        The playing of the piece, and the modification of the board, are done
        by the FocusGame itself--this method just updates the player's reserve
        """
        self._reserved -= 1

    def get_reserve(self):
        """
        Get method for reserved attribute--returns _reserved
        """
        return self._reserved

    def get_captured(self):
        """
        Get method for captured attribute--returns _captured
        """
        return self._captured

    def get_name(self):
        """
        Get method for player name
        """
        return self._name

    def get_color(self):
        """
        Get method for player color
        """
        return self._color