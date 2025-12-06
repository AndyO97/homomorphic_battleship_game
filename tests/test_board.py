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
