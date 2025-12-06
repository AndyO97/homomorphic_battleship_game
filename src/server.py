"""
Game server simulation for coordinating player communication.

Simulates a centralized server that handles communication between
two remote player instances without knowing their boards.
"""

from typing import Dict, Optional
from src.game_logic import GameLogic
from src.board import Board
from phe.paillier import PaillierPublicKey, PaillierPrivateKey


class GameServer:
    """
    Simulates a centralized game server.
    
    In a real scenario, this would handle network communication.
    Here, it coordinates game logic between two local player instances.
    """
    
    def __init__(self, game_logic: GameLogic):
        """
        Initialize the game server.
        
        Args:
            game_logic: The GameLogic instance managing the game
        """
        self.game_logic = game_logic
        self.game_started = False
    
    def start_game(self) -> Dict:
        """
        Start the game and notify players.
        
        Returns:
            Dictionary with game start information
        """
        self.game_started = True
        return {
            "status": "Game started!",
            "message": "Alice will go first.",
            "board_size": 10,
            "ships_per_player": 5
        }
    
    def process_player_guess(self, player_name: str, x: int, y: int) -> Dict:
        """
        Process a player's guess through the server.
        
        This simulates sending a guess to the server, which processes it
        homomorphically without revealing the target board.
        
        Args:
            player_name: "Alice" or "Bob"
            x: X coordinate (0-9)
            y: Y coordinate (0-9)
            
        Returns:
            Dictionary with the result of the guess
        """
        if not self.game_started:
            raise RuntimeError("Game not started")
        
        try:
            # Validate the guess
            self.game_logic.validate_guess(x, y)
            
            # Process the guess through homomorphic logic
            is_hit, ship_sunk = self.game_logic.make_guess(player_name, x, y)
            
            # Prepare response
            response = {
                "status": "success",
                "player": player_name,
                "coordinate": (x, y),
                "is_hit": is_hit,
                "ship_sunk": ship_sunk,
                "game_over": self.game_logic.game_state.game_over,
                "winner": self.game_logic.game_state.winner
            }
            
            # Switch turn for next player
            if not self.game_logic.game_state.game_over:
                self.game_logic.game_state.switch_turn()
            
            return response
        
        except ValueError as e:
            return {
                "status": "error",
                "message": str(e),
                "player": player_name
            }
    
    def get_game_state(self) -> Dict:
        """
        Get the current game state (visible to both players).
        
        Args:
            Returns: Dictionary with current game state
        """
        return self.game_logic.get_game_status()
    
    def get_whose_turn(self) -> str:
        """Get the name of the player whose turn it is."""
        return self.game_logic.game_state.current_turn
    
    def get_game_history(self) -> list:
        """Get the complete game history."""
        return self.game_logic.get_history()
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_logic.game_state.game_over
    
    def get_winner(self) -> Optional[str]:
        """Get the winner if the game is over."""
        return self.game_logic.game_state.winner


class PlayerInstance:
    """
    Represents a single player instance in the game.
    
    In a distributed setup, this would run on a separate machine.
    It manages only its own board and communicates via the server.
    """
    
    def __init__(self, player_name: str, board: Board, 
                 public_key: PaillierPublicKey, private_key: PaillierPrivateKey,
                 server: GameServer):
        """
        Initialize a player instance.
        
        Args:
            player_name: "Alice" or "Bob"
            board: The player's board
            public_key: The player's public key
            private_key: The player's private key
            server: Reference to the game server
        """
        self.player_name = player_name
        self.board = board
        self.public_key = public_key
        self.private_key = private_key
        self.server = server
        self.is_local_human = False  # True if controlled by human input
    
    def make_guess(self, x: int, y: int) -> Dict:
        """
        Make a guess through the server.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Result dictionary from the server
        """
        return self.server.process_player_guess(self.player_name, x, y)
    
    def get_board_status(self) -> Dict:
        """Get status of this player's own board."""
        return self.board.get_game_status()
