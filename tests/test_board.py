"""
Unit tests for the board module.
"""

import pytest
from board import Board, Ship


class TestShip:
    """Tests for the Ship class."""
    
    def test_ship_creation(self):
        """Test ship initialization."""
        ship = Ship(ship_id=0, name="Aircraft Carrier", size=5)
        assert ship.ship_id == 0
        assert ship.name == "Aircraft Carrier"
        assert ship.size == 5
        assert ship.hits == 0
        assert not ship.is_sunk()
    
    def test_ship_record_hit(self):
        """Test recording hits on a ship."""
        ship = Ship(ship_id=0, name="Test Ship", size=2)
        assert ship.hits == 0
        
        ship.record_hit()
        assert ship.hits == 1
        assert not ship.is_sunk()
        
        ship.record_hit()
        assert ship.hits == 2
        assert ship.is_sunk()
    
    def test_valid_horizontal_line(self):
        """Test validation of valid horizontal ship line."""
        coords = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        is_valid, error = Ship.is_valid_line(coords)
        assert is_valid is True
        assert error is None
    
    def test_valid_vertical_line(self):
        """Test validation of valid vertical ship line."""
        coords = [(5, 2), (5, 3), (5, 4)]
        is_valid, error = Ship.is_valid_line(coords)
        assert is_valid is True
        assert error is None
    
    def test_invalid_diagonal_line(self):
        """Test that diagonal lines are rejected."""
        coords = [(0, 0), (1, 1), (2, 2)]
        is_valid, error = Ship.is_valid_line(coords)
        assert is_valid is False
        assert "horizontally or vertically" in error.lower() or "straight line" in error.lower()
    
    def test_invalid_scattered_coordinates(self):
        """Test that scattered (non-continuous) coordinates are rejected."""
        coords = [(0, 0), (2, 0), (4, 0)]  # Missing (1,0) and (3,0)
        is_valid, error = Ship.is_valid_line(coords)
        assert is_valid is False
        assert "continuous" in error.lower() or "gaps" in error.lower()
    
    def test_invalid_mixed_horizontal_vertical(self):
        """Test that mixed horizontal/vertical coordinates are rejected."""
        coords = [(0, 0), (1, 0), (1, 1)]  # Last coord breaks the line
        is_valid, error = Ship.is_valid_line(coords)
        assert is_valid is False
    
    def test_valid_range_for_horizontal_ship(self):
        """Test getting valid range for horizontal ship."""
        coords = [(2, 3), (3, 3)]
        range_str = Ship.get_valid_range(coords, size=5)
        assert "horizontal" in range_str.lower()
        assert "4" in range_str  # Next coordinate should be x=4
    
    def test_valid_range_for_vertical_ship(self):
        """Test getting valid range for vertical ship."""
        coords = [(2, 1), (2, 2)]
        range_str = Ship.get_valid_range(coords, size=4)
        assert "vertical" in range_str.lower()
        assert "3" in range_str  # Next coordinate should be y=3


class TestBoard:
    """Tests for the Board class."""
    
    def test_board_initialization(self):
        """Test board creation."""
        board = Board("TestPlayer")
        assert board.player_name == "TestPlayer"
        assert len(board.board) == 100  # 10x10
        assert all(val == 0 for val in board.board.values())
        assert len(board.ships) == 0
    
    def test_board_size(self):
        """Test board dimensions."""
        board = Board()
        for x in range(10):
            for y in range(10):
                assert board.get_cell(x, y) == 0
    
    def test_get_cell_out_of_bounds(self):
        """Test getting cell out of bounds."""
        board = Board()
        with pytest.raises(ValueError):
            board.get_cell(-1, 0)
        with pytest.raises(ValueError):
            board.get_cell(10, 0)
        with pytest.raises(ValueError):
            board.get_cell(0, 10)
    
    def test_place_ships(self):
        """Test ship placement."""
        board = Board()
        board.place_ships()
        
        assert len(board.ships) == 5
        
        # Check ship sizes
        sizes = sorted([ship.size for ship in board.ships])
        assert sizes == [2, 2, 3, 4, 5]
        
        # Check total ship cells
        total_ship_cells = sum(1 for val in board.board.values() if val == 1)
        assert total_ship_cells == sum(ship.size for ship in board.ships)
    
    def test_ships_no_overlap(self):
        """Test that ships don't overlap."""
        board = Board()
        board.place_ships()
        
        all_coords = set()
        for ship in board.ships:
            for coord in ship.coordinates:
                assert coord not in all_coords, "Ships overlap!"
                all_coords.add(coord)
    
    def test_ships_within_bounds(self):
        """Test that ships fit within board boundaries."""
        board = Board()
        board.place_ships()
        
        for ship in board.ships:
            for x, y in ship.coordinates:
                assert 0 <= x < 10, f"Ship coordinate {x} out of X bounds"
                assert 0 <= y < 10, f"Ship coordinate {y} out of Y bounds"
    
    def test_record_hit_on_water(self):
        """Test recording a hit on water."""
        board = Board()
        board.place_ships()
        
        # Find a water cell
        water_cell = None
        for x in range(10):
            for y in range(10):
                if board.get_cell(x, y) == 0:
                    water_cell = (x, y)
                    break
            if water_cell:
                break
        
        assert water_cell is not None
        x, y = water_cell
        is_hit = board.record_hit_on_board(x, y)
        assert not is_hit
    
    def test_record_hit_on_ship(self):
        """Test recording a hit on a ship."""
        board = Board()
        board.place_ships()
        
        # Find a ship cell
        ship_cell = None
        for ship in board.ships:
            if ship.coordinates:
                ship_cell = ship.coordinates[0]
                break
        
        assert ship_cell is not None
        x, y = ship_cell
        is_hit = board.record_hit_on_board(x, y)
        assert is_hit
    
    def test_all_ships_sunk(self):
        """Test checking if all ships are sunk."""
        board = Board()
        board.place_ships()
        
        assert not board.all_ships_sunk()
        
        # Sink all ships
        for ship in board.ships:
            for _ in range(ship.size):
                ship.record_hit()
        
        assert board.all_ships_sunk()
    
    def test_get_ship_at(self):
        """Test finding ship at a coordinate."""
        board = Board()
        board.place_ships()
        
        for ship in board.ships:
            for coord in ship.coordinates:
                x, y = coord
                found_ship = board.get_ship_at(x, y)
                assert found_ship is ship
        
        # Test non-ship coordinate
        for x in range(10):
            for y in range(10):
                if board.get_cell(x, y) == 0:
                    assert board.get_ship_at(x, y) is None
                    break
    
    def test_random_placement_creates_continuous_lines(self):
        """Test that random placement creates valid continuous ship lines."""
        for _ in range(5):  # Test multiple times due to randomness
            board = Board()
            board.place_ships()
            
            for ship in board.ships:
                # Validate that each ship forms a continuous line
                is_valid, error = Ship.is_valid_line(ship.coordinates)
                assert is_valid, f"Ship {ship.name} has invalid coordinates: {error}"
                
                # Validate ship size matches coordinates
                assert len(ship.coordinates) == ship.size
    
    def test_random_placement_no_gaps(self):
        """Test that randomly placed ships have no gaps in their lines."""
        board = Board()
        board.place_ships()
        
        for ship in board.ships:
            coords = ship.coordinates
            if coords[0][0] == coords[1][0]:
                # Vertical ship
                y_values = sorted([y for x, y in coords])
                for i in range(1, len(y_values)):
                    assert y_values[i] == y_values[i-1] + 1, \
                        f"Ship {ship.name} has gap in vertical line"
            else:
                # Horizontal ship
                x_values = sorted([x for x, y in coords])
                for i in range(1, len(x_values)):
                    assert x_values[i] == x_values[i-1] + 1, \
                        f"Ship {ship.name} has gap in horizontal line"
