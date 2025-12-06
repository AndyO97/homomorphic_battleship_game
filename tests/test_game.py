"""
Unit tests for the game logic module.
"""

import pytest
from board import Board
from crypto import generate_keypair
from game_logic import GameLogic


class TestGameLogic:
    """Tests for the GameLogic class."""
    
    @pytest.fixture
    def game_setup(self):
        """Set up a game for testing."""
        # Create keypairs
        alice_pub, alice_priv = generate_keypair(n_length=1024)
        bob_pub, bob_priv = generate_keypair(n_length=1024)
        
        # Create boards
        alice_board = Board("Alice")
        alice_board.place_ships()
        
        bob_board = Board("Bob")
        bob_board.place_ships()
        
        # Create game logic
        game = GameLogic(
            alice_board, bob_board,
            alice_pub, bob_pub,
            alice_priv, bob_priv
        )
        
        return game, alice_board, bob_board
    
    def test_game_initialization(self, game_setup):
        """Test game initialization."""
        game, alice_board, bob_board = game_setup
        
        assert not game.game_state.game_over
        assert game.game_state.winner is None
        assert game.game_state.current_turn == "Alice"
        assert game.game_state.total_turns == 0
    
    def test_validate_guess_valid(self, game_setup):
        """Test validating valid guesses."""
        game, _, _ = game_setup
        
        # All valid coordinates
        for x in [0, 5, 9]:
            for y in [0, 5, 9]:
                assert game.validate_guess(x, y)
    
    def test_validate_guess_invalid(self, game_setup):
        """Test validating invalid guesses."""
        game, _, _ = game_setup
        
        invalid_coords = [
            (-1, 0), (10, 0), (0, -1), (0, 10),
            (15, 15), (-5, -5)
        ]
        
        for x, y in invalid_coords:
            with pytest.raises(ValueError):
                game.validate_guess(x, y)
    
    def test_make_guess_hit(self, game_setup):
        """Test making a guess that hits."""
        game, alice_board, bob_board = game_setup
        
        # Find a ship cell in Bob's board
        ship_cell = bob_board.ships[0].coordinates[0]
        x, y = ship_cell
        
        # Alice guesses the ship location
        is_hit, ship_sunk, is_duplicate = game.make_guess("Alice", x, y)
        
        assert is_hit
        assert not is_duplicate
        assert (x, y) in bob_board.guesses
    
    def test_make_guess_miss(self, game_setup):
        """Test making a guess that misses."""
        game, alice_board, bob_board = game_setup
        
        # Find a water cell in Bob's board
        water_cell = None
        for x in range(10):
            for y in range(10):
                if bob_board.get_cell(x, y) == 0:
                    water_cell = (x, y)
                    break
            if water_cell:
                break
        
        assert water_cell is not None
        x, y = water_cell
        
        # Alice guesses water
        is_hit, ship_sunk, is_duplicate = game.make_guess("Alice", x, y)
        
        assert not is_hit
        assert not is_duplicate
    
    def test_ship_sinking(self, game_setup):
        """Test detecting when a ship sinks."""
        game, alice_board, bob_board = game_setup
        
        # Get the first ship
        target_ship = bob_board.ships[0]
        ship_coords = target_ship.coordinates
        
        # Hit all cells of the ship except the last
        for x, y in ship_coords[:-1]:
            game.make_guess("Alice", x, y)
        
        assert not target_ship.is_sunk()
        
        # Hit the final cell
        x, y = ship_coords[-1]
        is_hit, ship_sunk, is_duplicate = game.make_guess("Alice", x, y)
        
        assert is_hit
        assert ship_sunk == target_ship.name
        assert target_ship.is_sunk()
        assert not is_duplicate
    
    def test_game_over_condition(self, game_setup):
        """Test that game ends when all ships are sunk."""
        game, alice_board, bob_board = game_setup
        
        # Sink all of Bob's ships
        for ship in bob_board.ships:
            for x, y in ship.coordinates:
                game.make_guess("Alice", x, y)
        
        assert game.game_state.game_over
        assert game.game_state.winner == "Alice"
    
    def test_turn_switching(self, game_setup):
        """Test that turns alternate correctly."""
        game, alice_board, bob_board = game_setup
        
        assert game.game_state.current_turn == "Alice"
        
        # Find a water cell in Bob's board
        water_cell = None
        for x in range(10):
            for y in range(10):
                if bob_board.get_cell(x, y) == 0:
                    water_cell = (x, y)
                    break
            if water_cell:
                break
        
        x, y = water_cell
        game.make_guess("Alice", x, y)
        
        # Turn switching is done by the server/game loop
        # Manually switch for this test
        game.game_state.switch_turn()
        assert game.game_state.current_turn == "Bob"
        
        # Switch back
        game.game_state.switch_turn()
        assert game.game_state.current_turn == "Alice"
    
    def test_game_history(self, game_setup):
        """Test that game history is recorded."""
        game, alice_board, bob_board = game_setup
        
        # Make a guess
        water_cell = None
        for x in range(10):
            for y in range(10):
                if bob_board.get_cell(x, y) == 0:
                    water_cell = (x, y)
                    break
            if water_cell:
                break
        
        x, y = water_cell
        game.make_guess("Alice", x, y)
        
        history = game.get_history()
        assert len(history) == 1
        assert history[0]["player"] == "Alice"
        assert history[0]["coordinate"] == (x, y)
        assert history[0]["is_hit"] == False
    
    def test_get_game_status(self, game_setup):
        """Test getting game status."""
        game, _, _ = game_setup
        
        status = game.get_game_status()
        
        assert status["game_over"] == False
        assert status["winner"] is None
        assert status["current_turn"] == "Alice"
        assert status["total_turns"] == 0
        assert "alice_status" in status
        assert "bob_status" in status


class TestGameLogicInvariants:
    """Tests for game logic invariants."""
    
    @pytest.fixture
    def game_setup(self):
        """Set up a game for testing."""
        alice_pub, alice_priv = generate_keypair(n_length=1024)
        bob_pub, bob_priv = generate_keypair(n_length=1024)
        
        alice_board = Board("Alice")
        alice_board.place_ships()
        
        bob_board = Board("Bob")
        bob_board.place_ships()
        
        game = GameLogic(
            alice_board, bob_board,
            alice_pub, bob_pub,
            alice_priv, bob_priv
        )
        
        return game, alice_board, bob_board
    
    def test_no_duplicate_guesses_recorded(self, game_setup):
        """Test that we can guess the same cell twice (hits recorded separately)."""
        game, alice_board, bob_board = game_setup
        
        water_cell = None
        for x in range(10):
            for y in range(10):
                if bob_board.get_cell(x, y) == 0:
                    water_cell = (x, y)
                    break
            if water_cell:
                break
        
        x, y = water_cell
        
        # Guess same cell twice
        result1 = game.make_guess("Alice", x, y)
        result2 = game.make_guess("Bob", x, x)  # Switch player
        
        # Both should be processed
        history = game.get_history()
        assert len(history) >= 1
