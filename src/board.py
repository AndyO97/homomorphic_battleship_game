"""
Board management for Battleship game.

Handles board creation, ship placement, encryption, and hit tracking.
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from phe.paillier import PaillierPublicKey, EncryptedNumber
import random


@dataclass
class Ship:
    """Represents a single ship on the board."""
    ship_id: int
    name: str
    size: int
    coordinates: List[Tuple[int, int]] = field(default_factory=list)
    hits: int = 0
    
    def is_sunk(self) -> bool:
        """Check if the ship is completely sunk."""
        return self.hits >= self.size
    
    def record_hit(self) -> None:
        """Record a hit on this ship."""
        self.hits += 1
    
    @staticmethod
    def is_valid_line(coords: List[Tuple[int, int]]) -> Tuple[bool, Optional[str]]:
        """
        Check if coordinates form a valid continuous line (horizontal or vertical).
        
        Args:
            coords: List of (x, y) coordinate tuples
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(coords) < 2:
            return True, None
        
        # Get first two coordinates to determine direction
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        
        # Check if horizontal or vertical
        if x1 == x2:
            # Vertical line - all x coordinates must be the same
            direction = "vertical"
            if not all(x == x1 for x, y in coords):
                return False, f"Ship must be in a straight vertical line. All x coordinates must be {x1}."
            
            # Check for continuous line (no gaps)
            y_coords = sorted([y for x, y in coords])
            for i in range(1, len(y_coords)):
                if y_coords[i] != y_coords[i-1] + 1:
                    return False, f"Ship must be continuous with no gaps. Y coordinates should be consecutive."
        
        elif y1 == y2:
            # Horizontal line - all y coordinates must be the same
            direction = "horizontal"
            if not all(y == y1 for x, y in coords):
                return False, f"Ship must be in a straight horizontal line. All y coordinates must be {y1}."
            
            # Check for continuous line (no gaps)
            x_coords = sorted([x for x, y in coords])
            for i in range(1, len(x_coords)):
                if x_coords[i] != x_coords[i-1] + 1:
                    return False, f"Ship must be continuous with no gaps. X coordinates should be consecutive."
        
        else:
            # Neither horizontal nor vertical
            return False, "Ship must be placed either horizontally or vertically in a straight line."
        
        return True, None
    
    @staticmethod
    def get_valid_range(coords: List[Tuple[int, int]], size: int) -> str:
        """
        Get the valid range for remaining coordinates of a ship.
        
        Args:
            coords: List of coordinates already placed
            size: Total size of the ship
            
        Returns:
            String describing valid range for next coordinate
        """
        if len(coords) < 1:
            return "Any coordinate on the board (0-9 for x and y)"
        
        if len(coords) == 1:
            x1, y1 = coords[0]
            return f"Can be horizontal (same y={y1}, x differs) or vertical (same x={x1}, y differs)"
        
        # After 2+ coordinates, direction is determined
        x1, y1 = coords[0]
        x2, y2 = coords[1]
        
        remaining = size - len(coords)
        
        if x1 == x2:
            # Vertical
            y_coords = sorted([y for x, y in coords])
            min_y = y_coords[0] - remaining
            max_y = y_coords[-1] + remaining
            min_y = max(min_y, 0)
            max_y = min(max_y, 9)
            
            # Next coordinate must continue the line
            if y_coords[-1] + 1 <= 9:
                next_valid = f"y must be {y_coords[-1] + 1} (continuing from current line)"
            else:
                next_valid = f"Line is complete at this end, no more room"
            
            return f"Vertical line: x={x1}, {next_valid}"
        
        else:  # y1 == y2
            # Horizontal
            x_coords = sorted([x for x, y in coords])
            min_x = x_coords[0] - remaining
            max_x = x_coords[-1] + remaining
            min_x = max(min_x, 0)
            max_x = min(max_x, 9)
            
            # Next coordinate must continue the line
            if x_coords[-1] + 1 <= 9:
                next_valid = f"x must be {x_coords[-1] + 1} (continuing from current line)"
            else:
                next_valid = f"Line is complete at this end, no more room"
            
            return f"Horizontal line: y={y1}, {next_valid}"


class Board:
    """Manages the Battleship board for a single player."""
    
    BOARD_SIZE = 10
    SHIP_SIZES = [5, 4, 3, 2, 2]  # Aircraft Carrier, Battleship, Submarine, Destroyer, Patrol Boat
    SHIP_NAMES = ["Aircraft Carrier", "Battleship", "Submarine", "Destroyer", "Patrol Boat"]
    
    def __init__(self, player_name: str = "Player"):
        """
        Initialize a board for a player.
        
        Args:
            player_name: Name of the player who owns this board
        """
        self.player_name = player_name
        self.board: Dict[Tuple[int, int], int] = {}
        self.ships: List[Ship] = []
        self.guesses: set = set()  # Track all guesses made against this board
        self._initialize_board()
    
    def _initialize_board(self) -> None:
        """Initialize an empty 10x10 board."""
        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                self.board[(x, y)] = 0  # 0 = water
    
    def place_ships(self) -> None:
        """
        Randomly place all 5 ships on the board.
        
        Ships are placed without overlap and must fit entirely on the board.
        """
        self.ships = []
        
        for ship_id, (size, name) in enumerate(zip(self.SHIP_SIZES, self.SHIP_NAMES)):
            ship = Ship(ship_id=ship_id, name=name, size=size)
            placed = False
            attempts = 0
            max_attempts = 100
            
            while not placed and attempts < max_attempts:
                # Randomly choose horizontal or vertical
                is_horizontal = random.choice([True, False])
                
                if is_horizontal:
                    x = random.randint(0, self.BOARD_SIZE - size)
                    y = random.randint(0, self.BOARD_SIZE - 1)
                    coordinates = [(x + i, y) for i in range(size)]
                else:
                    x = random.randint(0, self.BOARD_SIZE - 1)
                    y = random.randint(0, self.BOARD_SIZE - size)
                    coordinates = [(x, y + i) for i in range(size)]
                
                # Check for overlap
                if all(self.board[coord] == 0 for coord in coordinates):
                    # Place ship
                    for coord in coordinates:
                        self.board[coord] = 1  # 1 = part of ship
                    ship.coordinates = coordinates
                    self.ships.append(ship)
                    placed = True
                
                attempts += 1
            
            if not placed:
                raise ValueError(f"Could not place ship {name} after {max_attempts} attempts")
    
    def place_ships_manual(self) -> None:
        """
        Allow a player to manually place all 5 ships on the board.
        
        The player is prompted to enter coordinates for each ship in the format "x y"
        repeated for each cell of the ship. Validates that:
        - Coordinates are within bounds (0-9)
        - Ships form continuous horizontal or vertical lines
        - No overlaps with existing ships
        - No duplicate coordinates within a ship
        - Each ship has the correct size
        """
        self.ships = []
        print(f"\n{self.player_name}'s Manual Ship Placement")
        print("=" * 60)
        print("Enter coordinates for each cell of your ships (format: x y)")
        print("Ships must be placed in a straight line (horizontal or vertical)")
        print("Board coordinates range from 0-9 for both x and y")
        print()
        
        for ship_id, (size, name) in enumerate(zip(self.SHIP_SIZES, self.SHIP_NAMES)):
            ship = Ship(ship_id=ship_id, name=name, size=size)
            coordinates = []
            
            print(f"\nPlacing {name} (Size: {size})")
            print(f"Please enter {size} coordinates:")
            
            while len(coordinates) < size:
                try:
                    coord_input = input(f"  Coordinate {len(coordinates) + 1}/{size}: ").strip()
                    parts = coord_input.split()
                    
                    if len(parts) != 2:
                        print("  Invalid format. Please enter: x y")
                        continue
                    
                    x, y = int(parts[0]), int(parts[1])
                    
                    # Validate bounds
                    if not (0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE):
                        print(f"  Coordinates out of bounds. Please use 0-9.")
                        continue
                    
                    # Validate no repeat coordinates within this ship
                    if (x, y) in coordinates:
                        print(f"  Duplicate coordinate ({x}, {y}) in this ship. Please enter a different one.")
                        continue
                    
                    # Validate no overlap with existing ships
                    if self.board[(x, y)] != 0:
                        print(f"  Coordinate ({x}, {y}) already occupied by another ship. Please enter a different one.")
                        continue
                    
                    # Add to temporary list for validation
                    temp_coordinates = coordinates + [(x, y)]
                    
                    # Validate that coordinates form a continuous line
                    is_valid, error_msg = Ship.is_valid_line(temp_coordinates)
                    if not is_valid:
                        print(f"  Error: {error_msg}")
                        valid_range = Ship.get_valid_range(coordinates, size)
                        print(f"  Valid range for next coordinate: {valid_range}")
                        continue
                    
                    coordinates.append((x, y))
                    print(f"  [OK] {len(coordinates)}/{size} cells placed at ({x}, {y})")
                
                except ValueError:
                    print("  Invalid input. Please enter two integers (0-9).")
            
            # Place the ship
            for coord in coordinates:
                self.board[coord] = 1
            ship.coordinates = coordinates
            self.ships.append(ship)
            print(f"  [OK] {name} placed successfully at: {coordinates}")
        
        print(f"\n{self.player_name}'s board setup complete!")
    
    def get_cell(self, x: int, y: int) -> int:
        """
        Get the plaintext value of a cell.
        
        Args:
            x: X coordinate (0-9)
            y: Y coordinate (0-9)
            
        Returns:
            0 for water, 1 for ship
        """
        if not (0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE):
            raise ValueError(f"Coordinate ({x}, {y}) out of bounds")
        return self.board[(x, y)]
    
    def encrypt_board(self, public_key: PaillierPublicKey) -> Dict[Tuple[int, int], EncryptedNumber]:
        """
        Encrypt the entire board using the provided public key.
        
        Args:
            public_key: The Paillier public key for encryption
            
        Returns:
            Dictionary mapping coordinates to encrypted cell values
        """
        encrypted_board = {}
        for coord, value in self.board.items():
            encrypted_board[coord] = public_key.encrypt(value)
        return encrypted_board
    
    def record_hit_on_board(self, x: int, y: int) -> bool:
        """
        Record a hit at the specified coordinate.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if this was a hit (on a ship), False if it was a miss
        """
        if not (0 <= x < self.BOARD_SIZE and 0 <= y < self.BOARD_SIZE):
            raise ValueError(f"Coordinate ({x}, {y}) out of bounds")
        
        self.guesses.add((x, y))
        is_hit = self.board[(x, y)] == 1
        
        if is_hit:
            # Find which ship was hit and record the hit
            for ship in self.ships:
                if (x, y) in ship.coordinates:
                    ship.record_hit()
                    break
        
        return is_hit
    
    def get_ship_at(self, x: int, y: int) -> Optional[Ship]:
        """
        Get the ship at the specified coordinate, if any.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            The Ship object if there's a ship at this location, None otherwise
        """
        for ship in self.ships:
            if (x, y) in ship.coordinates:
                return ship
        return None
    
    def all_ships_sunk(self) -> bool:
        """Check if all ships are sunk."""
        return all(ship.is_sunk() for ship in self.ships)
    
    def get_game_status(self) -> Dict:
        """
        Get the current game status for this board.
        
        Returns:
            Dictionary with ship statuses
        """
        return {
            "player": self.player_name,
            "all_sunk": self.all_ships_sunk(),
            "ships": [
                {
                    "name": ship.name,
                    "size": ship.size,
                    "hits": ship.hits,
                    "sunk": ship.is_sunk()
                }
                for ship in self.ships
            ]
        }
    
    def print_board_state(self) -> None:
        """Print the plaintext board state (for debugging only)."""
        print(f"\n{self.player_name}'s Board (Plaintext - DEBUG ONLY):")
        print("   ", " ".join(str(i) for i in range(self.BOARD_SIZE)))
        for y in range(self.BOARD_SIZE):
            row = [str(self.board[(x, y)]) for x in range(self.BOARD_SIZE)]
            print(f"{y:2d}: {' '.join(row)}")
        print()
