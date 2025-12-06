"""
Core game logic for Homomorphic Battleship.

Handles turn management, hit checking, and game state.
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass, field
from phe.paillier import PaillierPublicKey, PaillierPrivateKey
from src.board import Board
from src.crypto import perform_homomorphic_hit_check, check_hit, decrypt_value


@dataclass
class GameState:
    """Represents the current state of the game."""
    game_over: bool = False
    winner: Optional[str] = None
    current_turn: str = "Alice"
    total_turns: int = 0
    history: list = field(default_factory=list)
    
    def switch_turn(self) -> None:
        """Switch to the other player's turn."""
        self.current_turn = "Bob" if self.current_turn == "Alice" else "Alice"
        self.total_turns += 1


class GameLogic:
    """Manages the game flow and rules."""
    
    def __init__(self, alice_board: Board, bob_board: Board,
                 alice_public_key: PaillierPublicKey, bob_public_key: PaillierPublicKey,
                 alice_private_key: PaillierPrivateKey, bob_private_key: PaillierPrivateKey):
        """
        Initialize the game logic.
        
        Args:
            alice_board: Alice's board
            bob_board: Bob's board
            alice_public_key: Alice's public key
            bob_public_key: Bob's public key
            alice_private_key: Alice's private key
            bob_private_key: Bob's private key
        """
        self.alice_board = alice_board
        self.bob_board = bob_board
        self.alice_public_key = alice_public_key
        self.bob_public_key = bob_public_key
        self.alice_private_key = alice_private_key
        self.bob_private_key = bob_private_key
        
        # Encrypt boards and store encrypted versions
        self.alice_encrypted_board = alice_board.encrypt_board(alice_public_key)
        self.bob_encrypted_board = bob_board.encrypt_board(bob_public_key)
        
        # Game state
        self.game_state = GameState()
    
    def make_guess(self, guessing_player: str, x: int, y: int) -> Tuple[bool, Optional[str], bool]:
        """
        Process a guess from one player against the opponent's board.
        
        Args:
            guessing_player: "Alice" or "Bob"
            x: X coordinate (0-9)
            y: Y coordinate (0-9)
            
        Returns:
            Tuple of (is_hit, ship_name_if_sunk, is_duplicate)
        """
        if self.game_state.game_over:
            raise RuntimeError("Game is already over!")
        
        if guessing_player not in ["Alice", "Bob"]:
            raise ValueError("Invalid player name")
        
        # Determine which board is being attacked
        if guessing_player == "Alice":
            target_board = self.bob_board
            target_encrypted_board = self.bob_encrypted_board
            target_private_key = self.bob_private_key
        else:
            target_board = self.alice_board
            target_encrypted_board = self.alice_encrypted_board
            target_private_key = self.alice_private_key
        
        # Get the encrypted cell
        if not (0 <= x < 10 and 0 <= y < 10):
            raise ValueError(f"Coordinate ({x}, {y}) out of bounds")
        
        encrypted_cell = target_encrypted_board[(x, y)]
        
        # Perform homomorphic hit check
        # We compute: (encrypted_cell - 1) * random_blinding
        # If cell is 1 (ship): 0 * random = 0 (HIT)
        # If cell is 0 (water): (-1) * random = random_junk (MISS)
        encrypted_result = perform_homomorphic_hit_check(encrypted_cell, 1)
        
        # Target player (defender) decrypts the result
        decrypted_result = decrypt_value(target_private_key, encrypted_result)
        
        # Determine if it's a hit
        is_hit = check_hit(decrypted_result)
        
        # Record the hit on the target board
        is_hit, is_duplicate = target_board.record_hit_on_board(x, y)
        
        # Check if a ship was sunk
        ship_sunk_name = None
        if is_hit and not is_duplicate:
            ship = target_board.get_ship_at(x, y)
            if ship and ship.is_sunk():
                ship_sunk_name = ship.name
        
        # Check for game over
        if target_board.all_ships_sunk():
            self.game_state.game_over = True
            self.game_state.winner = guessing_player
        
        # Record in history
        self.game_state.history.append({
            "turn": self.game_state.total_turns,
            "player": guessing_player,
            "coordinate": (x, y),
            "is_hit": is_hit,
            "ship_sunk": ship_sunk_name,
            "is_duplicate": is_duplicate
        })
        
        return is_hit, ship_sunk_name, is_duplicate
    
    def validate_guess(self, x: int, y: int) -> bool:
        """
        Validate that a guess is within bounds.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not (0 <= x < 10 and 0 <= y < 10):
            raise ValueError(f"Coordinate ({x}, {y}) out of bounds. Use 0-9.")
        return True
    
    def get_game_status(self) -> Dict:
        """
        Get the current game status.
        
        Returns:
            Dictionary with game information
        """
        return {
            "game_over": self.game_state.game_over,
            "winner": self.game_state.winner,
            "current_turn": self.game_state.current_turn,
            "total_turns": self.game_state.total_turns,
            "alice_status": self.alice_board.get_game_status(),
            "bob_status": self.bob_board.get_game_status(),
        }
    
    def get_history(self) -> list:
        """Get the game history."""
        return self.game_state.history
