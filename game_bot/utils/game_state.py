class GameState:
    def __init__(self):
        self.active_game = None
        self.players = []
        self.spy = None
        self.category = None
        self.round_number = 0

    def reset(self):
        """Resets the game state."""
        self.active_game = None
        self.players.clear()
        self.spy = None
        self.category = None
        self.round_number = 0

    def add_player(self, player_id: int, name: str):
        """Adds a new player to the game."""
        self.players.append({"id": player_id, "name": name, "active": True})

    def set_spy(self, spy_id: int):
        """Sets the spy for the current game."""
        self.spy = spy_id

    def get_active_players(self):
        """Returns a list of active players."""
        return [p for p in self.players if p["active"]]

    def eliminate_player(self, player_id: int):
        """Eliminates a player from the game."""
        for player in self.players:
            if player["id"] == player_id:
                player["active"] = False
                break
